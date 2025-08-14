from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import io
import base64
import os
from datetime import datetime, timedelta
import time
from base_agent import BaseAgent

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ReportAgent",
            agent_type="report_generator",
            capabilities=["pdf_generation", "chart_creation", "email_reports", "scheduled_reports"]
        )
        self.report_templates = {
            'daily': 'Günlük Analiz Raporu',
            'weekly': 'Haftalık Piyasa Raporu', 
            'analysis': 'Hisse Analiz Raporu',
            'performance': 'Sistem Performans Raporu'
        }
        self.setup_turkish_fonts()
        
    def setup_turkish_fonts(self):
        """Türkçe karakterler için font ayarları"""
        try:
            # DejaVu fonts kullan (çoğu sistemde mevcut)
            import matplotlib
            matplotlib.rcParams['font.family'] = ['DejaVu Sans']
        except:
            pass
        
    def can_handle_task(self, task):
        report_tasks = ['generate_pdf_report', 'create_chart', 'schedule_report', 'email_report']
        return task.get('type') in report_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'generate_pdf_report':
                result = self.generate_pdf_report(task.get('report_data'), task.get('report_type', 'analysis'))
            elif task_type == 'create_chart':
                result = self.create_analysis_chart(task.get('chart_data'))
            elif task_type == 'schedule_report':
                result = self.schedule_automatic_report(task.get('schedule_config'))
            elif task_type == 'email_report':
                result = self.prepare_email_report(task.get('email_config'))
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def generate_pdf_report(self, report_data, report_type='analysis'):
        """PDF rapor oluştur"""
        if not report_data:
            # Mock data ile test raporu
            report_data = {
                'symbol': 'THYAO',
                'analysis_date': datetime.now().isoformat(),
                'recommendation': 'GÜÇLÜ AL',
                'confidence': 85,
                'financial_score': 78,
                'technical_score': 82,
                'news_sentiment': 'Pozitif',
                'target_price': 105.50,
                'current_price': 91.50,
                'stop_loss': 85.40,
                'risk_level': 'Orta',
                'agent_analysis': {
                    'financial_agent': {'score': 78, 'status': 'Güçlü'},
                    'technical_agent': {'score': 82, 'status': 'Pozitif'},
                    'news_agent': {'score': 75, 'status': 'İyi'},
                    'data_agent': {'score': 80, 'status': 'Stabil'}
                }
            }
        
        # Dosya adı ve path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"analiz_raporu_{report_data.get('symbol', 'STOCK')}_{timestamp}.pdf"
        filepath = os.path.join('reports', filename)
        
        # Reports klasörü oluştur
        os.makedirs('reports', exist_ok=True)
        
        try:
            # PDF oluştur - basit encoding
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Başlık
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # Center
                textColor=colors.darkblue
            )
            
            story.append(Paragraph("Multi-Agent Finans AI Sistemi", title_style))
            story.append(Paragraph(f"{report_data.get('symbol')} Hisse Analiz Raporu", title_style))
            story.append(Spacer(1, 20))
            
            # Genel Bilgiler
            info_data = [
                ['Hisse Kodu:', report_data.get('symbol')],
                ['Analiz Tarihi:', datetime.now().strftime('%d.%m.%Y %H:%M')],
                ['Mevcut Fiyat:', f"TL {report_data.get('current_price')}"],
                ['Hedef Fiyat:', f"TL {report_data.get('target_price')}"],
                ['Onerilen Islem:', report_data.get('recommendation')],
                ['Guven Seviyesi:', f"{report_data.get('confidence')} %"]
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 2*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(Paragraph("Genel Bilgiler", styles['Heading2']))
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # Agent Analizleri
            story.append(Paragraph("Agent Analizleri", styles['Heading2']))
            
            agent_data = [['Agent', 'Skor', 'Durum', 'Degerlendirme']]
            for agent_name, analysis in report_data.get('agent_analysis', {}).items():
                agent_display = agent_name.replace('_agent', '').title()
                score = analysis.get('score', 0)
                status = analysis.get('status', 'Bilinmiyor')
                evaluation = self.get_score_evaluation(score)
                agent_data.append([agent_display, f"{score}/100", status, evaluation])
            
            agent_table = Table(agent_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
            agent_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(agent_table)
            story.append(Spacer(1, 20))
            
            # Risk Yönetimi
            story.append(Paragraph("Risk Yonetimi", styles['Heading2']))
            risk_content = f"""
            <para>
            • <b>Risk Seviyesi:</b> {report_data.get('risk_level', 'Orta')}<br/>
            • <b>Stop Loss:</b> TL {report_data.get('stop_loss', 0)}<br/>
            • <b>Beklenen Getiri:</b> {((report_data.get('target_price', 100) / report_data.get('current_price', 100) - 1) * 100):.1f} %<br/>
            • <b>Risk/Getiri Orani:</b> {self.calculate_risk_reward_ratio(report_data)}<br/>
            </para>
            """
            story.append(Paragraph(risk_content, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Sonuç ve Öneriler
            story.append(Paragraph("Sonuc ve Oneriler", styles['Heading2']))
            conclusion = self.generate_conclusion(report_data)
            story.append(Paragraph(conclusion, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Footer
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                alignment=1,
                textColor=colors.grey
            )
            story.append(Paragraph(f"Bu rapor Multi-Agent AI Sistemi tarafindan {datetime.now().strftime('%d.%m.%Y %H:%M')} tarihinde olusturulmustur.", footer_style))
            story.append(Paragraph("Bu rapor yatirim danismanligi degildir. Yatirim kararlarinizi almadan once uzmanlardan gorus aliniz.", footer_style))
            
            # PDF'i oluştur
            doc.build(story)
            
            return {
                "success": True,
                "report_path": filepath,
                "filename": filename,
                "file_size": os.path.getsize(filepath),
                "pages": 1,
                "report_type": report_type,
                "generation_time": datetime.now().isoformat(),
                "download_url": f"/reports/download/{filename}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"PDF oluşturma hatası: {str(e)}",
                "filename": filename
            }
    
    def get_score_evaluation(self, score):
        """Skora göre değerlendirme - Türkçe karakter yok"""
        if score >= 85:
            return "Mukemmel"
        elif score >= 70:
            return "Iyi"
        elif score >= 55:
            return "Orta"
        elif score >= 40:
            return "Zayif"
        else:
            return "Kotu"
    
    def calculate_risk_reward_ratio(self, data):
        """Risk/getiri oranını hesapla"""
        current = data.get('current_price', 100)
        target = data.get('target_price', 100)
        stop_loss = data.get('stop_loss', current * 0.9)
        
        potential_gain = target - current
        potential_loss = current - stop_loss
        
        if potential_loss > 0:
            ratio = potential_gain / potential_loss
            return f"1:{ratio:.1f}"
        return "1:1"
    
    def generate_conclusion(self, data):
        """Sonuç metni oluştur - Türkçe karakter sorunları için basit metin"""
        recommendation = data.get('recommendation', 'BEKLE')
        confidence = data.get('confidence', 50)
        symbol = data.get('symbol', 'HISSE')
        
        if recommendation in ['GUCLU AL', 'AL']:
            conclusion = f"""
            <para>
            <b>{symbol}</b> hissesi icin yapilan coklu-agent analizinde <b>{recommendation}</b> onerisi cikmistir. 
            %{confidence} guven seviyesi ile bu hissenin kisa-orta vadede pozitif performans gosterecegi degerlendirilmektedir.
            <br/><br/>
            <b>Onemli Noktalar:</b><br/>
            • Finansal ve teknik gostergeler pozitif sinyal veriyor<br/>
            • Piyasa duyarliligi olumlu<br/>
            • Risk yonetimi kurallarina dikkat edilmeli<br/>
            • Pozisyon buyuklugu risk toleransina uygun olmali
            </para>
            """
        elif recommendation in ['SAT', 'GUCLU SAT']:
            conclusion = f"""
            <para>
            <b>{symbol}</b> hissesi icin yapilan analiz sonucunda <b>{recommendation}</b> onerisi verilmistir.
            Mevcut piyasa kosullari ve teknik gostergeler negatif sinyal vermektedir.
            <br/><br/>
            <b>Dikkat Edilmesi Gerekenler:</b><br/>
            • Mevcut pozisyonlar gozden gecirilmeli<br/>
            • Stop loss seviyeleri guncellenmeli<br/>
            • Piyasa gelismeleri yakindan takip edilmeli
            </para>
            """
        else:
            conclusion = f"""
            <para>
            <b>{symbol}</b> hissesi icin yapilan analiz sonucunda <b>BEKLE</b> onerisi verilmistir.
            Mevcut piyasa kosullarinda net bir yon belirsizligi bulunmaktadir.
            <br/><br/>
            <b>Oneriler:</b><br/>
            • Piyasa gelismeleri yakindan izlenmeli<br/>
            • Teknik seviyelerdeki kirilimlar takip edilmeli<br/>
            • Yeni verilerin analizi beklenmelidir
            </para>
            """
        
        return conclusion
    
    def create_analysis_chart(self, chart_data):
        """Analiz grafiği oluştur"""
        try:
            # Matplotlib ile grafik oluştur
            plt.figure(figsize=(10, 6))
            plt.style.use('seaborn-v0_8')
            
            if not chart_data:
                # Mock chart data
                agents = ['Financial', 'Technical', 'News', 'Data']
                scores = [78, 82, 75, 80]
                colors_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                
                plt.bar(agents, scores, color=colors_list, alpha=0.8)
                plt.title('Agent Analiz Skorları', fontsize=16, fontweight='bold')
                plt.ylabel('Skor (0-100)', fontsize=12)
                plt.xlabel('AI Agent\'lar', fontsize=12)
                plt.ylim(0, 100)
                
                # Skor değerlerini bar'ların üstüne yaz
                for i, score in enumerate(scores):
                    plt.text(i, score + 2, str(score), ha='center', fontweight='bold')
            
            # Grafigi bytes olarak kaydet
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            
            # Base64 encode
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            plt.close()
            
            return {
                "success": True,
                "chart_base64": img_base64,
                "chart_type": "agent_scores",
                "format": "png"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Grafik oluşturma hatası: {str(e)}"
            }
    
    def schedule_automatic_report(self, schedule_config):
        """Otomatik rapor planlama"""
        if not schedule_config:
            schedule_config = {
                'frequency': 'daily',  # daily, weekly, monthly
                'time': '09:00',
                'recipients': ['admin@company.com'],
                'report_types': ['analysis', 'performance']
            }
        
        return {
            "success": True,
            "schedule_id": f"SCHEDULE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "config": schedule_config,
            "next_run": self.calculate_next_run_time(schedule_config),
            "status": "scheduled"
        }
    
    def calculate_next_run_time(self, config):
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
            # Pazartesi günü
            days_ahead = 0 - now.weekday()
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
    
    def prepare_email_report(self, email_config):
        """E-mail raporu hazırla"""
        if not email_config:
            email_config = {
                'recipients': ['admin@company.com'],
                'subject': 'Günlük Piyasa Analiz Raporu',
                'report_data': None
            }
        
        # E-mail içeriği oluştur
        email_content = self.generate_email_content(email_config.get('report_data'))
        
        return {
            "success": True,
            "email_prepared": True,
            "recipients": email_config.get('recipients'),
            "subject": email_config.get('subject'),
            "content_length": len(email_content),
            "attachments": 1,  # PDF rapor
            "ready_to_send": True,
            "note": "SMTP ayarları yapıldığında gönderilecek"
        }
    
    def generate_email_content(self, report_data):
        """E-mail içeriği oluştur"""
        return f"""
        <html>
        <body>
        <h2>🤖 Multi-Agent Finans AI Sistemi - Günlük Rapor</h2>
        <p>Merhaba,</p>
        <p>Bugünün piyasa analiz raporunu ekte bulabilirsiniz.</p>
        
        <h3>📊 Günün Öne Çıkanları:</h3>
        <ul>
        <li>En çok analiz edilen hisse: {report_data.get('top_symbol', 'THYAO') if report_data else 'THYAO'}</li>
        <li>Sistem durumu: Aktif ve stabil</li>
        <li>Agent performansı: %95 başarı oranı</li>
        </ul>
        
        <p>Detaylı analiz için ekteki PDF raporunu inceleyiniz.</p>
        
        <p>İyi günler,<br/>
        Multi-Agent AI Sistemi</p>
        </body>
        </html>
        """

# Test fonksiyonu
if __name__ == "__main__":
    agent = ReportAgent()
    
    # Test 1: PDF rapor oluştur
    task1 = {"type": "generate_pdf_report", "report_data": None}
    result1 = agent.process_task(task1)
    print("PDF Rapor:", result1)
    
    # Test 2: Grafik oluştur
    task2 = {"type": "create_chart", "chart_data": None}
    result2 = agent.process_task(task2)
    print("Grafik:", "Başarılı" if result2.get('success') else "Hata")
    
    print("Agent Durumu:", agent.get_status())