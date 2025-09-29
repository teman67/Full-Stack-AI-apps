"""
AWS SageMaker Integration
Provides ML model training, deployment, and inference capabilities
"""

import boto3
import json
import logging
import time
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class SageMakerService:
    """AWS SageMaker service for ML operations"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self.sagemaker_client = boto3.client('sagemaker', region_name=region_name)
        self.sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=region_name)
        
    async def create_training_job(
        self,
        job_name: str,
        algorithm_arn: str,
        role_arn: str,
        input_data_config: List[Dict[str, Any]],
        output_data_config: Dict[str, Any],
        resource_config: Dict[str, Any],
        hyperparameters: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Create a SageMaker training job"""
        try:
            training_job_config = {
                'TrainingJobName': job_name,
                'AlgorithmSpecification': {
                    'TrainingImage': algorithm_arn,
                    'TrainingInputMode': 'File'
                },
                'RoleArn': role_arn,
                'InputDataConfig': input_data_config,
                'OutputDataConfig': output_data_config,
                'ResourceConfig': resource_config,
                'StoppingCondition': {
                    'MaxRuntimeInSeconds': 3600  # 1 hour default
                }
            }
            
            if hyperparameters:
                training_job_config['HyperParameters'] = hyperparameters
            
            response = self.sagemaker_client.create_training_job(**training_job_config)
            
            return {
                "training_job_arn": response['TrainingJobArn'],
                "job_name": job_name,
                "status": "InProgress"
            }
            
        except ClientError as e:
            logger.error(f"SageMaker training job creation error: {e}")
            raise Exception(f"Failed to create training job: {str(e)}")
    
    async def create_model(
        self,
        model_name: str,
        execution_role_arn: str,
        primary_container: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a SageMaker model"""
        try:
            response = self.sagemaker_client.create_model(
                ModelName=model_name,
                PrimaryContainer=primary_container,
                ExecutionRoleArn=execution_role_arn
            )
            
            return {
                "model_arn": response['ModelArn'],
                "model_name": model_name
            }
            
        except ClientError as e:
            logger.error(f"SageMaker model creation error: {e}")
            raise Exception(f"Failed to create model: {str(e)}")
    
    async def create_endpoint_config(
        self,
        config_name: str,
        production_variants: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a SageMaker endpoint configuration"""
        try:
            response = self.sagemaker_client.create_endpoint_config(
                EndpointConfigName=config_name,
                ProductionVariants=production_variants
            )
            
            return {
                "endpoint_config_arn": response['EndpointConfigArn'],
                "config_name": config_name
            }
            
        except ClientError as e:
            logger.error(f"SageMaker endpoint config creation error: {e}")
            raise Exception(f"Failed to create endpoint config: {str(e)}")
    
    async def create_endpoint(
        self,
        endpoint_name: str,
        config_name: str
    ) -> Dict[str, Any]:
        """Create a SageMaker endpoint"""
        try:
            response = self.sagemaker_client.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=config_name
            )
            
            return {
                "endpoint_arn": response['EndpointArn'],
                "endpoint_name": endpoint_name,
                "status": "Creating"
            }
            
        except ClientError as e:
            logger.error(f"SageMaker endpoint creation error: {e}")
            raise Exception(f"Failed to create endpoint: {str(e)}")
    
    async def invoke_endpoint(
        self,
        endpoint_name: str,
        payload: Any,
        content_type: str = "application/json"
    ) -> Dict[str, Any]:
        """Invoke a SageMaker endpoint for inference"""
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType=content_type,
                Body=payload
            )
            
            result = response['Body'].read().decode()
            
            return {
                "result": json.loads(result) if content_type == "application/json" else result,
                "endpoint_name": endpoint_name,
                "content_type": response.get('ContentType', content_type)
            }
            
        except ClientError as e:
            logger.error(f"SageMaker endpoint invocation error: {e}")
            raise Exception(f"Failed to invoke endpoint: {str(e)}")
    
    async def create_processing_job(
        self,
        job_name: str,
        app_specification: Dict[str, Any],
        role_arn: str,
        processing_inputs: List[Dict[str, Any]] = None,
        processing_outputs: List[Dict[str, Any]] = None,
        resource_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a SageMaker processing job"""
        try:
            processing_job_config = {
                'ProcessingJobName': job_name,
                'AppSpecification': app_specification,
                'RoleArn': role_arn
            }
            
            if processing_inputs:
                processing_job_config['ProcessingInputs'] = processing_inputs
            
            if processing_outputs:
                processing_job_config['ProcessingOutputConfig'] = {
                    'Outputs': processing_outputs
                }
            
            if resource_config:
                processing_job_config['ProcessingResources'] = resource_config
            else:
                processing_job_config['ProcessingResources'] = {
                    'ClusterConfig': {
                        'InstanceType': 'ml.t3.medium',
                        'InstanceCount': 1,
                        'VolumeSizeInGB': 30
                    }
                }
            
            response = self.sagemaker_client.create_processing_job(**processing_job_config)
            
            return {
                "processing_job_arn": response['ProcessingJobArn'],
                "job_name": job_name,
                "status": "InProgress"
            }
            
        except ClientError as e:
            logger.error(f"SageMaker processing job creation error: {e}")
            raise Exception(f"Failed to create processing job: {str(e)}")
    
    async def get_training_job_status(self, job_name: str) -> Dict[str, Any]:
        """Get training job status"""
        try:
            response = self.sagemaker_client.describe_training_job(
                TrainingJobName=job_name
            )
            
            return {
                "job_name": job_name,
                "status": response['TrainingJobStatus'],
                "creation_time": response['CreationTime'].isoformat(),
                "training_start_time": response.get('TrainingStartTime', '').isoformat() if response.get('TrainingStartTime') else None,
                "training_end_time": response.get('TrainingEndTime', '').isoformat() if response.get('TrainingEndTime') else None,
                "model_artifacts": response.get('ModelArtifacts', {}),
                "failure_reason": response.get('FailureReason', '')
            }
            
        except ClientError as e:
            logger.error(f"Error getting training job status: {e}")
            raise Exception(f"Failed to get training job status: {str(e)}")
    
    async def get_endpoint_status(self, endpoint_name: str) -> Dict[str, Any]:
        """Get endpoint status"""
        try:
            response = self.sagemaker_client.describe_endpoint(
                EndpointName=endpoint_name
            )
            
            return {
                "endpoint_name": endpoint_name,
                "status": response['EndpointStatus'],
                "creation_time": response['CreationTime'].isoformat(),
                "last_modified_time": response['LastModifiedTime'].isoformat(),
                "endpoint_arn": response['EndpointArn'],
                "failure_reason": response.get('FailureReason', '')
            }
            
        except ClientError as e:
            logger.error(f"Error getting endpoint status: {e}")
            raise Exception(f"Failed to get endpoint status: {str(e)}")
    
    async def list_training_jobs(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """List training jobs"""
        try:
            response = self.sagemaker_client.list_training_jobs(
                MaxResults=max_results,
                SortBy='CreationTime',
                SortOrder='Descending'
            )
            
            jobs = []
            for job in response.get('TrainingJobSummaries', []):
                jobs.append({
                    "job_name": job['TrainingJobName'],
                    "status": job['TrainingJobStatus'],
                    "creation_time": job['CreationTime'].isoformat(),
                    "training_end_time": job.get('TrainingEndTime', '').isoformat() if job.get('TrainingEndTime') else None
                })
            
            return jobs
            
        except ClientError as e:
            logger.error(f"Error listing training jobs: {e}")
            raise Exception(f"Failed to list training jobs: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check SageMaker service health"""
        try:
            # Try to list training jobs as a health check
            self.sagemaker_client.list_training_jobs(MaxResults=1)
            
            return {
                "status": "healthy",
                "region": self.region_name,
                "service": "sagemaker"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "region": self.region_name,
                "service": "sagemaker",
                "error": str(e)
            }