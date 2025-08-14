import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class FinancialAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FinancialAgent",
            agent_type="financial_analyzer",
            capabilities=["balance_sheet_analysis", "income_statement", "ratio_calculation", "valuation"]
        )
        self.financial_ratios = {}
        
    def can_handle_task(self, task):
        """Bu agent hangi görevleri yapabilir?"""
        financial_tasks = ['analyze_balance_sheet', 'calculate_ratios', 'company_valuation', 'trend_analysis']
        return task.get('type') in financial_tasks
    
    def process_task(self, task):
        """Görevi işle"""
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'analyze_balance_sheet':
                result = self.analyze_balance_sheet(task.get('financial_data'))
            elif task_type == 'calculate_ratios':
                result = self.calculate_financial_ratios(task.get('company_code'))
            elif task_type == 'company_valuation':
                result = self.calculate_company_valuation(task.get('company_data'))
            elif task_type == 'trend_analysis':
                result = self.analyze_financial_trends(task.get('historical_data'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def analyze_balance_sheet(self, financial_data):
        """Bilanço analizi yap"""
        if not financial_data:
            # Mock data oluştur
            financial_data = {
                'current_assets': 1000000,
                'total_assets': 5000000,
                'current_liabilities': 500000,
                'total_liabilities': 2000000,
                'equity': 3000000,
                'revenue': 2000000,
                'net_income': 300000,
                'cash': 200000
            }
        
        # Temel oranları hesapla
        current_ratio = financial_data['current_assets'] / financial_data['current_liabilities']
        debt_to_equity = financial_data['total_liabilities'] / financial_data['equity']
        roa = financial_data['net_income'] / financial_data['total_assets']
        roe = financial_data['net_income'] / financial_data['equity']
        
        # Sağlık skoru hesapla (0-100)
        health_score = 0
        
        # Likidite kontrolü
        if current_ratio > 1.5:
            health_score += 25
        elif current_ratio > 1.0:
            health_score += 15
        
        # Borç kontrolü
        if debt_to_equity < 0.5:
            health_score += 25
        elif debt_to_equity < 1.0:
            health_score += 15
        
        # Karlılık kontrolü
        if roe > 0.15:
            health_score += 25
        elif roe > 0.10:
            health_score += 15
        
        # Varlık verimliliği
        if roa > 0.10:
            health_score += 25
        elif roa > 0.05:
            health_score += 15
        
        return {
            "financial_health_score": health_score,
            "ratios": {
                "current_ratio": round(current_ratio, 2),
                "debt_to_equity": round(debt_to_equity, 2),
                "return_on_assets": round(roa * 100, 2),
                "return_on_equity": round(roe * 100, 2)
            },
            "analysis": {
                "liquidity": "Güçlü" if current_ratio > 1.5 else "Orta" if current_ratio > 1.0 else "Zayıf",
                "leverage": "Düşük Risk" if debt_to_equity < 0.5 else "Orta Risk" if debt_to_equity < 1.0 else "Yüksek Risk",
                "profitability": "Mükemmel" if roe > 0.15 else "İyi" if roe > 0.10 else "Orta"
            },
            "recommendation": self.get_financial_recommendation(health_score)
        }
    
    def calculate_financial_ratios(self, company_code):
        """Finansal oranları hesapla"""
        # Mock veri ile hesaplama
        mock_data = {
            'pe_ratio': np.random.uniform(8, 25),
            'pb_ratio': np.random.uniform(0.5, 3.0),
            'dividend_yield': np.random.uniform(0, 8),
            'price_to_sales': np.random.uniform(0.5, 5.0),
            'debt_to_ebitda': np.random.uniform(0.5, 4.0)
        }
        
        # Değerleme analizi
        valuation = "Ucuz"
        if mock_data['pe_ratio'] > 20 or mock_data['pb_ratio'] > 2.5:
            valuation = "Pahalı"
        elif mock_data['pe_ratio'] > 15 or mock_data['pb_ratio'] > 1.8:
            valuation = "Makul"
        
        return {
            "company_code": company_code,
            "valuation_ratios": {
                "pe_ratio": round(mock_data['pe_ratio'], 2),
                "pb_ratio": round(mock_data['pb_ratio'], 2),
                "dividend_yield": round(mock_data['dividend_yield'], 2),
                "price_to_sales": round(mock_data['price_to_sales'], 2),
                "debt_to_ebitda": round(mock_data['debt_to_ebitda'], 2)
            },
            "valuation_assessment": valuation,
            "investment_score": self.calculate_investment_score(mock_data)
        }
    
    def calculate_investment_score(self, ratios):
        """Yatırım skoru hesapla (0-100)"""
        score = 50  # Başlangıç skoru
        
        # PE oranı değerlendirmesi
        if ratios['pe_ratio'] < 12:
            score += 15
        elif ratios['pe_ratio'] < 18:
            score += 5
        elif ratios['pe_ratio'] > 25:
            score -= 10
        
        # PB oranı değerlendirmesi
        if ratios['pb_ratio'] < 1.0:
            score += 15
        elif ratios['pb_ratio'] < 2.0:
            score += 5
        elif ratios['pb_ratio'] > 3.0:
            score -= 10
        
        # Temettü verimi
        if ratios['dividend_yield'] > 4:
            score += 10
        elif ratios['dividend_yield'] > 2:
            score += 5
        
        # Borç kontrolü
        if ratios['debt_to_ebitda'] < 2:
            score += 10
        elif ratios['debt_to_ebitda'] > 4:
            score -= 15
        
        return max(0, min(100, score))
    
    def get_financial_recommendation(self, health_score):
        """Finansal sağlığa göre öneri ver"""
        if health_score >= 80:
            return "GÜÇLÜ AL - Finansal durumu mükemmel"
        elif health_score >= 60:
            return "AL - İyi finansal durum"
        elif health_score >= 40:
            return "BEKLE - Orta risk seviyesi"
        else:
            return "SAT - Yüksek finansal risk"
    
    def calculate_company_valuation(self, company_data):
        """Şirket değerlemesi yap"""
        if not company_data:
            company_data = {
                'market_cap': 1000000000,  # 1 milyar TL
                'revenue': 500000000,      # 500 milyon TL
                'ebitda': 100000000,       # 100 milyon TL
                'net_income': 50000000,    # 50 milyon TL
                'shares_outstanding': 100000000  # 100 milyon hisse
            }
        
        # Temel değerleme metrikleri
        ev_revenue = company_data['market_cap'] / company_data['revenue']
        ev_ebitda = company_data['market_cap'] / company_data['ebitda']
        eps = company_data['net_income'] / company_data['shares_outstanding']
        
        return {
            "valuation_metrics": {
                "enterprise_value_to_revenue": round(ev_revenue, 2),
                "enterprise_value_to_ebitda": round(ev_ebitda, 2),
                "earnings_per_share": round(eps, 2),
                "market_cap_millions": round(company_data['market_cap'] / 1000000, 2)
            },
            "fair_value_estimate": round(eps * 15, 2),  # Basit PE 15 ile hesaplama
            "current_price_vs_fair_value": "Hesaplanacak"
        }

# Test fonksiyonu
if __name__ == "__main__":
    agent = FinancialAgent()
    
    # Test 1: Bilanço analizi
    task1 = {"type": "analyze_balance_sheet", "financial_data": None}
    result1 = agent.process_task(task1)
    print("Bilanço Analizi:", result1)
    
    # Test 2: Finansal oranlar
    task2 = {"type": "calculate_ratios", "company_code": "THYAO"}
    result2 = agent.process_task(task2)
    print("Finansal Oranlar:", result2)
    
    # Agent durumu
    print("Agent Durumu:", agent.get_status())