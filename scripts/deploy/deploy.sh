#!/bin/bash
set -e

# Full-Stack AI Apps Deployment Script
# Deploys AI applications to AWS, GCP, Azure, and Vercel

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="full-stack-ai"
ENVIRONMENT="${ENVIRONMENT:-dev}"
AWS_REGION="${AWS_REGION:-us-east-1}"
GCP_REGION="${GCP_REGION:-us-central1}"
AZURE_LOCATION="${AZURE_LOCATION:-East US}"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if required CLI tools are installed
    local tools=("aws" "gcloud" "az" "terraform" "docker" "kubectl")
    
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            error "$tool is not installed. Please install it before running this script."
            exit 1
        fi
    done
    
    # Check if Node.js and npm are installed for Vercel
    if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
        error "Node.js and npm are required for Vercel deployment."
        exit 1
    fi
    
    log "All prerequisites are satisfied."
}

# Authenticate with cloud providers
authenticate_clouds() {
    log "Authenticating with cloud providers..."
    
    # AWS
    if ! aws sts get-caller-identity &> /dev/null; then
        warning "AWS authentication required. Please run 'aws configure' first."
    else
        info "AWS authentication verified."
    fi
    
    # GCP
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 &> /dev/null; then
        warning "GCP authentication required. Please run 'gcloud auth login' first."
    else
        info "GCP authentication verified."
    fi
    
    # Azure
    if ! az account show &> /dev/null; then
        warning "Azure authentication required. Please run 'az login' first."
    else
        info "Azure authentication verified."
    fi
}

# Deploy to AWS
deploy_aws() {
    log "Deploying to AWS..."
    
    cd infrastructure/terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION"
    
    # Apply deployment
    if [ "$1" == "--auto-approve" ]; then
        terraform apply -auto-approve -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION"
    else
        terraform apply -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION"
    fi
    
    # Deploy Bedrock services
    log "Deploying AWS Bedrock services..."
    python3 ../../aws/bedrock/deploy.py --environment "$ENVIRONMENT" --region "$AWS_REGION"
    
    # Deploy SageMaker models
    log "Deploying SageMaker models..."
    python3 ../../aws/sagemaker/deploy.py --environment "$ENVIRONMENT" --region "$AWS_REGION"
    
    cd ../..
    log "AWS deployment completed."
}

# Deploy to GCP
deploy_gcp() {
    log "Deploying to Google Cloud Platform..."
    
    # Set up GCP project
    gcloud config set project "$PROJECT_NAME-$ENVIRONMENT"
    
    # Enable required APIs
    local apis=(
        "aiplatform.googleapis.com"
        "run.googleapis.com"
        "cloudbuild.googleapis.com"
        "container.googleapis.com"
    )
    
    for api in "${apis[@]}"; do
        gcloud services enable "$api"
    done
    
    # Deploy AI Platform services
    log "Deploying GCP AI Platform services..."
    python3 gcp/ai-platform/deploy.py --environment "$ENVIRONMENT" --region "$GCP_REGION"
    
    # Deploy Cloud Run services
    log "Deploying Cloud Run services..."
    gcloud run deploy "$PROJECT_NAME-api" \
        --image "gcr.io/$PROJECT_NAME-$ENVIRONMENT/ai-api:latest" \
        --platform managed \
        --region "$GCP_REGION" \
        --allow-unauthenticated
    
    log "GCP deployment completed."
}

# Deploy to Azure
deploy_azure() {
    log "Deploying to Microsoft Azure..."
    
    # Create resource group
    az group create --name "$PROJECT_NAME-$ENVIRONMENT" --location "$AZURE_LOCATION"
    
    # Deploy ARM template
    log "Deploying Azure resources..."
    az deployment group create \
        --resource-group "$PROJECT_NAME-$ENVIRONMENT" \
        --template-file infrastructure/arm-templates/main.json \
        --parameters environment="$ENVIRONMENT" location="$AZURE_LOCATION"
    
    # Deploy Cognitive Services
    log "Deploying Azure Cognitive Services..."
    python3 azure/cognitive-services/deploy.py --environment "$ENVIRONMENT" --location "$AZURE_LOCATION"
    
    log "Azure deployment completed."
}

# Deploy to Vercel
deploy_vercel() {
    log "Deploying to Vercel..."
    
    cd vercel
    
    # Install dependencies
    npm install
    
    # Build the project
    npm run build
    
    # Deploy to Vercel
    if command -v vercel &> /dev/null; then
        vercel deploy --prod
    else
        warning "Vercel CLI not found. Installing..."
        npm install -g vercel
        vercel deploy --prod
    fi
    
    cd ..
    log "Vercel deployment completed."
}

