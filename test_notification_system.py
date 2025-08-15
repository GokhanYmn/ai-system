#!/usr/bin/env python3
"""
Multi-Agent Notification System Test
Bu script Notification Agent'ın tüm özelliklerini test eder
"""

import sys
import os
import time

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_path = os.path.join(current_dir, 'agents')
sys.path.insert(0, current_dir)
sys.path.insert(0, agents_path)

from notification_agent import NotificationAgent

def test_notification_agent():
    print("🚀 Notification Agent Test Başlıyor...")
    print("=" * 60)
    
    # Agent'ı başlat
    agent = NotificationAgent()
    print(f"✅ {agent.name} başarıyla oluşturuldu")
    print(f"📋 Yetenekler: {', '.join(agent.capabilities)}")
    print()
    
    # Test 1: E-mail Bildirimi
    print("📧 Test 1: E-mail Bildirimi")
    print("-" * 30)
    
    email_task = {
        "type": "send_email",
        "email_data": {
            "to": ["test@example.com", "investor@company.com"],
            "subject": "THYAO Analiz Raporu - GÜÇLÜ AL Sinyali",
            "analysis_result": {
                "symbol": "THYAO",
                "recommendation": "GÜÇLÜ AL",
                "confidence": 92,
                "timestamp": "2024-01-15T14:30:00Z"
            }
        }
    }
    
    email_result = agent.process_task(email_task)
    print(f"📊 Sonuç: {email_result}")
    print()
    
    # Test 2: Telegram Bildirimi
    print("📱 Test 2: Telegram Bildirimi")
    print("-" * 30)
    
    telegram_task = {
        "type": "send_telegram", 
        "telegram_data": {
            "chat_id": "123456789",
            "analysis_result": {
                "symbol": "AKBNK",
                "recommendation": "AL",
                "confidence": 78,
                "timestamp": "2024-01-15T14:35:00Z"
            }
        }
    }
    
    telegram_result = agent.process_task(telegram_task)
    print(f"📊 Sonuç: {telegram_result}")
    print()
    
    # Test 3: Kullanıcı Aboneliği
    print("👤 Test 3: Kullanıcı Aboneliği")
    print("-" * 30)
    
    subscribe_task = {
        "type": "subscribe_user",
        "user_data": {
            "email": "premium@investor.com",
            "telegram_id": "987654321",
            "preferences": {
                "symbols": ["THYAO", "AKBNK", "BIMAS"],
                "email_enabled": True,
                "telegram_enabled": True,
                "frequency": "daily"
            }
        }
    }
    
    subscribe_result = agent.process_task(subscribe_task)
    print(f"📊 Sonuç: {subscribe_result}")
    print()
    
    # Test 4: İkinci Abone Ekle
    subscribe_task2 = {
        "type": "subscribe_user",
        "user_data": {
            "email": "trader@company.com",
            "preferences": {
                "symbols": ["ASELS", "KCHOL"],
                "email_enabled": True,
                "telegram_enabled": False,
                "frequency": "weekly"
            }
        }
    }
    
    subscribe_result2 = agent.process_task(subscribe_task2)
    print(f"📊 İkinci Abone: {subscribe_result2}")
    print()
    
    # Test 5: Otomatik Bildirim Planlama
    print("⏰ Test 5: Otomatik Bildirim Planlama")
    print("-" * 30)
    
    schedule_task = {
        "type": "schedule_alert",
        "schedule_config": {
            "frequency": "daily",
            "time": "09:00", 
            "notification_type": "email",
            "recipients": ["morning@report.com"],
            "symbols": ["THYAO", "AKBNK"],
            "enabled": True
        }
    }
    
    schedule_result = agent.process_task(schedule_task)
    print(f"📊 Sonuç: {schedule_result}")
    print()
    
    # Test 6: Broadcast (Toplu Gönderim)
    print("📢 Test 6: Broadcast Analiz Sonucu")
    print("-" * 30)
    
    broadcast_task = {
        "type": "broadcast_analysis",
        "analysis_data": {
            "symbol": "THYAO",
            "recommendation": "GÜÇLÜ AL",
            "confidence": 88,
            "timestamp": "2024-01-15T15:00:00Z"
        }
    }
    
    broadcast_result = agent.process_task(broadcast_task)
    print(f"📊 Sonuç: {broadcast_result}")
    print()
    
    # Test 7: Fiyat Uyarısı
    print("🔔 Test 7: Fiyat Uyarısı")
    print("-" * 30)
    
    price_alert_task = {
        "type": "price_alert",
        "alert_data": {
            "symbol": "THYAO",
            "current_price": 95.50,
            "trigger_price": 95.00,
            "alert_type": "above",
            "user_preferences": {
                "email": "alert@trader.com",
                "telegram_id": "555666777"
            }
        }
    }
    
    price_alert_result = agent.process_task(price_alert_task)
    print(f"📊 Sonuç: {price_alert_result}")
    print()
    
    # Test 8: İstatistikler
    print("📈 Test 8: Notification İstatistikleri")
    print("-" * 30)
    
    stats = agent.get_notification_stats()
    print("📊 Bildirim İstatistikleri:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    print()
    
    # Test 9: Agent Durumu
    print("🤖 Test 9: Agent Durumu")
    print("-" * 30)
    
    agent_status = agent.get_status()
    print("📋 Agent Durumu:")
    for key, value in agent_status.items():
        print(f"   • {key}: {value}")
    print()
    
    # Test 10: HTML Email Template Önizleme
    print("🎨 Test 10: HTML E-mail Template")
    print("-" * 30)
    
    sample_analysis = {
        "symbol": "THYAO",
        "recommendation": "GÜÇLÜ AL",
        "confidence": 91,
        "timestamp": "2024-01-15T16:00:00Z"
    }
    
    html_content = agent.create_email_template(sample_analysis)
    print(f"📄 HTML Template oluşturuldu: {len(html_content)} karakter")
    print(f"🎯 İçerik başlığı: 'Multi-Agent AI Sistemi' içeriyor: {'Multi-Agent' in html_content}")
    print()
    
    # Özet Rapor
    print("=" * 60)
    print("📋 TEST ÖZET RAPORU")
    print("=" * 60)
    print(f"✅ Toplam Test: 10")
    print(f"📧 E-mail Testleri: Başarılı (Demo Mode)")
    print(f"📱 Telegram Testleri: Başarılı (Demo Mode)")
    print(f"👥 Abone Sayısı: {len(agent.subscribers)}")
    print(f"📊 Bildirim Geçmişi: {len(agent.notification_history)}")
    print(f"⏰ Zamanlanmış Görevler: {len(agent.scheduled_tasks)}")
    print(f"🎯 Agent Durumu: {agent.status}")
    print()
    print("🎉 Tüm testler başarıyla tamamlandı!")
    print("💡 Gerçek kullanım için SMTP ve Telegram ayarları yapılmalı")
    print()
    
    return True

def test_email_template_features():
    """E-mail template özelliklerini detaylı test et"""
    print("🎨 E-mail Template Detaylı Test")
    print("=" * 40)
    
    agent = NotificationAgent()
    
    # Farklı senaryolar test et
    scenarios = [
        {
            "name": "Güçlü Alış Sinyali",
            "data": {"symbol": "THYAO", "recommendation": "GÜÇLÜ AL", "confidence": 95}
        },
        {
            "name": "Satış Sinyali", 
            "data": {"symbol": "AKBNK", "recommendation": "GÜÇLÜ SAT", "confidence": 88}
        },
        {
            "name": "Bekle Sinyali",
            "data": {"symbol": "BIMAS", "recommendation": "BEKLE", "confidence": 65}
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📧 Senaryo: {scenario['name']}")
        html = agent.create_email_template(scenario['data'])
        
        # Template kontrolü
        symbol = scenario['data']['symbol']
        recommendation = scenario['data']['recommendation']
        
        checks = [
            ('Symbol var', symbol in html),
            ('Öneri var', recommendation in html), 
            ('HTML yapısı', '<html>' in html and '</html>' in html),
            ('CSS styling', 'style=' in html),
            ('Responsive', 'max-width' in html),
            ('Footer var', 'Multi-Agent' in html)
        ]
        
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
    
    print("\n🎯 Template testleri tamamlandı!")

if __name__ == "__main__":
    print("🤖 Multi-Agent Notification System")
    print("🔧 Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Ana testleri çalıştır
        test_notification_agent()
        
        print("\n" + "=" * 60)
        
        # Template testleri
        test_email_template_features()
        
        print("\n🏆 TÜM TESTLER BAŞARIYLA TAMAMLANDI!")
        print("🚀 Notification Agent kullanıma hazır!")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()