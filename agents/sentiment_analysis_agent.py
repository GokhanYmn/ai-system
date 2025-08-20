import requests
import re
import json
from datetime import datetime, timedelta
import time
import numpy as np
from collections import defaultdict
from base_agent import BaseAgent

class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SentimentAnalysisAgent",
            agent_type="sentiment_analyzer",
            capabilities=["social_media_sentiment", "news_sentiment", "market_sentiment", "fear_greed_index"]
        )
        self.sentiment_cache = {}
        self.sentiment_keywords = {
            'very_positive': ['mükemmel', 'harika', 'muhteşem', 'süper', 'patlama', 'roket', 'moon'],
            'positive': ['iyi', 'güzel', 'olumlu', 'artış', 'yükseliş', 'kazanç', 'başarı', 'büyüme'],
            'neutral': ['normal', 'bekle', 'kararsız', 'belirsiz', 'değişim', 'açıklama'],
            'negative': ['kötü', 'düşüş', 'zarar', 'kayıp', 'satış', 'risk', 'sorun', 'endişe'],
            'very_negative': ['felaket', 'çöküş', 'panik', 'korku', 'kaos', 'alarm', 'kriz']
        }
        
    def can_handle_task(self, task):
        sentiment_tasks = [
            'analyze_social_sentiment', 'analyze_news_sentiment', 'calculate_fear_greed_index',
            'get_market_sentiment', 'track_sentiment_trends', 'sentiment_based_signals'
        ]
        return task.get('type') in sentiment_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'analyze_social_sentiment':
                result = self.analyze_social_media_sentiment(task.get('symbol'), task.get('platform'))
            elif task_type == 'analyze_news_sentiment':
                result = self.analyze_news_sentiment(task.get('news_data'))
            elif task_type == 'calculate_fear_greed_index':
                result = self.calculate_fear_greed_index(task.get('market_data'))
            elif task_type == 'get_market_sentiment':
                result = self.get_overall_market_sentiment(task.get('symbols'))
            elif task_type == 'track_sentiment_trends':
                result = self.track_sentiment_trends(task.get('symbol'), task.get('timeframe'))
            elif task_type == 'sentiment_based_signals':
                result = self.generate_sentiment_based_signals(task.get('symbol'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def analyze_social_media_sentiment(self, symbol, platform='twitter'):
        """Sosyal medya sentiment analizi"""
        if not symbol:
            symbol = 'THYAO'
        
        try:
            # Mock social media data (gerçek uygulamada Twitter/Reddit API)
            social_posts = self.get_mock_social_data(symbol, platform)
            
            sentiment_scores = []
            sentiment_distribution = {'very_positive': 0, 'positive': 0, 'neutral': 0, 'negative': 0, 'very_negative': 0}
            
            for post in social_posts:
                score = self.calculate_text_sentiment(post['text'])
                sentiment_scores.append(score)
                
                # Kategorize sentiment
                if score >= 0.6:
                    sentiment_distribution['very_positive'] += 1
                elif score >= 0.2:
                    sentiment_distribution['positive'] += 1
                elif score >= -0.2:
                    sentiment_distribution['neutral'] += 1
                elif score >= -0.6:
                    sentiment_distribution['negative'] += 1
                else:
                    sentiment_distribution['very_negative'] += 1
            
            # Overall sentiment
            overall_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
            
            # Sentiment strength
            sentiment_strength = self.calculate_sentiment_strength(sentiment_scores)
            
            # Volume analysis
            volume_trend = self.analyze_mention_volume(social_posts)
            
            return {
                "social_sentiment_analysis": {
                    "symbol": symbol,
                    "platform": platform,
                    "overall_sentiment": round(overall_sentiment, 3),
                    "sentiment_label": self.get_sentiment_label(overall_sentiment),
                    "sentiment_strength": sentiment_strength,
                    "sentiment_distribution": sentiment_distribution,
                    "total_mentions": len(social_posts),
                    "volume_trend": volume_trend,
                    "influential_posts": self.get_influential_posts(social_posts),
                    "sentiment_momentum": self.calculate_sentiment_momentum(sentiment_scores),
                    "reliability_score": self.calculate_reliability_score(len(social_posts), sentiment_strength)
                }
            }
            
        except Exception as e:
            return {"error": f"Social media sentiment analizi hatası: {str(e)}"}
    
    def analyze_news_sentiment(self, news_data):
        """Haber sentiment analizi"""
        if not news_data:
            # Mock news data
            news_data = [
                {"title": "THYAO üçüncü çeyrek sonuçları beklentileri aştı", "content": "Şirket güçlü büyüme gösterdi"},
                {"title": "Havacılık sektöründe olumlu gelişmeler", "content": "Sektör toparlanma sinyalleri veriyor"},
                {"title": "Piyasalarda genel belirsizlik devam ediyor", "content": "Yatırımcılar temkinli yaklaşım sergiliyor"}
            ]
        
        news_sentiments = []
        sentiment_timeline = []
        
        for news in news_data:
            # Title ve content sentiment
            title_sentiment = self.calculate_text_sentiment(news.get('title', ''))
            content_sentiment = self.calculate_text_sentiment(news.get('content', ''))
            
            # Weighted average (title daha önemli)
            combined_sentiment = (title_sentiment * 0.7) + (content_sentiment * 0.3)
            
            news_sentiments.append(combined_sentiment)
            sentiment_timeline.append({
                "timestamp": news.get('date', datetime.now().isoformat()),
                "sentiment": combined_sentiment,
                "title": news.get('title', '')[:50] + "..."
            })
        
        # Overall news sentiment
        overall_news_sentiment = np.mean(news_sentiments) if news_sentiments else 0
        
        # News impact score
        impact_score = self.calculate_news_impact(news_data, news_sentiments)
        
        return {
            "news_sentiment_analysis": {
                "overall_sentiment": round(overall_news_sentiment, 3),
                "sentiment_label": self.get_sentiment_label(overall_news_sentiment),
                "news_count": len(news_data),
                "sentiment_timeline": sentiment_timeline[-10:],  # Son 10 haber
                "impact_score": impact_score,
                "sentiment_volatility": np.std(news_sentiments) if news_sentiments else 0,
                "positive_news_ratio": len([s for s in news_sentiments if s > 0.2]) / len(news_sentiments) if news_sentiments else 0
            }
        }
    
    def calculate_fear_greed_index(self, market_data):
        """Korku & Açgözlülük endeksi hesapla"""
        if not market_data:
            # Mock market data
            market_data = {
                'market_volatility': 15.2,  # VIX benzeri
                'market_momentum': 5.8,     # 125 day average
                'market_volume': 85,        # Relative volume
                'put_call_ratio': 0.95,     # Options data
                'safe_haven_demand': 12     # Bond demand
            }
        
        # Fear & Greed bileşenleri (0-100 scale)
        components = {}
        
        # 1. Market Volatility (VIX)
        volatility = market_data.get('market_volatility', 15)
        volatility_score = max(0, min(100, 100 - (volatility - 10) * 5))  # Düşük volatilite = Greed
        components['volatility'] = volatility_score
        
        # 2. Market Momentum
        momentum = market_data.get('market_momentum', 0)
        momentum_score = max(0, min(100, 50 + momentum * 5))  # Pozitif momentum = Greed
        components['momentum'] = momentum_score
        
        # 3. Market Volume
        volume = market_data.get('market_volume', 100)
        volume_score = max(0, min(100, volume))  # Yüksek volume = interest
        components['volume'] = volume_score
        
        # 4. Put/Call Ratio
        put_call = market_data.get('put_call_ratio', 1.0)
        put_call_score = max(0, min(100, (2 - put_call) * 50))  # Düşük put/call = Greed
        components['put_call'] = put_call_score
        
        # 5. Safe Haven Demand
        safe_haven = market_data.get('safe_haven_demand', 50)
        safe_haven_score = max(0, min(100, 100 - safe_haven))  # Düşük safe haven demand = Greed
        components['safe_haven'] = safe_haven_score
        
        # Weighted average Fear & Greed Index
        weights = {'volatility': 0.25, 'momentum': 0.25, 'volume': 0.15, 'put_call': 0.20, 'safe_haven': 0.15}
        
        fear_greed_index = sum(components[key] * weights[key] for key in components.keys())
        
        # Kategorize
        if fear_greed_index >= 75:
            category = "Extreme Greed"
            signal = "SELL_SIGNAL"
        elif fear_greed_index >= 55:
            category = "Greed"
            signal = "CAUTION"
        elif fear_greed_index >= 45:
            category = "Neutral"
            signal = "HOLD"
        elif fear_greed_index >= 25:
            category = "Fear"
            signal = "OPPORTUNITY"
        else:
            category = "Extreme Fear"
            signal = "BUY_SIGNAL"
        
        return {
            "fear_greed_index": {
                "index_value": round(fear_greed_index, 1),
                "category": category,
                "signal": signal,
                "components": {k: round(v, 1) for k, v in components.items()},
                "interpretation": self.interpret_fear_greed(fear_greed_index),
                "historical_context": self.get_historical_context(fear_greed_index),
                "contrarian_opportunity": fear_greed_index < 30 or fear_greed_index > 70
            }
        }
    
    def get_overall_market_sentiment(self, symbols=None):
        """Genel piyasa sentiment"""
        if not symbols:
            symbols = ['THYAO', 'AKBNK', 'BIMAS', 'ASELS', 'KCHOL']
        
        symbol_sentiments = {}
        overall_scores = []
        
        for symbol in symbols:
            # Her sembol için sentiment analizi
            social_result = self.analyze_social_media_sentiment(symbol)
            
            if not social_result.get('error'):
                sentiment_score = social_result['social_sentiment_analysis']['overall_sentiment']
                symbol_sentiments[symbol] = {
                    'sentiment_score': sentiment_score,
                    'sentiment_label': self.get_sentiment_label(sentiment_score),
                    'mention_volume': social_result['social_sentiment_analysis']['total_mentions']
                }
                overall_scores.append(sentiment_score)
        
        # Market-wide sentiment
        market_sentiment = np.mean(overall_scores) if overall_scores else 0
        sentiment_dispersion = np.std(overall_scores) if overall_scores else 0
        
        # Sector analysis
        sector_sentiment = self.analyze_sector_sentiment(symbol_sentiments)
        
        return {
            "market_sentiment": {
                "overall_market_sentiment": round(market_sentiment, 3),
                "sentiment_label": self.get_sentiment_label(market_sentiment),
                "sentiment_dispersion": round(sentiment_dispersion, 3),
                "market_consensus": "Strong" if sentiment_dispersion < 0.3 else "Moderate" if sentiment_dispersion < 0.6 else "Weak",
                "symbol_sentiments": symbol_sentiments,
                "sector_sentiment": sector_sentiment,
                "market_mood": self.determine_market_mood(market_sentiment, sentiment_dispersion),
                "sentiment_extremes": self.identify_sentiment_extremes(symbol_sentiments)
            }
        }
    
    def track_sentiment_trends(self, symbol, timeframe='7d'):
        """Sentiment trend takibi"""
        if not symbol:
            symbol = 'THYAO'
        
        # Mock historical sentiment data
        days = 7 if timeframe == '7d' else 30 if timeframe == '30d' else 1
        
        sentiment_history = []
        base_sentiment = 0.1  # Starting sentiment
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            
            # Realistic sentiment evolution
            daily_change = np.random.normal(0, 0.1)  # Daily random walk
            base_sentiment += daily_change
            base_sentiment = max(-1, min(1, base_sentiment))  # Clamp between -1 and 1
            
            sentiment_history.append({
                'date': date.strftime('%Y-%m-%d'),
                'sentiment': round(base_sentiment, 3),
                'volume': np.random.randint(50, 200)  # Mock mention volume
            })
        
        # Trend analysis
        sentiment_values = [h['sentiment'] for h in sentiment_history]
        trend = self.calculate_sentiment_trend(sentiment_values)
        volatility = np.std(sentiment_values)
        
        return {
            "sentiment_trends": {
                "symbol": symbol,
                "timeframe": timeframe,
                "sentiment_history": sentiment_history,
                "trend_analysis": {
                    "direction": trend['direction'],
                    "strength": trend['strength'],
                    "slope": trend['slope'],
                    "volatility": round(volatility, 3)
                },
                "key_levels": {
                    "highest_sentiment": max(sentiment_values),
                    "lowest_sentiment": min(sentiment_values),
                    "current_vs_average": round(sentiment_values[-1] - np.mean(sentiment_values), 3)
                },
                "momentum": self.calculate_sentiment_momentum(sentiment_values[-5:])  # Last 5 days
            }
        }
    
    def generate_sentiment_based_signals(self, symbol):
        """Sentiment bazlı alım/satım sinyalleri"""
        if not symbol:
            symbol = 'THYAO'
        
        # Get current sentiment data
        social_sentiment = self.analyze_social_media_sentiment(symbol)
        
        if social_sentiment.get('error'):
            return {"error": "Sentiment verisi alınamadı"}
        
        sentiment_data = social_sentiment['social_sentiment_analysis']
        sentiment_score = sentiment_data['overall_sentiment']
        sentiment_strength = sentiment_data['sentiment_strength']
        volume = sentiment_data['total_mentions']
        
        # Signal generation logic
        signals = []
        signal_strength = 0
        
        # Extreme sentiment signals (contrarian)
        if sentiment_score > 0.7 and sentiment_strength > 0.6:
            signals.append({
                'type': 'SELL_SIGNAL',
                'reason': 'Extreme positive sentiment - potential overbought',
                'strength': 'HIGH',
                'timeframe': 'short_term'
            })
            signal_strength -= 0.8
            
        elif sentiment_score < -0.7 and sentiment_strength > 0.6:
            signals.append({
                'type': 'BUY_SIGNAL',
                'reason': 'Extreme negative sentiment - potential oversold',
                'strength': 'HIGH',
                'timeframe': 'short_term'
            })
            signal_strength += 0.8
        
        # Volume-backed sentiment
        if volume > 100 and sentiment_score > 0.3:
            signals.append({
                'type': 'BUY_SIGNAL',
                'reason': 'High volume positive sentiment',
                'strength': 'MEDIUM',
                'timeframe': 'medium_term'
            })
            signal_strength += 0.5
            
        elif volume > 100 and sentiment_score < -0.3:
            signals.append({
                'type': 'SELL_SIGNAL',
                'reason': 'High volume negative sentiment',
                'strength': 'MEDIUM',
                'timeframe': 'medium_term'
            })
            signal_strength -= 0.5
        
        # Momentum signals
        momentum = sentiment_data.get('sentiment_momentum', 0)
        if momentum > 0.5:
            signals.append({
                'type': 'MOMENTUM_BUY',
                'reason': 'Positive sentiment momentum',
                'strength': 'MEDIUM',
                'timeframe': 'short_term'
            })
            signal_strength += 0.3
            
        elif momentum < -0.5:
            signals.append({
                'type': 'MOMENTUM_SELL',
                'reason': 'Negative sentiment momentum',
                'strength': 'MEDIUM',
                'timeframe': 'short_term'
            })
            signal_strength -= 0.3
        
        # Overall signal
        if signal_strength > 0.5:
            overall_signal = "STRONG_BUY"
        elif signal_strength > 0.2:
            overall_signal = "BUY"
        elif signal_strength < -0.5:
            overall_signal = "STRONG_SELL"
        elif signal_strength < -0.2:
            overall_signal = "SELL"
        else:
            overall_signal = "HOLD"
        
        return {
            "sentiment_signals": {
                "symbol": symbol,
                "overall_signal": overall_signal,
                "signal_strength": round(signal_strength, 2),
                "individual_signals": signals,
                "sentiment_summary": {
                    "current_sentiment": sentiment_score,
                    "sentiment_label": self.get_sentiment_label(sentiment_score),
                    "volume": volume,
                    "momentum": momentum
                },
                "risk_assessment": self.assess_sentiment_risk(sentiment_score, sentiment_strength, volume),
                "confidence": self.calculate_signal_confidence(signals, sentiment_strength)
            }
        }
    
    # Yardımcı metodlar
    def get_mock_social_data(self, symbol, platform, count=50):
        """Mock sosyal medya verisi"""
        posts = []
        
        positive_templates = [
            f"{symbol} harika performans gösteriyor!",
            f"{symbol} için çok olumlu gelişmeler var",
            f"Bu hafta {symbol}'da güzel kazançlar elde ettim",
            f"{symbol} uzun vadede süper bir yatırım"
        ]
        
        negative_templates = [
            f"{symbol} son zamanlarda düşüş trendinde",
            f"{symbol} için endişeli hissediyorum",
            f"Bu piyasa koşullarında {symbol} riskli",
            f"{symbol}'da zarar ettim, satmayı düşünüyorum"
        ]
        
        neutral_templates = [
            f"{symbol} hakkında ne düşünüyorsunuz?",
            f"{symbol} için analiz arıyorum",
            f"{symbol} bekle mi al mı?",
            f"{symbol} fiyat hedefi nedir?"
        ]
        
        all_templates = positive_templates + negative_templates + neutral_templates
        
        for i in range(count):
            post = {
                'id': f"post_{i}",
                'text': np.random.choice(all_templates),
                'author': f"user_{i}",
                'timestamp': (datetime.now() - timedelta(hours=np.random.randint(0, 24))).isoformat(),
                'likes': np.random.randint(0, 100),
                'retweets': np.random.randint(0, 50)
            }
            posts.append(post)
        
        return posts
    
    def calculate_text_sentiment(self, text):
        """Metin sentiment skoru hesapla"""
        if not text:
            return 0
        
        text_lower = text.lower()
        score = 0
        
        # Keyword-based scoring
        for sentiment, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if sentiment == 'very_positive':
                        score += 0.8
                    elif sentiment == 'positive':
                        score += 0.4
                    elif sentiment == 'negative':
                        score -= 0.4
                    elif sentiment == 'very_negative':
                        score -= 0.8
        
        # Normalize score
        return max(-1, min(1, score))
    
    def get_sentiment_label(self, score):
        """Sentiment skorunu label'a çevir"""
        if score >= 0.6:
            return "Very Positive"
        elif score >= 0.2:
            return "Positive"
        elif score >= -0.2:
            return "Neutral"
        elif score >= -0.6:
            return "Negative"
        else:
            return "Very Negative"
    
    def calculate_sentiment_strength(self, sentiment_scores):
        """Sentiment gücü hesapla"""
        if not sentiment_scores:
            return 0
        
        # Standard deviation as strength indicator
        volatility = np.std(sentiment_scores)
        mean_abs = np.mean([abs(s) for s in sentiment_scores])
        
        strength = min(1, (mean_abs + volatility) / 2)
        return round(strength, 3)
    
    def analyze_mention_volume(self, posts):
        """Mention volume trendi"""
        recent_posts = len([p for p in posts if 
                           datetime.fromisoformat(p['timestamp']) > datetime.now() - timedelta(hours=6)])
        
        if recent_posts > len(posts) * 0.5:
            return "Increasing"
        elif recent_posts < len(posts) * 0.2:
            return "Decreasing"
        else:
            return "Stable"
    
    def get_influential_posts(self, posts):
        """Etkili postları bul"""
        # Sort by engagement (likes + retweets)
        sorted_posts = sorted(posts, 
                            key=lambda x: x.get('likes', 0) + x.get('retweets', 0), 
                            reverse=True)
        
        return sorted_posts[:3]  # Top 3
    
    def calculate_sentiment_momentum(self, sentiment_scores):
        """Sentiment momentum hesapla"""
        if len(sentiment_scores) < 3:
            return 0
        
        recent_avg = np.mean(sentiment_scores[-3:])
        older_avg = np.mean(sentiment_scores[:-3]) if len(sentiment_scores) > 3 else np.mean(sentiment_scores)
        
        momentum = recent_avg - older_avg
        return round(momentum, 3)
    
    def calculate_reliability_score(self, mention_count, sentiment_strength):
        """Güvenilirlik skoru"""
        volume_score = min(1, mention_count / 100)  # Max 100 mentions for full score
        strength_score = sentiment_strength
        
        reliability = (volume_score + strength_score) / 2
        return round(reliability, 3)
    
    def calculate_news_impact(self, news_data, sentiments):
        """Haber etki skoru"""
        if not news_data:
            return 0
        
        # Basit impact hesaplaması
        sentiment_strength = np.mean([abs(s) for s in sentiments]) if sentiments else 0
        news_count_factor = min(1, len(news_data) / 10)  # Max 10 news for full impact
        
        impact = sentiment_strength * news_count_factor * 100
        return round(impact, 1)
    
    def interpret_fear_greed(self, index_value):
        """Fear & Greed index yorumlama"""
        if index_value >= 75:
            return "Piyasa aşırı açgözlülük seviyesinde. Satış fırsatı olabilir."
        elif index_value >= 55:
            return "Piyasa açgözlülük seviyesinde. Dikkatli olun."
        elif index_value >= 45:
            return "Piyasa nötr seviyede. Dengeli yaklaşım sergileyin."
        elif index_value >= 25:
            return "Piyasa korku seviyesinde. Alım fırsatları arayın."
        else:
            return "Piyasa aşırı korku seviyesinde. Güçlü alım fırsatı."
    
    def get_historical_context(self, current_index):
        """Historik context"""
        if current_index > 80:
            return "Son 2 yılın en yüksek seviyelerinde"
        elif current_index < 20:
            return "Son 2 yılın en düşük seviyelerinde"
        else:
            return "Historik ortalama seviyelerinde"
    
    def analyze_sector_sentiment(self, symbol_sentiments):
        """Sektör sentiment analizi"""
        # Basit sektör mapping
        sector_map = {
            'THYAO': 'Transportation', 'AKBNK': 'Banking', 
            'BIMAS': 'Retail', 'ASELS': 'Defense', 'KCHOL': 'Holding'
        }
        
        sectors = defaultdict(list)
        for symbol, data in symbol_sentiments.items():
            sector = sector_map.get(symbol, 'Other')
            sectors[sector].append(data['sentiment_score'])
        
        sector_avg = {}
        for sector, scores in sectors.items():
            sector_avg[sector] = {
                'avg_sentiment': round(np.mean(scores), 3),
                'sentiment_label': self.get_sentiment_label(np.mean(scores))
            }
        
        return sector_avg
    
    def determine_market_mood(self, sentiment, dispersion):
        """Piyasa ruh hali"""
        if sentiment > 0.3 and dispersion < 0.3:
            return "Optimistic Consensus"
        elif sentiment < -0.3 and dispersion < 0.3:
            return "Pessimistic Consensus"
        elif dispersion > 0.6:
            return "Confused/Conflicted"
        elif sentiment > 0:
            return "Cautiously Optimistic"
        else:
            return "Cautiously Pessimistic"
    
    def identify_sentiment_extremes(self, symbol_sentiments):
        """Sentiment aşırılıkları"""
        extremes = {
            'most_positive': None,
            'most_negative': None
        }
        
        max_sentiment = -2
        min_sentiment = 2
        
        for symbol, data in symbol_sentiments.items():
            score = data['sentiment_score']
            if score > max_sentiment:
                max_sentiment = score
                extremes['most_positive'] = {'symbol': symbol, 'sentiment': score}
            
            if score < min_sentiment:
                min_sentiment = score
                extremes['most_negative'] = {'symbol': symbol, 'sentiment': score}
        
        return extremes
    
    def calculate_sentiment_trend(self, sentiment_values):
        """Sentiment trend hesaplama"""
        if len(sentiment_values) < 3:
            return {'direction': 'insufficient_data', 'strength': 0, 'slope': 0}
        
        # Linear regression slope
        x = np.arange(len(sentiment_values))
        slope = np.polyfit(x, sentiment_values, 1)[0]
        
        # Trend direction and strength
        if slope > 0.05:
            direction = "Improving"
            strength = min(1, slope * 10)
        elif slope < -0.05:
            direction = "Deteriorating"
            strength = min(1, abs(slope) * 10)
        else:
            direction = "Stable"
            strength = 0
        
        return {
            'direction': direction,
            'strength': round(strength, 3),
            'slope': round(slope, 4)
        }
    
    def assess_sentiment_risk(self, sentiment, strength, volume):
        """Sentiment risk değerlendirmesi"""
        risk_factors = []
        
        if abs(sentiment) > 0.7:
            risk_factors.append("Extreme sentiment levels")
        
        if strength > 0.8:
            risk_factors.append("High sentiment volatility")
        
        if volume < 30:
            risk_factors.append("Low sample size")
        
        risk_level = "HIGH" if len(risk_factors) >= 2 else "MEDIUM" if risk_factors else "LOW"
        
        return {
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
    
    def calculate_signal_confidence(self, signals, signal_strength):
        """Sinyal güven seviyesi"""
        if not signals:
            return 0
        
        signal_count = len(signals)
        strength_factor = abs(signal_strength)
        
        confidence = min(100, (signal_count * 20) + (strength_factor * 50))
        return round(confidence, 1)

# Test
if __name__ == "__main__":
    agent = SentimentAnalysisAgent()
    
    # Test 1: Social media sentiment
    task1 = {"type": "analyze_social_sentiment", "symbol": "THYAO", "platform": "twitter"}
    result1 = agent.process_task(task1)
    print("Social Sentiment:", result1)
    
    # Test 2: Fear & Greed Index
    task2 = {"type": "calculate_fear_greed_index", "market_data": None}
    result2 = agent.process_task(task2)
    print("Fear & Greed Index:", result2)
    
    # Test 3: Sentiment signals
    task3 = {"type": "sentiment_based_signals", "symbol": "THYAO"}
    result3 = agent.process_task(task3)
    print("Sentiment Signals:", result3)
    
    print("Agent Durumu:", agent.get_status())