"""
AWS Bedrock Integration
Provides access to Amazon's foundation models
"""

import boto3
import json
import logging
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BedrockService:
    """AWS Bedrock service for foundation model interactions"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
        self.bedrock_agent_client = boto3.client('bedrock-agent-runtime', region_name=region_name)
        
    async def generate_text(
        self, 
        prompt: str, 
        model_id: str = "anthropic.claude-v2",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate text using Bedrock foundation models"""
        try:
            # Prepare request body based on model
            if "claude" in model_id:
                body = json.dumps({
                    "prompt": f"\\n\\nHuman: {prompt}\\n\\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature
                })
            elif "titan" in model_id:
                body = json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": max_tokens,
                        "temperature": temperature,
                        "topP": 0.9
                    }
                })
            else:
                # Default format
                body = json.dumps({
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                })
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model response format
            if "claude" in model_id:
                generated_text = response_body.get('completion', '')
            elif "titan" in model_id:
                generated_text = response_body.get('results', [{}])[0].get('outputText', '')
            else:
                generated_text = response_body.get('generated_text', '')
            
            return {
                "generated_text": generated_text,
                "model_id": model_id,
                "input_tokens": response_body.get('input_tokens', 0),
                "output_tokens": response_body.get('output_tokens', 0)
            }
            
        except ClientError as e:
            logger.error(f"Bedrock text generation error: {e}")
            raise Exception(f"Failed to generate text: {str(e)}")
    
    async def generate_image(
        self,
        prompt: str,
        model_id: str = "stability.stable-diffusion-xl-v1",
        width: int = 512,
        height: int = 512
    ) -> Dict[str, Any]:
        """Generate images using Bedrock foundation models"""
        try:
            body = json.dumps({
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 10,
                "seed": 0,
                "steps": 50,
                "width": width,
                "height": height
            })
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract image data
            artifacts = response_body.get('artifacts', [])
            if artifacts:
                image_data = artifacts[0].get('base64', '')
                return {
                    "image_data": image_data,
                    "format": "base64",
                    "model_id": model_id,
                    "prompt": prompt
                }
            else:
                raise Exception("No image generated")
                
        except ClientError as e:
            logger.error(f"Bedrock image generation error: {e}")
            raise Exception(f"Failed to generate image: {str(e)}")
    
    async def create_agent(
        self,
        agent_name: str,
        foundation_model: str,
        instruction: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a Bedrock agent"""
        try:
            response = self.bedrock_agent_client.create_agent(
                agentName=agent_name,
                foundationModel=foundation_model,
                instruction=instruction,
                description=description,
                idleSessionTTLInSeconds=1800
            )
            
            return {
                "agent_id": response['agent']['agentId'],
                "agent_name": agent_name,
                "status": response['agent']['agentStatus'],
                "created_at": response['agent']['createdAt'].isoformat()
            }
            
        except ClientError as e:
            logger.error(f"Bedrock agent creation error: {e}")
            raise Exception(f"Failed to create agent: {str(e)}")
    
    async def invoke_agent(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        input_text: str
    ) -> Dict[str, Any]:
        """Invoke a Bedrock agent"""
        try:
            response = self.bedrock_agent_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=input_text
            )
            
            # Process streaming response
            event_stream = response['completion']
            agent_response = ""
            
            for event in event_stream:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        agent_response += chunk['bytes'].decode()
            
            return {
                "response": agent_response,
                "session_id": session_id,
                "agent_id": agent_id
            }
            
        except ClientError as e:
            logger.error(f"Bedrock agent invocation error: {e}")
            raise Exception(f"Failed to invoke agent: {str(e)}")
    
    async def list_foundation_models(self) -> List[Dict[str, Any]]:
        """List available foundation models"""
        try:
            bedrock_client = boto3.client('bedrock', region_name=self.region_name)
            response = bedrock_client.list_foundation_models()
            
            models = []
            for model in response.get('modelSummaries', []):
                models.append({
                    "model_id": model['modelId'],
                    "model_name": model['modelName'],
                    "provider_name": model['providerName'],
                    "input_modalities": model.get('inputModalities', []),
                    "output_modalities": model.get('outputModalities', []),
                    "inference_types": model.get('inferenceTypesSupported', [])
                })
            
            return models
            
        except ClientError as e:
            logger.error(f"Error listing foundation models: {e}")
            raise Exception(f"Failed to list models: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Bedrock service health"""
        try:
            # Try to list models as a health check
            bedrock_client = boto3.client('bedrock', region_name=self.region_name)
            bedrock_client.list_foundation_models()
            
            return {
                "status": "healthy",
                "region": self.region_name,
                "service": "bedrock"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "region": self.region_name,
                "service": "bedrock",
                "error": str(e)
            }