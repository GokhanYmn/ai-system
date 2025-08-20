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

# Mevcut agent'lar
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

# Yeni eklenen agent'lar
from portfolio_management_agent import PortfolioManagementAgent
from personal_portfolio_agent import PersonalPortfolioAgent
from sentiment_analysis_agent import SentimentAnalysisAgent
from performance_agent import PerformanceAgent

# Global variables
agent_system = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Multi-agent sistem başlatma"""
    global agent_system
    
    print("🚀 Multi-Agent Sistemi başlatılıyor...")
    
    # Initialize all agents (13 agent)
    agents = {
        # Mevcut agent'lar
        'news_agent': NewsAgent(),
        'financial_agent': FinancialAgent(),
        'technical_agent': TechnicalAgent(),
        'data_agent': DataAgent(),
        'decision_agent': DecisionAgent(),
        'trading_agent': TradingAgent(),
        'learning_agent': LearningAgent(),
        'report_agent': ReportAgent(),
        'notification_agent': NotificationAgent(),
        
        # Yeni eklenen agent'lar
        'portfolio_management_agent': PortfolioManagementAgent(),
        'personal_portfolio_agent': PersonalPortfolioAgent(),
        'sentiment_analysis_agent': SentimentAnalysisAgent(),
        'performance_agent': PerformanceAgent()
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
    description="13 Uzman AI Agent ile Kapsamlı Finansal Analiz",
    version="5.0.0",
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
    analysis_depth: str = "full"

class TaskRequest(BaseModel):
    agent_name: str
    task_type: str
    parameters: dict = {}

@app.get("/")
def root():
    return {
        "message": "🤖 Multi-Agent Finans AI Sistemi",
        "version": "5.0.0",
        "active_agents": len(agent_system['agents']) if agent_system else 0,
        "capabilities": [
            "📰 Haber Analizi",
            "📊 Finansal Analiz", 
            "📈 Teknik Analiz",
            "📊 Veri İşleme",
            "🧠 Karar Verme",
            "💼 İşlem Stratejisi",
            "📚 Sürekli Öğrenme",
            "🎯 Koordinasyon",
            "💰 Portföy Yönetimi",
            "👤 Kişisel Portföy Takibi",
            "❤️ Piyasa Duyarlılığı",
            "⚡ Performans İzleme",
            "📄 Rapor Oluşturma"
        ],
        "new_features": [
            "Portfolio optimization with Modern Portfolio Theory",
            "Personal portfolio tracking with P&L analysis",
            "Social media sentiment analysis",
            "Fear & Greed Index calculation",
            "Real-time performance monitoring",
            "Enhanced risk management"
        ],
        "endpoints": {
            "comprehensive_analysis": "/analysis/comprehensive/{symbol}",
            "enhanced_analysis": "/analysis/comprehensive-plus/{symbol}",
            "portfolio_optimization": "/portfolio/optimize",
            "personal_portfolio": "/personal-portfolio/*",
            "sentiment_analysis": "/sentiment/*",
            "performance_monitoring": "/performance/*",
            "agent_status": "/system/agents/status",
            "system_health": "/system/health"
        }
    }
# Mevcut endpoint'ler (korunuyor)
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
        "final_score": result['recommendation'].get('confidence', 50),
        "execution_summary": result['execution_summary'],
        "agent_contributions": result['agent_contributions'],
        "analysis_results": {
            "financial": {"investment_score": 75, "status": "success"},
            "technical": {"technical_score": 2.5, "signal": "AL", "status": "success"},
            "news": {"sentiment": "positive", "confidence": 0.8, "status": "success"}
        },
        "detailed_results": "Detaylı sonuçlar için /analysis/detailed/{analysis_id} endpoint'ini kullanın"
    }

@app.get("/analysis/quick/{symbol}")
def quick_analysis(symbol: str):
    """Hızlı analiz (sadece temel agent'lar)"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    agents = agent_system['agents']
    quick_results = {}
    
    try:
        news_task = {"type": "get_kap_news", "limit": 3}
        quick_results['news'] = agents['news_agent'].process_task(news_task)
        
        financial_task = {"type": "calculate_ratios", "company_code": symbol}
        quick_results['financial'] = agents['financial_agent'].process_task(financial_task)
        
        technical_task = {"type": "generate_signals", "price_data": None}
        quick_results['technical'] = agents['technical_agent'].process_task(technical_task)
        
        quick_recommendation = "BEKLE"
        scores = []
        financial_score = 50
        technical_score = 50
        
        if quick_results['financial'].get('investment_score'):
            financial_score = quick_results['financial']['investment_score']
            scores.append(financial_score)
        
        if quick_results['technical'].get('technical_score'):
            tech_score = quick_results['technical']['technical_score']
            technical_score = 50 + tech_score * 5
            scores.append(technical_score)
        
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
        
        confidence_level = "Yüksek" if len(scores) >= 2 else "Orta"
        
        return {
            "symbol": symbol.upper(),
            "quick_recommendation": str(quick_recommendation),
            "recommendation": str(quick_recommendation),
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

# YENİ PORTFOLIO MANAGEMENT ENDPOINTS
@app.post("/portfolio/optimize")
def optimize_portfolio(request: dict):
    """Portföy optimizasyonu"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    portfolio_agent = agent_system['agents']['portfolio_management_agent']
    
    task = {
        "type": "optimize_portfolio",
        "user_profile": request.get('user_profile'),
        "market_data": request.get('market_data')
    }
    
    result = portfolio_agent.process_task(task)
    return result

@app.post("/portfolio/allocate")
def calculate_asset_allocation(request: dict):
    """Varlık dağılımı hesaplama"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    portfolio_agent = agent_system['agents']['portfolio_management_agent']
    
    task = {
        "type": "asset_allocation",
        "risk_tolerance": request.get('risk_tolerance'),
        "investment_amount": request.get('investment_amount')
    }
    
    result = portfolio_agent.process_task(task)
    return result

@app.post("/portfolio/rebalance")
def rebalance_portfolio(request: dict):
    """Portföy dengeleme"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    portfolio_agent = agent_system['agents']['portfolio_management_agent']
    
    task = {
        "type": "rebalance_portfolio",
        "current_portfolio": request.get('current_portfolio'),
        "target_allocation": request.get('target_allocation')
    }
    
    result = portfolio_agent.process_task(task)
    return result

# YENİ PERSONAL PORTFOLIO ENDPOINTS
@app.post("/personal-portfolio/add-position")
def add_portfolio_position(request: dict):
    """Kişisel portföye pozisyon ekle"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    personal_agent = agent_system['agents']['personal_portfolio_agent']
    
    task = {
        "type": "add_portfolio_position",
        "user_id": request.get('user_id'),
        "position_data": request.get('position_data')
    }
    
    result = personal_agent.process_task(task)
    return result

@app.post("/personal-portfolio/update-prices")
def update_portfolio_prices(request: dict):
    """Portföy fiyatlarını güncelle"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    personal_agent = agent_system['agents']['personal_portfolio_agent']
    
    task = {
        "type": "update_portfolio",
        "user_id": request.get('user_id'),
        "current_prices": request.get('current_prices')
    }
    
    result = personal_agent.process_task(task)
    return result

@app.get("/personal-portfolio/performance/{user_id}")
def get_portfolio_performance(user_id: str):
    """Portföy performansını al"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    personal_agent = agent_system['agents']['personal_portfolio_agent']
    
    task = {
        "type": "calculate_portfolio_performance",
        "user_id": user_id
    }
    
    result = personal_agent.process_task(task)
    return result

@app.post("/personal-portfolio/analyze")
def analyze_personal_portfolio(request: dict):
    """Kişisel portföy analizi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    personal_agent = agent_system['agents']['personal_portfolio_agent']
    
    task = {
        "type": "analyze_personal_portfolio",
        "user_id": request.get('user_id'),
        "market_data": request.get('market_data')
    }
    
    result = personal_agent.process_task(task)
    return result

@app.post("/personal-portfolio/recommendations")
def get_personal_recommendations(request: dict):
    """Kişisel öneriler al"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    personal_agent = agent_system['agents']['personal_portfolio_agent']
    
    task = {
        "type": "generate_personal_recommendations",
        "user_id": request.get('user_id'),
        "market_analysis": request.get('market_analysis')
    }
    
    result = personal_agent.process_task(task)
    return result

# YENİ SENTIMENT ANALYSIS ENDPOINTS
@app.post("/sentiment/social/{symbol}")
def analyze_social_sentiment(symbol: str, platform: str = "twitter"):
    """Sosyal medya sentiment analizi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "analyze_social_sentiment",
        "symbol": symbol.upper(),
        "platform": platform
    }
    
    result = sentiment_agent.process_task(task)
    return result

@app.post("/sentiment/news")
def analyze_news_sentiment(request: dict):
    """Haber sentiment analizi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "analyze_news_sentiment",
        "news_data": request.get('news_data')
    }
    
    result = sentiment_agent.process_task(task)
    return result

@app.get("/sentiment/fear-greed")
def get_fear_greed_index():
    """Korku & Açgözlülük endeksi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "calculate_fear_greed_index",
        "market_data": None
    }
    
    result = sentiment_agent.process_task(task)
    return result

@app.get("/sentiment/market")
def get_market_sentiment():
    """Genel piyasa sentiment"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "get_market_sentiment",
        "symbols": ['THYAO', 'AKBNK', 'BIMAS', 'ASELS', 'KCHOL']
    }
    
    result = sentiment_agent.process_task(task)
    return result

