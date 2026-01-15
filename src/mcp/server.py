"""
MCP (Model Context Protocol) Server Implementation
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from enum import Enum

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from src.nostr.client import NostrClient
from src.llm.manager import LLMManager, LLMProvider
from src.utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class MCPMessageType(str, Enum):
    """MCP message types"""
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    HEARTBEAT = "heartbeat"

class MCPToolCall(BaseModel):
    """MCP tool call request"""
    tool: str
    parameters: Dict[str, Any]
    call_id: str

class MCPToolResult(BaseModel):
    """MCP tool result response"""
    call_id: str
    result: Any
    error: Optional[str] = None

class MCPServer:
    """MCP Server implementation"""
    
    def __init__(self, nostr_client: NostrClient, llm_manager: LLMManager):
        self.nostr_client = nostr_client
        self.llm_manager = llm_manager
        self.app = FastAPI(title="Dandelions MCP Server")
        self.websocket_clients: List[WebSocket] = []
        self.tools: Dict[str, callable] = {}
        
        self._setup_routes()
        self._register_tools()
    
    async def initialize(self):
        """Initialize MCP server"""
        logger.info("MCP Server initialized")
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "service": "Dandelions MCP Server",
                "version": "1.0.0",
                "tools": list(self.tools.keys())
            }
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self._handle_websocket(websocket)
    
    def _register_tools(self):
        """Register available MCP tools"""
        from src.mcp.tools import (
            generate_text,
            analyze_sentiment,
            summarize_content,
            translate_text,
            get_llm_status,
            switch_llm_provider,
            nostr_send_message,
            nostr_get_events
        )
        
        self.tools = {
            "generate_text": generate_text,
            "analyze_sentiment": analyze_sentiment,
            "summarize_content": summarize_content,
            "translate_text": translate_text,
            "get_llm_status": get_llm_status,
            "switch_llm_provider": switch_llm_provider,
            "nostr_send_message": nostr_send_message,
            "nostr_get_events": nostr_get_events
        }
        
        logger.info(f"Registered {len(self.tools)} MCP tools")
    
    async def _handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection"""
        await websocket.accept()
        self.websocket_clients.append(websocket)
        
        client_id = id(websocket)
        logger.info(f"New MCP client connected: {client_id}")
        
        try:
            while True:
                # Receive message
                data = await websocket.receive_text()
                
                try:
                    message = json.loads(data)
                    await self._process_message(message, websocket)
                    
                except json.JSONDecodeError:
                    await self._send_error(websocket, "Invalid JSON")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await self._send_error(websocket, str(e))
                    
        except WebSocketDisconnect:
            logger.info(f"MCP client disconnected: {client_id}")
        finally:
            self.websocket_clients.remove(websocket)
    
    async def _process_message(self, message: Dict, websocket: WebSocket):
        """Process incoming MCP message"""
        msg_type = message.get("type")
        
        if msg_type == MCPMessageType.TOOL_CALL:
            await self._handle_tool_call(message, websocket)
        elif msg_type == MCPMessageType.HEARTBEAT:
            await self._send_heartbeat(websocket)
        else:
            await self._send_error(websocket, f"Unknown message type: {msg_type}")
    
    async def _handle_tool_call(self, message: Dict, websocket: WebSocket):
        """Handle tool call request"""
        try:
            tool_call = MCPToolCall(**message)
            
            if tool_call.tool not in self.tools:
                await self._send_error(
                    websocket,
                    f"Tool not found: {tool_call.tool}",
                    tool_call.call_id
                )
                return
            
            # Execute tool
            tool_func = self.tools[tool_call.tool]
            result = await tool_func(
                **tool_call.parameters,
                nostr_client=self.nostr_client,
                llm_manager=self.llm_manager
            )
            
            # Send result
            response = MCPToolResult(
                call_id=tool_call.call_id,
                result=result
            )
            
            await websocket.send_text(response.json())
            
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            await self._send_error(
                websocket,
                str(e),
                message.get("call_id") if message else None
            )
    
    async def _send_error(self, websocket: WebSocket, error: str, call_id: Optional[str] = None):
        """Send error message"""
        error_msg = {
            "type": MCPMessageType.ERROR,
            "call_id": call_id,
            "error": error
        }
        await websocket.send_text(json.dumps(error_msg))
    
    async def _send_heartbeat(self, websocket: WebSocket):
        """Send heartbeat response"""
        heartbeat = {
            "type": MCPMessageType.HEARTBEAT,
            "timestamp": asyncio.get_event_loop().time()
        }
        await websocket.send_text(json.dumps(heartbeat))
    
    async def start(self):
        """Start MCP server"""
        import uvicorn
        
        config = uvicorn.Config(
            self.app,
            host=settings.MCP_HOST,
            port=settings.MCP_PORT,
            log_level="info"
        )
        self.server = uvicorn.Server(config)
        
        logger.info(f"MCP Server starting on {settings.MCP_HOST}:{settings.MCP_PORT}")
        
        # Run in background
        self.server_task = asyncio.create_task(self.server.serve())
    
    async def stop(self):
        """Stop MCP server"""
        if hasattr(self, 'server_task'):
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
        
        logger.info("MCP Server stopped")
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        message_json = json.dumps(message)
        
        disconnected_clients = []
        
        for client in self.websocket_clients:
            try:
                await client.send_text(message_json)
            except:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.websocket_clients.remove(client)
