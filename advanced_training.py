import gymnasium as gym
import torch
import torch.nn as nn
import numpy as np
import sys
import os

# Agent'ı import et
sys.path.append('agents')
from learning_agent import LearningAgent

class AdvancedLearningAgent(LearningAgent):
    def __init__(self, state_size=4, action_size=2, learning_rate=0.001):
        super().__init__(state_size, action_size, learning_rate)
        self.memory = []
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 10000:
            self.memory.pop(0)
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        import random
        batch = random.sample(self.memory, batch_size)
        states = torch.FloatTensor([e[0] for e in batch])
        actions = torch.LongTensor([e[1] for e in batch])
        rewards = torch.FloatTensor([e[2] for e in batch])
        next_states = torch.FloatTensor([e[3] for e in batch])
        dones = torch.BoolTensor([e[4] for e in batch])
        
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        next_q_values = self.q_network(next_states).max(1)[0].detach()
        target_q_values = rewards + (0.99 * next_q_values * ~dones)
        
        loss = nn.MSELoss()(current_q_values.squeeze(), target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def advanced_train():
    print("🚀 Gelişmiş eğitim başlıyor...")
    
    env = gym.make('CartPole-v1')
    agent = AdvancedLearningAgent()
    
    scores = []
    best_avg = 0
    
    for episode in range(500):
        state = env.reset()[0]
        total_reward = 0
        
        for step in range(500):
            action = agent.act(state)
            next_state, reward, done, truncated, _ = env.step(action)
            
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            
            state = next_state
            total_reward += reward
            
            if done or truncated:
                break
        
        scores.append(total_reward)
        
        if episode % 50 == 0:
            avg_score = np.mean(scores[-50:]) if len(scores) >= 50 else np.mean(scores)
            print(f"Episode {episode}: Ortalama = {avg_score:.1f}, Epsilon = {agent.epsilon:.3f}")
            
            if avg_score > best_avg:
                best_avg = avg_score
                os.makedirs('models', exist_ok=True)
                torch.save({
                    'model_state_dict': agent.q_network.state_dict(),
                    'epsilon': 0.01
                }, 'models/cartpole_agent.pth')
                print(f"💾 En iyi model kaydedildi! Skor: {avg_score:.1f}")
    
    print(f"✅ Eğitim tamamlandı! En iyi ortalama: {best_avg:.1f}")

if __name__ == "__main__":
    advanced_train()