@app.post("/sentiment/signals/{symbol}")
def get_sentiment_signals(symbol: str):
    """Sentiment bazlı sinyaller"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "sentiment_based_signals",
        "symbol": symbol.upper()
    }
    
    result = sentiment_agent.process_task(task)
    return result

@app.get("/sentiment/trends/{symbol}")
def get_sentiment_trends(symbol: str, timeframe: str = "7d"):
    """Sentiment trend takibi"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    
    task = {
        "type": "track_sentiment_trends",
        "symbol": symbol.upper(),
        "timeframe": timeframe
    }
    
    result = sentiment_agent.process_task(task)
    return result

# PERFORMANCE ENDPOINTS
@app.get("/performance/dashboard")
def get_performance_dashboard():
    """Performance dashboard verilerini al"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    performance_agent = agent_system['agents']['performance_agent']
    
    try:
        dashboard_data = performance_agent.get_performance_dashboard_data()
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard verisi alınamadı: {str(e)}")

@app.post("/performance/start")
def start_performance_monitoring():
    """Performance monitoring başlat"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    performance_agent = agent_system['agents']['performance_agent']
    
    task = {"type": "start_monitoring"}
    result = performance_agent.process_task(task)
    
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result.get('error', 'Monitoring başlatılamadı'))
    
    return result

