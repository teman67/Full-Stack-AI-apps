"""
Google Cloud Platform AI Integration
Provides access to Vertex AI and other GCP AI services
"""

import logging
from typing import Dict, Any, List, Optional
from google.cloud import aiplatform
from google.cloud import run_v2
import json

logger = logging.getLogger(__name__)

class GCPVertexAIService:
    """GCP Vertex AI service for AI/ML operations"""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=project_id, location=location)
        
    async def generate_text(
        self,
        prompt: str,
        model_name: str = "text-bison@001",
        temperature: float = 0.7,
        max_output_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Generate text using Vertex AI models"""
        try:
            from vertexai.language_models import TextGenerationModel
            
            model = TextGenerationModel.from_pretrained(model_name)
            
            response = model.predict(
                prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=0.8,
                top_k=40
            )
            
            return {
                "generated_text": response.text,
                "model_name": model_name,
                "safety_attributes": response.safety_attributes if hasattr(response, 'safety_attributes') else {},
                "is_blocked": response.is_blocked if hasattr(response, 'is_blocked') else False
            }
            
        except Exception as e:
            logger.error(f"Vertex AI text generation error: {e}")
            raise Exception(f"Failed to generate text: {str(e)}")
    
    async def generate_embeddings(
        self,
        texts: List[str],
        model_name: str = "textembedding-gecko@001"
    ) -> Dict[str, Any]:
        """Generate embeddings using Vertex AI"""
        try:
            from vertexai.language_models import TextEmbeddingModel
            
            model = TextEmbeddingModel.from_pretrained(model_name)
            embeddings = model.get_embeddings(texts)
            
            return {
                "embeddings": [embedding.values for embedding in embeddings],
                "model_name": model_name,
                "dimension": len(embeddings[0].values) if embeddings else 0
            }
            
        except Exception as e:
            logger.error(f"Vertex AI embedding generation error: {e}")
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    async def create_custom_model(
        self,
        display_name: str,
        training_data_uri: str,
        model_type: str = "TEXT_CLASSIFICATION"
    ) -> Dict[str, Any]:
        """Create and train a custom model"""
        try:
            from google.cloud import aiplatform
            
            # Create training job
            job = aiplatform.CustomTrainingJob(
                display_name=f"{display_name}-training-job",
                script_path="training_script.py",
                container_uri="gcr.io/cloud-aiplatform/training/pytorch-gpu.1-9:latest",
                requirements=["torch", "transformers"],
                model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-9:latest"
            )
            
            # Start training
            model = job.run(
                dataset=training_data_uri,
                replica_count=1,
                machine_type="n1-standard-4",
                accelerator_type="NVIDIA_TESLA_K80",
                accelerator_count=1
            )
            
            return {
                "model_name": model.display_name,
                "model_resource_name": model.resource_name,
                "state": model.state,
                "create_time": model.create_time.isoformat() if model.create_time else None
            }
            
        except Exception as e:
            logger.error(f"Custom model creation error: {e}")
            raise Exception(f"Failed to create custom model: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Vertex AI service health"""
        try:
            # Try to list models as a health check
            from google.cloud import aiplatform
            
            models = aiplatform.Model.list(project=self.project_id, location=self.location)
            
            return {
                "status": "healthy",
                "project_id": self.project_id,
                "location": self.location,
                "available_models": len(list(models)),
                "service": "vertex-ai"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "project_id": self.project_id,
                "location": self.location,
                "service": "vertex-ai",
                "error": str(e)
            }