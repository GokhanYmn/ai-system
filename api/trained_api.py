from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np
import sys
import os

# Agent'ı import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.learning_agent import LearningAgent

app = FastAPI(title="Eğitilmiş AI Agent API")

# Global eğitilmiş agent
trained_agent = None

@app.on_event("startup")
async def load_model():
    global trained_agent
    
    trained_agent = LearningAgent()
    
    # Eğitilmiş modeli yükle
    model_path = "models/cartpole_agent.pth"
    if os.path.exists(model_path):
        checkpoint = torch.load(model_path)
        trained_agent.q_network.load_state_dict(checkpoint['model_state_dict'])
        trained_agent.epsilon = 0.01  # Test için düşük epsilon
        print(f"✅ Eğitilmiş model yüklendi!")
    else:
        print("⚠️ Model bulunamadı")

class StateRequest(BaseModel):
    state: list

@app.get("/")
def root():
    return {"message": "Eğitilmiş AI Agent API", "model_loaded": trained_agent is not None}

@app.post("/predict")
def predict(request: StateRequest):
    state = np.array(request.state)
    action = trained_agent.act(state)
    return {"action": int(action), "epsilon": trained_agent.epsilon}

@app.post("/test_performance")
def test_performance():
    import gymnasium as gym
    
    env = gym.make('CartPole-v1')
    scores = []
    
    # 5 test oyunu
    for game in range(5):
        state = env.reset()[0]
        total_reward = 0
        
        for step in range(500):
            action = trained_agent.act(state)
            next_state, reward, done, truncated, _ = env.step(action)
            state = next_state
            total_reward += reward
            
            if done or truncated:
                break
        
        scores.append(total_reward)
    
    env.close()
    avg_score = np.mean(scores)
    
    return {
        "scores": scores,
        "average": float(avg_score),
        "status": "Mükemmel!" if avg_score > 100 else "İyi!" if avg_score > 50 else "Gelişmeli"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)