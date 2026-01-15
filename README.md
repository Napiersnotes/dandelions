🌸 Dandelions - Multi-LLM Nostr MCP Bot with Intelligent Agent Framework

Dandelions is a sophisticated, user-friendly Nostr bot framework featuring seamless multi-LLM integration (DeepSeek, Mistral, OpenAI, Anthropic, Ollama, and more) with full Model Context Protocol (MCP) server capabilities. Designed for accessibility without sacrificing power, it enables both beginners and developers to deploy intelligent agents across the Nostr network.

docs/images/banner.png

"Like dandelion seeds spreading across digital meadows, intelligent agents propagate through the Nostr network"

✨ Core Features

🤖 Multi-LLM Orchestration Engine

· Unified Provider Interface: Single API for 7+ LLM providers
· Simultaneous Operation: Run multiple LLMs in parallel with intelligent load balancing
· Provider Agnostic: Switch between providers without code changes
· Cost Optimization: Automatic provider selection based on cost/performance ratios
· Failover & Redundancy: Automatic fallback during provider outages

🌐 Advanced Nostr Integration

· Multi-Relay Architecture: Connect to unlimited Nostr relays simultaneously
· Event-Driven Architecture: Real-time processing of mentions, DMs, and reactions
· Encrypted Communication: Secure end-to-end encrypted messaging
· Metadata Management: Dynamic profile and relay list updates
· Zap Integration: Bitcoin Lightning payment support

🔌 Full MCP (Model Context Protocol) Implementation

· Standards-Compliant: Full implementation of Model Context Protocol specification
· Tool Calling System: Dynamic tool registration and execution
· WebSocket API: Real-time bidirectional communication
· Plugin Architecture: Extend functionality with custom tools and providers
· Protocol Buffers: Efficient serialization for high-performance messaging

🎨 Professional User Experience

· Interactive Setup Wizard: Guided configuration for complete beginners
· Web Dashboard: Comprehensive monitoring and control interface
· CLI & API: Multiple access methods for different user types
· Visual Analytics: Real-time performance and cost monitoring
· Mobile Responsive: Access from any device

🔧 Enterprise-Grade Infrastructure

· Async-First Architecture: High-performance concurrent processing
· Type Safety: Full Python type hints throughout the codebase
· Comprehensive Logging: Structured logging with multiple output formats
· Database Persistence: SQLite, PostgreSQL, or MySQL support
· Docker & Kubernetes: Production-ready container orchestration
· Security First: Encrypted credentials, rate limiting, and CORS protection

🏗️ Architecture Overview

Dandelions follows a modular microservices architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Dashboard (Streamlit)                │
│                   http://localhost:8501                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  MCP Server (FastAPI)                       │
│                WebSocket: localhost:8080/ws                 │
└──────────┬──────────────┬───────────────────────────────────┘
           │              │
┌──────────▼────┐ ┌──────▼──────────┐ ┌──────────────────────┐
│  LLM Manager  │ │  Nostr Client   │ │  Database Layer      │
│               │ │                  │ │                      │
│ • DeepSeek    │ │ • Multi-relay   │ │ • SQLAlchemy ORM     │
│ • Mistral     │ │ • Event-driven  │ │ • Alembic migrations │
│ • OpenAI      │ │ • Encryption    │ │ • Query optimization│
│ • Anthropic   │ │ • NIP standards │ │ • Connection pooling │
│ • Ollama      │ │ • WebSocket     │ └──────────────────────┘
│ • Groq        │ │   connections   │
│ • Together AI │ └──────────────────┘
└───────────────┘
```

🚀 Getting Started

System Requirements

· Python: 3.10 or higher (3.11+ recommended for performance)
· RAM: Minimum 4GB, 8GB+ recommended for multiple LLMs
· Storage: 1GB free space for models and database
· Network: Stable internet connection for LLM APIs

Installation Methods

Method 1: PyPI Installation (Recommended for Users)

```bash
# Install the stable release
pip install dandelions-bot

# Or install with web interface extras
pip install dandelions-bot[web,llm-all]

# For development features
pip install dandelions-bot[dev,docs]
```

Method 2: Docker Deployment (Production)

```bash
# Clone repository
git clone https://github.com/dafyddnapier/dandelions.git
cd dandelions

# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f dandelions
```

Method 3: Source Installation (Developers)

```bash
# Clone the repository
git clone https://github.com/dafyddnapier/dandelions.git
cd dandelions

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev,test,llm-all]"

# Initialize database
alembic upgrade head

# Run the interactive setup wizard
dandelions setup
```

🧙 Interactive Setup Wizard

Dandelions features an intuitive setup wizard that guides you through configuration:

```bash
# Launch the setup wizard
dandelions setup
```

The wizard includes:

1. Nostr Configuration: Generate or import keys, configure relays
2. LLM Provider Setup: Configure multiple AI providers with API keys
3. MCP Server Settings: Network configuration and security
4. Web Dashboard: Authentication and interface customization
5. Connection Testing: Validate all configured services
6. Performance Tuning: Adjust based on your hardware

📋 Configuration Guide

Environment Variables

Create a .env file in your project root:

```env
# ===== NOSTR CONFIGURATION =====
NOSTR_PRIVATE_KEY=nsec1yourprivatekeyhere
NOSTR_RELAYS=wss://relay.damus.io,wss://nos.lol,wss://relay.snort.social

# ===== LLM PROVIDER API KEYS =====
# DeepSeek AI
DEEPSEEK_API_KEY=sk-your-deepseek-key
DEEPSEEK_MODEL=deepseek-chat

# Mistral AI  
MISTRAL_API_KEY=your-mistral-key
MISTRAL_MODEL=mistral-medium-latest

# OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-claude-key
ANTHROPIC_MODEL=claude-3-opus-20240229

# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:13b

# ===== WEB INTERFACE =====
WEB_UI_ENABLED=true
WEB_UI_PORT=8501
WEB_UI_AUTH_ENABLED=true
WEB_UI_USERNAME=admin
WEB_UI_PASSWORD=your-secure-password

# ===== MCP SERVER =====
MCP_HOST=0.0.0.0
MCP_PORT=8080

# ===== DATABASE =====
DATABASE_URL=sqlite:///data/dandelions.db
# For PostgreSQL: postgresql://user:password@localhost/dandelions

# ===== ADVANCED =====
LOG_LEVEL=INFO
WORKER_COUNT=4
API_RATE_LIMIT=100
```

YAML Configuration File

For advanced users, create config/settings.yaml:

```yaml
app:
  name: "Dandelions"
  version: "1.0.0"
  debug: false
  log_level: "INFO"

nostr:
  private_key: "${NOSTR_PRIVATE_KEY}"
  relays:
    - "wss://relay.damus.io"
    - "wss://nos.lol"
    - "wss://relay.snort.social"
    - "wss://relay.primal.net"
  auto_follow_back: true
  zap_support: false

llm_providers:
  deepseek:
    enabled: true
    api_key: "${DEEPSEEK_API_KEY}"
    model: "deepseek-chat"
    temperature: 0.7
    max_tokens: 4096
    priority: 1
    cost_per_1k_input: 0.00014
    cost_per_1k_output: 0.00028

  mistral:
    enabled: true
    api_key: "${MISTRAL_API_KEY}"
    model: "mistral-medium-latest"
    temperature: 0.7
    max_tokens: 8192
    priority: 2
    cost_per_1k_input: 0.0007
    cost_per_1k_output: 0.0021

  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    model: "llama2:13b"
    temperature: 0.7
    max_tokens: 4096
    priority: 3
    cost_per_1k_input: 0.0
    cost_per_1k_output: 0.0

mcp_server:
  host: "0.0.0.0"
  port: 8080
  max_connections: 50
  rate_limit_per_minute: 1000
  enable_tls: false
  tls_cert_path: "/path/to/cert.pem"
  tls_key_path: "/path/to/key.pem"

web_ui:
  enabled: true
  host: "0.0.0.0"
  port: 8501
  auth:
    enabled: true
    username: "${WEB_UI_USERNAME}"
    password: "${WEB_UI_PASSWORD}"
  theme: "dark"
  default_llm_provider: "deepseek"

database:
  url: "${DATABASE_URL}"
  pool_size: 20
  max_overflow: 40
  echo: false

performance:
  worker_count: 4
  max_concurrent_requests: 10
  request_timeout: 30
  cache_enabled: true
  cache_ttl: 300