@app.post("/performance/stop")
def stop_performance_monitoring():
    """Performance monitoring durdur"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    performance_agent = agent_system['agents']['performance_agent']
    
    task = {"type": "stop_monitoring"}
    result = performance_agent.process_task(task)
    
    return result

@app.post("/performance/optimize")
def optimize_system_performance():
    """Sistem performansını optimize et"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    performance_agent = agent_system['agents']['performance_agent']
    
    task = {"type": "optimize_system"}
    result = performance_agent.process_task(task)
    
    return result

# GELİŞMİŞ KAPSAMLI ANALİZ (Tüm Agent'ları Kullanır)
@app.post("/analysis/comprehensive-plus/{symbol}")
def comprehensive_analysis_plus(symbol: str):
    """Yeni agent'larla gelişmiş kapsamlı analiz"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    
    # Mevcut analysis'i çalıştır
    base_result = coordinator.process_task({
        "type": "run_full_analysis",
        "symbol": symbol.upper()
    })
    
    if not base_result.get('success'):
        raise HTTPException(status_code=500, detail=base_result.get('error', 'Analiz başarısız'))
    
    # Sentiment analizi ekle
    sentiment_agent = agent_system['agents']['sentiment_analysis_agent']
    sentiment_result = sentiment_agent.process_task({
        "type": "analyze_social_sentiment",
        "symbol": symbol.upper(),
        "platform": "twitter"
    })
    
    sentiment_signals = sentiment_agent.process_task({
        "type": "sentiment_based_signals",
        "symbol": symbol.upper()
    })
    
    # Portfolio önerisi
    portfolio_agent = agent_system['agents']['portfolio_management_agent']
    portfolio_recommendation = portfolio_agent.process_task({
        "type": "generate_portfolio_recommendation",
        "user_data": {
            'risk_tolerance': 'moderate',
            'investment_amount': 100000,
            'age': 35
        }
    })
    
    # Enhanced result
    enhanced_result = base_result.copy()
    enhanced_result.update({
        "sentiment_analysis": sentiment_result.get('social_sentiment_analysis', {}),
        "sentiment_signals": sentiment_signals.get('sentiment_signals', {}),
        "portfolio_recommendation": portfolio_recommendation.get('comprehensive_recommendation', {}),
        "enhanced_features": [
            "Social media sentiment analysis",
            "Portfolio optimization recommendations", 
            "Sentiment-based trading signals",
            "Risk-adjusted position sizing",
            "Fear & Greed Index integration",
            "Personal portfolio context"
        ]
    })
    
    return enhanced_result

# Mevcut endpoint'ler devam ediyor...
@app.post("/agents/{agent_name}/task")
def execute_agent_task(agent_name: str, task_request: TaskRequest):
    """Belirli bir agent'a özel görev ver"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    if agent_name not in agent_system['agents']:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' bulunamadı")
    
    agent = agent_system['agents'][agent_name]
    
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
    
    try:
        agents = agent_system['agents']
        
        financial_result = agents['financial_agent'].process_task({"type": "calculate_ratios", "company_code": symbol})
        technical_result = agents['technical_agent'].process_task({"type": "generate_signals", "price_data": None})
        
        report_data = {
            'symbol': symbol.upper(),
            'analysis_date': datetime.now().isoformat(),
            'recommendation': technical_result.get('overall_signal', 'BEKLE'),
            'confidence': financial_result.get('investment_score', 75),
            'financial_score': financial_result.get('investment_score', 75),
            'technical_score': abs(technical_result.get('technical_score', 2)) * 20 + 40,
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

@app.get("/learning/performance")
def get_learning_performance():
    """Öğrenme performansını göster"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    learning_agent = agent_system['agents']['learning_agent']
    
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

def get_system_summary():
    """Sistem özet raporu"""
    if not agent_system:
        raise HTTPException(status_code=503, detail="Sistem başlatılmadı")
    
    coordinator = agent_system['coordinator']
    agents = agent_system['agents']
    
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
            "Continuous learning and adaptation",
            "Portfolio optimization",
            "Sentiment analysis",
            "Performance monitoring"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)