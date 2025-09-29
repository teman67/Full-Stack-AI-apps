"""
AI Agents System
Autonomous AI agents for complex task execution
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentType(Enum):
    CONVERSATIONAL = "conversational"
    TASK_EXECUTOR = "task_executor"
    ANALYZER = "analyzer"
    DECISION_MAKER = "decision_maker"
    RESEARCH = "research"

class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentAction:
    """Represents an action that an agent can take"""
    id: str
    name: str
    description: str
    parameters: Dict[str, Any]
    result: Optional[Any] = None
    status: str = "pending"
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class AgentTask:
    """Represents a task assigned to an agent"""
    id: str
    description: str
    type: str
    priority: int = 1
    context: Dict[str, Any] = None
    status: AgentStatus = AgentStatus.IDLE
    actions: List[AgentAction] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}
        if self.actions is None:
            self.actions = []

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, agent_id: str, name: str, agent_type: AgentType, description: str = ""):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.description = description
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.memory: List[Dict[str, Any]] = []
        
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a complete task"""
        try:
            self.current_task = task
            self.status = AgentStatus.EXECUTING
            task.status = AgentStatus.EXECUTING
            
            # Simple task execution
            result = {
                "task_id": task.id,
                "task_description": task.description,
                "agent_name": self.name,
                "response": f"Agent {self.name} processed: {task.description}",
                "completed_at": datetime.now().isoformat()
            }
            
            task.result = result
            task.status = AgentStatus.COMPLETED
            task.completed_at = datetime.now()
            
            self.status = AgentStatus.IDLE
            self.current_task = None
            
            return result
            
        except Exception as e:
            error_result = {
                "task_id": task.id,
                "error": str(e),
                "agent_name": self.name,
                "status": "error"
            }
            
            task.result = error_result
            task.status = AgentStatus.ERROR
            self.status = AgentStatus.ERROR
            
            return error_result
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type.value,
            "status": self.status.value,
            "current_task": self.current_task.id if self.current_task else None,
            "memory_items": len(self.memory)
        }

class AgentOrchestrator:
    """Orchestrates multiple agents and manages task distribution"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent '{agent.name}' with ID '{agent.agent_id}'")
    
    async def create_task(
        self,
        description: str,
        task_type: str = "general",
        priority: int = 1,
        context: Dict[str, Any] = None
    ) -> AgentTask:
        """Create a new task"""
        task = AgentTask(
            id=str(uuid.uuid4()),
            description=description,
            type=task_type,
            priority=priority,
            context=context or {}
        )
        
        self.task_queue.append(task)
        logger.info(f"Created task '{task.id}': {description}")
        
        return task
    
    def _select_agent_for_task(self, task: AgentTask) -> Optional[BaseAgent]:
        """Select the best agent for a given task"""
        available_agents = [agent for agent in self.agents.values() if agent.status == AgentStatus.IDLE]
        
        if not available_agents:
            return None
        
        return available_agents[0]
    
    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a specific task"""
        task = next((t for t in self.task_queue if t.id == task_id), None)
        
        if not task:
            return {"error": f"Task {task_id} not found"}
        
        agent = self._select_agent_for_task(task)
        
        if not agent:
            return {"error": "No available agents"}
        
        # Remove from queue
        self.task_queue.remove(task)
        
        # Execute task
        result = await agent.execute_task(task)
        
        # Move to completed tasks
        self.completed_tasks.append(task)
        
        return result
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for the agent system"""
        try:
            return {
                "status": "healthy",
                "total_agents": len(self.agents),
                "active_agents": len([a for a in self.agents.values() if a.status != AgentStatus.ERROR]),
                "queued_tasks": len(self.task_queue),
                "system": "agent-orchestrator"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "system": "agent-orchestrator",
                "error": str(e)
            }

# Global orchestrator instance
orchestrator = AgentOrchestrator()

# Initialize default agents
def initialize_default_agents():
    """Initialize default agents"""
    # Default agent
    default_agent = BaseAgent("default-001", "DefaultAgent", AgentType.TASK_EXECUTOR)
    orchestrator.register_agent(default_agent)
    
    logger.info("Default agents initialized")

# Initialize on module load
initialize_default_agents()