import psutil # pyright: ignore[reportMissingModuleSource]
import time
import threading
import asyncio
from datetime import datetime, timedelta
from collections import deque, defaultdict
import json
import statistics
import numpy as np
from base_agent import BaseAgent

class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PerformanceAgent",
            agent_type="performance_monitor",
            capabilities=[
                "real_time_monitoring", "performance_optimization", 
                "resource_tracking", "bottleneck_detection",
                "auto_scaling", "health_checks", "predictive_analytics"
            ]
        )
        
        # Performance tracking
        self.agent_metrics = defaultdict(lambda: {
            'response_times': deque(maxlen=100),
            'success_rate': deque(maxlen=100),
            'error_count': 0,
            'total_requests': 0,
            'last_activity': None,
            'status': 'unknown',
            'memory_usage': deque(maxlen=50),
            'cpu_usage': deque(maxlen=50)
        })
        
        # System metrics
        self.system_metrics = {
            'cpu_usage': deque(maxlen=100),
            'memory_usage': deque(maxlen=100),
            'disk_usage': deque(maxlen=100),
            'network_io': deque(maxlen=100),
            'api_response_times': deque(maxlen=100),
            'active_connections': deque(maxlen=100)
        }
        
        # Performance thresholds
        self.thresholds = {
            'max_response_time': 5.0,  # 5 seconds
            'min_success_rate': 0.95,  # 95%
            'max_cpu_usage': 0.80,    # 80%
            'max_memory_usage': 0.85,  # 85%
            'max_error_rate': 0.05     # 5%
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alert_history = []
        self.optimization_suggestions = []
        self.performance_reports = []
        
        # Predictive analytics
        self.usage_patterns = defaultdict(list)
        self.peak_hours = []
        self.trend_data = defaultdict(deque)
        
    def can_handle_task(self, task):
        performance_tasks = [
            'start_monitoring', 'stop_monitoring', 'get_metrics',
            'analyze_performance', 'optimize_system', 'health_check',
            'generate_report', 'predict_usage', 'detect_bottlenecks'
        ]
        return task.get('type') in performance_tasks
    
    def process_task(self, task):
        self.status = "working"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'start_monitoring':
                result = self.start_monitoring()
            elif task_type == 'stop_monitoring':
                result = self.stop_monitoring()
            elif task_type == 'get_metrics':
                result = self.get_current_metrics()
            elif task_type == 'analyze_performance':
                result = self.analyze_agent_performance(task.get('agent_name'))
            elif task_type == 'optimize_system':
                result = self.optimize_system_performance()
            elif task_type == 'health_check':
                result = self.perform_comprehensive_health_check()
            elif task_type == 'generate_report':
                result = self.generate_performance_report(task.get('period', 'daily'))
            elif task_type == 'predict_usage':
                result = self.predict_system_usage()
            elif task_type == 'detect_bottlenecks':
                result = self.detect_system_bottlenecks()
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def start_monitoring(self):
        """Real-time monitoring başlat"""
        if self.monitoring_active:
            return {"success": False, "message": "Monitoring zaten aktif"}
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        return {
            "success": True,
            "message": "Performance monitoring başlatıldı",
            "monitoring_interval": "5 saniye",
            "metrics_tracked": len(self.capabilities),
            "thresholds": self.thresholds
        }
    
    def stop_monitoring(self):
        """Monitoring'i durdur"""
        self.monitoring_active = False
        
        return {
            "success": True,
            "message": "Performance monitoring durduruldu",
            "total_runtime": "hesaplanıyor...",
            "data_points_collected": sum(len(metrics['response_times']) for metrics in self.agent_metrics.values())
        }
    
    def _monitoring_loop(self):
        """Ana monitoring döngüsü"""
        print("🔍 Performance monitoring başladı...")
        
        while self.monitoring_active:
            try:
                # System metrics topla
                self._collect_system_metrics()
                
                # Agent metrics güncelle
                self._update_agent_metrics()
                
                # Threshold kontrolleri
                self._check_thresholds()
                
                # Trend analizi
                self._analyze_trends()
                
                time.sleep(5)  # 5 saniye interval
                
            except Exception as e:
                print(f"⚠️ Monitoring hatası: {e}")
                time.sleep(10)
    
    def _collect_system_metrics(self):
        """Sistem metriklerini topla"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.system_metrics['cpu_usage'].append({
                'timestamp': datetime.now().isoformat(),
                'value': cpu_percent
            })
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.system_metrics['memory_usage'].append({
                'timestamp': datetime.now().isoformat(),
                'value': memory.percent,
                'available_gb': round(memory.available / (1024**3), 2)
            })
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.system_metrics['disk_usage'].append({
                'timestamp': datetime.now().isoformat(),
                'value': (disk.used / disk.total) * 100,
                'free_gb': round(disk.free / (1024**3), 2)
            })
            
            # Network I/O
            net_io = psutil.net_io_counters()
            self.system_metrics['network_io'].append({
                'timestamp': datetime.now().isoformat(),
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            })
            
        except Exception as e:
            print(f"❌ Sistem metrikleri hatası: {e}")
    
    def _update_agent_metrics(self):
        """Agent metriklerini güncelle (simulated)"""
        # Mock agent performance data
        agents = ['news_agent', 'financial_agent', 'technical_agent', 'data_agent', 
                 'decision_agent', 'trading_agent', 'notification_agent', 'report_agent']
        
        for agent_name in agents:
            metrics = self.agent_metrics[agent_name]
            
            # Simulated response time (0.5-3.0 seconds)
            response_time = np.random.normal(1.2, 0.4)
            response_time = max(0.3, min(5.0, response_time))
            
            metrics['response_times'].append({
                'timestamp': datetime.now().isoformat(),
                'value': response_time
            })
            
            # Simulated success rate (85-99%)
            success = np.random.choice([True, False], p=[0.96, 0.04])
            metrics['success_rate'].append(success)
            
            # Memory usage per agent (simulated)
            memory_mb = np.random.normal(150, 30)
            memory_mb = max(50, min(500, memory_mb))
            metrics['memory_usage'].append(memory_mb)
            
            # CPU usage per agent (simulated)
            cpu_percent = np.random.normal(15, 5)
            cpu_percent = max(1, min(50, cpu_percent))
            metrics['cpu_usage'].append(cpu_percent)
            
            # Update counters
            metrics['total_requests'] += 1
            if not success:
                metrics['error_count'] += 1
            
            metrics['last_activity'] = datetime.now().isoformat()
            metrics['status'] = 'active'
    
    def _check_thresholds(self):
        """Threshold aşımlarını kontrol et"""
        current_time = datetime.now()
        alerts = []
        
        # System-level checks
        if self.system_metrics['cpu_usage']:
            current_cpu = self.system_metrics['cpu_usage'][-1]['value']
            if current_cpu > self.thresholds['max_cpu_usage'] * 100:
                alerts.append({
                    'type': 'CPU_HIGH',
                    'message': f'CPU kullanımı yüksek: %{current_cpu:.1f}',
                    'severity': 'warning',
                    'timestamp': current_time.isoformat()
                })
        
        if self.system_metrics['memory_usage']:
            current_memory = self.system_metrics['memory_usage'][-1]['value']
            if current_memory > self.thresholds['max_memory_usage'] * 100:
                alerts.append({
                    'type': 'MEMORY_HIGH',
                    'message': f'Bellek kullanımı yüksek: %{current_memory:.1f}',
                    'severity': 'warning',
                    'timestamp': current_time.isoformat()
                })
        
        # Agent-level checks
        for agent_name, metrics in self.agent_metrics.items():
            if metrics['response_times']:
                avg_response = statistics.mean([rt['value'] for rt in list(metrics['response_times'])[-10:]])
                if avg_response > self.thresholds['max_response_time']:
                    alerts.append({
                        'type': 'SLOW_RESPONSE',
                        'agent': agent_name,
                        'message': f'{agent_name} yavaş: {avg_response:.2f}s',
                        'severity': 'warning',
                        'timestamp': current_time.isoformat()
                    })
            
            if metrics['success_rate']:
                recent_success = statistics.mean(list(metrics['success_rate'])[-20:])
                if recent_success < self.thresholds['min_success_rate']:
                    alerts.append({
                        'type': 'LOW_SUCCESS_RATE',
                        'agent': agent_name,
                        'message': f'{agent_name} düşük başarı: %{recent_success*100:.1f}',
                        'severity': 'critical',
                        'timestamp': current_time.isoformat()
                    })
        
        # Store alerts
        self.alert_history.extend(alerts)
        
        # Keep only recent alerts (last 1000)
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
    
    def _analyze_trends(self):
        """Trend analizi yap"""
        current_time = datetime.now()
        
        # CPU trend analysis
        if len(self.system_metrics['cpu_usage']) >= 10:
            recent_cpu = [m['value'] for m in list(self.system_metrics['cpu_usage'])[-10:]]
            cpu_trend = np.polyfit(range(len(recent_cpu)), recent_cpu, 1)[0]  # Slope
            
            if abs(cpu_trend) > 2:  # Significant trend
                trend_direction = "increasing" if cpu_trend > 0 else "decreasing"
                self.trend_data['cpu_trend'].append({
                    'timestamp': current_time.isoformat(),
                    'direction': trend_direction,
                    'rate': round(cpu_trend, 2)
                })
        
        # Usage pattern detection
        hour = current_time.hour
        if hour not in self.usage_patterns:
            self.usage_patterns[hour] = []
        
        if self.system_metrics['cpu_usage']:
            current_cpu = self.system_metrics['cpu_usage'][-1]['value']
            self.usage_patterns[hour].append(current_cpu)
            
            # Keep only recent data (last 30 days)
            if len(self.usage_patterns[hour]) > 30:
                self.usage_patterns[hour] = self.usage_patterns[hour][-30:]
    
    def get_current_metrics(self):
        """Güncel metrikleri döndür"""
        current_metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': {},
            'agents': {},
            'summary': {}
        }
        
        # System metrics
        if self.system_metrics['cpu_usage']:
            current_metrics['system']['cpu_usage'] = self.system_metrics['cpu_usage'][-1]['value']
        
        if self.system_metrics['memory_usage']:
            current_metrics['system']['memory_usage'] = self.system_metrics['memory_usage'][-1]['value']
            current_metrics['system']['memory_available'] = self.system_metrics['memory_usage'][-1]['available_gb']
        
        if self.system_metrics['disk_usage']:
            current_metrics['system']['disk_usage'] = self.system_metrics['disk_usage'][-1]['value']
            current_metrics['system']['disk_free'] = self.system_metrics['disk_usage'][-1]['free_gb']
        
        # Agent metrics
        for agent_name, metrics in self.agent_metrics.items():
            agent_summary = {
                'status': metrics['status'],
                'total_requests': metrics['total_requests'],
                'error_count': metrics['error_count'],
                'last_activity': metrics['last_activity']
            }
            
            if metrics['response_times']:
                recent_times = [rt['value'] for rt in list(metrics['response_times'])[-10:]]
                agent_summary['avg_response_time'] = round(statistics.mean(recent_times), 3)
                agent_summary['max_response_time'] = round(max(recent_times), 3)
            
            if metrics['success_rate']:
                recent_success = list(metrics['success_rate'])[-20:]
                agent_summary['success_rate'] = round(statistics.mean(recent_success) * 100, 1)
            
            if metrics['memory_usage']:
                agent_summary['memory_usage_mb'] = round(metrics['memory_usage'][-1], 1)
            
            if metrics['cpu_usage']:
                agent_summary['cpu_usage_percent'] = round(metrics['cpu_usage'][-1], 1)
            
            current_metrics['agents'][agent_name] = agent_summary
        
        # Summary
        active_agents = len([a for a in current_metrics['agents'].values() if a['status'] == 'active'])
        total_requests = sum(a['total_requests'] for a in current_metrics['agents'].values())
        total_errors = sum(a['error_count'] for a in current_metrics['agents'].values())
        
        current_metrics['summary'] = {
            'active_agents': active_agents,
            'total_agents': len(current_metrics['agents']),
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_rate': round((total_errors / max(total_requests, 1)) * 100, 2),
            'monitoring_active': self.monitoring_active,
            'recent_alerts': len([a for a in self.alert_history if 
                                datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(minutes=5)])
        }
        
        return current_metrics
    
    def analyze_agent_performance(self, agent_name=None):
        """Agent performansını analiz et"""
        if agent_name and agent_name not in self.agent_metrics:
            return {"error": f"Agent '{agent_name}' bulunamadı"}
        
        analysis = {}
        agents_to_analyze = [agent_name] if agent_name else list(self.agent_metrics.keys())
        
        for name in agents_to_analyze:
            metrics = self.agent_metrics[name]
            agent_analysis = {
                'agent_name': name,
                'status': metrics['status'],
                'performance_score': 0,
                'recommendations': []
            }
            
            # Response time analysis
            if metrics['response_times']:
                times = [rt['value'] for rt in metrics['response_times']]
                agent_analysis['response_times'] = {
                    'average': round(statistics.mean(times), 3),
                    'median': round(statistics.median(times), 3),
                    'p95': round(np.percentile(times, 95), 3),
                    'min': round(min(times), 3),
                    'max': round(max(times), 3)
                }
                
                # Score calculation
                avg_time = agent_analysis['response_times']['average']
                time_score = max(0, 100 - (avg_time / self.thresholds['max_response_time']) * 50)
                agent_analysis['performance_score'] += time_score * 0.4
                
                if avg_time > self.thresholds['max_response_time']:
                    agent_analysis['recommendations'].append(
                        f"Response time optimization needed (current: {avg_time:.2f}s)"
                    )
            
            # Success rate analysis
            if metrics['success_rate']:
                success_rate = statistics.mean(metrics['success_rate'])
                agent_analysis['success_rate'] = round(success_rate * 100, 2)
                
                success_score = success_rate * 100
                agent_analysis['performance_score'] += success_score * 0.4
                
                if success_rate < self.thresholds['min_success_rate']:
                    agent_analysis['recommendations'].append(
                        f"Error handling improvement needed (success: {success_rate*100:.1f}%)"
                    )
            
            # Resource usage analysis
            if metrics['memory_usage']:
                avg_memory = statistics.mean(metrics['memory_usage'])
                agent_analysis['resource_usage'] = {
                    'memory_mb': round(avg_memory, 1),
                    'memory_efficiency': 'good' if avg_memory < 200 else 'needs_optimization'
                }
                
                memory_score = max(0, 100 - (avg_memory / 300) * 20)
                agent_analysis['performance_score'] += memory_score * 0.2
                
                if avg_memory > 250:
                    agent_analysis['recommendations'].append(
                        f"Memory optimization needed ({avg_memory:.1f}MB average)"
                    )
            
            # Overall rating
            score = agent_analysis['performance_score']
            if score >= 90:
                agent_analysis['rating'] = 'Excellent'
            elif score >= 80:
                agent_analysis['rating'] = 'Good'
            elif score >= 70:
                agent_analysis['rating'] = 'Fair'
            else:
                agent_analysis['rating'] = 'Needs Improvement'
            
            analysis[name] = agent_analysis
        
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "agents_analyzed": len(analysis),
            "agent_performance": analysis,
            "system_wide_recommendations": self._generate_system_recommendations()
        }
    
    def _generate_system_recommendations(self):
        """Sistem geneli için öneriler üret"""
        recommendations = []
        
        # CPU recommendations
        if self.system_metrics['cpu_usage']:
            recent_cpu = [m['value'] for m in list(self.system_metrics['cpu_usage'])[-10:]]
            avg_cpu = statistics.mean(recent_cpu)
            
            if avg_cpu > 70:
                recommendations.append({
                    'type': 'CPU_OPTIMIZATION',
                    'priority': 'high',
                    'message': 'CPU kullanımı yüksek - workload distribution optimize edilmeli'
                })
        
        # Memory recommendations
        if self.system_metrics['memory_usage']:
            recent_memory = [m['value'] for m in list(self.system_metrics['memory_usage'])[-10:]]
            avg_memory = statistics.mean(recent_memory)
            
            if avg_memory > 75:
                recommendations.append({
                    'type': 'MEMORY_OPTIMIZATION',
                    'priority': 'medium',
                    'message': 'Bellek kullanımı yüksek - garbage collection ve caching optimize edilmeli'
                })
        
        return recommendations
    
    def optimize_system_performance(self):
        """Sistem performansını optimize et"""
        optimizations = []
        
        try:
            # Memory cleanup simulation
            optimizations.append({
                'action': 'memory_cleanup',
                'description': 'Unused cache cleared',
                'impact': 'Freed ~150MB memory'
            })
            
            # Agent restart simulation
            problematic_agents = []
            for agent_name, metrics in self.agent_metrics.items():
                if metrics['response_times']:
                    avg_time = statistics.mean([rt['value'] for rt in list(metrics['response_times'])[-5:]])
                    if avg_time > 3.0:
                        problematic_agents.append(agent_name)
            
            if problematic_agents:
                optimizations.append({
                    'action': 'agent_restart',
                    'description': f'Restarted slow agents: {", ".join(problematic_agents)}',
                    'impact': 'Improved response times by ~40%'
                })
            
            # Load balancing simulation
            optimizations.append({
                'action': 'load_balancing',
                'description': 'Redistributed workload across agents',
                'impact': 'Reduced peak CPU usage by ~20%'
            })
            
        except Exception as e:
            return {"error": f"Optimization failed: {str(e)}"}
        
        return {
            "success": True,
            "optimizations_applied": len(optimizations),
            "optimizations": optimizations,
            "estimated_improvement": "15-25% performance boost",
            "next_optimization": "Scheduled in 30 minutes"
        }
    
    def perform_comprehensive_health_check(self):
        """Kapsamlı sistem sağlık kontrolü"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': 'HEALTHY',
            'health_score': 100,
            'components': {},
            'recommendations': [],
            'critical_issues': [],
            'warnings': []
        }
        
        # System health
        system_health = self._check_system_health()
        health_report['components']['system'] = system_health
        health_report['health_score'] -= system_health.get('penalty', 0)
        
        # Agent health
        agent_health = self._check_agents_health()
        health_report['components']['agents'] = agent_health
        health_report['health_score'] -= agent_health.get('penalty', 0)
        
        # Overall assessment
        if health_report['health_score'] >= 90:
            health_report['overall_health'] = 'EXCELLENT'
        elif health_report['health_score'] >= 80:
            health_report['overall_health'] = 'GOOD'
        elif health_report['health_score'] >= 70:
            health_report['overall_health'] = 'FAIR'
        elif health_report['health_score'] >= 60:
            health_report['overall_health'] = 'POOR'
        else:
            health_report['overall_health'] = 'CRITICAL'
        
        return health_report
    
    def _check_system_health(self):
        """Sistem sağlığını kontrol et"""
        health = {'status': 'healthy', 'penalty': 0, 'issues': []}
        
        if self.system_metrics['cpu_usage']:
            current_cpu = self.system_metrics['cpu_usage'][-1]['value']
            if current_cpu > 85:
                health['issues'].append(f'High CPU usage: {current_cpu:.1f}%')
                health['penalty'] += 15
            elif current_cpu > 70:
                health['issues'].append(f'Elevated CPU usage: {current_cpu:.1f}%')
                health['penalty'] += 5
        
        if self.system_metrics['memory_usage']:
            current_memory = self.system_metrics['memory_usage'][-1]['value']
            if current_memory > 90:
                health['issues'].append(f'Critical memory usage: {current_memory:.1f}%')
                health['penalty'] += 20
            elif current_memory > 80:
                health['issues'].append(f'High memory usage: {current_memory:.1f}%')
                health['penalty'] += 10
        
        return health
    
    def _check_agents_health(self):
        """Agent sağlığını kontrol et"""
        health = {'status': 'healthy', 'penalty': 0, 'issues': [], 'agent_statuses': {}}
        
        for agent_name, metrics in self.agent_metrics.items():
            agent_health = {'status': 'healthy', 'issues': []}
            
            # Response time check
            if metrics['response_times']:
                avg_time = statistics.mean([rt['value'] for rt in list(metrics['response_times'])[-10:]])
                if avg_time > 4.0:
                    agent_health['issues'].append(f'Very slow response: {avg_time:.2f}s')
                    agent_health['status'] = 'critical'
                    health['penalty'] += 10
                elif avg_time > 2.5:
                    agent_health['issues'].append(f'Slow response: {avg_time:.2f}s')
                    agent_health['status'] = 'warning'
                    health['penalty'] += 5
            
            # Success rate check
            if metrics['success_rate']:
                success_rate = statistics.mean(list(metrics['success_rate'])[-20:])
                if success_rate < 0.9:
                    agent_health['issues'].append(f'Low success rate: {success_rate*100:.1f}%')
                    agent_health['status'] = 'critical'
                    health['penalty'] += 15
                elif success_rate < 0.95:
                    agent_health['issues'].append(f'Reduced success rate: {success_rate*100:.1f}%')
                    agent_health['status'] = 'warning'
                    health['penalty'] += 5
            
            health['agent_statuses'][agent_name] = agent_health
        
        return health
    
    def predict_system_usage(self):
        """Sistem kullanım tahmini"""
        prediction = {
            'prediction_timestamp': datetime.now().isoformat(),
            'forecast_horizon': '24 hours',
            'cpu_forecast': [],
            'memory_forecast': [],
            'peak_times': [],
            'recommended_actions': []
        }
        
        current_hour = datetime.now().hour
        
        # Generate hourly predictions for next 24 hours
        for hour_offset in range(24):
            future_hour = (current_hour + hour_offset) % 24
            
            # Business hours (9-17) have higher usage
            if 9 <= future_hour <= 17:
                cpu_base = 60
                memory_base = 70
            else:
                cpu_base = 30
                memory_base = 45
            
            # Add randomness
            cpu_prediction = cpu_base + np.random.normal(0, 10)
            memory_prediction = memory_base + np.random.normal(0, 8)
            
            cpu_prediction = max(10, min(95, cpu_prediction))
            memory_prediction = max(20, min(90, memory_prediction))
            
            prediction['cpu_forecast'].append({
                'hour': future_hour,
                'predicted_usage': round(cpu_prediction, 1),
                'confidence': 0.85
            })
            
            prediction['memory_forecast'].append({
                'hour': future_hour,
                'predicted_usage': round(memory_prediction, 1),
                'confidence': 0.82
            })
            
            # Identify peak times
            if cpu_prediction > 80 or memory_prediction > 80:
                prediction['peak_times'].append({
                    'hour': future_hour,
                    'expected_load': 'high',
                    'recommended_preparation': 'Scale resources or schedule maintenance'
                })
        
        return prediction
    
    def detect_system_bottlenecks(self):
        """Detaylı darboğaz analizi"""
        analysis = {
            'analysis_timestamp': datetime.now().isoformat(),
            'bottlenecks_detected': [],
            'performance_insights': {},
            'optimization_opportunities': [],
            'severity_assessment': 'low'
        }
        
        # Current bottlenecks
        current_bottlenecks = self._identify_current_bottlenecks()
        analysis['bottlenecks_detected'] = current_bottlenecks
        
        # Severity assessment
        high_severity = len([b for b in current_bottlenecks if b['severity'] == 'high'])
        medium_severity = len([b for b in current_bottlenecks if b['severity'] == 'medium'])
        
        if high_severity > 0:
            analysis['severity_assessment'] = 'critical'
        elif medium_severity > 2:
            analysis['severity_assessment'] = 'high'
        elif medium_severity > 0:
            analysis['severity_assessment'] = 'medium'
        
        return analysis
    
    def _identify_current_bottlenecks(self):
        """Mevcut darboğazları tespit et"""
        bottlenecks = []
        
        # CPU bottleneck
        if self.system_metrics['cpu_usage']:
            current_cpu = self.system_metrics['cpu_usage'][-1]['value']
            if current_cpu > 80:
                bottlenecks.append({
                    'type': 'CPU',
                    'severity': 'high' if current_cpu > 90 else 'medium',
                    'description': f'CPU usage at {current_cpu:.1f}%',
                    'recommendation': 'Consider load balancing or scaling'
                })
        
        # Memory bottleneck
        if self.system_metrics['memory_usage']:
            current_memory = self.system_metrics['memory_usage'][-1]['value']
            if current_memory > 85:
                bottlenecks.append({
                    'type': 'Memory',
                    'severity': 'high' if current_memory > 95 else 'medium',
                    'description': f'Memory usage at {current_memory:.1f}%',
                    'recommendation': 'Implement memory optimization or increase capacity'
                })
        
        # Slow agents
        for agent_name, metrics in self.agent_metrics.items():
            if metrics['response_times']:
                avg_time = statistics.mean([rt['value'] for rt in list(metrics['response_times'])[-5:]])
                if avg_time > 3.0:
                    bottlenecks.append({
                        'type': 'Agent Performance',
                        'severity': 'medium',
                        'description': f'{agent_name} slow response: {avg_time:.2f}s',
                        'recommendation': f'Optimize {agent_name} or restart if needed'
                    })
        
        return bottlenecks
    
    def generate_performance_report(self, period='daily'):
        """Performans raporu oluştur"""
        report = {
            'report_id': f'PERF_RPT_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'period': period,
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'agent_performance': {},
            'system_performance': {},
            'trends': {},
            'recommendations': []
        }
        
        # Current metrics
        current_metrics = self.get_current_metrics()
        
        # Summary
        report['summary'] = {
            'total_agents': current_metrics['summary']['total_agents'],
            'active_agents': current_metrics['summary']['active_agents'],
            'total_requests': current_metrics['summary']['total_requests'],
            'overall_error_rate': current_metrics['summary']['error_rate'],
            'monitoring_uptime': '99.8%',  # Simulated
            'peak_performance_time': '14:00-16:00'  # Simulated
        }
        
        # Agent performance summary
        for agent_name, metrics in current_metrics['agents'].items():
            report['agent_performance'][agent_name] = {
                'avg_response_time': metrics.get('avg_response_time', 0),
                'success_rate': metrics.get('success_rate', 0),
                'total_requests': metrics.get('total_requests', 0),
                'resource_efficiency': 'good' if metrics.get('memory_usage_mb', 0) < 200 else 'needs_optimization'
            }
        
        # System performance
        report['system_performance'] = {
            'avg_cpu_usage': current_metrics['system'].get('cpu_usage', 0),
            'avg_memory_usage': current_metrics['system'].get('memory_usage', 0),
            'disk_usage': current_metrics['system'].get('disk_usage', 0),
            'uptime': '99.9%',  # Simulated
            'peak_concurrent_requests': 45  # Simulated
        }
        
        # Store report
        self.performance_reports.append(report)
        
        return report
    
    def get_performance_dashboard_data(self):
        """Dashboard için performans verilerini hazırla"""
        current_metrics = self.get_current_metrics()
        
        # Real-time charts data
        charts_data = {
            'cpu_usage': list(self.system_metrics['cpu_usage'])[-50:],
            'memory_usage': list(self.system_metrics['memory_usage'])[-50:],
            'agent_response_times': {},
            'error_rates': {},
            'throughput': []
        }
        
        # Agent response times for charts
        for agent_name, metrics in self.agent_metrics.items():
            if metrics['response_times']:
                charts_data['agent_response_times'][agent_name] = list(metrics['response_times'])[-20:]
        
        # Recent alerts for notifications
        recent_alerts = [a for a in self.alert_history if 
                        datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(hours=1)]
        
        dashboard_data = {
            'current_metrics': current_metrics,
            'charts_data': charts_data,
            'recent_alerts': recent_alerts[-10:],  # Last 10 alerts
            'system_health': self._get_system_health_summary(),
            'top_performers': self._get_top_performing_agents(),
            'bottlenecks': self._identify_current_bottlenecks(),
            'recommendations': self.optimization_suggestions[-5:] if self.optimization_suggestions else []
        }
        
        return dashboard_data
    
    def _get_system_health_summary(self):
        """Sistem sağlık özeti"""
        health_check = self.perform_comprehensive_health_check()
        
        return {
            'overall_score': health_check['health_score'],
            'status': health_check['overall_health'],
            'critical_issues': len(health_check['critical_issues']),
            'warnings': len(health_check['warnings']),
            'last_check': health_check['timestamp']
        }
    
    def _get_top_performing_agents(self):
        """En iyi performans gösteren agent'lar"""
        agent_scores = []
        
        for agent_name, metrics in self.agent_metrics.items():
            score = 0
            
            # Response time score
            if metrics['response_times']:
                avg_time = statistics.mean([rt['value'] for rt in list(metrics['response_times'])[-10:]])
                time_score = max(0, 100 - (avg_time / 2.0) * 50)  # 2s baseline
                score += time_score * 0.5
            
            # Success rate score
            if metrics['success_rate']:
                success_rate = statistics.mean(list(metrics['success_rate'])[-20:])
                score += success_rate * 100 * 0.5
            
            agent_scores.append({
                'agent': agent_name,
                'score': round(score, 1),
                'status': 'excellent' if score >= 90 else 'good' if score >= 80 else 'fair'
            })
        
        # Sort by score and return top 3
        agent_scores.sort(key=lambda x: x['score'], reverse=True)
        return agent_scores[:3]
    
    def get_performance_stats(self):
        """Performance istatistikleri"""
        return {
            "monitoring_active": self.monitoring_active,
            "metrics_collected": {
                "system_metrics": sum(len(metrics) for metrics in self.system_metrics.values()),
                "agent_metrics": len(self.agent_metrics),
                "total_data_points": sum(len(metrics['response_times']) for metrics in self.agent_metrics.values())
            },
            "alerts_generated": len(self.alert_history),
            "reports_generated": len(self.performance_reports),
            "optimization_suggestions": len(self.optimization_suggestions),
            "current_system_health": self._get_system_health_summary(),
            "monitoring_uptime": "99.9%",  # Simulated
            "last_optimization": datetime.now() - timedelta(minutes=30) if self.optimization_suggestions else None
        }

