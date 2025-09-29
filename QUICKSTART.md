# Full-Stack AI Apps - Quick Start Guide

This guide will help you get started with the Full-Stack AI Apps framework quickly.

## Prerequisites

- Node.js 18+
- Python 3.9+
- Docker & Docker Compose
- Cloud CLI tools (AWS CLI, gcloud, Azure CLI)
- Terraform 1.5+

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/teman67/Full-Stack-AI-apps.git
cd Full-Stack-AI-apps

# Copy environment variables
cp .env.example .env
# Edit .env with your actual values

# Install dependencies
npm install
pip install -r requirements.txt
```

### 2. Start with Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f ai-app
```

This starts:
- 🚀 Main AI Application (http://localhost:8000)
- 🗄️ PostgreSQL database
- 📦 Redis cache
- 🔍 Chroma vector database
- 📊 Prometheus monitoring (http://localhost:9090)
- 📈 Grafana dashboards (http://localhost:3001)

### 3. Access the Applications

- **Main API**: http://localhost:8000
- **Chat Demo**: http://localhost:8000 (opens chat interface)
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Chat API
curl -X POST http://localhost:8000/api/v1/rag/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Full-Stack AI Apps?"}'

# List available agents
curl http://localhost:8000/api/v1/agents/

# Create a task for an agent
curl -X POST http://localhost:8000/api/v1/agents/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Analyze the benefits of multi-cloud AI deployment", "task_type": "analysis"}'
```

## Cloud Deployment

### AWS Deployment

```bash
# Configure AWS credentials
aws configure

# Deploy infrastructure
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

# Deploy AI services
./scripts/deploy/deploy.sh --aws
```

### Multi-Cloud Deployment

```bash
# Deploy to all clouds
./scripts/deploy/deploy.sh --all --auto-approve

# Deploy to specific clouds
./scripts/deploy/deploy.sh --aws --gcp --azure
```

## Key Features Demonstration

### 1. RAG (Retrieval Augmented Generation)

```python
from src.rag.system import create_chroma_rag

# Initialize RAG system
rag = await create_chroma_rag("knowledge_base")

# Add documents
documents = [
    {
        "content": "Your knowledge content here",
        "metadata": {"source": "doc1.txt", "type": "technical"}
    }
]
await rag.add_documents(documents)

# Query the system
result = await rag.query("What is the main topic?", top_k=3)
print(result.generated_response)
```

### 2. AI Agents

```python
from src.agents.system import orchestrator

# Create a task
task = await orchestrator.create_task(
    description="Research the latest AI trends",
    task_type="research",
    priority=1
)

# Execute the task
result = await orchestrator.execute_task(task.id)
print(result)
```

### 3. MCP (Model Context Protocol)

```python
from src.mcp.server import MCPClient

# Initialize MCP client
client = MCPClient("http://localhost:8080/mcp")
await client.connect()

# Generate text
response = await client.generate_text("Explain quantum computing", model="gpt-4")
print(response)
```

### 4. Multi-Cloud AI Services

```python
# AWS Bedrock
from aws.bedrock.service import BedrockService
bedrock = BedrockService()
result = await bedrock.generate_text("Hello AI", model_id="anthropic.claude-v2")

# GCP Vertex AI  
from gcp.vertex_ai.service import GCPVertexAIService
vertex = GCPVertexAIService("your-project-id")
result = await vertex.generate_text("Hello AI", model_name="text-bison@001")

# Azure OpenAI
from azure.cognitive_services.service import AzureOpenAIService
azure_ai = AzureOpenAIService("your-endpoint", "your-key")
result = await azure_ai.generate_text("Hello AI", deployment_name="gpt-35-turbo")
```

## Development Mode

### Local Development

```bash
# Start in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Or run directly
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=src --cov-report=html
```

## Configuration

### Environment Variables

Key variables in `.env`:

```bash
# Application
NODE_ENV=development
ENVIRONMENT=dev
PORT=8000

# Cloud Providers
AWS_REGION=us-east-1
GCP_PROJECT_ID=your-project
AZURE_LOCATION=East US

# AI Services
OPENAI_API_KEY=your-key
PINECONE_API_KEY=your-key

# Security
JWT_SECRET=your-secret
ENCRYPTION_KEY=your-key
```

### Cloud Configuration

Each cloud provider requires specific setup:

**AWS**: Configure credentials with `aws configure`
**GCP**: Set up service account and `GOOGLE_APPLICATION_CREDENTIALS`
**Azure**: Use `az login` or set up service principal
**Vercel**: Set up Vercel token for deployments

## Monitoring & Observability

### Grafana Dashboards

1. Open http://localhost:3001
2. Login: admin/admin123
3. Import dashboard from `monitoring/grafana/dashboards/`

### Prometheus Metrics

View metrics at http://localhost:9090:
- `http_requests_total` - API request counts
- `rag_query_duration_seconds` - RAG query performance
- `agent_task_completion_rate` - Agent success rates

### Logs

View application logs:

```bash
# Docker logs
docker-compose logs -f ai-app

# File logs
tail -f logs/app.log
tail -f logs/security_audit.log
```

## Security Best Practices

The framework includes comprehensive security features:

1. **Authentication**: JWT-based with role-based access control
2. **Encryption**: AES-256 encryption for sensitive data
3. **Rate Limiting**: Configurable rate limits per endpoint
4. **Input Validation**: Sanitization and PII detection
5. **Audit Logging**: Complete security audit trail
6. **CORS/CSP**: Proper CORS and Content Security Policy

## Troubleshooting

### Common Issues

**Port Conflicts**:
```bash
# Check what's running on ports
sudo lsof -i :8000
sudo lsof -i :3000
```

**Docker Issues**:
```bash
# Restart services
docker-compose down
docker-compose up -d

# Rebuild images
docker-compose build --no-cache
```

**Database Issues**:
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

**Cloud Authentication**:
```bash
# AWS
aws sts get-caller-identity

# GCP
gcloud auth list

# Azure
az account show
```

### Debugging

Enable debug mode:

```bash
# Environment variable
DEBUG=true

# Python logging
LOG_LEVEL=DEBUG
```

## Production Deployment

### Scaling Recommendations

- **Horizontal Scaling**: Use Kubernetes with HPA
- **Database**: Use managed database services
- **Vector Database**: Scale Pinecone/Weaviate clusters
- **Caching**: Use Redis cluster
- **Load Balancing**: Use cloud load balancers

### Performance Optimization

1. **Enable caching** at multiple levels
2. **Use CDN** for static assets  
3. **Optimize vector search** with proper indexing
4. **Monitor resource usage** and scale accordingly
5. **Use connection pooling** for databases

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory
2. **Read Architecture Docs**: Deep dive into `docs/architecture/`  
3. **Customize Agents**: Build your own agent types
4. **Extend RAG**: Add more vector databases
5. **Add Models**: Integrate additional LLMs

## Support & Contributing

- 📖 **Documentation**: See `docs/` directory
- 🐛 **Issues**: Report on GitHub
- 💬 **Discussions**: Join community discussions
- 🔧 **Contributing**: See `CONTRIBUTING.md`

## License

MIT License - see [LICENSE](LICENSE) for details.

---

🚀 **Happy building with Full-Stack AI Apps!**