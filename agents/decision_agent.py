import numpy as np
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DecisionAgent",
            agent_type="decision_maker",
            capabilities=["risk_assessment", "portfolio_optimization", "strategy_selection", "decision_making"]
        )
        self.risk_tolerance = "moderate"
        self.decision_history = []
        
    def can_handle_task(self, task):
        decision_tasks = ['make_investment_decision', 'assess_portfolio_risk', 'optimize_allocation', 'strategy_recommendation']
        return task.get('type') in decision_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'make_investment_decision':
                result = self.make_investment_decision(task.get('analysis_data'))
            elif task_type == 'assess_portfolio_risk':
                result = self.assess_portfolio_risk(task.get('portfolio_data'))
            elif task_type == 'optimize_allocation':
                result = self.optimize_portfolio_allocation(task.get('assets'))
            elif task_type == 'strategy_recommendation':
                result = self.recommend_strategy(task.get('market_conditions'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def make_investment_decision(self, analysis_data):
        """Yatırım kararı ver"""
        if not analysis_data:
            # Mock analysis data
            analysis_data = {
                'final_score': 75,
                'recommendation': 'GÜÇLÜ AL',
                'risk_level': 'Orta',
                'consensus': 'Güçlü Fikir Birliği',
                'technical_signal': 'ALIŞ',
                'financial_health': 80,
                'news_sentiment': 'positive'
            }
        
        # Risk-adjusted decision making
        base_score = analysis_data.get('final_score', 50)
        risk_level = analysis_data.get('risk_level', 'Orta')
        
        # Risk tolerance adjustment
        risk_multiplier = self.get_risk_multiplier(risk_level)
        adjusted_score = base_score * risk_multiplier
        
        # Position sizing
        position_size = self.calculate_position_size(adjusted_score, risk_level)
        
        # Stop loss ve take profit seviyeleri
        stop_loss, take_profit = self.calculate_stop_take_levels(analysis_data)
        
        # Final decision
        decision = self.generate_final_decision(adjusted_score, position_size)
        
        # Decision confidence
        confidence = self.calculate_decision_confidence(analysis_data)
        
        decision_result = {
            "investment_decision": {
                "action": decision['action'],
                "position_size_pct": position_size,
                "confidence": confidence,
                "rationale": decision['rationale']
            },
            "risk_management": {
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "max_loss_pct": min(position_size * 0.2, 2),  # Max %2 portföy kaybı
                "risk_reward_ratio": take_profit / stop_loss if stop_loss > 0 else 0
            },
            "timing": {
                "urgency": "Yüksek" if adjusted_score > 80 else "Orta" if adjusted_score > 60 else "Düşük",
                "holding_period": self.estimate_holding_period(analysis_data),
                "entry_strategy": "Kademeli" if risk_level in ['Yüksek', 'Çok Yüksek'] else "Tek Seferde"
            },
            "monitoring": {
                "review_frequency": "Günlük" if risk_level == 'Yüksek' else "Haftalık",
                "key_indicators": self.identify_key_indicators(analysis_data),
                "exit_conditions": self.define_exit_conditions(analysis_data)
            }
        }
        
        # Store decision in history
        self.decision_history.append({
            "timestamp": datetime.now(),
            "decision": decision_result,
            "input_data": analysis_data
        })
        
        return decision_result
    
    def get_risk_multiplier(self, risk_level):
        """Risk seviyesine göre çarpan"""
        multipliers = {
            'Çok Düşük': 1.1,
            'Düşük': 1.05,
            'Orta-Düşük': 1.0,
            'Orta': 0.95,
            'Yüksek': 0.85,
            'Çok Yüksek': 0.7
        }
        return multipliers.get(risk_level, 0.9)
    
    def calculate_position_size(self, score, risk_level):
        """Pozisyon büyüklüğü hesapla (%portföy)"""
        base_size = 10  # %10 base position
        
        # Score adjustment
        if score > 80:
            base_size *= 1.5
        elif score > 70:
            base_size *= 1.2
        elif score < 40:
            base_size *= 0.5
        elif score < 30:
            base_size *= 0.3
        
        # Risk adjustment
        risk_adjustments = {
            'Çok Düşük': 1.3,
            'Düşük': 1.1,
            'Orta-Düşük': 1.0,
            'Orta': 0.9,
            'Yüksek': 0.6,
            'Çok Yüksek': 0.3
        }
        
        final_size = base_size * risk_adjustments.get(risk_level, 0.8)
        return min(max(round(final_size, 1), 1.0), 25.0)  # Min %1, Max %25
    
    def calculate_stop_take_levels(self, analysis_data):
        """Stop loss ve take profit seviyeleri"""
        risk_level = analysis_data.get('risk_level', 'Orta')
        volatility = analysis_data.get('volatility', 0.15)  # Default %15
        
        # Risk level'a göre stop loss
        stop_loss_pcts = {
            'Çok Düşük': 3,
            'Düşük': 5,
            'Orta-Düşük': 7,
            'Orta': 10,
            'Yüksek': 15,
            'Çok Yüksek': 20
        }
        
        stop_loss = stop_loss_pcts.get(risk_level, 10)
        
        # Take profit (genellikle stop loss'un 2-3 katı)
        risk_reward = 2.5
        if analysis_data.get('final_score', 50) > 80:
            risk_reward = 3.0
        elif analysis_data.get('final_score', 50) < 40:
            risk_reward = 1.5
        
        take_profit = stop_loss * risk_reward
        
        return round(stop_loss, 1), round(take_profit, 1)
    
    def generate_final_decision(self, adjusted_score, position_size):
        """Final kararı oluştur"""
        if adjusted_score >= 75:
            action = "GÜÇLÜ AL"
            rationale = f"Yüksek skor ({adjusted_score:.1f}) ve uygun risk profili"
        elif adjusted_score >= 60:
            action = "AL"
            rationale = f"Pozitif skor ({adjusted_score:.1f}) ve makul risk"
        elif adjusted_score >= 45:
            action = "BEKLE"
            rationale = f"Kararsız skor ({adjusted_score:.1f}), daha fazla analiz gerekli"
        elif adjusted_score >= 30:
            action = "ZAYIF SAT"
            rationale = f"Düşük skor ({adjusted_score:.1f}), risk yüksek"
        else:
            action = "GÜÇLÜ SAT"
            rationale = f"Çok düşük skor ({adjusted_score:.1f}), yüksek risk"
        
        return {"action": action, "rationale": rationale}
    
    def calculate_decision_confidence(self, analysis_data):
        """Karar güvenilirliği hesapla"""
        factors = []
        
        # Consensus strength
        consensus = analysis_data.get('consensus', 'Zayıf')
        if 'Güçlü' in consensus:
            factors.append(0.3)
        elif 'Orta' in consensus:
            factors.append(0.2)
        else:
            factors.append(0.1)
        
        # Data quality
        if analysis_data.get('final_score', 0) != 0:
            factors.append(0.25)
        
        # Multiple confirmations
        confirmations = sum(1 for key in ['technical_signal', 'financial_health', 'news_sentiment'] 
                          if key in analysis_data)
        factors.append(min(confirmations * 0.15, 0.45))
        
        confidence = sum(factors)
        return min(round(confidence * 100, 1), 95.0)
    
    def estimate_holding_period(self, analysis_data):
        """Tahmini elde tutma süresi"""
        technical_signal = analysis_data.get('technical_signal', '')
        financial_health = analysis_data.get('financial_health', 50)
        
        if financial_health > 80 and 'GÜÇLÜ' in technical_signal:
            return "Uzun Vade (6+ ay)"
        elif financial_health > 60:
            return "Orta Vade (2-6 ay)"
        else:
            return "Kısa Vade (1-2 ay)"
    
    def identify_key_indicators(self, analysis_data):
        """Takip edilecek temel göstergeler"""
        indicators = ["Fiyat hareketi", "Hacim değişimi"]
        
        if analysis_data.get('news_sentiment'):
            indicators.append("Haber akışı")
        
        if analysis_data.get('financial_health', 0) > 0:
            indicators.append("Finansal oranlar")
        
        indicators.append("Sektör performansı")
        
        return indicators
    
    def define_exit_conditions(self, analysis_data):
        """Çıkış koşulları tanımla"""
        conditions = []
        
        # Technical exit
        conditions.append("Stop loss seviyesine ulaşma")
        conditions.append("Take profit hedefine ulaşma")
        
        # Fundamental exit
        if analysis_data.get('financial_health', 0) > 60:
            conditions.append("Finansal sağlık skorunda %20+ düşüş")
        
        # News-based exit
        conditions.append("Kritik olumsuz haber")
        
        # Time-based exit
        conditions.append("Beklenen sürede hedef gerçekleşmezse")
        
        return conditions
    
    def assess_portfolio_risk(self, portfolio_data):
        """Portföy riskini değerlendir"""
        if not portfolio_data:
            portfolio_data = {
                'positions': [
                    {'symbol': 'THYAO', 'weight': 30, 'beta': 1.2},
                    {'symbol': 'AKBNK', 'weight': 25, 'beta': 1.5},
                    {'symbol': 'BIMAS', 'weight': 20, 'beta': 0.8},
                    {'symbol': 'ASELS', 'weight': 15, 'beta': 1.1},
                    {'symbol': 'CASH', 'weight': 10, 'beta': 0.0}
                ]
            }
        
        positions = portfolio_data['positions']
        
        # Portfolio beta calculation
        portfolio_beta = sum(pos['weight'] * pos['beta'] for pos in positions) / 100
        
        # Concentration risk
        max_weight = max(pos['weight'] for pos in positions)
        concentration_risk = "Yüksek" if max_weight > 40 else "Orta" if max_weight > 25 else "Düşük"
        
        # Diversification score
        num_positions = len([p for p in positions if p['symbol'] != 'CASH'])
        diversification = "İyi" if num_positions >= 8 else "Orta" if num_positions >= 5 else "Zayıf"
        
        # Risk assessment
        if portfolio_beta > 1.3:
            risk_level = "Yüksek"
        elif portfolio_beta > 1.1:
            risk_level = "Orta-Yüksek"
        elif portfolio_beta > 0.9:
            risk_level = "Orta"
        else:
            risk_level = "Düşük"
        
        return {
            "portfolio_risk": {
                "overall_risk": risk_level,
                "portfolio_beta": round(portfolio_beta, 2),
                "concentration_risk": concentration_risk,
                "diversification": diversification,
                "max_single_position": f"{max_weight}%"
            },
            "risk_metrics": {
                "var_estimate": f"{round(portfolio_beta * 2.5, 1)}%",  # Simplified VaR
                "max_drawdown_estimate": f"{round(portfolio_beta * 15, 1)}%",
                "volatility_estimate": f"{round(portfolio_beta * 18, 1)}%"
            },
            "recommendations": self.generate_portfolio_recommendations(portfolio_beta, concentration_risk, num_positions)
        }
    
    def generate_portfolio_recommendations(self, beta, concentration, positions):
        """Portföy önerileri"""
        recommendations = []
        
        if beta > 1.3:
            recommendations.append("Portföy betasını düşürün - düşük riskli varlıklar ekleyin")
        
        if concentration == "Yüksek":
            recommendations.append("Konsantrasyon riskini azaltın - pozisyonları dengeleyın")
        
        if positions < 5:
            recommendations.append("Diversifikasyonu artırın - daha fazla varlık ekleyin")
        
        if not recommendations:
            recommendations.append("Portföy risk profili uygun görünüyor")
        
        return recommendations

# Test
if __name__ == "__main__":
    agent = DecisionAgent()
    
    # Test 1: Investment decision
    mock_analysis = {
        'final_score': 78,
        'recommendation': 'GÜÇLÜ AL',
        'risk_level': 'Orta-Düşük',
        'consensus': 'Güçlü Fikir Birliği'
    }
    
    task1 = {"type": "make_investment_decision", "analysis_data": mock_analysis}
    result1 = agent.process_task(task1)
    print("Yatırım Kararı:", result1)
    
    # Test 2: Portfolio risk
    task2 = {"type": "assess_portfolio_risk", "portfolio_data": None}
    result2 = agent.process_task(task2)
    print("Portföy Risk:", result2)
    
    print("Agent Durumu:", agent.get_status())