monitoring:
  enable_metrics: true
  metrics_port: 9090
  enable_health_endpoints: true
  log_retention_days: 30
```

🚦 Running Dandelions

Basic Startup

```bash
# Start with all features enabled
dandelions start

# Start without web interface (headless mode)
dandelions start --no-web-ui

# Start with custom configuration
dandelions start --config /path/to/custom_config.yaml

# Run in development mode with hot reload
dandelions start --dev --reload
```

Service Management

```bash
# Check system status
dandelions status

# Test all connections
dandelions test-connections

# List available LLM providers
dandelions list-providers

# View logs in real-time
dandelions logs --follow

# Backup configuration and data
dandelions backup --output backup.tar.gz

# Restore from backup
dandelions restore --input backup.tar.gz
```

🖥️ Web Dashboard

Once running, access the dashboard at http://localhost:8501:

Dashboard Features:

1. Real-time Chat Interface
   · Direct chat with configured LLMs
   · Conversation history
   · Multi-provider comparison
   · Export conversations
2. System Monitoring
   · LLM provider status and latency
   · Nostr relay connections
   · Resource usage (CPU, memory, network)
   · Cost tracking and projections
3. Configuration Management
   · Visual settings editor
   · Environment variable management
   · Profile switching
   · Import/export configurations
4. Analytics & Insights
   · Usage statistics by provider
   · Cost breakdown reports
   · Performance metrics
   · Error rate monitoring
5. Nostr Interaction Tools
   · Direct message interface
   · Event browser
   · Profile management
   · Relay health checks

🔌 MCP Client Integration

Dandelions implements the full Model Context Protocol specification, allowing integration with various MCP clients.

Connect with Claude Desktop:

1. Add to Claude Desktop configuration (~/Library/Application Support/Claude/claude_desktop_config.json):

```json
{
  "mcpServers": {
    "dandelions": {
      "command": "dandelions",
      "args": ["mcp", "serve"],
      "env": {
        "DANDELIONS_CONFIG": "/path/to/your/config.yaml"
      }
    }
  }
}
```

Connect via WebSocket:

```python
import asyncio
import websockets
import json

async def mcp_client_example():
    async with websockets.connect('ws://localhost:8080/ws') as websocket:
        # List available tools
        list_tools_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        await websocket.send(json.dumps(list_tools_msg))
        response = await websocket.recv()
        print("Available tools:", json.loads(response))
        
        # Call a tool
        generate_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "generate_text",
                "arguments": {
                    "prompt": "Explain quantum entanglement",
                    "provider": "deepseek",
                    "temperature": 0.7
                }
            }
        }
        
        await websocket.send(json.dumps(generate_msg))
        response = await websocket.recv()
        print("Generated text:", json.loads(response))

asyncio.run(mcp_client_example())
```

🛠️ Available MCP Tools

Dandelions comes with a comprehensive set of built-in tools:

Text Generation & Analysis

· generate_text - Generate text using any configured LLM
· analyze_sentiment - Sentiment analysis of text
· summarize_content - Summarize long documents or conversations
· translate_text - Translate between 100+ languages
· extract_entities - Named entity recognition
· classify_text - Text classification into categories

Nostr Operations

· nostr_send_message - Send encrypted or public messages
· nostr_get_events - Query events with filters
· nostr_get_profile - Retrieve user profiles
· nostr_update_metadata - Update your profile metadata
· nostr_follow_user - Follow/unfollow users
· nostr_create_list - Create and manage contact lists

LLM Management

· llm_list_providers - List all available LLM providers
· llm_test_provider - Test connection to a specific provider
· llm_switch_default - Change the default provider
· llm_get_usage - Get usage statistics and costs
· llm_set_parameters - Update generation parameters

System & Monitoring

· system_get_status - Get system health and status
· system_get_metrics - Retrieve performance metrics
· system_update_config - Update configuration on the fly
· system_restart_service - Restart specific services
· system_backup_data - Create backup of all data

🧩 Extending Dandelions

Creating Custom Tools

Create a new Python file in src/mcp/tools/custom_tools.py:

```python
from typing import Dict, Any
from pydantic import BaseModel, Field
from src.mcp.tools import register_tool

class WeatherParameters(BaseModel):
    location: str = Field(description="City and country for weather")
    units: str = Field(default="metric", description="Units: metric or imperial")

