# Full-Stack AI Apps

Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP: scalable, secure and observable.

## 🚀 Overview

This repository provides a comprehensive, production-ready framework for deploying AI applications across multiple cloud platforms. It includes infrastructure-as-code, MLOps pipelines, AI agents, RAG implementations, and observability tools.

## 🏗️ Architecture

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│      AWS        │      GCP        │     Azure       │     Vercel      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ • Bedrock       │ • Vertex AI     │ • OpenAI        │ • Edge Runtime  │
│ • SageMaker     │ • AI Platform   │ • Cognitive     │ • Functions     │
│ • Lambda        │ • Cloud Run     │ • Container     │ • KV Store      │
│ • ECS/EKS       │ • GKE           │ • AKS           │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
                           │
                    ┌──────┴──────┐
                    │   MLOps     │
                    │  Pipeline   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │   RAG   │        │ Agents  │        │   MCP   │
   │ System  │        │ System  │        │Protocol │
   └─────────┘        └─────────┘        └─────────┘
```

## 📁 Repository Structure

```
├── aws/                    # AWS-specific deployments
│   ├── bedrock/           # Amazon Bedrock implementations
│   ├── sagemaker/         # SageMaker ML models
│   ├── ai-agents/         # AWS-based AI agents
│   ├── rag/              # RAG on AWS
│   └── mlops/            # AWS MLOps pipelines
├── gcp/                   # Google Cloud deployments
├── azure/                 # Microsoft Azure deployments
├── vercel/               # Vercel edge deployments
├── infrastructure/        # IaC templates
│   ├── terraform/        # Multi-cloud Terraform
│   ├── cloudformation/   # AWS CloudFormation
│   ├── arm-templates/    # Azure ARM templates
│   └── kubernetes/       # K8s manifests
├── src/                  # Source code
│   ├── common/          # Shared utilities
│   ├── mcp/            # Model Context Protocol
│   └── utils/          # Helper functions
├── examples/             # Sample applications
│   ├── chat-app/        # AI chat application
│   ├── document-qa/     # Document Q&A system
│   └── image-generation/ # Image generation app
├── monitoring/           # Observability stack
├── security/            # Security configurations
└── docs/               # Documentation
```

## 🛠️ Technologies

### Cloud Platforms
- **AWS**: Bedrock, SageMaker, Lambda, ECS, EKS
- **GCP**: Vertex AI, Cloud Run, GKE, AI Platform
- **Azure**: OpenAI Service, Cognitive Services, Container Instances, AKS
- **Vercel**: Edge Runtime, Serverless Functions, KV Store

### AI/ML Stack
- **LLMs**: GPT-4, Claude, Llama, Mistral
- **Vector Databases**: Pinecone, Weaviate, Chroma
- **ML Frameworks**: TensorFlow, PyTorch, Transformers
- **Model Context Protocol (MCP)**: Latest AI interaction standard

### Infrastructure & Operations
- **IaC**: Terraform, CloudFormation, ARM Templates
- **Containers**: Docker, Kubernetes
- **CI/CD**: GitHub Actions, Jenkins, GitLab CI
- **Monitoring**: Prometheus, Grafana, CloudWatch, Application Insights

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker
- Terraform 1.5+
- Cloud CLI tools (AWS CLI, gcloud, Azure CLI)

### Installation
```bash
git clone https://github.com/teman67/Full-Stack-AI-apps.git
cd Full-Stack-AI-apps
./scripts/setup/install-dependencies.sh
```

### Deploy to AWS
```bash
cd aws/bedrock
terraform init
terraform apply
```

### Deploy to Vercel
```bash
cd vercel
npm install
vercel deploy
```

## 📋 Features

### ✅ Multi-Cloud Support
- Unified deployment across AWS, GCP, Azure, and Vercel
- Cross-cloud data synchronization
- Disaster recovery and failover

### ✅ AI/ML Capabilities
- Large Language Model integration
- Retrieval Augmented Generation (RAG)
- Autonomous AI agents
- Model Context Protocol (MCP) support

### ✅ MLOps Pipeline
- Automated model training and deployment
- Model versioning and rollback
- A/B testing framework
- Performance monitoring

### ✅ Security & Compliance
- IAM role management
- Secrets management
- Data encryption at rest and in transit
- Audit logging

### ✅ Observability
- Real-time monitoring and alerting
- Distributed tracing
- Performance metrics
- Custom dashboards

## 🎯 Use Cases

1. **Enterprise Chat Assistant**: Deploy a secure, scalable chat bot across multiple clouds
2. **Document Intelligence**: Extract insights from documents using RAG
3. **Content Generation**: Generate images, text, and multimedia content
4. **Decision Support**: AI agents for complex decision-making workflows

## 📖 Documentation

- [Architecture Guide](docs/architecture/README.md)
- [Deployment Guide](docs/deployment/README.md)
- [API Reference](docs/api/README.md)
- [Security Best Practices](docs/security/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🏷️ Tags

`ai` `ml` `aws` `gcp` `azure` `vercel` `mlops` `bedrock` `sagemaker` `rag` `agents` `mcp` `terraform` `kubernetes` `observability` `security`