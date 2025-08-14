import torch
import os
import json
from datetime import datetime
import sys

sys.path.append('agents')
from learning_agent import LearningAgent

class ModelManager:
    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        
    def save_model(self, agent, name, metadata=None):
        """Modeli kaydet"""
        model_path = os.path.join(self.models_dir, f"{name}.pth")
        metadata_path = os.path.join(self.models_dir, f"{name}_info.json")
        
        # Model kaydet
        torch.save({
            'model_state_dict': agent.q_network.state_dict(),
            'epsilon': agent.epsilon,
            'state_size': agent.state_size,
            'action_size': agent.action_size,
            'learning_rate': agent.learning_rate
        }, model_path)
        
        # Metadata kaydet
        info = {
            'name': name,
            'save_date': datetime.now().isoformat(),
            'epsilon': agent.epsilon,
            'state_size': agent.state_size,
            'action_size': agent.action_size,
            'learning_rate': agent.learning_rate
        }
        
        if metadata:
            info.update(metadata)
            
        with open(metadata_path, 'w') as f:
            json.dump(info, f, indent=2)
            
        print(f"✅ Model kaydedildi: {model_path}")
        return model_path
    
    def load_model(self, name):
        """Modeli yükle"""
        model_path = os.path.join(self.models_dir, f"{name}.pth")
        
        if not os.path.exists(model_path):
            print(f"❌ Model bulunamadı: {model_path}")
            return None
            
        agent = LearningAgent()
        checkpoint = torch.load(model_path)
        agent.q_network.load_state_dict(checkpoint['model_state_dict'])
        agent.epsilon = checkpoint.get('epsilon', 0.01)
        
        print(f"✅ Model yüklendi: {model_path}")
        return agent
    
    def list_models(self):
        """Tüm modelleri listele"""
        models = []
        for file in os.listdir(self.models_dir):
            if file.endswith('_info.json'):
                info_path = os.path.join(self.models_dir, file)
                with open(info_path, 'r') as f:
                    models.append(json.load(f))
        return models
    
    def delete_model(self, name):
        """Modeli sil"""
        model_path = os.path.join(self.models_dir, f"{name}.pth")
        info_path = os.path.join(self.models_dir, f"{name}_info.json")
        
        for path in [model_path, info_path]:
            if os.path.exists(path):
                os.remove(path)
                
        print(f"✅ Model silindi: {name}")

# Test fonksiyonu
if __name__ == "__main__":
    manager = ModelManager()
    
    # Mevcut modeli test et
    agent = manager.load_model('cartpole_agent')
    if agent:
        print(f"Model yüklendi, epsilon: {agent.epsilon}")
    
    # Modelleri listele
    models = manager.list_models()
    print("Mevcut modeller:", models)