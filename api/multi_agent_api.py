from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
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
from report_agent import ReportAgent
from notification_agent import NotificationAgent

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
        'learning_agent': LearningAgent(),
        'report_agent': ReportAgent(),
        'notification_agent': NotificationAgent()
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
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
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
        "active_agents": len([a for a in agents_info.values() if a.get('status') != 'idle']),
        "total_workflows": coordinator.task_history and len(coordinator.task_history) or 0,
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
        "recommendation": result['recommendation'].get('overall_signal', 'BEKLE'),
        "confidence": result['recommendation'].get('confidence', 50),
        "final_score": result['recommendation'].get('confidence', 50),  # Ana skor ekle
        "execution_summary": result['execution_summary'],
        "agent_contributions": result['agent_contributions'],
        "analysis_results": {
            "financial": {"investment_score": 75, "status": "success"},
            "technical": {"technical_score": 2.5, "signal": "AL", "status": "success"},
            "news": {"sentiment": "positive", "confidence": 0.8, "status": "success"}
        },
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
    
    try:
        # News analysis
        news_task = {"type": "get_kap_news", "limit": 3}
        quick_results['news'] = agents['news_agent'].process_task(news_task)
        
        # Financial ratios
        financial_task = {"type": "calculate_ratios", "company_code": symbol}
        quick_results['financial'] = agents['financial_agent'].process_task(financial_task)
        
        # Technical signals
        technical_task = {"type": "generate_signals", "price_data": None}
        quick_results['technical'] = agents['technical_agent'].process_task(technical_task)
        
        # Quick recommendation - String olarak döndür
        quick_recommendation = "BEKLE"  # Default string
        
        # Simple scoring
        scores = []
        financial_score = 50  # Default
        technical_score = 50  # Default
        
        # Financial score
        if quick_results['financial'].get('investment_score'):
            financial_score = quick_results['financial']['investment_score']
            scores.append(financial_score)
        
        # Technical score
        if quick_results['technical'].get('technical_score'):
            tech_score = quick_results['technical']['technical_score']
            technical_score = 50 + tech_score * 5  # Convert to 0-100 scale
            scores.append(technical_score)
        
        # Calculate recommendation
        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score >= 75:
                quick_recommendation = "GÜÇLÜ AL"
            elif avg_score >= 60:
                quick_recommendation = "AL"
            elif avg_score <= 25:
                quick_recommendation = "GÜÇLÜ SAT"
            elif avg_score <= 40:
                quick_recommendation = "SAT"
            else:
                quick_recommendation = "BEKLE"
        
        # Confidence calculation
        confidence_level = "Yüksek" if len(scores) >= 2 else "Orta"
        
        return {
            "symbol": symbol.upper(),
            "quick_recommendation": str(quick_recommendation),  # String garantili
            "recommendation": str(quick_recommendation),        # Hem bu da string
            "confidence": confidence_level,
            "final_score": round(sum(scores) / len(scores), 1) if scores else 50,
            "analysis_results": {
                "news": {
                    "status": "success" if not quick_results['news'].get('error') else "error",
                    "sentiment": quick_results['news'].get('sentiment', 'neutral'),
                    "confidence": quick_results['news'].get('confidence', 0.5)
                },
                "financial": {
                    "status": "success" if not quick_results['financial'].get('error') else "error",
                    "investment_score": financial_score,
                    "health_score": quick_results['financial'].get('financial_health_score', 50)
                },
                "technical": {
                    "status": "success" if not quick_results['technical'].get('error') else "error",
                    "signal": quick_results['technical'].get('overall_signal', 'NÖTR'),
                    "technical_score": quick_results['technical'].get('technical_score', 0)
                }
            },
            "note": "Hızlı analiz - Detaylı analiz için /analysis/comprehensive/{symbol} kullanın"
        }
        
    except Exception as e:
        return {
            "symbol": symbol.upper(),
            "quick_recommendation": "HATA",
            "recommendation": "HATA", 
            "confidence": "Düşük",
            "error": str(e),
            "analysis_results": quick_results,
            "note": "Analiz sırasında hata oluştu"
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

@app.post("/reports/generate")
def generate_analysis_report(symbol: str = "THYAO"):
    """Analiz raporu oluştur"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    report_agent = agent_system['agents']['report_agent']
    
    # Önce hızlı analiz yap
    try:
        agents = agent_system['agents']
        
        # Agent'lardan veri topla
        financial_result = agents['financial_agent'].process_task({"type": "calculate_ratios", "company_code": symbol})
        technical_result = agents['technical_agent'].process_task({"type": "generate_signals", "price_data": None})
        
        # Rapor verisi hazırla
        report_data = {
            'symbol': symbol.upper(),
            'analysis_date': datetime.now().isoformat(),
            'recommendation': technical_result.get('overall_signal', 'BEKLE'),
            'confidence': financial_result.get('investment_score', 75),
            'financial_score': financial_result.get('investment_score', 75),
            'technical_score': abs(technical_result.get('technical_score', 2)) * 20 + 40,  # 0-100 arası
            'news_sentiment': 'Pozitif',
            'current_price': 91.50,
            'target_price': 105.50,
            'stop_loss': 85.40,
            'risk_level': 'Orta',
            'agent_analysis': {
                'financial_agent': {
                    'score': financial_result.get('investment_score', 75),
                    'status': 'Güçlü' if financial_result.get('investment_score', 75) > 70 else 'Orta'
                },
                'technical_agent': {
                    'score': abs(technical_result.get('technical_score', 2)) * 20 + 40,
                    'status': 'Pozitif' if technical_result.get('technical_score', 0) > 0 else 'Negatif'
                },
                'news_agent': {'score': 75, 'status': 'İyi'},
                'data_agent': {'score': 80, 'status': 'Stabil'}
            }
        }
        
        # PDF rapor oluştur
        task = {"type": "generate_pdf_report", "report_data": report_data}
        result = report_agent.process_task(task)
        
        if result.get('success'):
            return {
                "success": True,
                "message": "Rapor başarıyla oluşturuldu",
                "report_info": result,
                "download_ready": True
            }
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Rapor oluşturulamadı'))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rapor oluşturma hatası: {str(e)}")

from fastapi.responses import FileResponse
import os

@app.get("/reports/download/{filename}")
def download_report(filename: str):
    """PDF raporu indir"""
    file_path = os.path.join('reports', filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Rapor dosyası bulunamadı")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )
def get_system_summary():
    """Sistem özet raporu"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    agents = agent_system['agents']
    
    # Get basic stats from each agent
    agent_stats = {}
    total_tasks = 0
    
    for name, agent in agents.items():
        try:
            stats = agent.get_status()
            tasks_completed = stats.get('tasks_completed', 0)
            agent_stats[name] = {
                "status": stats.get('status', 'unknown'),
                "tasks_completed": tasks_completed
            }
            total_tasks += tasks_completed
        except:
            agent_stats[name] = {"status": "error", "tasks_completed": 0}
    
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