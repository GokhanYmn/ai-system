from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np
import sys
import os

# Agent'ı import et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.learning_agent import LearningAgent

app = FastAPI(title="AI Agent API")

# Global agent
agent = LearningAgent()

class StateRequest(BaseModel):
    state: list

@app.get("/")
def root():
    return {"message": "AI Agent API çalışıyor!"}

@app.post("/predict")
def predict(request: StateRequest):
    state = np.array(request.state)
    action = agent.act(state)
    return {"action": int(action)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)