from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Import all agents
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
agents_path = os.path.join(project_root, 'agents')
sys.path.insert(0, project_root)
sys.path.insert(0, agents_path)

from news_agent import NewsAgent
from financial_agent import FinancialAgent
from technical_agent import TechnicalAgent
from data_agent import DataAgent
from decision_agent import DecisionAgent
from trading_agent import TradingAgent
from learning_agent import LearningAgent
from coordinator_agent import CoordinatorAgent

# Global variables
agent_system = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Multi-agent sistem başlatma"""
    global agent_system
    
    print("🚀 Multi-Agent Sistemi başlatılıyor...")
    
    # Initialize all agents
    agents = {
        'news_agent': NewsAgent(),
        'financial_agent': FinancialAgent(),
        'technical_agent': TechnicalAgent(),
        'data_agent': DataAgent(),
        'decision_agent': DecisionAgent(),
        'trading_agent': TradingAgent(),
        'learning_agent': LearningAgent()
    }
    
    # Initialize coordinator
    coordinator = CoordinatorAgent()
    
    # Register all agents with coordinator
    for name, agent in agents.items():
        coordinator.register_agent(name, agent)
    
    agent_system = {
        'coordinator': coordinator,
        'agents': agents
    }
    
    print("✅ Tüm agent'lar başarıyla başlatıldı!")
    print(f"📊 Sistemde {len(agents)} agent aktif")
    
    yield
    
    print("🛑 Multi-Agent sistemi kapatılıyor...")

app = FastAPI(
    title="🤖 Multi-Agent Finans AI Sistemi",
    description="7 Uzman AI Agent ile Kapsamlı Finansal Analiz",
    version="4.0.0",
    lifespan=lifespan
)

# CORS Middleware ekle - React bağlantısı için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    symbol: str
    analysis_depth: str = "full"  # full, quick, custom

class TaskRequest(BaseModel):
    agent_name: str
    task_type: str
    parameters: dict = {}

@app.get("/")
def root():
    return {
        "message": "🤖 Multi-Agent Finans AI Sistemi",
        "version": "4.0.0",
        "active_agents": len(agent_system['agents']) if agent_system else 0,
        "capabilities": [
            "📰 Haber Analizi",
            "📊 Finansal Analiz", 
            "📈 Teknik Analiz",
            "📊 Veri İşleme",
            "🧠 Karar Verme",
            "💼 İşlem Stratejisi",
            "📚 Sürekli Öğrenme",
            "🎯 Koordinasyon"
        ],
        "endpoints": {
            "comprehensive_analysis": "/analysis/comprehensive/{symbol}",
            "agent_status": "/system/agents/status",
            "system_health": "/system/health",
            "individual_agent": "/agents/{agent_name}/task"
        }
    }

@app.get("/system/agents/status")
def get_agents_status():
    """Tüm agent'ların durumunu göster"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem henüz başlatılmadı")
    
    coordinator = agent_system['coordinator']
    agents_info = coordinator.get_registered_agents()
    
    return {
        "system_status": "operational",
        "total_agents": len(agents_info),
        "agents": agents_info,
        "coordinator_status": coordinator.get_status()
    }

@app.get("/system/health")
def system_health_check():
    """Sistem sağlık kontrolü"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    health_task = {"type": "system_health_check"}
    health_report = coordinator.process_task(health_task)
    
    return health_report

@app.post("/analysis/comprehensive/{symbol}")
def comprehensive_analysis(symbol: str):
    """Kapsamlı çoklu-agent analizi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    
    # Run full analysis workflow
    analysis_task = {
        "type": "run_full_analysis",
        "symbol": symbol.upper()
    }
    
    result = coordinator.process_task(analysis_task)
    
    if not result.get('success'):
        raise HTTPException(status_code=500, detail=result.get('error', 'Analiz başarısız'))
    
    return {
        "analysis_id": result['workflow_id'],
        "symbol": symbol.upper(),
        "timestamp": result.get('timestamp'),
        "recommendation": result['recommendation'],
        "execution_summary": result['execution_summary'],
        "agent_contributions": result['agent_contributions'],
        "detailed_results": "Detaylı sonuçlar için /analysis/detailed/{analysis_id} endpoint'ini kullanın"
    }

