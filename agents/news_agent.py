import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NewsAgent",
            agent_type="news_analyzer",
            capabilities=["kap_news", "sentiment_analysis", "news_categorization"]
        )
        self.kap_base_url = "https://www.kap.org.tr"
        self.news_cache = []
        self.sentiment_keywords = {
            'positive': ['artış', 'yükseliş', 'başarı', 'kâr', 'büyüme', 'gelişme', 'iyileştirme', 'pozitif', 'arttı', 'yükseldi', 'kazanç', 'getiri'],
            'negative': ['düşüş', 'azalış', 'zarar', 'risk', 'sorun', 'olumsuz', 'negatif', 'kriz', 'düştü', 'azaldı', 'kayıp', 'tehdit'],
            'neutral': ['açıklama', 'duyuru', 'bilgilendirme', 'toplantı', 'karar', 'onay', 'imza', 'sözleşme']
        }
    
    def can_handle_task(self, task):
        """Bu agent hangi görevleri yapabilir?"""
        news_tasks = ['get_kap_news', 'analyze_sentiment', 'categorize_news', 'company_news']
        return task.get('type') in news_tasks
    
    def process_task(self, task):
        """Görevi işle"""
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'get_kap_news':
                result = self.get_recent_kap_news(task.get('limit', 10))
            elif task_type == 'analyze_sentiment':
                result = self.analyze_news_sentiment(task.get('news_text'))
            elif task_type == 'company_news':
                result = self.get_company_news(task.get('company_code'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def get_recent_kap_news(self, limit=10):
        """KAP'dan gerçek haberleri al"""
        try:
            # RealDataConnector kullan
            from real_data_connector import RealDataConnector
            connector = RealDataConnector()
            
            # Gerçek KAP verilerini al
            kap_data = connector.get_kap_disclosures(limit)
            
            if kap_data.get('success'):
                processed_news = []
                
                for disclosure in kap_data.get('disclosures', []):
                    # Sentiment analizi ekle
                    sentiment = self.analyze_news_sentiment(disclosure.get('content', ''))
                    
                    news_item = {
                        'id': disclosure.get('id'),
                        'title': disclosure.get('title'),
                        'company': disclosure.get('company'),
                        'company_code': disclosure.get('company_code'),
                        'content': disclosure.get('content'),
                        'date': disclosure.get('date'),
                        'disclosure_type': disclosure.get('disclosure_type', 'unknown'),
                        'sentiment': sentiment,
                        'url': disclosure.get('url'),
                        'data_source': kap_data.get('source', 'UNKNOWN')
                    }
                    processed_news.append(news_item)
                
                self.news_cache.extend(processed_news)
                
                return {
                    "success": True,
                    "news_count": len(processed_news),
                    "news": processed_news,
                    "data_source": kap_data.get('source'),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "error": "KAP veri alımı başarısız"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_news_sentiment(self, text):
        """Haber sentimentini analiz et"""
        if not text:
            return {"sentiment": "neutral", "confidence": 0.0}
        
        text_lower = text.lower()
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text_lower)
        neutral_count = sum(1 for word in self.sentiment_keywords['neutral'] if word in text_lower)
        
        total_words = positive_count + negative_count + neutral_count
        
        if total_words == 0:
            return {"sentiment": "neutral", "confidence": 0.5}
        
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = "positive"
            confidence = positive_count / total_words
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = "negative"
            confidence = negative_count / total_words
        else:
            sentiment = "neutral"
            confidence = neutral_count / total_words if neutral_count > 0 else 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2),
            "positive_signals": positive_count,
            "negative_signals": negative_count,
            "neutral_signals": neutral_count
        }
    
    def get_company_news(self, company_code):
        """Belirli şirketin haberlerini al"""
        company_news = [news for news in self.news_cache if news.get('company_code') == company_code]
        
        return {
            "company_code": company_code,
            "news_count": len(company_news),
            "news": company_news,
            "overall_sentiment": self.calculate_overall_sentiment(company_news)
        }
    
    def calculate_overall_sentiment(self, news_list):
        """Haberlerin genel sentimentini hesapla"""
        if not news_list:
            return {"sentiment": "neutral", "confidence": 0.0}
        
        sentiments = [news.get('sentiment', {}) for news in news_list]
        
        positive_total = sum(s.get('positive_signals', 0) for s in sentiments)
        negative_total = sum(s.get('negative_signals', 0) for s in sentiments)
        
        if positive_total > negative_total:
            return {"sentiment": "positive", "strength": "strong" if positive_total > negative_total * 2 else "moderate"}
        elif negative_total > positive_total:
            return {"sentiment": "negative", "strength": "strong" if negative_total > positive_total * 2 else "moderate"}
        else:
            return {"sentiment": "neutral", "strength": "balanced"}

# Test fonksiyonu
if __name__ == "__main__":
    agent = NewsAgent()
    
    # Test 1: KAP haberlerini al
    task1 = {"type": "get_kap_news", "limit": 5}
    result1 = agent.process_task(task1)
    print("KAP Haberleri:", result1)
    
    # Test 2: Sentiment analizi
    task2 = {"type": "analyze_sentiment", "news_text": "Şirketimiz bu çeyrekte büyük artış ve kâr elde etmiştir"}
    result2 = agent.process_task(task2)
    print("Sentiment Analizi:", result2)
    
    # Agent durumu
    print("Agent Durumu:", agent.get_status())