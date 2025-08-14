import gymnasium as gym
import torch
import numpy as np
import sys
import os

# Agent'ı import et
sys.path.append('agents')
from learning_agent import LearningAgent

def train_agent():
    print("🚀 Agent eğitimi başlıyor...")
    
    # Ortam oluştur
    env = gym.make('CartPole-v1')
    agent = LearningAgent()
    
    scores = []
    
    # 100 episode eğitim (hızlı test için)
    for episode in range(100):
        state = env.reset()[0]
        total_reward = 0
        
        for step in range(500):
            action = agent.act(state)
            next_state, reward, done, truncated, _ = env.step(action)
            
            state = next_state
            total_reward += reward
            
            if done or truncated:
                break
        
        scores.append(total_reward)
        
        # Her 25 episodda rapor
        if episode % 25 == 0:
            avg_score = np.mean(scores[-25:]) if len(scores) >= 25 else np.mean(scores)
            print(f"Episode {episode}: Ortalama skor = {avg_score:.1f}")
    
    # Modeli kaydet
    os.makedirs('models', exist_ok=True)
    torch.save({
        'model_state_dict': agent.q_network.state_dict(),
        'epsilon': agent.epsilon
    }, 'models/cartpole_agent.pth')
    
    print("✅ Eğitim tamamlandı ve model kaydedildi!")

if __name__ == "__main__":
    train_agent()