"""Workflow Analytics - Analytics and metrics for multi-agent workflows."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class AgentType(Enum):
    NVIDIA_GPU = "nvidia"
    AWS_TRAINIUM = "trainium"
    GOOGLE_TPU = "tpu"
    CPU = "cpu"


class Protocol(Enum):
    MCP = "mcp"
    A2A = "a2a"
    CUSTOM = "custom"
    HTTP = "http"


@dataclass
class WorkflowMetrics:
    workflow_id: str
    duration: float
    tasks_completed: int
    tasks_failed: int
    agents_used: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"workflow_id": self.workflow_id, "duration": self.duration, 
                "tasks_completed": self.tasks_completed, "agents": self.agents_used}


@dataclass
class AgentMetrics:
    agent_id: str
    tasks_completed: int
    total_duration: float
    success_rate: float
    last_active: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"agent_id": self.agent_id, "tasks": self.tasks_completed, 
                "avg_duration": self.total_duration / max(self.tasks_completed, 1)}


class WorkflowAnalytics:
    """Analytics and metrics for multi-agent workflows."""
    
    def __init__(self):
        self.workflows: Dict[str, WorkflowMetrics] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
    
    def track_workflow(self, workflow_id: str, data: Dict[str, Any]) -> None:
        metrics = WorkflowMetrics(
            workflow_id=workflow_id,
            duration=data.get("duration", 0),
            tasks_completed=data.get("tasks_completed", 0),
            tasks_failed=data.get("tasks_failed", 0),
            agents_used=data.get("agents_used", [])
        )
        self.workflows[workflow_id] = metrics
        
        for agent_id in metrics.agents_used:
            if agent_id not in self.agent_metrics:
                self.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id, tasks_completed=0, total_duration=0, success_rate=1.0)
            self.agent_metrics[agent_id].tasks_completed += 1
            self.agent_metrics[agent_id].total_duration += metrics.duration / max(len(metrics.agents_used), 1)
    
    def get_metrics(self) -> Dict[str, Any]:
        if not self.workflows:
            return {"total_workflows": 0, "avg_duration": 0}
        
        durations = [w.duration for w in self.workflows.values()]
        return {
            "total_workflows": len(self.workflows),
            "avg_duration": sum(durations) / len(durations),
            "total_tasks": sum(w.tasks_completed for w in self.workflows.values()),
            "agent_count": len(self.agent_metrics)
        }
    
    def get_agent_stats(self, agent_id: str) -> Optional[Dict[str, Any]]:
        metrics = self.agent_metrics.get(agent_id)
        return metrics.to_dict() if metrics else None
    
    def get_top_agents(self, limit: int = 5) -> List[Dict[str, Any]]:
        sorted_agents = sorted(self.agent_metrics.values(), key=lambda a: a.tasks_completed, reverse=True)
        return [a.to_dict() for a in sorted_agents[:limit]]


__all__ = ["WorkflowAnalytics", "WorkflowMetrics", "AgentMetrics", "AgentType", "Protocol"]