@app.post("/agents/{agent_name}/task")
def execute_agent_task(agent_name: str, task_request: TaskRequest):
    """Belirli bir agent'a özel görev ver"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    if agent_name not in agent_system['agents']:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' bulunamadı")
    
    agent = agent_system['agents'][agent_name]
    
    # Create task
    task = {
        "type": task_request.task_type,
        **task_request.parameters
    }
    
    try:
        result = agent.process_task(task)
        return {
            "agent": agent_name,
            "task_type": task_request.task_type,
            "result": result,
            "agent_status": agent.get_status()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent görevi başarısız: {str(e)}")

@app.get("/agents/{agent_name}/status")
def get_agent_status(agent_name: str):
    """Belirli agent'ın durumunu göster"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    if agent_name not in agent_system['agents']:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' bulunamadı")
    
    agent = agent_system['agents'][agent_name]
    return agent.get_status()

@app.get("/analysis/quick/{symbol}")
def quick_analysis(symbol: str):
    """Hızlı analiz (sadece temel agent'lar)"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    agents = agent_system['agents']
    quick_results = {}
    
    # News analysis
    news_task = {"type": "get_kap_news", "limit": 3}
    quick_results['news'] = agents['news_agent'].process_task(news_task)
    
    # Financial ratios
    financial_task = {"type": "calculate_ratios", "company_code": symbol}
    quick_results['financial'] = agents['financial_agent'].process_task(financial_task)
    
    # Technical signals
    technical_task = {"type": "generate_signals", "price_data": None}
    quick_results['technical'] = agents['technical_agent'].process_task(technical_task)
    
    # Quick recommendation
    quick_recommendation = "BEKLE"  # Default
    
    # Simple scoring
    scores = []
    if quick_results['financial'].get('investment_score'):
        scores.append(quick_results['financial']['investment_score'])
    
    if quick_results['technical'].get('technical_score'):
        tech_score = quick_results['technical']['technical_score']
        scores.append(50 + tech_score * 5)  # Convert to 0-100 scale
    
    if scores:
        avg_score = sum(scores) / len(scores)
        if avg_score >= 70:
            quick_recommendation = "AL"
        elif avg_score <= 30:
            quick_recommendation = "SAT"
    
    return {
        "symbol": symbol.upper(),
        "quick_recommendation": quick_recommendation,
        "confidence": "orta",
        "analysis_results": quick_results,
        "note": "Hızlı analiz - Detaylı analiz için /analysis/comprehensive/{symbol} kullanın"
    }

@app.get("/learning/performance")
def get_learning_performance():
    """Öğrenme performansını göster"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    learning_agent = agent_system['agents']['learning_agent']
    
    # Get learning metrics
    if hasattr(learning_agent, 'get_agent_metrics'):
        metrics = learning_agent.get_agent_metrics()
    else:
        metrics = {
            "epsilon": learning_agent.epsilon,
            "learning_rate": learning_agent.learning_rate
        }
    
    return {
        "learning_status": "active",
        "agent_metrics": metrics,
        "performance_trend": "stable",
        "recommendation": "Sistem sürekli öğrenmeye devam ediyor"
    }

@app.post("/trading/execute")
def execute_trade(trade_params: dict):
    """İşlem emri ver"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    trading_agent = agent_system['agents']['trading_agent']
    
    task = {
        "type": "execute_trade",
        "trade_params": trade_params
    }
    
    result = trading_agent.process_task(task)
    
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'İşlem başarısız'))
    
    return result

@app.get("/reports/summary")
def get_system_summary():
    """Sistem özet raporu"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    agents = agent_system['agents']
    
    # Get basic stats from each agent
    agent_stats = {}
    for name, agent in agents.items():
        try:
            stats = agent.get_status()
            agent_stats[name] = {
                "status": stats.get('status', 'unknown'),
                "tasks_completed": stats.get('tasks_completed', 0)
            }
        except:
            agent_stats[name] = {"status": "error", "tasks_completed": 0}
    
    total_tasks = sum(stat.get('tasks_completed', 0) for stat in agent_stats.values())
    
    return {
        "system_overview": {
            "total_agents": len(agents),
            "total_tasks_completed": total_tasks,
            "system_uptime": "active",
            "overall_health": "healthy"
        },
        "agent_summary": agent_stats,
        "coordinator_status": coordinator.get_status(),
        "capabilities": [
            "Real-time market analysis",
            "Multi-source data integration", 
            "Risk-adjusted decision making",
            "Automated trading execution",
            "Continuous learning and adaptation"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)