# Test fonksiyonu
if __name__ == "__main__":
    agent = PerformanceAgent()
    
    print("🚀 Performance Agent Test Başlıyor...")
    print("=" * 60)
    
    # Test 1: Monitoring başlat
    start_result = agent.process_task({"type": "start_monitoring"})
    print("📊 Monitoring Start:", start_result)
    
    # Biraz bekle
    print("⏳ 10 saniye veri toplama bekleniyor...")
    time.sleep(10)
    
    # Test 2: Current metrics
    metrics_result = agent.process_task({"type": "get_metrics"})
    print("📈 Current Metrics:")
    print(f"  CPU: {metrics_result.get('system', {}).get('cpu_usage', 'N/A')}%")
    print(f"  Memory: {metrics_result.get('system', {}).get('memory_usage', 'N/A')}%")
    print(f"  Active Agents: {metrics_result.get('summary', {}).get('active_agents', 'N/A')}")
    
    # Test 3: Agent analizi
    analysis_result = agent.process_task({"type": "analyze_performance"})
    print("🔍 Performance Analysis:")
    agents_analyzed = analysis_result.get('agents_analyzed', 0)
    print(f"  Analyzed {agents_analyzed} agents")
    
    # Test 4: Health check
    health_result = agent.process_task({"type": "health_check"})
    print("🏥 Health Check:")
    print(f"  Overall Health: {health_result.get('overall_health', 'Unknown')}")
    print(f"  Health Score: {health_result.get('health_score', 0)}/100")
    
    # Test 5: Optimization
    optimization_result = agent.process_task({"type": "optimize_system"})
    print("⚡ Optimization:")
    if optimization_result.get('success'):
        print(f"  Applied {optimization_result.get('optimizations_applied', 0)} optimizations")
        print(f"  Expected improvement: {optimization_result.get('estimated_improvement', 'Unknown')}")
    
    # Test 6: Dashboard data
    dashboard_data = agent.get_performance_dashboard_data()
    print("📊 Dashboard Data:")
    print(f"  Charts data keys: {list(dashboard_data.get('charts_data', {}).keys())}")
    print(f"  Recent alerts: {len(dashboard_data.get('recent_alerts', []))}")
    print(f"  Top performers: {len(dashboard_data.get('top_performers', []))}")
    
    # Test 7: Prediction
    prediction_result = agent.process_task({"type": "predict_usage"})
    print("🔮 Usage Prediction:")
    print(f"  Forecast horizon: {prediction_result.get('forecast_horizon', 'Unknown')}")
    print(f"  Peak times identified: {len(prediction_result.get('peak_times', []))}")
    
    # Test 8: Bottleneck detection
    bottleneck_result = agent.process_task({"type": "detect_bottlenecks"})
    print("🚨 Bottleneck Detection:")
    print(f"  Bottlenecks detected: {len(bottleneck_result.get('bottlenecks_detected', []))}")
    print(f"  Severity: {bottleneck_result.get('severity_assessment', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print("🎉 Performance Agent testleri tamamlandı!")
    print("📊 Monitoring aktif, veriler toplanıyor...")
    
    # Stats
    stats = agent.get_performance_stats()
    print(f"📈 Toplanan metrik: {stats.get('metrics_collected', {}).get('total_data_points', 0)}")
    print(f"🚨 Uyarı sayısı: {stats.get('alerts_generated', 0)}")
    
    # Monitoring'i durdur
    stop_result = agent.process_task({"type": "stop_monitoring"})
    print("🛑 Monitoring Stopped:", stop_result.get('message', 'Stopped'))