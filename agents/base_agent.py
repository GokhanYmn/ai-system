from abc import ABC, abstractmethod
import torch
import numpy as np
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, name, agent_type, capabilities=None):
        self.name = name
        self.agent_type = agent_type
        self.capabilities = capabilities or []
        self.status = "idle"  # idle, working, learning
        self.created_at = datetime.now()
        self.task_history = []
        
    @abstractmethod
    def process_task(self, task):
        """Her agent kendi görevini işler"""
        pass
    
    @abstractmethod
    def can_handle_task(self, task):
        """Bu agent bu görevi yapabilir mi?"""
        pass
    
    def get_status(self):
        return {
            "name": self.name,
            "type": self.agent_type,
            "status": self.status,
            "capabilities": self.capabilities,
            "tasks_completed": len(self.task_history)
        }
    
    def add_task_to_history(self, task, result, duration):
        self.task_history.append({
            "task": task,
            "result": result,
            "duration": duration,
            "timestamp": datetime.now()
        })