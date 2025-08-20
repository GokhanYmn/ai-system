import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class PortfolioManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PortfolioManagementAgent",
            agent_type="portfolio_optimizer",
            capabilities=["portfolio_optimization", "asset_allocation", "rebalancing", "diversification_analysis"]
        )
        self.portfolio_templates = {
            'conservative': {'bonds': 60, 'stocks': 30, 'cash': 10},
            'moderate': {'bonds': 40, 'stocks': 50, 'alternatives': 10},
            'aggressive': {'stocks': 70, 'alternatives': 20, 'cash': 10}
        }
        
    def can_handle_task(self, task):
        portfolio_tasks = [
            'optimize_portfolio', 'asset_allocation', 'rebalance_portfolio', 
            'analyze_diversification', 'generate_portfolio_recommendation'
        ]
        return task.get('type') in portfolio_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'optimize_portfolio':
                result = self.optimize_portfolio(task.get('user_profile'), task.get('market_data'))
            elif task_type == 'asset_allocation':
                result = self.calculate_asset_allocation(task.get('risk_tolerance'), task.get('investment_amount'))
            elif task_type == 'rebalance_portfolio':
                result = self.rebalance_portfolio(task.get('current_portfolio'), task.get('target_allocation'))
            elif task_type == 'analyze_diversification':
                result = self.analyze_diversification(task.get('portfolio_holdings'))
            elif task_type == 'generate_portfolio_recommendation':
                result = self.generate_comprehensive_recommendation(task.get('user_data'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def optimize_portfolio(self, user_profile, market_data=None):
        """Modern Portföy Teorisi ile portföy optimizasyonu"""
        if not user_profile:
            user_profile = {
                'risk_tolerance': 'moderate',
                'investment_horizon': 'medium_term',
                'investment_amount': 100000,
                'age': 35,
                'income_level': 'middle'
            }
        
        risk_tolerance = user_profile.get('risk_tolerance', 'moderate')
        investment_amount = user_profile.get('investment_amount', 100000)
        age = user_profile.get('age', 35)
        
        # Risk tolerance'a göre allocation
        if risk_tolerance == 'conservative':
            base_allocation = {
                'government_bonds': 40,
                'corporate_bonds': 20,
                'blue_chip_stocks': 25,
                'index_funds': 10,
                'cash': 5
            }
        elif risk_tolerance == 'moderate':
            base_allocation = {
                'index_funds': 35,
                'blue_chip_stocks': 30,
                'growth_stocks': 15,
                'bonds': 15,
                'alternatives': 5
            }
        else:  # aggressive
            base_allocation = {
                'growth_stocks': 40,
                'tech_stocks': 25,
                'emerging_markets': 15,
                'alternatives': 15,
                'cash': 5
            }
        
        # Yaş faktörü ayarlaması
        age_factor = min(age / 100, 0.7)  # Max %70 bond allocation
        if age > 50:
            # Yaşla birlikte risk azalt
            if 'bonds' in base_allocation:
                base_allocation['bonds'] += 10
            if 'cash' in base_allocation:
                base_allocation['cash'] += 5
            if 'growth_stocks' in base_allocation:
                base_allocation['growth_stocks'] -= 10
            if 'tech_stocks' in base_allocation:
                base_allocation['tech_stocks'] -= 5
        
        # Yatırım miktarlarını hesapla
        portfolio_amounts = {}
        for asset, percentage in base_allocation.items():
            portfolio_amounts[asset] = {
                'percentage': percentage,
                'amount': (percentage / 100) * investment_amount,
                'recommendation': self.get_asset_recommendation(asset)
            }
        
        # Risk metrikleri
        expected_return = self.calculate_expected_return(base_allocation)
        risk_score = self.calculate_portfolio_risk(base_allocation)
        
        return {
            "optimized_portfolio": portfolio_amounts,
            "risk_metrics": {
                "expected_annual_return": f"{expected_return:.1f}%",
                "risk_score": risk_score,
                "sharpe_ratio": expected_return / max(risk_score, 1),
                "diversification_score": self.calculate_diversification_score(base_allocation)
            },
            "rebalancing_frequency": "quarterly" if risk_tolerance == "aggressive" else "semi_annually",
            "recommendations": self.generate_optimization_recommendations(base_allocation, user_profile)
        }
    
    def calculate_asset_allocation(self, risk_tolerance, investment_amount):
        """Risk toleransına göre varlık dağılımı"""
        if not risk_tolerance:
            risk_tolerance = 'moderate'
        
        allocations = {
            'conservative': {
                'stocks': 30, 'bonds': 50, 'cash': 15, 'alternatives': 5
            },
            'moderate': {
                'stocks': 60, 'bonds': 25, 'cash': 10, 'alternatives': 5
            },
            'aggressive': {
                'stocks': 80, 'bonds': 10, 'cash': 5, 'alternatives': 5
            }
        }
        
        allocation = allocations.get(risk_tolerance, allocations['moderate'])
        
        # Yatırım miktarlarını hesapla
        amounts = {}
        for asset, percentage in allocation.items():
            amounts[asset] = {
                'percentage': percentage,
                'amount': (percentage / 100) * investment_amount,
                'min_investment': 1000,  # Minimum yatırım
                'suggested_instruments': self.get_suggested_instruments(asset)
            }
        
        return {
            "allocation_strategy": allocation,
            "investment_amounts": amounts,
            "total_invested": investment_amount,
            "risk_level": risk_tolerance,
            "expected_volatility": self.get_expected_volatility(risk_tolerance)
        }
    
    def rebalance_portfolio(self, current_portfolio, target_allocation):
        """Portföy dengeleme önerileri"""
        if not current_portfolio:
            current_portfolio = {
                'stocks': {'current_value': 60000, 'target_percentage': 60},
                'bonds': {'current_value': 30000, 'target_percentage': 25},
                'cash': {'current_value': 10000, 'target_percentage': 15}
            }
        
        total_value = sum(asset['current_value'] for asset in current_portfolio.values())
        rebalancing_actions = []
        
        for asset, data in current_portfolio.items():
            current_percentage = (data['current_value'] / total_value) * 100
            target_percentage = data.get('target_percentage', 0)
            difference = target_percentage - current_percentage
            
            if abs(difference) > 5:  # %5'ten fazla sapma varsa rebalance
                action_amount = (difference / 100) * total_value
                
                action = {
                    'asset': asset,
                    'current_percentage': round(current_percentage, 1),
                    'target_percentage': target_percentage,
                    'difference': round(difference, 1),
                    'action': 'BUY' if difference > 0 else 'SELL',
                    'amount': abs(action_amount),
                    'priority': 'HIGH' if abs(difference) > 10 else 'MEDIUM'
                }
                rebalancing_actions.append(action)
        
        # Rebalancing maliyeti hesaplama
        total_transaction_cost = sum(action['amount'] * 0.001 for action in rebalancing_actions)  # %0.1 komisyon
        
        return {
            "rebalancing_needed": len(rebalancing_actions) > 0,
            "actions_required": rebalancing_actions,
            "total_portfolio_value": total_value,
            "estimated_transaction_cost": total_transaction_cost,
            "rebalancing_benefit": self.calculate_rebalancing_benefit(rebalancing_actions),
            "recommended_frequency": "quarterly"
        }
    
    def analyze_diversification(self, portfolio_holdings):
        """Portföy çeşitlendirme analizi"""
        if not portfolio_holdings:
            portfolio_holdings = {
                'technology_stocks': 40,
                'financial_stocks': 20,
                'healthcare_stocks': 15,
                'energy_stocks': 10,
                'bonds': 15
            }
        
        # Sektör dağılımı analizi
        sector_concentration = self.calculate_sector_concentration(portfolio_holdings)
        
        # Covariance ve correlation analizi (basitleştirilmiş)
        correlation_risk = self.estimate_correlation_risk(portfolio_holdings)
        
        # Diversification score hesaplama
        diversification_score = self.calculate_diversification_score(portfolio_holdings)
        
        warnings = []
        recommendations = []
        
        # Konsantrasyon kontrolleri
        for asset, percentage in portfolio_holdings.items():
            if percentage > 25:
                warnings.append(f"{asset} çok yüksek konsantrasyon: %{percentage}")
                recommendations.append(f"{asset} pozisyonunu azaltın")
        
        if diversification_score < 60:
            recommendations.append("Portföy çeşitlendirmesini artırın")
            recommendations.append("Farklı sektörlerden varlık ekleyin")
        
        return {
            "diversification_analysis": {
                "diversification_score": diversification_score,
                "sector_concentration": sector_concentration,
                "correlation_risk": correlation_risk,
                "concentration_warnings": warnings,
                "improvement_recommendations": recommendations
            },
            "optimal_sector_allocation": self.get_optimal_sector_allocation(),
            "diversification_grade": self.get_diversification_grade(diversification_score)
        }
    
    def generate_comprehensive_recommendation(self, user_data):
        """Kapsamlı portföy önerisi"""
        if not user_data:
            user_data = {
                'age': 35,
                'risk_tolerance': 'moderate',
                'investment_amount': 100000,
                'investment_horizon': 'long_term',
                'current_portfolio': None,
                'financial_goals': ['retirement', 'house_purchase']
            }
        
        # Temel portföy optimizasyonu
        optimization_result = self.optimize_portfolio(user_data)
        
        # Asset allocation
        allocation_result = self.calculate_asset_allocation(
            user_data.get('risk_tolerance'), 
            user_data.get('investment_amount')
        )
        
        # Hedefe yönelik öneriler
        goal_based_recommendations = self.generate_goal_based_recommendations(
            user_data.get('financial_goals', []),
            user_data.get('investment_horizon', 'medium_term')
        )
        
        return {
            "comprehensive_recommendation": {
                "user_profile_summary": {
                    "age": user_data.get('age'),
                    "risk_tolerance": user_data.get('risk_tolerance'),
                    "investment_horizon": user_data.get('investment_horizon'),
                    "total_investment": user_data.get('investment_amount')
                },
                "optimized_portfolio": optimization_result["optimized_portfolio"],
                "asset_allocation": allocation_result["allocation_strategy"],
                "goal_based_strategies": goal_based_recommendations,
                "monitoring_schedule": {
                    "review_frequency": "monthly",
                    "rebalancing_frequency": "quarterly",
                    "strategy_review": "annually"
                },
                "next_steps": [
                    "Önerilen varlık dağılımını uygulayın",
                    "İlk yatırımı kademeli olarak yapın",
                    "Aylık performans takibi başlatın",
                    "Risk toleransını 6 ayda bir gözden geçirin"
                ]
            }
        }
    
    # Yardımcı metodlar
    def get_asset_recommendation(self, asset_type):
        recommendations = {
            'government_bonds': "Düşük risk, sabit getiri",
            'corporate_bonds': "Orta risk, hükümet tahvilinden yüksek getiri",
            'blue_chip_stocks': "Büyük, istikrarlı şirketler",
            'growth_stocks': "Yüksek büyüme potansiyeli",
            'index_funds': "Çeşitlendirilmiş, düşük maliyet",
            'alternatives': "Emlak, emtia, kripto"
        }
        return recommendations.get(asset_type, "Genel yatırım aracı")
    
    def calculate_expected_return(self, allocation):
        # Basit beklenen getiri hesaplama
        expected_returns = {
            'government_bonds': 5, 'corporate_bonds': 6, 'blue_chip_stocks': 8,
            'growth_stocks': 12, 'tech_stocks': 15, 'index_funds': 7,
            'bonds': 5, 'stocks': 10, 'alternatives': 8, 'cash': 2
        }
        
        total_return = 0
        for asset, percentage in allocation.items():
            asset_return = expected_returns.get(asset, 6)
            total_return += (percentage / 100) * asset_return
        
        return total_return
    
    def calculate_portfolio_risk(self, allocation):
        # Basit risk skoru hesaplama
        risk_scores = {
            'government_bonds': 1, 'corporate_bonds': 2, 'blue_chip_stocks': 3,
            'growth_stocks': 4, 'tech_stocks': 5, 'index_funds': 2,
            'bonds': 2, 'stocks': 4, 'alternatives': 4, 'cash': 0
        }
        
        total_risk = 0
        for asset, percentage in allocation.items():
            asset_risk = risk_scores.get(asset, 3)
            total_risk += (percentage / 100) * asset_risk
        
        return total_risk
    
    def calculate_diversification_score(self, allocation):
        # Herfindahl-Hirschman Index benzeri diversification score
        sum_squared = sum((percentage ** 2) for percentage in allocation.values())
        diversification_score = 100 - (sum_squared / 100)
        return max(0, min(100, diversification_score))
    
    def get_suggested_instruments(self, asset_type):
        instruments = {
            'stocks': ['VOO (S&P 500 ETF)', 'VTI (Total Market ETF)', 'Blue chip stocks'],
            'bonds': ['AGG (Bond ETF)', 'Government bonds', 'Corporate bonds'],
            'cash': ['High-yield savings', 'Money market funds', 'CDs'],
            'alternatives': ['REITs', 'Commodities', 'Gold ETF']
        }
        return instruments.get(asset_type, ['Diversified instruments'])
    
    def get_expected_volatility(self, risk_tolerance):
        volatilities = {
            'conservative': '5-8%',
            'moderate': '8-12%',
            'aggressive': '12-18%'
        }
        return volatilities.get(risk_tolerance, '8-12%')
    
    def calculate_sector_concentration(self, holdings):
        sectors = {}
        for holding, percentage in holdings.items():
            if 'stocks' in holding.lower():
                sector = holding.replace('_stocks', '')
                sectors[sector] = percentage
        return sectors
    
    def estimate_correlation_risk(self, holdings):
        # Basit correlation risk estimation
        stock_percentage = sum(v for k, v in holdings.items() if 'stock' in k.lower())
        if stock_percentage > 70:
            return "HIGH"
        elif stock_percentage > 50:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_optimal_sector_allocation(self):
        return {
            'technology': '15-20%',
            'healthcare': '12-15%',
            'financial': '10-15%',
            'consumer_goods': '10-12%',
            'industrial': '8-10%',
            'energy': '5-8%',
            'other': '20-25%'
        }
    
    def get_diversification_grade(self, score):
        if score >= 80:
            return "A - Excellent"
        elif score >= 70:
            return "B - Good"
        elif score >= 60:
            return "C - Fair"
        else:
            return "D - Needs Improvement"
    
    def generate_goal_based_recommendations(self, goals, horizon):
        recommendations = {}
        
        for goal in goals:
            if goal == 'retirement':
                recommendations['retirement'] = {
                    'strategy': 'Long-term growth with gradual shift to conservative',
                    'allocation': 'Age-based allocation (100-age)% in stocks',
                    'instruments': ['401k', 'IRA', 'Index funds', 'Target-date funds']
                }
            elif goal == 'house_purchase':
                recommendations['house_purchase'] = {
                    'strategy': 'Capital preservation with moderate growth',
                    'allocation': '60% bonds, 30% stocks, 10% cash',
                    'instruments': ['CDs', 'High-yield savings', 'Conservative bond funds']
                }
        
        return recommendations
    
    def calculate_rebalancing_benefit(self, actions):
        if not actions:
            return 0
        
        # Basit rebalancing benefit estimation
        total_deviation = sum(abs(action['difference']) for action in actions)
        estimated_benefit = total_deviation * 0.1  # %0.1 benefit per % deviation
        
        return f"{estimated_benefit:.2f}% annual return improvement"
    
    def generate_optimization_recommendations(self, allocation, user_profile):
        recommendations = []
        
        age = user_profile.get('age', 35)
        risk_tolerance = user_profile.get('risk_tolerance', 'moderate')
        
        if age > 55 and any('growth' in asset for asset in allocation.keys()):
            recommendations.append("Yaşınız nedeniyle growth yatırımlarını azaltmayı düşünün")
        
        if risk_tolerance == 'conservative' and any('tech' in asset for asset in allocation.keys()):
            recommendations.append("Risk toleransınıza göre teknoloji yatırımlarını sınırlayın")
        
        recommendations.append("Portföyü 3 ayda bir gözden geçirin")
        recommendations.append("Piyasa volatilitesinde pozisyon büyüklüklerini ayarlayın")
        
        return recommendations

# Test
if __name__ == "__main__":
    agent = PortfolioManagementAgent()
    
    # Test 1: Portfolio optimization
    user_profile = {
        'risk_tolerance': 'moderate',
        'investment_amount': 50000,
        'age': 30,
        'investment_horizon': 'long_term'
    }
    
    task1 = {"type": "optimize_portfolio", "user_profile": user_profile}
    result1 = agent.process_task(task1)
    print("Portfolio Optimization:", result1)
    
    print("Agent Durumu:", agent.get_status())