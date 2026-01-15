"""
Nostr Client Implementation
"""

import asyncio
import json
from typing import Dict, List, Optional, Callable
from datetime import datetime
import uuid

from pynostr.key import PrivateKey
from pynostr.event import Event, EventKind
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters

from src.llm.manager import LLMManager, LLMProvider
from src.utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class NostrClient:
    """Nostr client with LLM integration"""
    
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
        self.relay_manager = RelayManager()
        self.private_key: Optional[PrivateKey] = None
        self.public_key: Optional[str] = None
        self.subscriptions: Dict[str, asyncio.Task] = {}
        self.event_handlers: Dict[EventKind, List[Callable]] = {}
        self.running = False
        
    async def initialize(self):
        """Initialize Nostr client"""
        # Load or generate private key
        self._load_keys()
        
        # Connect to relays
        await self._connect_to_relays()
        
        # Register event handlers
        self._register_handlers()
        
        logger.info(f"Nostr client initialized for pubkey: {self.public_key}")
    
    def _load_keys(self):
        """Load or generate Nostr keys"""
        if settings.NOSTR_PRIVATE_KEY:
            self.private_key = PrivateKey.from_nsec(settings.NOSTR_PRIVATE_KEY)
        else:
            # Generate new key pair
            self.private_key = PrivateKey()
            logger.warning(f"Generated new private key: {self.private_key.bech32()}")
            logger.info(f"Public key: {self.private_key.public_key.bech32()}")
        
        self.public_key = self.private_key.public_key.hex()
    
    async def _connect_to_relays(self):
        """Connect to configured relays"""
        for relay_url in settings.NOSTR_RELAYS:
            try:
                self.relay_manager.add_relay(relay_url)
                logger.info(f"Added relay: {relay_url}")
            except Exception as e:
                logger.error(f"Failed to add relay {relay_url}: {e}")
    
    def _register_handlers(self):
        """Register event handlers"""
        from src.nostr.handlers import (
            handle_text_note,
            handle_direct_message,
            handle_reaction,
            handle_metadata
        )
        
        self.register_handler(EventKind.TEXT_NOTE, handle_text_note)
        self.register_handler(EventKind.ENCRYPTED_DIRECT_MESSAGE, handle_direct_message)
        self.register_handler(EventKind.REACTION, handle_reaction)
        self.register_handler(EventKind.SET_METADATA, handle_metadata)
    
    def register_handler(self, kind: EventKind, handler: Callable):
        """Register event handler for specific event kind"""
        if kind not in self.event_handlers:
            self.event_handlers[kind] = []
        self.event_handlers[kind].append(handler)
    
    async def start(self):
        """Start listening for events"""
        self.running = True
        
        # Subscribe to relevant events
        await self._subscribe_to_events()
        
        # Start relay connections
        self.relay_manager.run_sync()
        
        # Start event processing loop
        asyncio.create_task(self._event_loop())
        
        logger.info("Nostr client started")
    
    async def _subscribe_to_events(self):
        """Subscribe to Nostr events"""
        # Subscribe to mentions
        mention_filters = FiltersList([
            Filters(
                kinds=[EventKind.TEXT_NOTE, EventKind.ENCRYPTED_DIRECT_MESSAGE],
                pubkey_refs=[self.public_key],
                limit=100
            )
        ])
        
        subscription_id = str(uuid.uuid4())
        self.relay_manager.add_subscription_on_all_relays(subscription_id, mention_filters)
        self.subscriptions[subscription_id] = asyncio.create_task(
            self._process_subscription(subscription_id)
        )
    
    async def _event_loop(self):
        """Main event processing loop"""
        while self.running:
            try:
                # Check for new events
                event_pool = self.relay_manager.event_pool
                
                while not event_pool.empty():
                    event_tuple = event_pool.get()
                    if event_tuple:
                        event_json, relay_url = event_tuple
                        await self._process_event(event_json, relay_url)
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in event loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_event(self, event_json: Dict, relay_url: str):
        """Process incoming Nostr event"""
        try:
            event = Event.from_dict(event_json)
            
            # Call registered handlers
            handlers = self.event_handlers.get(event.kind, [])
            for handler in handlers:
                await handler(event, self, self.llm_manager)
                
        except Exception as e:
            logger.error(f"Error processing event: {e}")
    
    async def send_message(
        self,
        content: str,
        recipient_pubkey: Optional[str] = None,
        kind: EventKind = EventKind.TEXT_NOTE,
        tags: List[List[str]] = None
    ):
        """Send Nostr event"""
        try:
            event = Event(
                content=content,
                kind=kind,
                pubkey=self.public_key,
                tags=tags or []
            )
            
            if recipient_pubkey and kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
                # Encrypt for recipient
                event.encrypt(content, recipient_pubkey)
            
            event.sign(self.private_key.hex())
            
            # Publish to relays
            self.relay_manager.publish_event(event)
            
            logger.info(f"Sent event {event.id} to {len(self.relay_manager.relays)} relays")
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise
    
    async def _process_subscription(self, subscription_id: str):
        """Process subscription events"""
        # Implementation for subscription processing
        pass
    
    async def stop(self):
        """Stop the Nostr client"""
        self.running = False
        
        # Cancel subscriptions
        for task in self.subscriptions.values():
            task.cancel()
        
        # Close relay connections
        self.relay_manager.close_all_relay_connections()
        
        logger.info("Nostr client stopped")
