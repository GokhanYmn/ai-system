import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class LearningAgent:
    def __init__(self, state_size=4, action_size=2, learning_rate=0.001):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = learning_rate
        
        # Neural network oluştur
        self.q_network = self._build_model()
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
        
    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_size)
        )
        return model
    
    def act(self, state):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        q_values = self.q_network(state_tensor)
        return np.argmax(q_values.cpu().data.numpy())
    
    def learn_from_trading_data(self, trading_results):
        """İşlem sonuçlarından öğren"""
        if not trading_results:
            return {"message": "Öğrenme verisi yok"}
        
        # Mock learning process
        success_rate = trading_results.get('success_rate', 0.5)
        avg_return = trading_results.get('avg_return', 0.0)
        
        # Epsilon adjustment based on performance
        if success_rate > 0.7 and avg_return > 0.05:
            self.epsilon = max(self.epsilon * 0.95, 0.01)  # Reduce exploration
        elif success_rate < 0.4 or avg_return < -0.05:
            self.epsilon = min(self.epsilon * 1.1, 0.3)   # Increase exploration
        
        return {
            "learning_update": "completed",
            "new_epsilon": self.epsilon,
            "performance_assessment": "improving" if success_rate > 0.6 else "needs_work"
        }
    
    def get_agent_metrics(self):
        """Agent metrikleri"""
        return {
            "name": self.name if hasattr(self, 'name') else "LearningAgent",
            "type": "reinforcement_learner",
            "epsilon": self.epsilon,
            "learning_rate": self.learning_rate,
            "memory_size": len(self.memory) if hasattr(self, 'memory') and self.memory else 0,
            "status": "adaptive_learning"
        }