import React, { useState, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Statistic,
  Button,
  Progress,
  Table,
  Alert,
  Tabs,
  Typography,
  Space,
  Tag,
  List,
  Modal,
  Spin,
  message
} from 'antd';
import {
  DashboardOutlined,
  ThunderboltOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ReloadOutlined,
  RocketOutlined,
  WarningOutlined,
  TrophyOutlined,
  FireOutlined
} from '@ant-design/icons';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { apiService } from '../services/api';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const PerformanceDashboard = () => {
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [monitoringActive, setMonitoringActive] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(null);

  useEffect(() => {
    loadDashboardData();
    
    if (autoRefresh) {
      const interval = setInterval(loadDashboardData, 5000); // 5 saniye
      setRefreshInterval(interval);
      return () => clearInterval(interval);
    }
    
    return () => {
      if (refreshInterval) clearInterval(refreshInterval);
    };
  }, [autoRefresh]);

  const loadDashboardData = async () => {
    try {
      const response = await apiService.getPerformanceDashboard();
      setDashboardData(response.data);
      setMonitoringActive(response.data.current_metrics?.summary?.monitoring_active || false);
    } catch (error) {
      console.error('Dashboard data yüklenemedi:', error);
      // Mock data for demo
      setDashboardData({
        current_metrics: {
          system: { cpu_usage: 45.2, memory_usage: 67.8, disk_usage: 23.4 },
          agents: {
            news_agent: { avg_response_time: 1.2, success_rate: 96.5, status: 'active' },
            financial_agent: { avg_response_time: 0.8, success_rate: 98.2, status: 'active' },
            technical_agent: { avg_response_time: 1.5, success_rate: 94.1, status: 'active' },
            data_agent: { avg_response_time: 2.1, success_rate: 97.3, status: 'active' }
          },
          summary: { active_agents: 10, total_requests: 1245, error_rate: 2.1 }
        },
        charts_data: {
          cpu_usage: generateMockChartData('cpu', 20),
          memory_usage: generateMockChartData('memory', 20),
          agent_response_times: {
            news_agent: generateMockChartData('response', 10),
            financial_agent: generateMockChartData('response', 10)
          }
        },
        system_health: { overall_score: 87, status: 'GOOD', warnings: 1, critical_issues: 0 },
        top_performers: [
          { agent: 'financial_agent', score: 98.2, status: 'excellent' },
          { agent: 'data_agent', score: 95.7, status: 'excellent' },
          { agent: 'news_agent', score: 92.1, status: 'good' }
        ],
        bottlenecks: [
          { type: 'Agent Performance', severity: 'medium', description: 'technical_agent slow response: 2.1s' }
        ],
        recent_alerts: [
          { type: 'SLOW_RESPONSE', message: 'technical_agent yavaş: 2.1s', severity: 'warning', timestamp: new Date().toISOString() }
        ]
      });
    }
  };

  const generateMockChartData = (type, count) => {
    const data = [];
    const now = new Date();
    
    for (let i = count; i >= 0; i--) {
      const time = new Date(now.getTime() - i * 30000); // 30 saniye aralık
      let value;
      
      switch (type) {
        case 'cpu':
          value = 30 + Math.random() * 40 + Math.sin(i / 5) * 15;
          break;
        case 'memory':
          value = 50 + Math.random() * 30 + Math.sin(i / 3) * 10;
          break;
        case 'response':
          value = 0.5 + Math.random() * 2 + Math.sin(i / 4) * 0.5;
          break;
        default:
          value = Math.random() * 100;
      }
      
      data.push({
        timestamp: time.toISOString(),
        time: time.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        value: Math.max(0, value)
      });
    }
    
    return data;
  };

  const startMonitoring = async () => {
    setLoading(true);
    try {
      await apiService.startPerformanceMonitoring();
      message.success('Performance monitoring başlatıldı!');
      setMonitoringActive(true);
      setAutoRefresh(true);
    } catch (error) {
      message.error('Monitoring başlatılamadı: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const stopMonitoring = async () => {
    setLoading(true);
    try {
      await apiService.stopPerformanceMonitoring();
      message.success('Performance monitoring durduruldu!');
      setMonitoringActive(false);
      setAutoRefresh(false);
    } catch (error) {
      message.error('Monitoring durdurulamadı: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const optimizeSystem = async () => {
    setLoading(true);
    try {
      const response = await apiService.optimizeSystemPerformance();
      if (response.data.success) {
        message.success(`✨ Sistem optimize edildi! ${response.data.estimated_improvement}`);
        loadDashboardData();
      }
    } catch (error) {
      message.error('Optimizasyon başarısız: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score) => {
    if (score >= 90) return '#52c41a';
    if (score >= 80) return '#faad14';
    if (score >= 70) return '#ff7a45';
    return '#f5222d';
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#f5222d';
      case 'high': return '#fa8c16';
      case 'medium': return '#faad14';
      case 'low': return '#52c41a';
      default: return '#d9d9d9';
    }
  };

  const renderSystemMetrics = () => (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={8}>
        <Card>
          <Statistic
            title="CPU Kullanımı"
            value={dashboardData?.current_metrics?.system?.cpu_usage || 0}
            suffix="%"
            precision={1}
            valueStyle={{ color: getHealthColor(100 - (dashboardData?.current_metrics?.system?.cpu_usage || 0)) }}
            prefix={<ThunderboltOutlined />}
          />
          <Progress 
            percent={dashboardData?.current_metrics?.system?.cpu_usage || 0} 
            size="small" 
            strokeColor={getHealthColor(100 - (dashboardData?.current_metrics?.system?.cpu_usage || 0))}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={8}>
        <Card>
          <Statistic
            title="Bellek Kullanımı"
            value={dashboardData?.current_metrics?.system?.memory_usage || 0}
            suffix="%"
            precision={1}
            valueStyle={{ color: getHealthColor(100 - (dashboardData?.current_metrics?.system?.memory_usage || 0)) }}
            prefix={<DashboardOutlined />}
          />
          <Progress 
            percent={dashboardData?.current_metrics?.system?.memory_usage || 0} 
            size="small"
            strokeColor={getHealthColor(100 - (dashboardData?.current_metrics?.system?.memory_usage || 0))}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={8}>
        <Card>
          <Statistic
            title="Sistem Sağlığı"
            value={dashboardData?.system_health?.overall_score || 0}
            suffix="/100"
            valueStyle={{ color: getHealthColor(dashboardData?.system_health?.overall_score || 0) }}
            prefix={<CheckCircleOutlined />}
          />
          <div style={{ marginTop: 8 }}>
            <Tag color={getHealthColor(dashboardData?.system_health?.overall_score || 0)}>
              {dashboardData?.system_health?.status || 'UNKNOWN'}
            </Tag>
          </div>
        </Card>
      </Col>
    </Row>
  );

  const renderRealTimeCharts = () => (
    <Row gutter={[16, 16]}>
      <Col xs={24} lg={12}>
        <Card title="📊 CPU Kullanımı (Real-time)" size="small">
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={dashboardData?.charts_data?.cpu_usage || []}>
              <defs>
                <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1890ff" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#1890ff" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)}%`, 'CPU']}
                labelStyle={{ color: '#000' }}
              />
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke="#1890ff" 
                fillOpacity={1} 
                fill="url(#colorCpu)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </Col>
      
      <Col xs={24} lg={12}>
        <Card title="💾 Bellek Kullanımı (Real-time)" size="small">
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={dashboardData?.charts_data?.memory_usage || []}>
              <defs>
                <linearGradient id="colorMemory" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#52c41a" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#52c41a" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis domain={[0, 100]} />
              <Tooltip 
                formatter={(value) => [`${value.toFixed(1)}%`, 'Memory']}
                labelStyle={{ color: '#000' }}
              />
              <Area 
                type="monotone" 
                dataKey="value" 
                stroke="#52c41a" 
                fillOpacity={1} 
                fill="url(#colorMemory)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </Col>
    </Row>
  );

  const renderAgentPerformance = () => {
    const agentData = dashboardData?.current_metrics?.agents || {};
    const dataSource = Object.entries(agentData).map(([name, data], index) => ({
      key: index,
      agent: name.replace('_agent', '').toUpperCase(),
      responseTime: data.avg_response_time || 0,
      successRate: data.success_rate || 0,
      status: data.status || 'unknown'
    }));

    const columns = [
      {
        title: '🤖 Agent',
        dataIndex: 'agent',
        key: 'agent',
        render: (text) => <Text strong>{text}</Text>
      },
      {
        title: '⏱️ Response Time',
        dataIndex: 'responseTime',
        key: 'responseTime',
        render: (value) => (
          <span style={{ color: value > 2 ? '#f5222d' : value > 1 ? '#faad14' : '#52c41a' }}>
            {value.toFixed(2)}s
          </span>
        ),
        sorter: (a, b) => a.responseTime - b.responseTime
      },
      {
        title: '✅ Success Rate',
        dataIndex: 'successRate',
        key: 'successRate',
        render: (value) => (
          <div>
            <Progress 
              percent={value} 
              size="small" 
              strokeColor={value > 95 ? '#52c41a' : value > 90 ? '#faad14' : '#f5222d'}
            />
            <Text style={{ fontSize: 12 }}>{value.toFixed(1)}%</Text>
          </div>
        ),
        sorter: (a, b) => a.successRate - b.successRate
      },
      {
        title: '📊 Status',
        dataIndex: 'status',
        key: 'status',
        render: (status) => (
          <Tag color={status === 'active' ? 'green' : status === 'working' ? 'blue' : 'orange'}>
            {status.toUpperCase()}
          </Tag>
        )
      }
    ];

    return (
      <Card title="🤖 Agent Performance Matrix" size="small">
        <Table 
          dataSource={dataSource}
          columns={columns}
          pagination={false}
          size="small"
        />
      </Card>
    );
  };

  const renderTopPerformers = () => (
    <Card title="🏆 Top Performers" size="small">
      <List
        dataSource={dashboardData?.top_performers || []}
        renderItem={(item, index) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <div style={{ 
                  width: 32, 
                  height: 32, 
                  borderRadius: '50%', 
                  backgroundColor: index === 0 ? '#faad14' : index === 1 ? '#d9d9d9' : '#cd7f32',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 'bold'
                }}>
                  {index + 1}
                </div>
              }
              title={<Text strong>{item.agent?.replace('_agent', '').toUpperCase()}</Text>}
              description={
                <div>
                  <Text type="secondary">Score: {item.score}%</Text>
                  <Tag color={item.status === 'excellent' ? 'green' : 'blue'} style={{ marginLeft: 8 }}>
                    {item.status}
                  </Tag>
                </div>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  );

  const renderBottlenecks = () => (
    <Card title="🚨 Bottlenecks & Alerts" size="small">
      {dashboardData?.bottlenecks?.length > 0 ? (
        <List
          dataSource={dashboardData.bottlenecks}
          renderItem={(item) => (
            <List.Item>
              <Alert
                message={item.description}
                type={item.severity === 'high' ? 'error' : 'warning'}
                showIcon
                size="small"
                style={{ width: '100%' }}
                action={
                  <Button size="small" type="text">
                    Fix
                  </Button>
                }
              />
            </List.Item>
          )}
        />
      ) : (
        <Alert
          message="No Bottlenecks Detected"
          description="System is running smoothly! 🚀"
          type="success"
          showIcon
        />
      )}
    </Card>
  );

  const renderControls = () => (
    <Card title="⚡ Performance Controls" size="small">
      <Space direction="vertical" style={{ width: '100%' }}>
        <Row gutter={16}>
          <Col span={12}>
            <Button
              type="primary"
              icon={<RocketOutlined />}
              onClick={monitoringActive ? stopMonitoring : startMonitoring}
              loading={loading}
              danger={monitoringActive}
              block
            >
              {monitoringActive ? 'Stop Monitoring' : 'Start Monitoring'}
            </Button>
          </Col>
          <Col span={12}>
            <Button
              icon={<FireOutlined />}
              onClick={optimizeSystem}
              loading={loading}
              block
            >
              Auto Optimize
            </Button>
          </Col>
        </Row>
        
        <Row gutter={16}>
          <Col span={12}>
            <Button
              icon={<ReloadOutlined />}
              onClick={loadDashboardData}
              loading={loading}
              block
            >
              Refresh Data
            </Button>
          </Col>
          <Col span={12}>
            <Button
              icon={<ClockCircleOutlined />}
              onClick={() => setAutoRefresh(!autoRefresh)}
              type={autoRefresh ? 'primary' : 'default'}
              block
            >
              Auto Refresh: {autoRefresh ? 'ON' : 'OFF'}
            </Button>
          </Col>
        </Row>
      </Space>
    </Card>
  );

  if (!dashboardData) {
    return (
      <div style={{ textAlign: 'center', padding: 50 }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text type="secondary">Performance dashboard yükleniyor...</Text>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Space>
          <DashboardOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Performance Dashboard</Title>
          {monitoringActive && (
            <Tag color="green" icon={<CheckCircleOutlined />}>
              Monitoring Active
            </Tag>
          )}
        </Space>
        
        <Space>
          <Text type="secondary" style={{ fontSize: 12 }}>
            Last Update: {new Date().toLocaleTimeString('tr-TR')}
          </Text>
          {autoRefresh && (
            <Tag color="blue" icon={<ClockCircleOutlined />}>
              Auto Refresh
            </Tag>
          )}
        </Space>
      </div>

      {/* System Metrics Overview */}
      {renderSystemMetrics()}

      {/* Real-time Charts */}
      <div style={{ marginTop: 24 }}>
        {renderRealTimeCharts()}
      </div>

      {/* Agent Performance & Analysis */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} lg={16}>
          {renderAgentPerformance()}
        </Col>
        <Col xs={24} lg={8}>
          {renderControls()}
        </Col>
      </Row>

      {/* Bottlenecks & Top Performers */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          {renderBottlenecks()}
        </Col>
        <Col xs={24} lg={12}>
          {renderTopPerformers()}
        </Col>
      </Row>

      {/* Recent Alerts */}
      {dashboardData?.recent_alerts?.length > 0 && (
        <Card title="📋 Recent Alerts" size="small" style={{ marginTop: 16 }}>
          <List
            dataSource={dashboardData.recent_alerts.slice(0, 5)}
            renderItem={(alert) => (
              <List.Item>
                <Alert
                  message={alert.message}
                  type={alert.severity === 'critical' ? 'error' : 'warning'}
                  showIcon
                  size="small"
                  style={{ width: '100%' }}
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default PerformanceDashboard;