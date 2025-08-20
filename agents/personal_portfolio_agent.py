import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class PersonalPortfolioAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PersonalPortfolioAgent",
            agent_type="personal_portfolio_tracker",
            capabilities=["portfolio_tracking", "performance_analysis", "profit_loss_calculation", "personal_recommendations"]
        )
        self.user_portfolios = {}  # Kullanıcı portföylerini sakla
        
    def can_handle_task(self, task):
        portfolio_tasks = [
            'add_portfolio_position', 'update_portfolio', 'calculate_portfolio_performance',
            'analyze_personal_portfolio', 'generate_personal_recommendations', 'track_profit_loss'
        ]
        return task.get('type') in portfolio_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'add_portfolio_position':
                result = self.add_portfolio_position(task.get('user_id'), task.get('position_data'))
            elif task_type == 'update_portfolio':
                result = self.update_portfolio_prices(task.get('user_id'), task.get('current_prices'))
            elif task_type == 'calculate_portfolio_performance':
                result = self.calculate_portfolio_performance(task.get('user_id'))
            elif task_type == 'analyze_personal_portfolio':
                result = self.analyze_personal_portfolio(task.get('user_id'), task.get('market_data'))
            elif task_type == 'generate_personal_recommendations':
                result = self.generate_personal_recommendations(task.get('user_id'), task.get('market_analysis'))
            elif task_type == 'track_profit_loss':
                result = self.track_profit_loss(task.get('user_id'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def add_portfolio_position(self, user_id, position_data):
        """Kullanıcının portföyüne yeni pozisyon ekle"""
        if not position_data:
            position_data = {
                'symbol': 'THYAO',
                'quantity': 1000,
                'purchase_price': 85.50,
                'purchase_date': datetime.now().isoformat(),
                'asset_type': 'stock'
            }
        
        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = {
                'positions': [],
                'created_date': datetime.now(),
                'last_updated': datetime.now()
            }
        
        # Pozisyon bilgilerini hazırla
        position = {
            'id': f"{user_id}_{position_data['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'symbol': position_data['symbol'],
            'quantity': position_data['quantity'],
            'purchase_price': position_data['purchase_price'],
            'purchase_date': position_data.get('purchase_date', datetime.now().isoformat()),
            'asset_type': position_data.get('asset_type', 'stock'),
            'current_price': position_data['purchase_price'],  # Başlangıçta alış fiyatı
            'total_cost': position_data['quantity'] * position_data['purchase_price'],
            'current_value': position_data['quantity'] * position_data['purchase_price'],
            'unrealized_pnl': 0,
            'unrealized_pnl_pct': 0,
            'status': 'active'
        }
        
        # Aynı sembolden varsa birleştir veya yeni pozisyon ekle
        existing_position = self.find_existing_position(user_id, position_data['symbol'])
        
        if existing_position:
            # Mevcut pozisyonu güncelle (average down/up)
            updated_position = self.merge_positions(existing_position, position)
            # Eski pozisyonu kaldır, yeniyi ekle
            self.user_portfolios[user_id]['positions'] = [
                p for p in self.user_portfolios[user_id]['positions'] 
                if p['symbol'] != position_data['symbol']
            ]
            self.user_portfolios[user_id]['positions'].append(updated_position)
        else:
            # Yeni pozisyon ekle
            self.user_portfolios[user_id]['positions'].append(position)
        
        self.user_portfolios[user_id]['last_updated'] = datetime.now()
        
        return {
            "success": True,
            "position_added": position,
            "portfolio_summary": self.get_portfolio_summary(user_id),
            "message": f"{position_data['symbol']} pozisyonu portföye eklendi"
        }
    
    def update_portfolio_prices(self, user_id, current_prices):
        """Portföydeki pozisyonların güncel fiyatlarını güncelle"""
        if user_id not in self.user_portfolios:
            return {"error": "Kullanıcı portföyü bulunamadı"}
        
        if not current_prices:
            # Mock current prices
            current_prices = {
                'THYAO': 92.30,
                'AKBNK': 46.80,
                'BIMAS': 188.50
            }
        
        updated_positions = []
        total_unrealized_pnl = 0
        
        for position in self.user_portfolios[user_id]['positions']:
            symbol = position['symbol']
            
            if symbol in current_prices:
                # Güncel fiyatı güncelle
                position['current_price'] = current_prices[symbol]
                position['current_value'] = position['quantity'] * current_prices[symbol]
                position['unrealized_pnl'] = position['current_value'] - position['total_cost']
                position['unrealized_pnl_pct'] = (position['unrealized_pnl'] / position['total_cost']) * 100
                
                total_unrealized_pnl += position['unrealized_pnl']
            
            updated_positions.append(position)
        
        self.user_portfolios[user_id]['positions'] = updated_positions
        self.user_portfolios[user_id]['last_updated'] = datetime.now()
        
        return {
            "success": True,
            "updated_positions": len(updated_positions),
            "total_unrealized_pnl": total_unrealized_pnl,
            "portfolio_summary": self.get_portfolio_summary(user_id)
        }
    
    def calculate_portfolio_performance(self, user_id):
        """Portföy performansını hesapla"""
        if user_id not in self.user_portfolios:
            return {"error": "Kullanıcı portföyü bulunamadı"}
        
        portfolio = self.user_portfolios[user_id]
        positions = portfolio['positions']
        
        # Toplam değerler
        total_cost = sum(pos['total_cost'] for pos in positions)
        total_current_value = sum(pos['current_value'] for pos in positions)
        total_unrealized_pnl = total_current_value - total_cost
        total_pnl_pct = (total_unrealized_pnl / total_cost * 100) if total_cost > 0 else 0
        
        # En iyi ve en kötü performans gösteren pozisyonlar
        best_performer = max(positions, key=lambda x: x['unrealized_pnl_pct']) if positions else None
        worst_performer = min(positions, key=lambda x: x['unrealized_pnl_pct']) if positions else None
        
        # Sektör dağılımı (basit)
        sector_allocation = self.calculate_sector_allocation(positions)
        
        # Risk metrikleri
        portfolio_volatility = self.estimate_portfolio_volatility(positions)
        
        return {
            "portfolio_performance": {
                "total_positions": len(positions),
                "total_invested": total_cost,
                "current_portfolio_value": total_current_value,
                "total_unrealized_pnl": total_unrealized_pnl,
                "total_return_pct": round(total_pnl_pct, 2),
                "best_performer": {
                    "symbol": best_performer['symbol'],
                    "return_pct": round(best_performer['unrealized_pnl_pct'], 2),
                    "profit": best_performer['unrealized_pnl']
                } if best_performer else None,
                "worst_performer": {
                    "symbol": worst_performer['symbol'],
                    "return_pct": round(worst_performer['unrealized_pnl_pct'], 2),
                    "loss": worst_performer['unrealized_pnl']
                } if worst_performer else None,
                "sector_allocation": sector_allocation,
                "risk_metrics": {
                    "estimated_volatility": portfolio_volatility,
                    "risk_level": self.assess_portfolio_risk_level(total_pnl_pct, portfolio_volatility),
                    "diversification_score": self.calculate_portfolio_diversification(positions)
                }
            },
            "last_updated": portfolio['last_updated'].isoformat()
        }
    
    def analyze_personal_portfolio(self, user_id, market_data=None):
        """Kişisel portföy analizi ve öneriler"""
        if user_id not in self.user_portfolios:
            return {"error": "Kullanıcı portföyü bulunamadı"}
        
        # Mevcut performansı al
        performance = self.calculate_portfolio_performance(user_id)
        positions = self.user_portfolios[user_id]['positions']
        
        # Her pozisyon için detaylı analiz
        position_analysis = []
        for position in positions:
            analysis = self.analyze_individual_position(position, market_data)
            position_analysis.append(analysis)
        
        # Portföy seviyesi öneriler
        portfolio_recommendations = self.generate_portfolio_level_recommendations(positions, performance)
        
        # Risk analizi
        risk_analysis = self.analyze_portfolio_risk(positions)
        
        return {
            "personal_portfolio_analysis": {
                "portfolio_overview": performance["portfolio_performance"],
                "position_analysis": position_analysis,
                "portfolio_recommendations": portfolio_recommendations,
                "risk_analysis": risk_analysis,
                "rebalancing_suggestions": self.suggest_rebalancing(positions),
                "tax_optimization": self.analyze_tax_optimization(positions)
            }
        }
    
    def generate_personal_recommendations(self, user_id, market_analysis=None):
        """Kişisel portföye özel öneriler üret"""
        if user_id not in self.user_portfolios:
            return {"error": "Kullanıcı portföyü bulunamadı"}
        
        positions = self.user_portfolios[user_id]['positions']
        
        # Her pozisyon için BUY/SELL/HOLD önerisi
        position_recommendations = []
        
        for position in positions:
            recommendation = self.generate_position_recommendation(position, market_analysis)
            position_recommendations.append(recommendation)
        
        # Genel portföy önerileri
        general_recommendations = []
        
        # Konsantrasyon kontrolü
        total_value = sum(pos['current_value'] for pos in positions)
        for position in positions:
            weight = (position['current_value'] / total_value) * 100
            if weight > 25:
                general_recommendations.append({
                    "type": "CONCENTRATION_RISK",
                    "message": f"{position['symbol']} pozisyonu portföyün %{weight:.1f}'ini oluşturuyor. Risk yönetimi için pozisyonu küçültmeyi düşünün.",
                    "priority": "HIGH"
                })
        
        # Kar realizasyonu önerileri
        for position in positions:
            if position['unrealized_pnl_pct'] > 20:
                general_recommendations.append({
                    "type": "PROFIT_TAKING",
                    "message": f"{position['symbol']} %{position['unrealized_pnl_pct']:.1f} kazançta. Kısmi kar realizasyonu yapabilirsiniz.",
                    "priority": "MEDIUM"
                })
        
        # Stop loss önerileri
        for position in positions:
            if position['unrealized_pnl_pct'] < -10:
                general_recommendations.append({
                    "type": "STOP_LOSS",
                    "message": f"{position['symbol']} %{abs(position['unrealized_pnl_pct']):.1f} zararда. Stop loss seviyenizi gözden geçirin.",
                    "priority": "HIGH"
                })
        
        return {
            "personal_recommendations": {
                "position_specific": position_recommendations,
                "general_recommendations": general_recommendations,
                "portfolio_optimization": self.suggest_portfolio_optimization(positions),
                "next_actions": self.prioritize_actions(position_recommendations, general_recommendations)
            }
        }
    
    def track_profit_loss(self, user_id):
        """Detaylı kar/zarar takibi"""
        if user_id not in self.user_portfolios:
            return {"error": "Kullanıcı portföyü bulunamadı"}
        
        positions = self.user_portfolios[user_id]['positions']
        
        # Günlük, haftalık, aylık P&L (simulated)
        pnl_tracking = {
            "daily_pnl": self.calculate_daily_pnl(positions),
            "weekly_pnl": self.calculate_weekly_pnl(positions),
            "monthly_pnl": self.calculate_monthly_pnl(positions),
            "inception_to_date": self.calculate_total_pnl(positions)
        }
        
        # En karlı ve zararlı pozisyonlar
        profitable_positions = [pos for pos in positions if pos['unrealized_pnl'] > 0]
        losing_positions = [pos for pos in positions if pos['unrealized_pnl'] < 0]
        
        return {
            "profit_loss_tracking": {
                "pnl_summary": pnl_tracking,
                "profitable_positions": len(profitable_positions),
                "losing_positions": len(losing_positions),
                "win_rate": (len(profitable_positions) / len(positions) * 100) if positions else 0,
                "average_gain": np.mean([pos['unrealized_pnl_pct'] for pos in profitable_positions]) if profitable_positions else 0,
                "average_loss": np.mean([pos['unrealized_pnl_pct'] for pos in losing_positions]) if losing_positions else 0,
                "largest_gain": max([pos['unrealized_pnl'] for pos in positions]) if positions else 0,
                "largest_loss": min([pos['unrealized_pnl'] for pos in positions]) if positions else 0
            }
        }
    
    # Yardımcı metodlar
    def find_existing_position(self, user_id, symbol):
        """Aynı sembolden mevcut pozisyon var mı kontrol et"""
        if user_id not in self.user_portfolios:
            return None
        
        for position in self.user_portfolios[user_id]['positions']:
            if position['symbol'] == symbol and position['status'] == 'active':
                return position
        return None
    
    def merge_positions(self, existing, new):
        """İki pozisyonu birleştir (average cost)"""
        total_quantity = existing['quantity'] + new['quantity']
        total_cost = existing['total_cost'] + new['total_cost']
        average_price = total_cost / total_quantity
        
        merged = existing.copy()
        merged['quantity'] = total_quantity
        merged['purchase_price'] = average_price
        merged['total_cost'] = total_cost
        merged['current_value'] = total_quantity * existing['current_price']
        merged['unrealized_pnl'] = merged['current_value'] - total_cost
        merged['unrealized_pnl_pct'] = (merged['unrealized_pnl'] / total_cost) * 100
        
        return merged
    
    def get_portfolio_summary(self, user_id):
        """Portföy özeti"""
        if user_id not in self.user_portfolios:
            return {}
        
        positions = self.user_portfolios[user_id]['positions']
        total_cost = sum(pos['total_cost'] for pos in positions)
        total_value = sum(pos['current_value'] for pos in positions)
        
        return {
            "total_positions": len(positions),
            "total_invested": total_cost,
            "current_value": total_value,
            "unrealized_pnl": total_value - total_cost,
            "return_pct": ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        }
    
    def calculate_sector_allocation(self, positions):
        """Basit sektör dağılımı"""
        total_value = sum(pos['current_value'] for pos in positions)
        
        # Basit sektör mapping (gerçek uygulamada API'den alınır)
        sector_map = {
            'THYAO': 'Transportation', 'AKBNK': 'Banking', 'BIMAS': 'Retail',
            'ASELS': 'Defense', 'KCHOL': 'Holding'
        }
        
        sectors = {}
        for position in positions:
            sector = sector_map.get(position['symbol'], 'Other')
            weight = (position['current_value'] / total_value) * 100
            sectors[sector] = sectors.get(sector, 0) + weight
        
        return sectors
    
    def estimate_portfolio_volatility(self, positions):
        """Portföy volatilitesi tahmini"""
        # Basit volatilite hesaplama
        volatilities = []
        for position in positions:
            # Mock volatility based on return
            volatility = abs(position['unrealized_pnl_pct']) * 0.5
            volatilities.append(volatility)
        
        return np.mean(volatilities) if volatilities else 0
    
    def assess_portfolio_risk_level(self, return_pct, volatility):
        """Risk seviyesi değerlendirmesi"""
        if volatility < 5:
            return "LOW"
        elif volatility < 15:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def calculate_portfolio_diversification(self, positions):
        """Portföy çeşitlendirme skoru"""
        if len(positions) < 2:
            return 20
        elif len(positions) < 5:
            return 60
        elif len(positions) < 10:
            return 80
        else:
            return 95
    
    def analyze_individual_position(self, position, market_data):
        """Bireysel pozisyon analizi"""
        analysis = {
            "symbol": position['symbol'],
            "current_status": {
                "quantity": position['quantity'],
                "avg_cost": position['purchase_price'],
                "current_price": position['current_price'],
                "unrealized_pnl": position['unrealized_pnl'],
                "return_pct": position['unrealized_pnl_pct']
            },
            "technical_analysis": self.get_technical_analysis(position['symbol'], market_data),
            "risk_assessment": self.assess_position_risk(position),
            "recommendation": self.get_position_recommendation(position)
        }
        return analysis
    
    def generate_portfolio_level_recommendations(self, positions, performance):
        """Portföy seviyesi öneriler"""
        recommendations = []
        
        portfolio_return = performance["portfolio_performance"]["total_return_pct"]
        
        if portfolio_return > 15:
            recommendations.append("Portföy güçlü performans gösteriyor. Kısmi kar realizasyonu düşünebilirsiniz.")
        elif portfolio_return < -10:
            recommendations.append("Portföy zararда. Risk yönetimi stratejinizi gözden geçirin.")
        
        if len(positions) < 5:
            recommendations.append("Portföy çeşitlendirmesi artırılabilir.")
        
        return recommendations
    
    def analyze_portfolio_risk(self, positions):
        """Portföy risk analizi"""
        total_value = sum(pos['current_value'] for pos in positions)
        
        # Konsantrasyon riski
        max_position_weight = max((pos['current_value'] / total_value) * 100 for pos in positions) if positions else 0
        
        return {
            "concentration_risk": "HIGH" if max_position_weight > 30 else "MEDIUM" if max_position_weight > 20 else "LOW",
            "largest_position_weight": round(max_position_weight, 1),
            "number_of_positions": len(positions),
            "risk_recommendation": "Konsantrasyon riskini azaltın" if max_position_weight > 25 else "Risk seviyesi uygun"
        }
    
    def suggest_rebalancing(self, positions):
        """Rebalancing önerileri"""
        if len(positions) < 3:
            return {"needed": False, "reason": "Yeterli pozisyon yok"}
        
        total_value = sum(pos['current_value'] for pos in positions)
        target_weight = 100 / len(positions)  # Eşit ağırlık
        
        rebalancing_needed = any(
            abs((pos['current_value'] / total_value) * 100 - target_weight) > 10 
            for pos in positions
        )
        
        return {
            "needed": rebalancing_needed,
            "target_allocation": f"{target_weight:.1f}% per position",
            "reason": "Pozisyon ağırlıkları dengesizleşti" if rebalancing_needed else "Denge uygun"
        }
    
    def analyze_tax_optimization(self, positions):
        """Vergi optimizasyonu analizi"""
        profitable_positions = [pos for pos in positions if pos['unrealized_pnl'] > 0]
        losing_positions = [pos for pos in positions if pos['unrealized_pnl'] < 0]
        
        return {
            "tax_loss_harvesting_opportunities": len(losing_positions),
            "potential_tax_savings": sum(abs(pos['unrealized_pnl']) for pos in losing_positions) * 0.15,  # %15 vergi oranı
            "long_term_positions": len([pos for pos in positions if self.is_long_term_position(pos)]),
            "recommendation": "Zarar eden pozisyonlarla vergi optimizasyonu yapabilirsiniz" if losing_positions else "Vergi optimizasyonu fırsatı yok"
        }
    
    def generate_position_recommendation(self, position, market_analysis):
        """Pozisyon özel önerisi"""
        pnl_pct = position['unrealized_pnl_pct']
        
        if pnl_pct > 20:
            action = "PARTIAL_SELL"
            reason = "Yüksek kazanç - kısmi kar realizasyonu"
        elif pnl_pct < -15:
            action = "REVIEW_STOP_LOSS"
            reason = "Yüksek zarar - stop loss gözden geçir"
        elif -5 <= pnl_pct <= 15:
            action = "HOLD"
            reason = "Normal aralıkta - bekle"
        else:
            action = "MONITOR"
            reason = "Yakın takip gerekli"
        
        return {
            "symbol": position['symbol'],
            "action": action,
            "reason": reason,
            "current_return": pnl_pct,
            "suggested_target": self.calculate_target_price(position),
            "stop_loss_suggestion": self.calculate_stop_loss(position)
        }
    
    def suggest_portfolio_optimization(self, positions):
        """Portföy optimizasyon önerileri"""
        return {
            "diversification": "Sektör çeşitlendirmesi artırılabilir",
            "risk_management": "Stop loss seviyeleri belirleyin",
            "rebalancing": "3 ayda bir rebalancing yapın"
        }
    
    def prioritize_actions(self, position_recs, general_recs):
        """Öncelikli aksiyonlar"""
        high_priority = [rec for rec in general_recs if rec.get('priority') == 'HIGH']
        urgent_positions = [rec for rec in position_recs if rec['action'] in ['PARTIAL_SELL', 'REVIEW_STOP_LOSS']]
        
        return {
            "immediate_actions": high_priority[:3],
            "position_actions": urgent_positions[:3],
            "next_review_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
    
    # Yardımcı hesaplama metodları
    def calculate_daily_pnl(self, positions):
        return sum(pos['unrealized_pnl'] * 0.1 for pos in positions)  # Mock daily change
    
    def calculate_weekly_pnl(self, positions):
        return sum(pos['unrealized_pnl'] * 0.7 for pos in positions)  # Mock weekly change
    
    def calculate_monthly_pnl(self, positions):
        return sum(pos['unrealized_pnl'] for pos in positions)  # Current unrealized
    
    def calculate_total_pnl(self, positions):
        return sum(pos['unrealized_pnl'] for pos in positions)
    
    def get_technical_analysis(self, symbol, market_data):
        return {"rsi": 65, "macd": "bullish", "trend": "upward"}  # Mock
    
    def assess_position_risk(self, position):
        volatility = abs(position['unrealized_pnl_pct']) * 0.5
        return {"volatility": volatility, "risk_level": "medium"}
    
    def get_position_recommendation(self, position):
        if position['unrealized_pnl_pct'] > 15:
            return "CONSIDER_SELLING"
        elif position['unrealized_pnl_pct'] < -10:
            return "REVIEW_POSITION"
        else:
            return "HOLD"
    
    def is_long_term_position(self, position):
        purchase_date = datetime.fromisoformat(position['purchase_date'])
        return (datetime.now() - purchase_date).days > 365
    
    def calculate_target_price(self, position):
        return position['current_price'] * 1.15  # %15 hedef
    
    def calculate_stop_loss(self, position):
        return position['purchase_price'] * 0.9  # %10 stop loss

# Test
if __name__ == "__main__":
    agent = PersonalPortfolioAgent()
    
    # Test portfolio ekleme
    position_data = {
        'symbol': 'THYAO',
        'quantity': 1000,
        'purchase_price': 85.50,
        'asset_type': 'stock'
    }
    
    task1 = {"type": "add_portfolio_position", "user_id": "user123", "position_data": position_data}
    result1 = agent.process_task(task1)
    print("Position Added:", result1)
    
    # Test portföy analizi
    task2 = {"type": "analyze_personal_portfolio", "user_id": "user123"}
    result2 = agent.process_task(task2)
    print("Portfolio Analysis:", result2)
    
    print("Agent Durumu:", agent.get_status())