# Set up monitoring
setup_monitoring() {
    log "Setting up monitoring and observability..."
    
    # Deploy Prometheus and Grafana
    kubectl apply -f monitoring/kubernetes/prometheus/
    kubectl apply -f monitoring/kubernetes/grafana/
    
    # Configure CloudWatch dashboards for AWS
    aws logs create-log-group --log-group-name "/aws/ai-apps/$ENVIRONMENT" --region "$AWS_REGION" || true
    
    # Set up application performance monitoring
    python3 scripts/monitoring/setup-apm.py --environment "$ENVIRONMENT"
    
    log "Monitoring setup completed."
}

# Deploy MLOps pipeline
setup_mlops() {
    log "Setting up MLOps pipeline..."
    
    # Deploy ML pipeline to each cloud
    python3 aws/mlops/deploy_pipeline.py --environment "$ENVIRONMENT"
    python3 gcp/mlops/deploy_pipeline.py --environment "$ENVIRONMENT"
    python3 azure/mlops/deploy_pipeline.py --environment "$ENVIRONMENT"
    
    log "MLOps pipeline setup completed."
}

# Initialize AI agents
setup_ai_agents() {
    log "Setting up AI agents..."
    
    # Deploy agent services
    python3 src/agents/deploy.py --environment "$ENVIRONMENT"
    
    # Configure MCP servers
    python3 src/mcp/setup.py --environment "$ENVIRONMENT"
    
    log "AI agents setup completed."
}

# Main deployment function
main() {
    log "Starting Full-Stack AI Apps deployment..."
    log "Environment: $ENVIRONMENT"
    log "AWS Region: $AWS_REGION"
    log "GCP Region: $GCP_REGION"
    log "Azure Location: $AZURE_LOCATION"
    
    # Parse command line arguments
    CLOUDS=()
    AUTO_APPROVE=false
    SKIP_MONITORING=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --aws)
                CLOUDS+=("aws")
                shift
                ;;
            --gcp)
                CLOUDS+=("gcp")
                shift
                ;;
            --azure)
                CLOUDS+=("azure")
                shift
                ;;
            --vercel)
                CLOUDS+=("vercel")
                shift
                ;;
            --all)
                CLOUDS=("aws" "gcp" "azure" "vercel")
                shift
                ;;
            --auto-approve)
                AUTO_APPROVE=true
                shift
                ;;
            --skip-monitoring)
                SKIP_MONITORING=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [--aws|--gcp|--azure|--vercel|--all] [--auto-approve] [--skip-monitoring]"
                echo "  --aws            Deploy to AWS only"
                echo "  --gcp            Deploy to GCP only"
                echo "  --azure          Deploy to Azure only"
                echo "  --vercel         Deploy to Vercel only"
                echo "  --all            Deploy to all clouds"
                echo "  --auto-approve   Skip confirmation prompts"
                echo "  --skip-monitoring Skip monitoring setup"
                exit 0
                ;;
            *)
                error "Unknown option $1"
                exit 1
                ;;
        esac
    done
    
    # Default to all clouds if none specified
    if [ ${#CLOUDS[@]} -eq 0 ]; then
        CLOUDS=("aws" "gcp" "azure" "vercel")
    fi
    
    check_prerequisites
    authenticate_clouds
    
    # Deploy to selected clouds
    for cloud in "${CLOUDS[@]}"; do
        case $cloud in
            "aws")
                if [ "$AUTO_APPROVE" == "true" ]; then
                    deploy_aws --auto-approve
                else
                    deploy_aws
                fi
                ;;
            "gcp")
                deploy_gcp
                ;;
            "azure")
                deploy_azure
                ;;
            "vercel")
                deploy_vercel
                ;;
        esac
    done
    
    # Set up additional services
    setup_mlops
    setup_ai_agents
    
    if [ "$SKIP_MONITORING" != "true" ]; then
        setup_monitoring
    fi
    
    log "Full-Stack AI Apps deployment completed successfully!"
    log "Check the deployed services:"
    
    for cloud in "${CLOUDS[@]}"; do
        case $cloud in
            "aws")
                info "AWS: Check the AWS Console or use AWS CLI"
                ;;
            "gcp")
                info "GCP: https://console.cloud.google.com/"
                ;;
            "azure")
                info "Azure: https://portal.azure.com/"
                ;;
            "vercel")
                info "Vercel: https://vercel.com/dashboard"
                ;;
        esac
    done
}

# Run the main function
main "$@"