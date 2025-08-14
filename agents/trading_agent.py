import numpy as np
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class TradingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TradingAgent",
            agent_type="trading_executor",
            capabilities=["order_management", "execution_strategy", "position_tracking", "trade_optimization"]
        )
        self.active_positions = {}
        self.trade_history = []
        self.execution_parameters = {
            'slippage_tolerance': 0.1,  # %0.1
            'max_order_size': 1000000,  # 1M TL
            'trading_hours': {'start': 9, 'end': 18}
        }
        
    def can_handle_task(self, task):
        trading_tasks = ['execute_trade', 'manage_position', 'calculate_trade_size', 'optimize_execution']
        return task.get('type') in trading_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'execute_trade':
                result = self.execute_trade_order(task.get('trade_params'))
            elif task_type == 'manage_position':
                result = self.manage_existing_position(task.get('symbol'))
            elif task_type == 'calculate_trade_size':
                result = self.calculate_optimal_trade_size(task.get('decision_data'))
            elif task_type == 'optimize_execution':
                result = self.optimize_trade_execution(task.get('order_params'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def execute_trade_order(self, trade_params):
        """İşlem emrini gerçekleştir"""
        if not trade_params:
            # Mock trade parameters
            trade_params = {
                'symbol': 'THYAO',
                'action': 'BUY',
                'quantity': 1000,
                'price': 91.50,
                'order_type': 'LIMIT',
                'stop_loss': 85.40,
                'take_profit': 107.10
            }
        
        # Pre-execution checks
        execution_checks = self.pre_execution_validation(trade_params)
        if not execution_checks['valid']:
            return {
                "success": False,
                "error": execution_checks['reason'],
                "trade_id": None
            }
        
        # Calculate execution details
        execution_details = self.calculate_execution_details(trade_params)
        
        # Simulate order execution
        trade_id = f"TRD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Market impact and slippage simulation
        executed_price = self.simulate_market_execution(
            trade_params['price'], 
            trade_params['quantity'],
            trade_params['action']
        )
        
        # Create trade record
        trade_record = {
            'trade_id': trade_id,
            'symbol': trade_params['symbol'],
            'action': trade_params['action'],
            'quantity': trade_params['quantity'],
            'requested_price': trade_params['price'],
            'executed_price': executed_price,
            'total_value': trade_params['quantity'] * executed_price,
            'commission': execution_details['commission'],
            'net_amount': execution_details['net_amount'],
            'slippage': abs(executed_price - trade_params['price']) / trade_params['price'] * 100,
            'execution_time': datetime.now(),
            'stop_loss': trade_params.get('stop_loss'),
            'take_profit': trade_params.get('take_profit'),
            'status': 'EXECUTED'
        }
        
        # Update positions
        self.update_position_tracking(trade_record)
        
        # Add to history
        self.trade_history.append(trade_record)
        
        return {
            "success": True,
            "trade_id": trade_id,
            "execution_summary": {
                "symbol": trade_record['symbol'],
                "action": trade_record['action'],
                "quantity": trade_record['quantity'],
                "executed_price": round(executed_price, 2),
                "total_cost": round(trade_record['total_value'], 2),
                "commission": round(execution_details['commission'], 2),
                "slippage_pct": round(trade_record['slippage'], 3)
            },
            "position_update": self.get_position_summary(trade_params['symbol']),
            "next_actions": self.suggest_next_actions(trade_record)
        }
    
    def pre_execution_validation(self, trade_params):
        """Emir öncesi kontroller"""
        checks = []
        
        # Market hours check
        current_hour = datetime.now().hour
        if not (self.execution_parameters['trading_hours']['start'] <= current_hour <= self.execution_parameters['trading_hours']['end']):
            return {"valid": False, "reason": "Piyasa saatleri dışında"}
        
        # Order size check
        total_value = trade_params['quantity'] * trade_params['price']
        if total_value > self.execution_parameters['max_order_size']:
            return {"valid": False, "reason": f"Emir büyüklüğü limit aşıyor: {total_value:,.0f} TL"}
        
        # Price reasonableness (mock check)
        if trade_params['price'] <= 0:
            return {"valid": False, "reason": "Geçersiz fiyat"}
        
        # Quantity check
        if trade_params['quantity'] <= 0:
            return {"valid": False, "reason": "Geçersiz miktar"}
        
        return {"valid": True, "reason": "Tüm kontroller başarılı"}
    
    def calculate_execution_details(self, trade_params):
        """İşlem detaylarını hesapla"""
        total_value = trade_params['quantity'] * trade_params['price']
        
        # Commission calculation (simplified)
        commission_rate = 0.001  # %0.1
        commission = max(total_value * commission_rate, 5.0)  # Minimum 5 TL
        
        # Other fees
        exchange_fee = total_value * 0.0003  # Borsa payı
        total_fees = commission + exchange_fee
        
        if trade_params['action'] == 'BUY':
            net_amount = total_value + total_fees
        else:  # SELL
            net_amount = total_value - total_fees
        
        return {
            'total_value': total_value,
            'commission': commission,
            'exchange_fee': exchange_fee,
            'total_fees': total_fees,
            'net_amount': net_amount
        }
    
    def simulate_market_execution(self, requested_price, quantity, action):
        """Piyasa etkisi ve kayma simülasyonu"""
        # Market impact based on order size
        market_impact_factor = min(quantity / 10000, 0.005)  # Max %0.5 impact
        
        # Random slippage
        random_slippage = np.random.uniform(-0.001, 0.001)  # ±%0.1
        
        # Total impact
        if action == 'BUY':
            total_impact = market_impact_factor + abs(random_slippage)
        else:  # SELL
            total_impact = -(market_impact_factor + abs(random_slippage))
        
        executed_price = requested_price * (1 + total_impact)
        return max(executed_price, 0.01)  # Minimum 1 kuruş
    
    def update_position_tracking(self, trade_record):
        """Pozisyon takibini güncelle"""
        symbol = trade_record['symbol']
        
        if symbol not in self.active_positions:
            self.active_positions[symbol] = {
                'quantity': 0,
                'avg_cost': 0,
                'total_cost': 0,
                'unrealized_pnl': 0,
                'first_purchase': None
            }
        
        position = self.active_positions[symbol]
        
        if trade_record['action'] == 'BUY':
            # Add to position
            new_total_cost = position['total_cost'] + trade_record['total_value']
            new_quantity = position['quantity'] + trade_record['quantity']
            new_avg_cost = new_total_cost / new_quantity if new_quantity > 0 else 0
            
            position['quantity'] = new_quantity
            position['avg_cost'] = new_avg_cost
            position['total_cost'] = new_total_cost
            
            if position['first_purchase'] is None:
                position['first_purchase'] = trade_record['execution_time']
                
        else:  # SELL
            # Reduce position
            position['quantity'] -= trade_record['quantity']
            if position['quantity'] <= 0:
                # Position closed
                del self.active_positions[symbol]
    
    def get_position_summary(self, symbol):
        """Pozisyon özetini al"""
        if symbol not in self.active_positions:
            return {"status": "No position"}
        
        position = self.active_positions[symbol]
        current_price = np.random.uniform(80, 120)  # Mock current price
        
        current_value = position['quantity'] * current_price
        unrealized_pnl = current_value - position['total_cost']
        unrealized_pnl_pct = (unrealized_pnl / position['total_cost']) * 100 if position['total_cost'] > 0 else 0
        
        return {
            "symbol": symbol,
            "quantity": position['quantity'],
            "avg_cost": round(position['avg_cost'], 2),
            "current_price": round(current_price, 2),
            "current_value": round(current_value, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "unrealized_pnl_pct": round(unrealized_pnl_pct, 2),
            "holding_period_days": (datetime.now() - position['first_purchase']).days if position['first_purchase'] else 0
        }
    
    def suggest_next_actions(self, trade_record):
        """Sonraki eylem önerileri"""
        suggestions = []
        
        if trade_record['action'] == 'BUY':
            suggestions.extend([
                "Stop loss emrini yerleştirin",
                "Take profit seviyelerini takip edin",
                "Pozisyonu günlük olarak izleyin"
            ])
        else:
            suggestions.extend([
                "Pozisyon kapatma sonrası performans değerlendirmesi yapın",
                "Benzer fırsatları arayın"
            ])
        
        # Risk check
        if trade_record['slippage'] > 0.2:
            suggestions.append(f"⚠️ Yüksek kayma ({trade_record['slippage']:.3f}%) - emir stratejisini gözden geçirin")
        
        return suggestions
    
    def calculate_optimal_trade_size(self, decision_data):
        """Optimal işlem büyüklüğünü hesapla"""
        if not decision_data:
            decision_data = {
                'position_size_pct': 10,
                'portfolio_value': 1000000,  # 1M TL
                'stop_loss': 7,
                'confidence': 75,
                'risk_level': 'Orta'
            }
        
        # Eksik parametreleri kontrol et ve varsayılan değerleri ata
        if 'portfolio_value' not in decision_data:
            decision_data['portfolio_value'] = 1000000  # Default 1M TL
        
        if 'position_size_pct' not in decision_data:
            decision_data['position_size_pct'] = 10  # Default %10
        
        if 'stop_loss' not in decision_data:
            decision_data['stop_loss'] = 7  # Default %7
        
        if 'confidence' not in decision_data:
            decision_data['confidence'] = 75  # Default %75
        
        if 'risk_level' not in decision_data:
            decision_data['risk_level'] = 'Orta'  # Default risk level
        
        # Base calculation
        base_amount = decision_data['portfolio_value'] * (decision_data['position_size_pct'] / 100)
        
        # Confidence adjustment
        confidence_multiplier = decision_data['confidence'] / 100
        adjusted_amount = base_amount * confidence_multiplier
        
        # Risk-based position sizing (Kelly Criterion simplified)
        win_prob = confidence_multiplier
        avg_win = 15  # Expected %15 win
        avg_loss = decision_data['stop_loss']
        
        kelly_fraction = (win_prob * avg_win - (1 - win_prob) * avg_loss) / avg_win
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        
        kelly_amount = decision_data['portfolio_value'] * kelly_fraction
        
        # Use more conservative of the two
        final_amount = min(adjusted_amount, kelly_amount)
        
        # Round to reasonable lot size
        final_amount = round(final_amount / 1000) * 1000  # Round to nearest 1000 TL
        
        return {
            "optimal_trade_size": {
                "amount_tl": final_amount,
                "portfolio_pct": round((final_amount / decision_data['portfolio_value']) * 100, 2),
                "calculation_method": "Conservative of Confidence-Adjusted and Kelly"
            },
            "calculations": {
                "base_amount": base_amount,
                "confidence_adjusted": adjusted_amount,
                "kelly_amount": kelly_amount,
                "kelly_fraction": round(kelly_fraction, 4)
            },
            "risk_metrics": {
                "max_loss_amount": final_amount * (decision_data['stop_loss'] / 100),
                "max_loss_portfolio_pct": round((final_amount * decision_data['stop_loss'] / 100) / decision_data['portfolio_value'] * 100, 2)
            }
        }
    
    def get_trading_performance(self):
        """İşlem performansını hesapla"""
        if not self.trade_history:
            return {"message": "Henüz işlem yapılmamış"}
        
        total_trades = len(self.trade_history)
        total_value = sum(trade['total_value'] for trade in self.trade_history)
        total_commission = sum(trade['commission'] for trade in self.trade_history)
        avg_slippage = np.mean([trade['slippage'] for trade in self.trade_history])
        
        return {
            "trading_stats": {
                "total_trades": total_trades,
                "total_volume": round(total_value, 2),
                "total_commission": round(total_commission, 2),
                "avg_slippage_pct": round(avg_slippage, 3),
                "commission_rate": round((total_commission / total_value) * 100, 3) if total_value > 0 else 0
            },
            "active_positions": len(self.active_positions),
            "execution_quality": "İyi" if avg_slippage < 0.1 else "Orta" if avg_slippage < 0.2 else "Zayıf"
        }

# Test
if __name__ == "__main__":
    agent = TradingAgent()
    
    # Test 1: Execute trade
    mock_trade = {
        'symbol': 'THYAO',
        'action': 'BUY',
        'quantity': 1000,
        'price': 91.50,
        'order_type': 'LIMIT',
        'stop_loss': 85.40,
        'take_profit': 107.10
    }
    
    task1 = {"type": "execute_trade", "trade_params": mock_trade}
    result1 = agent.process_task(task1)
    print("İşlem Sonucu:", result1)
    
    # Test 2: Calculate trade size
    mock_decision = {
        'position_size_pct': 12,
        'portfolio_value': 500000,
        'stop_loss': 7,
        'confidence': 78
    }
    
    task2 = {"type": "calculate_trade_size", "decision_data": mock_decision}
    result2 = agent.process_task(task2)
    print("İşlem Büyüklüğü:", result2)
    
    print("Agent Durumu:", agent.get_status())
    print("Performans:", agent.get_trading_performance())