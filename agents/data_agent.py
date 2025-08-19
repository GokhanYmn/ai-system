import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class DataAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DataAgent",
            agent_type="data_processor",
            capabilities=["data_collection", "statistical_analysis", "trend_calculation", "data_fusion"]
        )
        self.data_cache = {}
        
    def can_handle_task(self, task):
        data_tasks = ['collect_market_data', 'statistical_analysis', 'combine_agent_data', 'trend_analysis']
        return task.get('type') in data_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'collect_market_data':
                result = self.collect_market_data(task.get('symbol'))
            elif task_type == 'statistical_analysis':
                result = self.perform_statistical_analysis(task.get('data'))
            elif task_type == 'combine_agent_data':
                result = self.combine_multiple_agent_data(task.get('agent_results'))
            elif task_type == 'trend_analysis':
                result = self.analyze_data_trends(task.get('historical_data'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def collect_market_data(self, symbol):
        """Gerçek piyasa verilerini topla"""
        try:
            from real_data_connector import RealDataConnector
            connector = RealDataConnector()
            
            # Gerçek fiyat verilerini al
            price_data = connector.get_stock_price_data(symbol)
            forex_data = connector.get_exchange_rates()
            
            if price_data.get('success'):
                current_time = datetime.now()
                
                market_data = {
                    'symbol': symbol,
                    'current_price': price_data.get('current_price', 0),
                    'previous_close': price_data.get('previous_close', 0),
                    'volume': price_data.get('volume', 0),
                    'market_cap': price_data.get('market_cap'),
                    'currency': price_data.get('currency', 'TRY'),
                    'timestamp': current_time.isoformat(),
                    'market_session': self.get_market_session(current_time),
                    'data_source': price_data.get('source'),
                    'price_change': price_data.get('current_price', 0) - price_data.get('previous_close', 0),
                    'price_change_pct': ((price_data.get('current_price', 0) - price_data.get('previous_close', 0)) / price_data.get('previous_close', 1)) * 100
                }
                
                # Forex data ekle
                if forex_data.get('success'):
                    market_data['forex_rates'] = forex_data.get('rates', {})
                    market_data['usd_try'] = forex_data.get('rates', {}).get('USD_TRY', 30)
                
                # Sector data (mock - gerçek API eklenebilir)
                sectors = ['Teknoloji', 'Finans', 'Enerji', 'Sanayi', 'Tüketim']
                market_data['sector'] = np.random.choice(sectors)
                market_data['sector_performance'] = np.random.uniform(-5, 5)
                
                # PE ratio estimation (basit hesaplama)
                if price_data.get('current_price'):
                    market_data['pe_ratio'] = np.random.uniform(8, 25)  # Mock PE
                    market_data['dividend_yield'] = np.random.uniform(0, 8)
                    market_data['beta'] = np.random.uniform(0.5, 2.0)
                
                # Store in cache
                self.data_cache[symbol] = market_data
                
                return {
                    "success": True,
                    "data": market_data,
                    "data_quality_score": self.assess_data_quality(market_data)
                }
            else:
                return {"success": False, "error": "Fiyat verisi alınamadı"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_market_session(self, time):
        """Piyasa seansını belirle"""
        hour = time.hour
        if 9 <= hour < 18:
            return "Ana Seans"
        elif 18 <= hour < 20:
            return "Gece Seansı"
        else:
            return "Kapalı"
    
    def assess_data_quality(self, data):
        """Veri kalitesini değerlendir"""
        score = 100
        
        # Volume kontrolü
        if data.get('volume', 0) < 100000:
            score -= 20
        
        # Price volatility kontrolü
        if data.get('beta', 1) > 1.8:
            score -= 10
        
        # PE ratio makullük kontrolü
        pe = data.get('pe_ratio', 15)
        if pe > 30 or pe < 5:
            score -= 15
        
        # Data source quality
        if data.get('data_source') == 'YAHOO_FINANCE':
            score += 5
        elif data.get('data_source') == 'MOCK_DATA':
            score -= 15
        
        return max(0, score)
    
    def perform_statistical_analysis(self, data):
        """İstatistiksel analiz yap"""
        if not data:
            # Mock numerical data
            data = np.random.normal(100, 15, 100)
        
        if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            stats = {
                'mean': np.mean(data),
                'median': np.median(data),
                'std_dev': np.std(data),
                'variance': np.var(data),
                'min': np.min(data),
                'max': np.max(data),
                'range': np.max(data) - np.min(data),
                'skewness': self.calculate_skewness(data),
                'count': len(data)
            }
            
            # Percentiles
            stats['percentiles'] = {
                'p25': np.percentile(data, 25),
                'p75': np.percentile(data, 75),
                'p90': np.percentile(data, 90),
                'p95': np.percentile(data, 95)
            }
            
            # Data distribution analysis
            stats['distribution_analysis'] = self.analyze_distribution(data)
            
            return {
                "statistics": {k: round(v, 2) if isinstance(v, (int, float)) else v for k, v in stats.items()},
                "insights": self.generate_statistical_insights(stats)
            }
        
        return {"error": "Uygun veri formatı değil"}
    
    def calculate_skewness(self, data):
        """Çarpıklık hesapla"""
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        skew = (n / ((n-1) * (n-2))) * np.sum(((data - mean) / std) ** 3)
        return skew
    
    def analyze_distribution(self, data):
        """Dağılım analizi"""
        mean = np.mean(data)
        std = np.std(data)
        
        # Normal dağılıma yakınlık kontrolü
        within_1_std = np.sum(np.abs(data - mean) <= std) / len(data)
        within_2_std = np.sum(np.abs(data - mean) <= 2*std) / len(data)
        
        if within_1_std > 0.65 and within_2_std > 0.95:
            distribution_type = "Normal'e Yakın"
        elif within_1_std < 0.5:
            distribution_type = "Geniş Dağılım"
        else:
            distribution_type = "Orta Dağılım"
        
        return {
            "type": distribution_type,
            "within_1_std_pct": round(within_1_std * 100, 1),
            "within_2_std_pct": round(within_2_std * 100, 1)
        }
    
    def generate_statistical_insights(self, stats):
        """İstatistik yorumları üret"""
        insights = []
        
        # Volatilite yorumu
        cv = stats['std_dev'] / stats['mean'] if stats['mean'] != 0 else 0
        if cv > 0.3:
            insights.append("Yüksek volatilite - Riskli yatırım")
        elif cv < 0.1:
            insights.append("Düşük volatilite - Stabil yatırım")
        else:
            insights.append("Orta volatilite - Dengeli risk")
        
        # Trend yorumu
        if abs(stats['skewness']) > 1:
            insights.append("Asimetrik dağılım - Trend eğilimi var")
        else:
            insights.append("Simetrik dağılım - Dengeli hareket")
        
        return insights
    
    def combine_multiple_agent_data(self, agent_results):
        """Birden fazla agent'ın sonuçlarını birleştir"""
        if not agent_results:
            agent_results = {
                'news_agent': {'sentiment': 'positive', 'confidence': 0.7},
                'financial_agent': {'health_score': 75, 'recommendation': 'AL'},
                'technical_agent': {'signal': 'ALIŞ', 'strength': 3}
            }
        
        combined_score = 0
        weight_sum = 0
        
        # Agent ağırlıkları
        weights = {
            'news_agent': 0.2,
            'financial_agent': 0.4,
            'technical_agent': 0.4
        }
        
        analysis_summary = {}
        
        for agent_name, result in agent_results.items():
            weight = weights.get(agent_name, 0.1)
            
            # Her agent'tan skor çıkar
            if agent_name == 'news_agent':
                sentiment = result.get('sentiment', 'neutral')
                confidence = result.get('confidence', 0.5)
                score = (1 if sentiment == 'positive' else -1 if sentiment == 'negative' else 0) * confidence * 100
            elif agent_name == 'financial_agent':
                score = result.get('health_score', 50)
            elif agent_name == 'technical_agent':
                signal = result.get('signal', 'NÖTR')
                strength = result.get('strength', 1)
                if 'ALIŞ' in signal:
                    score = 70 + (strength * 5)
                elif 'SATIŞ' in signal:
                    score = 30 - (strength * 5)
                else:
                    score = 50
            else:
                score = 50
            
            combined_score += score * weight
            weight_sum += weight
            analysis_summary[agent_name] = {"score": round(score, 1), "weight": weight}
        
        final_score = combined_score / weight_sum if weight_sum > 0 else 50
        
        # Nihai tavsiye
        if final_score >= 70:
            recommendation = "GÜÇLÜ AL"
        elif final_score >= 60:
            recommendation = "AL"
        elif final_score >= 40:
            recommendation = "BEKLE"
        else:
            recommendation = "SAT"
        
        return {
            "combined_analysis": {
                "final_score": round(final_score, 1),
                "recommendation": recommendation,
                "confidence_level": "Yüksek" if abs(final_score - 50) > 20 else "Orta",
                "agent_contributions": analysis_summary
            },
            "consensus": self.calculate_consensus(agent_results),
            "risk_assessment": self.assess_combined_risk(final_score)
        }
    
    def calculate_consensus(self, agent_results):
        """Agent'lar arası fikir birliğini hesapla"""
        if len(agent_results) < 2:
            return {"consensus_level": "Yetersiz Veri", "agreement_pct": 0}
        
        # Basit consensus hesaplama
        positive_signals = sum(1 for result in agent_results.values() 
                             if any(word in str(result).lower() for word in ['al', 'positive', 'güçlü']))
        
        total_agents = len(agent_results)
        agreement_pct = (positive_signals / total_agents) * 100
        
        if agreement_pct >= 80:
            consensus = "Güçlü Fikir Birliği"
        elif agreement_pct >= 60:
            consensus = "Orta Fikir Birliği"
        else:
            consensus = "Zayıf Fikir Birliği"
        
        return {"consensus_level": consensus, "agreement_pct": round(agreement_pct, 1)}
    
    def assess_combined_risk(self, final_score):
        """Birleşik risk değerlendirmesi"""
        if final_score >= 80:
            return {"risk_level": "Düşük", "risk_score": 20}
        elif final_score >= 60:
            return {"risk_level": "Orta-Düşük", "risk_score": 40}
        elif final_score >= 40:
            return {"risk_level": "Orta", "risk_score": 60}
        elif final_score >= 20:
            return {"risk_level": "Yüksek", "risk_score": 80}
        else:
            return {"risk_level": "Çok Yüksek", "risk_score": 95}

# Test
if __name__ == "__main__":
    agent = DataAgent()
    
    # Test 1: Market data toplama
    task1 = {"type": "collect_market_data", "symbol": "THYAO"}
    result1 = agent.process_task(task1)
    print("Market Data:", result1)
    
    # Test 2: Agent verilerini birleştirme
    task2 = {"type": "combine_agent_data", "agent_results": None}
    result2 = agent.process_task(task2)
    print("Birleşik Analiz:", result2)
    
    print("Agent Durumu:", agent.get_status())
    