@register_tool(name="get_weather", description="Get current weather for a location")
async def get_weather(
    location: str,
    units: str = "metric",
    **kwargs
) -> Dict[str, Any]:
    """
    Get current weather information.
    
    Args:
        location: City and country (e.g., "Berlin, Germany")
        units: Temperature units (metric or imperial)
    
    Returns:
        Dict with weather information
    """
    # Implementation using a weather API
    return {
        "location": location,
        "temperature": 22.5,
        "conditions": "Sunny",
        "humidity": 65,
        "units": units
    }
```

Adding New LLM Providers

Create a new provider in src/llm/providers/:

```python
from typing import Dict, Any, Optional
import httpx
from src.llm.base import BaseLLMProvider, LLMConfig
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CustomAIProvider(BaseLLMProvider):
    """Custom AI provider implementation"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.base_url or "https://api.custom-ai.com/v1"
        self.client = None
    
    async def initialize(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        logger.info(f"CustomAI provider initialized")
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        response = await self.client.post(
            "/completions",
            json={
                "model": self.config.model,
                "prompt": prompt,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                **kwargs
            }
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "content": data["choices"][0]["text"],
            "model": data["model"],
            "usage": data.get("usage", {}),
            "cost": self._calculate_cost(data.get("usage", {}))
        }
```

📊 Performance Tuning

Resource Allocation

Adjust config/performance.yaml:

```yaml
concurrency:
  max_workers: 8  # Number of async workers
  max_pending_tasks: 100  # Maximum queued tasks
  
llm:
  timeout: 30  # Seconds before timing out
  retry_attempts: 3  # Retry failed requests
  batch_size: 10  # Batch size for processing
  
caching:
  enabled: true
  ttl: 300  # Cache time-to-live in seconds
  max_size: 1000  # Maximum cache entries
  
database:
  pool_size: 20
  max_overflow: 40
  pool_recycle: 3600
```

Monitoring & Metrics

Dandelions includes Prometheus metrics endpoint at http://localhost:9090/metrics:

```bash
# Install Prometheus and Grafana for visualization
docker-compose -f monitoring/docker-compose.yml up -d
```

Key metrics tracked:

· LLM request latency by provider
· Token usage and costs
· Nostr event processing rates
· System resource utilization
· Error rates and types

🔒 Security Considerations

API Key Security

```yaml
security:
  # Environment variable encryption
  encrypt_env_vars: true
  encryption_key_path: "/secure/encryption.key"
  
  # API key rotation
  auto_rotate_keys: true
  rotation_days: 30
  
  # Access control
  ip_whitelist:
    - "127.0.0.1"
    - "192.168.1.0/24"
  
  # Rate limiting
  enable_rate_limiting: true
  requests_per_minute: 100
  burst_limit: 50
```

Best Practices

1. Never commit .env files to version control
2. Use different API keys for development and production
3. Enable authentication for the web interface
4. Regularly update dependencies and the application
5. Monitor access logs for suspicious activity
6. Use HTTPS/WSS in production environments

🚢 Deployment

Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  dandelions:
    image: ghcr.io/dafyddnapier/dandelions:latest
    container_name: dandelions
    restart: unless-stopped
    ports:
      - "8501:8501"  # Web UI
      - "8080:8080"  # MCP Server
    volumes:
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:password@postgres/dandelions
    depends_on:
      - postgres
      - redis
  
  postgres:
    image: postgres:15
    container_name: dandelions-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: dandelions
      POSTGRES_USER: dandelions
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    container_name: dandelions-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
  
  nginx:
    image: nginx:alpine
    container_name: dandelions-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - dandelions

volumes:
  postgres_data:
  redis_data:
```

Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dandelions
  namespace: dandelions
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dandelions
  template:
    metadata:
      labels:
        app: dandelions
    spec:
      containers:
      - name: dandelions
        image: ghcr.io/dafyddnapier/dandelions:latest
        ports:
        - containerPort: 8501
          name: web-ui
        - containerPort: 8080
          name: mcp
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: dandelions-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

🧪 Testing & Development

Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run linting and type checking
flake8 src/
black --check src/
mypy src/
```

Development Environment

```bash
# Install development dependencies
pip install -e ".[dev,test,docs]"

# Set up pre-commit hooks
pre-commit install

# Run the development server with hot reload
dandelions start --dev --reload

# Generate documentation
cd docs && make html

# Create a distribution package
python setup.py sdist bdist_wheel
```

🐛 Troubleshooting

Common Issues

Issue: "Unable to connect to Nostr relays"

```bash
# Check relay status
dandelions test-nostr

# Try alternative relays
export NOSTR_RELAYS="wss://relay.primal.net,wss://relay.current.fyi"
```

Issue: "LLM API key invalid"

```bash
# Verify API key format
echo $DEEPSEEK_API_KEY | head -c 10

# Test specific provider
dandelions test-provider deepseek

# Regenerate API key from provider dashboard
```

Issue: "Web interface not loading"

```bash
# Check if port is in use
netstat -tulpn | grep :8501

# Run on alternative port
dandelions start --web-ui-port 8502

# Check firewall settings
sudo ufw allow 8501/tcp
```

Getting Help

1. Check the logs: dandelions logs --tail 50
2. Enable debug mode: dandelions start --log-level DEBUG
3. Search existing issues: GitHub Issues
4. Join the community: Nostr Channel

📈 Roadmap

Version 2.0 (Q2 2024)

· Plugin Marketplace: Community-contributed tools and providers
· Advanced Analytics: Machine learning insights on Nostr network
· Multi-Agent Systems: Cooperative agent networks
· Voice Interface: Voice input/output support
· Mobile Application: iOS and Android native apps

Version 1.x (Current)

· Multi-LLM Support: DeepSeek, Mistral, OpenAI, Anthropic, Ollama
· Full MCP Implementation: Standards-compliant protocol server
· Web Dashboard: Comprehensive monitoring interface
· Nostr Integration: Multi-relay support with encryption
· Docker Deployment: Production-ready containerization

🤝 Contributing

We welcome contributions from developers of all skill levels! Here's how to get involved:

Ways to Contribute

1. Report bugs and suggest features via GitHub Issues
2. Submit pull requests for bug fixes and enhancements
3. Improve documentation and create tutorials
4. Add new LLM providers or tools
5. Translate the interface into new languages
6. Share your use cases and success stories

Development Workflow

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/your-username/dandelions.git

# 3. Create a feature branch
git checkout -b feature/amazing-feature

# 4. Make your changes
# 5. Run tests
pytest

# 6. Commit with semantic messages
git commit -m "feat: add new LLM provider"

# 7. Push to your fork
git push origin feature/amazing-feature

# 8. Open a Pull Request
```

Code Standards

· Follow PEP 8 for Python code
· Use Conventional Commits for commit messages
· Include tests for new features
· Update documentation for user-facing changes
· Add type hints for all function signatures

📄 License

Dandelions is released under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2024 Dafydd Napier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

🙏 Acknowledgments

Core Development

· Dafydd Napier - Creator and Lead Developer
· Nostr Protocol Community - For the amazing decentralized network
· Model Context Protocol Team - For the excellent protocol specification
· All LLM Providers - For their incredible AI models and APIs

Special Thanks

· Early testers and bug reporters
· Documentation contributors
· Open-source library maintainers
· The entire Nostr ecosystem

Sponsors & Supporters

This project is supported by:

· DeepSeek AI
· Mistral AI
· Community donations via Bitcoin/Nostr zaps

🔗 Links & Resources

· Official Website: https://dandelions.ai
· GitHub Repository: https://github.com/dafyddnapier/dandelions
· Documentation: https://docs.dandelions.ai
· Issue Tracker: https://github.com/dafyddnapier/dandelions/issues
· Discord Community: https://discord.gg/dandelions
· Nostr Channel: npub1dandelions... (check GitHub for latest)
· Twitter/X: @dandelions_ai

🌟 Support the Project

Dandelions is free and open-source software. You can support its development:

1. Star the repository on GitHub
2. Contribute code or documentation
3. Report issues and suggest features
4. Share with your network
5. Donate via Bitcoin or Nostr zaps

```
Bitcoin: bc1q... (see GitHub for address)
Nostr: npub1dandelions... (DM for zap invoice)
```

---

"The most sophisticated Nostr agent framework, making AI accessible across the decentralized web."

Built with ❤️ by Dafydd Napier and contributors