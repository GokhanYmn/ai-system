import asyncio
from datetime import datetime
import time
from base_agent import BaseAgent

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CoordinatorAgent",
            agent_type="orchestrator",
            capabilities=["workflow_management", "agent_coordination", "decision_synthesis", "system_monitoring"]
        )
        self.registered_agents = {}
        self.workflow_history = []
        self.system_performance = {}
        
    def register_agent(self, agent_name, agent_instance):
        """Agent'ı sisteme kaydet"""
        self.registered_agents[agent_name] = {
            'instance': agent_instance,
            'status': 'registered',
            'last_used': None,
            'task_count': 0,
            'success_rate': 1.0
        }
        
    def can_handle_task(self, task):
        orchestration_tasks = ['run_full_analysis', 'coordinate_agents', 'generate_report', 'system_health_check']
        return task.get('type') in orchestration_tasks
    
    def process_task(self, task):
        self.status = "coordinating"
        start_time = time.time()
        
        try:
            task_type = task.get('type')
            
            if task_type == 'run_full_analysis':
                result = self.run_comprehensive_analysis(task.get('symbol', 'THYAO'))
            elif task_type == 'coordinate_agents':
                result = self.coordinate_multi_agent_workflow(task.get('workflow_data'))
            elif task_type == 'generate_report':
                result = self.generate_comprehensive_report(task.get('analysis_data'))
            elif task_type == 'system_health_check':
                result = self.perform_system_health_check()
            else:
                result = {"error": "Desteklenmeyen görev tipi"}
            
            duration = time.time() - start_time
            self.add_task_to_history(task, result, duration)
            
        except Exception as e:
            result = {"error": str(e)}
            duration = time.time() - start_time
        
        self.status = "idle"
        return result
    
    def run_comprehensive_analysis(self, symbol):
        """Tüm agent'ları koordine ederek kapsamlı analiz yap"""
        workflow_id = f"ANALYSIS_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Workflow steps
        workflow_results = {
            'workflow_id': workflow_id,
            'symbol': symbol,
            'start_time': datetime.now(),
            'steps': {},
            'final_recommendation': None
        }
        
        try:
            # Step 1: News Analysis
            if 'news_agent' in self.registered_agents:
                news_task = {'type': 'get_kap_news', 'limit': 5}
                news_result = self.execute_agent_task('news_agent', news_task)
                workflow_results['steps']['news_analysis'] = news_result
            
            # Step 2: Financial Analysis
            if 'financial_agent' in self.registered_agents:
                financial_task = {'type': 'calculate_ratios', 'company_code': symbol}
                financial_result = self.execute_agent_task('financial_agent', financial_task)
                workflow_results['steps']['financial_analysis'] = financial_result
            
            # Step 3: Technical Analysis
            if 'technical_agent' in self.registered_agents:
                technical_task = {'type': 'generate_signals', 'price_data': None}
                technical_result = self.execute_agent_task('technical_agent', technical_task)
                workflow_results['steps']['technical_analysis'] = technical_result
            
            # Step 4: Data Integration
            if 'data_agent' in self.registered_agents:
                agent_results = {
                    'news_agent': workflow_results['steps'].get('news_analysis', {}),
                    'financial_agent': workflow_results['steps'].get('financial_analysis', {}),
                    'technical_agent': workflow_results['steps'].get('technical_analysis', {})
                }
                data_task = {'type': 'combine_agent_data', 'agent_results': agent_results}
                data_result = self.execute_agent_task('data_agent', data_task)
                workflow_results['steps']['data_integration'] = data_result
            
            # Step 5: Decision Making
            if 'decision_agent' in self.registered_agents:
                analysis_data = workflow_results['steps'].get('data_integration', {}).get('combined_analysis', {})
                decision_task = {'type': 'make_investment_decision', 'analysis_data': analysis_data}
                decision_result = self.execute_agent_task('decision_agent', decision_task)
                workflow_results['steps']['decision_making'] = decision_result
            
            # Step 6: Trading Strategy
            if 'trading_agent' in self.registered_agents:
                decision_data = workflow_results['steps'].get('decision_making', {})
                trading_task = {'type': 'calculate_trade_size', 'decision_data': decision_data}
                trading_result = self.execute_agent_task('trading_agent', trading_task)
                workflow_results['steps']['trading_strategy'] = trading_result
            
            # Generate Final Recommendation
            workflow_results['final_recommendation'] = self.synthesize_final_recommendation(workflow_results['steps'])
            workflow_results['end_time'] = datetime.now()
            workflow_results['total_duration'] = (workflow_results['end_time'] - workflow_results['start_time']).total_seconds()
            
            # Store workflow
            self.workflow_history.append(workflow_results)
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "analysis_complete": True,
                "symbol": symbol,
                "recommendation": workflow_results['final_recommendation'],
                "execution_summary": self.create_execution_summary(workflow_results),
                "agent_contributions": self.analyze_agent_contributions(workflow_results['steps'])
            }
            
        except Exception as e:
            return {
                "success": False,
                "workflow_id": workflow_id,
                "error": str(e),
                "partial_results": workflow_results.get('steps', {})
            }
    
    def execute_agent_task(self, agent_name, task):
        """Belirli bir agent'a görev ver"""
        if agent_name not in self.registered_agents:
            return {"error": f"Agent {agent_name} kayıtlı değil"}
        
        agent_info = self.registered_agents[agent_name]
        agent_instance = agent_info['instance']
        
        try:
            # Task execution
            result = agent_instance.process_task(task)
            
            # Update agent stats
            agent_info['last_used'] = datetime.now()
            agent_info['task_count'] += 1
            
            if not result.get('error'):
                agent_info['success_rate'] = (agent_info['success_rate'] * (agent_info['task_count'] - 1) + 1) / agent_info['task_count']
            else:
                agent_info['success_rate'] = (agent_info['success_rate'] * (agent_info['task_count'] - 1)) / agent_info['task_count']
            
            return result
            
        except Exception as e:
            agent_info['success_rate'] = (agent_info['success_rate'] * (agent_info['task_count'] - 1)) / agent_info['task_count']
            return {"error": f"Agent execution failed: {str(e)}"}
    
    def synthesize_final_recommendation(self, workflow_steps):
        """Tüm analiz sonuçlarını birleştirip final öneri oluştur"""
        recommendation = {
            'overall_signal': 'HOLD',
            'confidence': 50,
            'reasoning': [],
            'risk_level': 'MEDIUM',
            'suggested_allocation': 0,
            'time_horizon': 'MEDIUM_TERM'
        }
        
        # Data integration'dan ana sonucu al
        data_integration = workflow_steps.get('data_integration', {})
        combined_analysis = data_integration.get('combined_analysis', {})
        
        if combined_analysis:
            recommendation['overall_signal'] = combined_analysis.get('recommendation', 'HOLD')
            recommendation['confidence'] = combined_analysis.get('final_score', 50)
        
        # Decision making'den detayları al
        decision_making = workflow_steps.get('decision_making', {})
        investment_decision = decision_making.get('investment_decision', {})
        
        if investment_decision:
            recommendation['suggested_allocation'] = investment_decision.get('position_size_pct', 0)
            recommendation['reasoning'].append(investment_decision.get('rationale', ''))
        
        # Risk assessment
        risk_management = decision_making.get('risk_management', {})
        if risk_management:
            recommendation['stop_loss'] = risk_management.get('stop_loss')
            recommendation['take_profit'] = risk_management.get('take_profit')
        
        # Trading strategy
        trading_strategy = workflow_steps.get('trading_strategy', {})
        optimal_size = trading_strategy.get('optimal_trade_size', {})
        if optimal_size:
            recommendation['optimal_trade_amount'] = optimal_size.get('amount_tl')
        
        return recommendation
    
    def create_execution_summary(self, workflow_results):
        """İşlem özetini oluştur"""
        total_agents_used = len([step for step in workflow_results['steps'].values() if not step.get('error')])
        
        return {
            'workflow_duration_seconds': workflow_results.get('total_duration', 0),
            'agents_utilized': total_agents_used,
            'steps_completed': len(workflow_results['steps']),
            'success_rate': total_agents_used / len(workflow_results['steps']) if workflow_results['steps'] else 0,
            'completion_status': 'COMPLETE' if total_agents_used > 3 else 'PARTIAL'
        }
    
    def analyze_agent_contributions(self, workflow_steps):
        """Agent katkılarını analiz et"""
        contributions = {}
        
        for step_name, result in workflow_steps.items():
            agent_name = step_name.replace('_analysis', '').replace('_', '_agent')
            
            if not result.get('error'):
                contributions[agent_name] = {
                    'status': 'success',
                    'contribution_quality': 'high' if result else 'medium',
                    'processing_time': 'normal'
                }
            else:
                contributions[agent_name] = {
                    'status': 'failed',
                    'error': result.get('error'),
                    'contribution_quality': 'none'
                }
        
        return contributions
    
    def perform_system_health_check(self):
        """Sistem sağlık kontrolü"""
        health_report = {
            'overall_health': 'HEALTHY',
            'timestamp': datetime.now(),
            'agents_status': {},
            'system_metrics': {},
            'recommendations': []
        }
        
        # Agent health check
        for agent_name, agent_info in self.registered_agents.items():
            agent_health = {
                'status': 'active' if agent_info['last_used'] else 'inactive',
                'success_rate': round(agent_info['success_rate'] * 100, 1),
                'tasks_completed': agent_info['task_count'],
                'last_used': agent_info['last_used'].isoformat() if agent_info['last_used'] else 'never'
            }
            
            if agent_info['success_rate'] < 0.8:
                agent_health['warning'] = 'Low success rate'
                health_report['recommendations'].append(f"Check {agent_name} performance")
            
            health_report['agents_status'][agent_name] = agent_health
        
        # System metrics
        health_report['system_metrics'] = {
            'total_agents': len(self.registered_agents),
            'active_agents': len([a for a in self.registered_agents.values() if a['last_used']]),
            'total_workflows': len(self.workflow_history),
            'avg_workflow_duration': self.calculate_avg_workflow_duration()
        }
        
        # Overall health assessment
        active_rate = health_report['system_metrics']['active_agents'] / health_report['system_metrics']['total_agents']
        if active_rate < 0.5:
            health_report['overall_health'] = 'WARNING'
            health_report['recommendations'].append("Low agent utilization")
        
        return health_report
    
    def calculate_avg_workflow_duration(self):
        """Ortalama workflow süresini hesapla"""
        if not self.workflow_history:
            return 0
        
        durations = [w.get('total_duration', 0) for w in self.workflow_history]
        return round(sum(durations) / len(durations), 2)
    
    def get_registered_agents(self):
        """Kayıtlı agent'ları listele"""
        return {
            name: {
                'type': info['instance'].agent_type if hasattr(info['instance'], 'agent_type') else 'unknown',
                'capabilities': info['instance'].capabilities if hasattr(info['instance'], 'capabilities') else [],
                'status': info['status'],
                'task_count': info['task_count'],
                'success_rate': round(info['success_rate'] * 100, 1)
            }
            for name, info in self.registered_agents.items()
        }

# Test
if __name__ == "__main__":
    coordinator = CoordinatorAgent()
    
    # Mock agents registration (test için)
    class MockAgent:
        def __init__(self, name, agent_type):
            self.name = name
            self.agent_type = agent_type
            self.capabilities = ['mock_capability']
            
        def process_task(self, task):
            return {"success": True, "mock_result": f"Processed by {self.name}"}
    
    # Register mock agents
    coordinator.register_agent('news_agent', MockAgent('NewsAgent', 'news_analyzer'))
    coordinator.register_agent('financial_agent', MockAgent('FinancialAgent', 'financial_analyzer'))
    coordinator.register_agent('technical_agent', MockAgent('TechnicalAgent', 'technical_analyzer'))
    
    # Test coordination
    task = {"type": "run_full_analysis", "symbol": "THYAO"}
    result = coordinator.process_task(task)
    print("Koordinasyon Sonucu:", result)
    
    # Health check
    health = coordinator.perform_system_health_check()
    print("Sistem Sağlığı:", health)
    
    print("Agent Durumu:", coordinator.get_status())