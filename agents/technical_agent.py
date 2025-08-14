import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechnicalAgent",
            agent_type="technical_analyzer",
            capabilities=["price_analysis", "indicators", "pattern_recognition", "trend_analysis"]
        )
        
    def can_handle_task(self, task):
        """Bu agent hangi görevleri yapabilir?"""
        technical_tasks = ['calculate_indicators', 'trend_analysis', 'support_resistance', 'generate_signals']
        return task.get('type') in technical_tasks
    
    def process_task(self, task):
        """Görevi işle"""
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'calculate_indicators':
                result = self.calculate_technical_indicators(task.get('price_data'))
            elif task_type == 'trend_analysis':
                result = self.analyze_trend(task.get('price_data'))
            elif task_type == 'support_resistance':
                result = self.find_support_resistance(task.get('price_data'))
            elif task_type == 'generate_signals':
                result = self.generate_trading_signals(task.get('price_data'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def generate_mock_price_data(self, days=50):
        """Test için mock fiyat verisi oluştur"""
        np.random.seed(42)
        base_price = 100
        prices = [base_price]
        
        for i in range(days-1):
            change = np.random.normal(0, 2)  # %2 volatilite
            new_price = prices[-1] * (1 + change/100)
            prices.append(max(new_price, 1))  # Minimum 1 TL
        
        dates = [datetime.now() - timedelta(days=days-i) for i in range(days)]
        
        # OHLC verileri oluştur
        data = []
        for i, price in enumerate(prices):
            high = price * np.random.uniform(1.00, 1.03)
            low = price * np.random.uniform(0.97, 1.00)
            open_price = prices[i-1] if i > 0 else price
            close = price
            volume = np.random.randint(100000, 1000000)
            
            data.append({
                'date': dates[i],
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        return data
    
    def calculate_technical_indicators(self, price_data):
        """Teknik indikatörleri hesapla"""
        if not price_data:
            price_data = self.generate_mock_price_data()
        
        closes = [item['close'] for item in price_data]
        volumes = [item['volume'] for item in price_data]
        
        # Moving Averages
        ma_5 = self.simple_moving_average(closes, 5)
        ma_20 = self.simple_moving_average(closes, 20)
        
        # RSI
        rsi = self.calculate_rsi(closes)
        
        # MACD
        macd_line, signal_line = self.calculate_macd(closes)
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(closes)
        
        current_price = closes[-1]
        
        return {
            "current_price": round(current_price, 2),
            "moving_averages": {
                "ma_5": round(ma_5, 2),
                "ma_20": round(ma_20, 2),
                "trend": "Yükseliş" if current_price > ma_20 else "Düşüş"
            },
            "momentum_indicators": {
                "rsi": round(rsi, 2),
                "rsi_signal": "Aşırı Alım" if rsi > 70 else "Aşırı Satım" if rsi < 30 else "Nötr"
            },
            "trend_indicators": {
                "macd": round(macd_line, 4),
                "signal": round(signal_line, 4),
                "macd_signal": "Al" if macd_line > signal_line else "Sat"
            },
            "volatility": {
                "bb_upper": round(bb_upper, 2),
                "bb_middle": round(bb_middle, 2),
                "bb_lower": round(bb_lower, 2),
                "position": "Üst Band Yakın" if current_price > bb_middle else "Alt Band Yakın"
            }
        }
    
    def simple_moving_average(self, prices, period):
        """Basit hareketli ortalama"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        return sum(prices[-period:]) / period
    
    def calculate_rsi(self, prices, period=14):
        """RSI hesapla"""
        if len(prices) < period + 1:
            return 50
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices):
        """MACD hesapla"""
        if len(prices) < 26:
            return 0, 0
        
        ema_12 = self.exponential_moving_average(prices, 12)
        ema_26 = self.exponential_moving_average(prices, 26)
        macd_line = ema_12 - ema_26
        
        # Signal line (MACD'nin 9 günlük EMA'sı)
        signal_line = macd_line * 0.9  # Basitleştirilmiş
        
        return macd_line, signal_line
    
    def exponential_moving_average(self, prices, period):
        """Üssel hareketli ortalama"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Bollinger Bands hesapla"""
        if len(prices) < period:
            sma = sum(prices) / len(prices)
            std = np.std(prices)
        else:
            recent_prices = prices[-period:]
            sma = sum(recent_prices) / period
            std = np.std(recent_prices)
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def generate_trading_signals(self, price_data):
        """Al/Sat sinyalleri üret"""
        indicators = self.calculate_technical_indicators(price_data)
        
        signals = []
        score = 0
        
        # MA sinyali
        if indicators['moving_averages']['trend'] == "Yükseliş":
            signals.append("MA: Alış Sinyali")
            score += 2
        else:
            signals.append("MA: Satış Sinyali")
            score -= 2
        
        # RSI sinyali
        rsi = indicators['momentum_indicators']['rsi']
        if rsi < 30:
            signals.append("RSI: Aşırı Satım - Alış Fırsatı")
            score += 3
        elif rsi > 70:
            signals.append("RSI: Aşırı Alım - Satış Sinyali")
            score -= 3
        else:
            signals.append("RSI: Nötr Bölge")
        
        # MACD sinyali
        if indicators['trend_indicators']['macd_signal'] == "Al":
            signals.append("MACD: Alış Sinyali")
            score += 1
        else:
            signals.append("MACD: Satış Sinyali")
            score -= 1
        
        # Genel sinyal
        if score >= 3:
            overall_signal = "GÜÇLÜ ALIŞ"
        elif score >= 1:
            overall_signal = "ZAYIF ALIŞ"
        elif score <= -3:
            overall_signal = "GÜÇLÜ SATIŞ"
        elif score <= -1:
            overall_signal = "ZAYIF SATIŞ"
        else:
            overall_signal = "NÖTR"
        
        return {
            "overall_signal": overall_signal,
            "signal_strength": abs(score),
            "individual_signals": signals,
            "technical_score": score,
            "indicators_summary": indicators
        }

# Test fonksiyonu
if __name__ == "__main__":
    agent = TechnicalAgent()
    
    # Test 1: Teknik indikatörler
    task1 = {"type": "calculate_indicators", "price_data": None}
    result1 = agent.process_task(task1)
    print("Teknik İndikatörler:", result1)
    
    # Test 2: Al/Sat sinyalleri
    task2 = {"type": "generate_signals", "price_data": None}
    result2 = agent.process_task(task2)
    print("Al/Sat Sinyalleri:", result2)
    
    # Agent durumu
    print("Agent Durumu:", agent.get_status())