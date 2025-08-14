from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import numpy as np
import gymnasium as gym
import sys
import os

# Import'lar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.learning_agent import LearningAgent
from model_manager import ModelManager

app = FastAPI(title="Gelişmiş AI Agent API", version="3.0.0")

# Global objeler
model_manager = ModelManager()
current_agent = None

@app.on_event("startup")
async def startup():
    global current_agent
    # En iyi modeli yükle
    current_agent = model_manager.load_model('cartpole_agent')
    if current_agent is None:
        current_agent = LearningAgent()
        current_agent.epsilon = 0.01

class StateRequest(BaseModel):
    state: list

class ModelInfo(BaseModel):
    name: str
    description: str = ""

@app.get("/")
def root():
    return {
        "message": "🤖 Gelişmiş AI Agent API",
        "version": "3.0.0",
        "features": ["Model Yönetimi", "Performans Testi", "Tahmin", "Agent Durumu"],
        "current_agent_loaded": current_agent is not None
    }

@app.get("/agent/status")
def get_agent_status():
    """Agent durumunu göster"""
    if current_agent is None:
        return {"status": "not_loaded"}
    
    return {
        "status": "ready",
        "epsilon": current_agent.epsilon,
        "state_size": current_agent.state_size,
        "action_size": current_agent.action_size,
        "model_type": "Deep Q-Network"
    }

@app.post("/agent/predict")
def predict_action(request: StateRequest):
    """Eylem tahmini yap"""
    if current_agent is None:
        raise HTTPException(status_code=400, detail="Agent yüklenmedi")
    
    if len(request.state) != 4:
        raise HTTPException(status_code=400, detail="State 4 elemanlı olmalı")
    
    state = np.array(request.state)
    
    # Epsilon-greedy olmadan, sadece en iyi aksiyon
    state_tensor = torch.FloatTensor(state).unsqueeze(0)
    with torch.no_grad():
        q_values = current_agent.q_network(state_tensor)
        action = int(torch.argmax(q_values).item())
        confidence = float(torch.max(q_values).item())
    
    return {
        "action": action,
        "action_name": "Sol" if action == 0 else "Sağ",
        "confidence": confidence,
        "epsilon": current_agent.epsilon
    }

@app.post("/agent/test")
def test_agent_performance():
    """Agent performansını test et"""
    if current_agent is None:
        raise HTTPException(status_code=400, detail="Agent yüklenmedi")
    
    env = gym.make('CartPole-v1')
    scores = []
    
    # Orijinal epsilon'u sakla
    original_epsilon = current_agent.epsilon
    current_agent.epsilon = 0.0  # Test için deterministik
    
    # 10 test oyunu
    for game in range(10):
        state = env.reset()[0]
        total_reward = 0
        
        for step in range(500):
            action = current_agent.act(state)
            next_state, reward, done, truncated, _ = env.step(action)
            state = next_state
            total_reward += reward
            
            if done or truncated:
                break
        
        scores.append(total_reward)
    
    # Epsilon'u geri yükle
    current_agent.epsilon = original_epsilon
    env.close()
    
    avg_score = np.mean(scores)
    max_score = max(scores)
    min_score = min(scores)
    
    return {
        "scores": scores,
        "average_score": float(avg_score),
        "max_score": int(max_score),
        "min_score": int(min_score),
        "games_played": 10,
        "performance_level": "🏆 Mükemmel!" if avg_score > 300 else "✅ Çok İyi!" if avg_score > 100 else "👍 İyi" if avg_score > 50 else "⚠️ Gelişmeli"
    }

@app.get("/models/list")
def list_models():
    """Tüm modelleri listele"""
    models = model_manager.list_models()
    return {"models": models, "count": len(models)}

@app.post("/models/save")
def save_current_model(info: ModelInfo):
    """Mevcut modeli kaydet"""
    if current_agent is None:
        raise HTTPException(status_code=400, detail="Agent yüklenmedi")
    
    metadata = {
        "description": info.description,
        "saved_by": "API"
    }
    
    model_path = model_manager.save_model(current_agent, info.name, metadata)
    return {"message": f"Model '{info.name}' kaydedildi", "path": model_path}

@app.post("/models/load/{model_name}")
def load_model(model_name: str):
    """Belirtilen modeli yükle"""
    global current_agent
    
    agent = model_manager.load_model(model_name)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' bulunamadı")
    
    current_agent = agent
    return {"message": f"Model '{model_name}' yüklendi", "epsilon": current_agent.epsilon}

@app.delete("/models/{model_name}")
def delete_model(model_name: str):
    """Modeli sil"""
    try:
        model_manager.delete_model(model_name)
        return {"message": f"Model '{model_name}' silindi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)