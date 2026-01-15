"""
LLM Manager for handling multiple providers simultaneously
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import importlib

from pydantic import BaseModel, Field
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    DEEPSEEK = "deepseek"
    MISTRAL = "mistral"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    GROQ = "groq"
    TOGETHER = "together"

@dataclass
class LLMConfig:
    """Configuration for an LLM provider"""
    provider: LLMProvider
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    enabled: bool = True
    priority: int = 1

class LLMResponse(BaseModel):
    """Standardized LLM response"""
    content: str
    model: str
    provider: LLMProvider
    usage: Dict[str, int] = Field(default_factory=dict)
    latency: float
    cost: Optional[float] = None

class LLMManager:
    """Manager for multiple LLM providers with load balancing"""
    
    def __init__(self):
        self.providers: Dict[LLMProvider, Any] = {}
        self.configs: Dict[LLMProvider, LLMConfig] = {}
        self.round_robin_index: Dict[LLMProvider, int] = {}
    
    async def initialize(self):
        """Initialize all configured LLM providers"""
        from config.settings import settings
        
        logger.info("Initializing LLM providers...")
        
        # Load provider configurations
        for provider_name, config_data in settings.LLM_PROVIDERS.items():
            try:
                provider = LLMProvider(provider_name.lower())
                config = LLMConfig(
                    provider=provider,
                    api_key=config_data.get('api_key'),
                    base_url=config_data.get('base_url'),
                    model=config_data.get('model'),
                    temperature=config_data.get('temperature', 0.7),
                    max_tokens=config_data.get('max_tokens', 4096),
                    enabled=config_data.get('enabled', True),
                    priority=config_data.get('priority', 1)
                )
                
                self.configs[provider] = config
                
                if config.enabled:
                    await self._load_provider(provider, config)
                    
            except ValueError:
                logger.warning(f"Unknown provider: {provider_name}")
        
        logger.info(f"Initialized {len(self.providers)} LLM providers")
    
    async def _load_provider(self, provider: LLMProvider, config: LLMConfig):
        """Dynamically load a provider module"""
        try:
            module_name = f"src.llm.{provider.value}"
            module = importlib.import_module(module_name)
            
            provider_class = getattr(module, f"{provider.name.capitalize()}Provider")
            provider_instance = provider_class(config)
            await provider_instance.initialize()
            
            self.providers[provider] = provider_instance
            self.round_robin_index[provider] = 0
            
            logger.info(f"Loaded provider: {provider.value}")
            
        except Exception as e:
            logger.error(f"Failed to load provider {provider}: {e}")
    
    async def generate(
        self,
        prompt: str,
        provider: Optional[LLMProvider] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate response from LLM(s)
        
        Args:
            prompt: Input prompt
            provider: Specific provider to use (None for auto-selection)
            model: Specific model to use
            temperature: Generation temperature
            **kwargs: Additional provider-specific parameters
        
        Returns:
            LLMResponse object
        """
        if provider:
            # Use specific provider
            return await self._generate_with_provider(
                provider, prompt, model, temperature, **kwargs
            )
        else:
            # Use all available providers (ensemble) or load balanced
            return await self._generate_ensemble(prompt, model, temperature, **kwargs)
    
    async def _generate_with_provider(
        self,
        provider: LLMProvider,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate using specific provider"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not available")
        
        provider_instance = self.providers[provider]
        
        # Override config if specified
        config = self.configs[provider].copy()
        if model:
            config.model = model
        if temperature is not None:
            config.temperature = temperature
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            response = await provider_instance.generate(
                prompt=prompt,
                config=config,
                **kwargs
            )
            
            latency = asyncio.get_event_loop().time() - start_time
            
            return LLMResponse(
                content=response.content,
                model=response.model,
                provider=provider,
                usage=response.usage,
                latency=latency,
                cost=response.cost
            )
            
        except Exception as e:
            logger.error(f"Error generating with {provider}: {e}")
            raise
    
    async def _generate_ensemble(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        strategy: str = "best_of_n",
        n: int = 3,
        **kwargs
    ) -> LLMResponse:
        """
        Generate using multiple providers with different strategies
        
        Strategies:
        - best_of_n: Get responses from N providers, choose best
        - load_balanced: Round-robin between providers
        - consensus: Get all responses, find consensus
        """
        if strategy == "load_balanced":
            # Get next provider in round-robin
            available_providers = list(self.providers.keys())
            if not available_providers:
                raise ValueError("No LLM providers available")
            
            current_index = self.round_robin_index.get('all', 0)
            provider = available_providers[current_index % len(available_providers)]
            self.round_robin_index['all'] = current_index + 1
            
            return await self._generate_with_provider(
                provider, prompt, model, temperature, **kwargs
            )
        
        elif strategy == "best_of_n":
            # Query N providers in parallel, choose best
            available_providers = list(self.providers.keys())[:n]
            
            tasks = []
            for provider in available_providers:
                task = self._generate_with_provider(
                    provider, prompt, model, temperature, **kwargs
                )
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter successful responses
            successful = [r for r in responses if not isinstance(r, Exception)]
            
            if not successful:
                raise Exception("All providers failed")
            
            # Choose based on confidence score (simplified)
            best_response = max(successful, key=lambda r: len(r.content))
            return best_response
        
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def list_providers(self) -> List[Dict]:
        """List all available providers with status"""
        providers_info = []
        
        for provider, instance in self.providers.items():
            config = self.configs[provider]
            providers_info.append({
                "name": provider.value,
                "enabled": config.enabled,
                "model": config.model,
                "status": "connected" if instance.is_connected() else "disconnected",
                "priority": config.priority
            })
        
        return providers_info
    
    async def test_all_providers(self) -> Dict[str, bool]:
        """Test connectivity to all providers"""
        results = {}
        
        for provider, instance in self.providers.items():
            try:
                success = await instance.test_connection()
                results[provider.value] = success
            except Exception as e:
                logger.error(f"Test failed for {provider}: {e}")
                results[provider.value] = False
        
        return results
