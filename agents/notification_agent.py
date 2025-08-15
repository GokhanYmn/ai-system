import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule
import threading
import time
from datetime import datetime, timedelta
import os
from base_agent import BaseAgent

class NotificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NotificationAgent",
            agent_type="notification_manager",
            capabilities=["email_notifications", "telegram_bot", "scheduled_alerts", "real_time_notifications"]
        )
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': os.getenv('SENDER_EMAIL', 'your_email@gmail.com'),
            'sender_password': os.getenv('SENDER_PASSWORD', 'your_app_password'),
            'enabled': False  # Güvenlik için varsayılan kapalı
        }
        self.telegram_config = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'enabled': False  # Varsayılan kapalı
        }
        self.subscribers = []
        self.notification_history = []
        self.scheduled_tasks = []
        
    def can_handle_task(self, task):
        notification_tasks = [
            'send_email', 'send_telegram', 'schedule_alert', 
            'subscribe_user', 'broadcast_analysis', 'price_alert'
        ]
        return task.get('type') in notification_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'send_email':
                result = self.send_email_notification(task.get('email_data'))
            elif task_type == 'send_telegram':
                result = self.send_telegram_message(task.get('telegram_data'))
            elif task_type == 'schedule_alert':
                result = self.schedule_notification(task.get('schedule_config'))
            elif task_type == 'subscribe_user':
                result = self.subscribe_user(task.get('user_data'))
            elif task_type == 'broadcast_analysis':
                result = self.broadcast_analysis_result(task.get('analysis_data'))
            elif task_type == 'price_alert':
                result = self.send_price_alert(task.get('alert_data'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def send_email_notification(self, email_data):
        """E-mail bildirimi gönder"""
        if not self.email_config['enabled']:
            return {
                "success": False, 
                "error": "E-mail servisi etkin değil",
                "note": "Demo modda çalışıyor"
            }
        
        if not email_data:
            email_data = {
                'to': ['investor@example.com'],
                'subject': 'Multi-Agent AI Sistemi - Analiz Raporu',
                'analysis_result': {
                    'symbol': 'THYAO',
                    'recommendation': 'GÜÇLÜ AL',
                    'confidence': 85,
                    'timestamp': datetime.now().isoformat()
                }
            }
        
        try:
            # E-mail içeriği oluştur
            html_content = self.create_email_template(email_data.get('analysis_result'))
            
            # MIME message oluştur
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(email_data['to'])
            msg['Subject'] = email_data['subject']
            
            # HTML content ekle
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # PDF eki varsa ekle
            if email_data.get('pdf_attachment'):
                self.attach_pdf(msg, email_data['pdf_attachment'])
            
            # E-mail gönder (Demo mode)
            if self.email_config['enabled'] and self.email_config['sender_password']:
                server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.send_message(msg)
                server.quit()
                
                delivery_status = "delivered"
            else:
                delivery_status = "demo_mode"
            
            # Geçmişe kaydet
            notification_record = {
                'type': 'email',
                'recipients': email_data['to'],
                'subject': email_data['subject'],
                'sent_at': datetime.now().isoformat(),
                'status': delivery_status,
                'content_preview': email_data.get('analysis_result', {}).get('symbol', 'N/A')
            }
            self.notification_history.append(notification_record)
            
            return {
                "success": True,
                "message": f"E-mail {len(email_data['to'])} alıcıya gönderildi",
                "recipients": email_data['to'],
                "delivery_status": delivery_status,
                "notification_id": len(self.notification_history)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"E-mail gönderim hatası: {str(e)}"
            }
    
    def create_email_template(self, analysis_result):
        """Profesyonel e-mail şablonu"""
        symbol = analysis_result.get('symbol', 'UNKNOWN')
        recommendation = analysis_result.get('recommendation', 'BEKLE')
        confidence = analysis_result.get('confidence', 50)
        timestamp = analysis_result.get('timestamp', datetime.now().isoformat())
        
        # Renk seçimi
        if 'AL' in recommendation:
            color = '#52c41a'
            icon = '📈'
        elif 'SAT' in recommendation:
            color = '#f5222d' 
            icon = '📉'
        else:
            color = '#faad14'
            icon = '⏳'
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Multi-Agent AI Analiz Raporu</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
                <h1 style="margin: 0; font-size: 28px;">🤖 Multi-Agent AI Sistemi</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Finansal Analiz Raporu</p>
            </div>
            
            <!-- Ana Sonuç -->
            <div style="background: {color}; color: white; padding: 25px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="margin: 0; font-size: 24px;">{icon} {symbol}</h2>
                <h1 style="margin: 15px 0 5px 0; font-size: 32px;">{recommendation}</h1>
                <p style="margin: 0; font-size: 18px; opacity: 0.9;">Güven: %{confidence}</p>
            </div>
            
            <!-- Detaylar -->
            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #1890ff; margin-top: 0;">📊 Analiz Detayları</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;"><strong>Hisse Kodu:</strong></td>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">{symbol}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;"><strong>Analiz Zamanı:</strong></td>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">{datetime.fromisoformat(timestamp.replace('Z', '+00:00') if timestamp.endswith('Z') else timestamp).strftime('%d.%m.%Y %H:%M')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;"><strong>Öneri:</strong></td>
                        <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; text-align: right; color: {color}; font-weight: bold;">{recommendation}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;"><strong>Güven Seviyesi:</strong></td>
                        <td style="padding: 8px 0; text-align: right;"><strong>%{confidence}</strong></td>
                    </tr>
                </table>
            </div>
            
            <!-- Agent Analizleri -->
            <div style="background: #fff; border: 1px solid #e0e0e0; padding: 25px; border-radius: 10px; margin-bottom: 25px;">
                <h3 style="color: #1890ff; margin-top: 0;">🤖 AI Agent Analizleri</h3>
                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
                    <div style="flex: 1; min-width: 120px; text-align: center; padding: 15px; background: #f0f9ff; border-radius: 8px;">
                        <div style="font-size: 24px;">📰</div>
                        <div style="font-weight: bold; margin: 5px 0;">News Agent</div>
                        <div style="color: #52c41a;">✅ Pozitif</div>
                    </div>
                    <div style="flex: 1; min-width: 120px; text-align: center; padding: 15px; background: #f0f9ff; border-radius: 8px;">
                        <div style="font-size: 24px;">💰</div>
                        <div style="font-weight: bold; margin: 5px 0;">Financial</div>
                        <div style="color: #1890ff;">📊 Güçlü</div>
                    </div>
                    <div style="flex: 1; min-width: 120px; text-align: center; padding: 15px; background: #f0f9ff; border-radius: 8px;">
                        <div style="font-size: 24px;">📈</div>
                        <div style="font-weight: bold; margin: 5px 0;">Technical</div>
                        <div style="color: #52c41a;">⬆️ Yükseliş</div>
                    </div>
                </div>
            </div>
            
            <!-- Risk Uyarısı -->
            <div style="background: #fff2e8; border-left: 4px solid #faad14; padding: 20px; margin-bottom: 25px; border-radius: 0 8px 8px 0;">
                <h4 style="color: #d48806; margin-top: 0;">⚠️ Risk Uyarısı</h4>
                <p style="margin-bottom: 0; color: #8c5e00;">Bu rapor yatırım danışmanlığı değildir. Yatırım kararlarınızı almadan önce uzmanlardan görüş alınız. Geçmiş performans gelecekteki sonuçları garanti etmez.</p>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 20px; color: #666; font-size: 14px; border-top: 1px solid #e0e0e0;">
                <p style="margin: 0 0 10px 0;">Multi-Agent Finans AI Sistemi tarafından oluşturulmuştur</p>
                <p style="margin: 0; font-size: 12px;">🤖 7 Uzman AI Agent • 📊 Gerçek Zamanlı Analiz • 🎯 Akıllı Kararlar</p>
            </div>
            
        </body>
        </html>
        """
        
        return html_template
    
    def attach_pdf(self, msg, pdf_path):
        """PDF dosyasını e-mail'e ekle"""
        try:
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(pdf_path)}'
            )
            msg.attach(part)
        except Exception as e:
            print(f"PDF ekleme hatası: {e}")
    
    def send_telegram_message(self, telegram_data):
        """Telegram bot üzerinden mesaj gönder"""
        if not self.telegram_config['enabled'] or not self.telegram_config['bot_token']:
            return {
                "success": False,
                "error": "Telegram bot etkin değil",
                "note": "Demo modda çalışıyor"
            }
        
        if not telegram_data:
            telegram_data = {
                'chat_id': '123456789',
                'analysis_result': {
                    'symbol': 'THYAO',
                    'recommendation': 'GÜÇLÜ AL',
                    'confidence': 85
                }
            }
        
        try:
            # Telegram mesaj formatı
            analysis = telegram_data.get('analysis_result', {})
            symbol = analysis.get('symbol', 'UNKNOWN')
            recommendation = analysis.get('recommendation', 'BEKLE')
            confidence = analysis.get('confidence', 50)
            
            # Emoji seçimi
            if 'AL' in recommendation:
                emoji = '🚀'
            elif 'SAT' in recommendation:
                emoji = '📉'
            else:
                emoji = '⏳'
            
            message = f"""
{emoji} *Multi-Agent AI Analiz*

📊 *Hisse:* `{symbol}`
🎯 *Öneri:* *{recommendation}*
📈 *Güven:* %{confidence}

🤖 *7 AI Agent* koordineli analiz sonucu
⏰ *Zaman:* {datetime.now().strftime('%H:%M')}

_Bu analiz yatırım tavsiyesi değildir._
            """
            
            # API çağrısı (demo mode)
            url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
            payload = {
                'chat_id': telegram_data['chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            # Demo mode için simüle et
            if self.telegram_config['enabled']:
                response = requests.post(url, json=payload, timeout=10)
                delivery_status = "delivered" if response.status_code == 200 else "failed"
            else:
                delivery_status = "demo_mode"
            
            return {
                "success": True,
                "message": "Telegram mesajı gönderildi",
                "chat_id": telegram_data['chat_id'],
                "delivery_status": delivery_status
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Telegram gönderim hatası: {str(e)}"
            }
    
    def schedule_notification(self, schedule_config):
        """Otomatik bildirim planla"""
        if not schedule_config:
            schedule_config = {
                'frequency': 'daily',  # daily, weekly, monthly
                'time': '09:00',
                'notification_type': 'email',
                'recipients': ['admin@company.com'],
                'symbols': ['THYAO', 'AKBNK'],
                'enabled': True
            }
        
        schedule_id = f"SCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Schedule'a görev ekle
        def send_scheduled_notification():
            print(f"⏰ Zamanlanmış bildirim çalışıyor: {schedule_id}")
            # Burada analiz yapılıp bildirim gönderilir
            
        frequency = schedule_config.get('frequency', 'daily')
        time_str = schedule_config.get('time', '09:00')
        
        if frequency == 'daily':
            schedule.every().day.at(time_str).do(send_scheduled_notification)
        elif frequency == 'weekly':
            schedule.every().monday.at(time_str).do(send_scheduled_notification)
        elif frequency == 'monthly':
            schedule.every().month.at(time_str).do(send_scheduled_notification)
        
        # Kaydet
        self.scheduled_tasks.append({
            'id': schedule_id,
            'config': schedule_config,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        })
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "message": f"{frequency} bildirim planlandı",
            "next_run": self.calculate_next_run(schedule_config)
        }
    
    def calculate_next_run(self, config):
        """Sonraki çalışma zamanını hesapla"""
        frequency = config.get('frequency', 'daily')
        time_str = config.get('time', '09:00')
        
        now = datetime.now()
        hour, minute = map(int, time_str.split(':'))
        
        if frequency == 'daily':
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif frequency == 'weekly':
            days_ahead = 0 - now.weekday()  # Pazartesi
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:  # monthly
            if now.day <= 1:
                next_run = now.replace(day=1, hour=hour, minute=minute, second=0, microsecond=0)
            else:
                # Gelecek ay
                if now.month == 12:
                    next_run = now.replace(year=now.year+1, month=1, day=1, hour=hour, minute=minute)
                else:
                    next_run = now.replace(month=now.month+1, day=1, hour=hour, minute=minute)
        
        return next_run.isoformat()
    
    def subscribe_user(self, user_data):
        """Kullanıcı aboneliği ekle"""
        if not user_data:
            user_data = {
                'email': 'investor@example.com',
                'telegram_id': '123456789',
                'preferences': {
                    'symbols': ['THYAO', 'AKBNK'],
                    'email_enabled': True,
                    'telegram_enabled': False,
                    'frequency': 'daily'
                }
            }
        
        # Mevcut aboneyi kontrol et
        existing = next((sub for sub in self.subscribers if sub['email'] == user_data['email']), None)
        
        if existing:
            # Güncelle
            existing.update(user_data)
            existing['updated_at'] = datetime.now().isoformat()
            message = "Abonelik güncellendi"
        else:
            # Yeni ekle
            user_data['subscribed_at'] = datetime.now().isoformat()
            user_data['id'] = len(self.subscribers) + 1
            self.subscribers.append(user_data)
            message = "Yeni abonelik eklendi"
        
        return {
            "success": True,
            "message": message,
            "subscriber_id": user_data.get('id'),
            "total_subscribers": len(self.subscribers)
        }
    
    def broadcast_analysis_result(self, analysis_data):
        """Analiz sonucunu tüm abonelere gönder"""
        if not analysis_data:
            analysis_data = {
                'symbol': 'THYAO',
                'recommendation': 'GÜÇLÜ AL',
                'confidence': 85,
                'timestamp': datetime.now().isoformat()
            }
        
        if not self.subscribers:
            return {
                "success": False,
                "message": "Abone bulunamadı",
                "sent_count": 0
            }
        
        sent_count = 0
        errors = []
        
        for subscriber in self.subscribers:
            try:
                preferences = subscriber.get('preferences', {})
                symbol = analysis_data.get('symbol')
                
                # Sembol filtrelemesi
                if symbol not in preferences.get('symbols', []):
                    continue
                
                # E-mail gönder
                if preferences.get('email_enabled', True) and subscriber.get('email'):
                    email_task = {
                        'to': [subscriber['email']],
                        'subject': f'{symbol} Analiz Sonucu - {analysis_data.get("recommendation")}',
                        'analysis_result': analysis_data
                    }
                    email_result = self.send_email_notification(email_task)
                    if email_result.get('success'):
                        sent_count += 1
                
                # Telegram gönder
                if preferences.get('telegram_enabled', False) and subscriber.get('telegram_id'):
                    telegram_task = {
                        'chat_id': subscriber['telegram_id'],
                        'analysis_result': analysis_data
                    }
                    telegram_result = self.send_telegram_message(telegram_task)
                    if telegram_result.get('success'):
                        sent_count += 1
                        
            except Exception as e:
                errors.append(f"Abone {subscriber.get('email', 'unknown')}: {str(e)}")
        
        return {
            "success": True,
            "message": f"Broadcast tamamlandı",
            "sent_count": sent_count,
            "total_subscribers": len(self.subscribers),
            "errors": errors if errors else None
        }
    
    def send_price_alert(self, alert_data):
        """Fiyat uyarısı gönder"""
        if not alert_data:
            alert_data = {
                'symbol': 'THYAO',
                'current_price': 92.50,
                'trigger_price': 90.00,
                'alert_type': 'above',  # above, below
                'user_preferences': {
                    'email': 'investor@example.com',
                    'telegram_id': '123456789'
                }
            }
        
        symbol = alert_data['symbol']
        current_price = alert_data['current_price']
        trigger_price = alert_data['trigger_price']
        alert_type = alert_data['alert_type']
        
        # Uyarı mesajı oluştur
        if alert_type == 'above':
            message = f"🔔 {symbol} fiyatı {trigger_price} TL'nin üzerine çıktı!\n💰 Mevcut fiyat: {current_price} TL"
        else:
            message = f"⚠️ {symbol} fiyatı {trigger_price} TL'nin altına düştü!\n💰 Mevcut fiyat: {current_price} TL"
        
        # E-mail ve Telegram gönder
        notifications_sent = 0
        user_prefs = alert_data.get('user_preferences', {})
        
        if user_prefs.get('email'):
            email_result = self.send_email_notification({
                'to': [user_prefs['email']],
                'subject': f'Fiyat Uyarısı: {symbol}',
                'analysis_result': {
                    'symbol': symbol,
                    'recommendation': 'UYARI',
                    'confidence': 100,
                    'price_info': message
                }
            })
            if email_result.get('success'):
                notifications_sent += 1
        
        if user_prefs.get('telegram_id'):
            telegram_result = self.send_telegram_message({
                'chat_id': user_prefs['telegram_id'],
                'analysis_result': {
                    'symbol': symbol,
                    'recommendation': 'FİYAT UYARISI',
                    'confidence': 100,
                    'custom_message': message
                }
            })
            if telegram_result.get('success'):
                notifications_sent += 1
        
        return {
            "success": True,
            "message": "Fiyat uyarısı gönderildi",
            "alert_type": alert_type,
            "notifications_sent": notifications_sent
        }
    
    def get_notification_stats(self):
        """Bildirim istatistikleri"""
        email_count = len([n for n in self.notification_history if n['type'] == 'email'])
        telegram_count = len([n for n in self.notification_history if n['type'] == 'telegram'])
        
        return {
            "total_notifications": len(self.notification_history),
            "email_notifications": email_count,
            "telegram_notifications": telegram_count,
            "active_subscribers": len(self.subscribers),
            "scheduled_tasks": len(self.scheduled_tasks),
            "last_notification": self.notification_history[-1] if self.notification_history else None
        }
    
    def start_scheduler(self):
        """Zamanlanmış görevleri başlat"""
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Her dakika kontrol et
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("📅 Bildirim zamanlayıcısı başlatıldı")

# Test fonksiyonu
if __name__ == "__main__":
    agent = NotificationAgent()
    
    # Test 1: E-mail bildirimi
    email_task = {"type": "send_email", "email_data": None}
    result1 = agent.process_task(email_task)
    print("E-mail Test:", result1)
    
    # Test 2: Telegram bildirimi
    telegram_task = {"type": "send_telegram", "telegram_data": None}
    result2 = agent.process_task(telegram_task)
    print("Telegram Test:", result2)
    
    # Test 3: Kullanıcı aboneliği
    subscribe_task = {"type": "subscribe_user", "user_data": None}
    result3 = agent.process_task(subscribe_task)
    print("Abonelik Test:", result3)
    
    # İstatistikler
    print("İstatistikler:", agent.get_notification_stats())
    
    print("Agent Durumu:", agent.get_status())