import React, { useState, useEffect } from 'react';
import { Layout, Row, Col, Card, Statistic, Button, Typography, Spin, Alert } from 'antd';
import { 
  RobotOutlined, 
  ThunderboltOutlined, 
  DollarOutlined, 
  BarChartOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import AgentStatus from './AgentStatus';
import AnalysisPanel from './AnalysisPanel';
import Charts from './Charts';
import TradingPanel from './TradingPanel';
import { apiService } from '../services/api';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

const Dashboard = () => {
  const [systemData, setSystemData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [systemHealth, setSystemHealth] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    loadDashboardData();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [statusRes, healthRes, summaryRes] = await Promise.all([
        apiService.getSystemStatus(),
        apiService.getSystemHealth(),
        apiService.getSystemSummary(),
      ]);

      setSystemData({
        status: statusRes.data,
        health: healthRes.data,
        summary: summaryRes.data,
      });
      setSystemHealth(healthRes.data.overall_health);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Dashboard data loading error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (health) => {
    if (health === 'HEALTHY') return '#52c41a';
    if (health === 'WARNING') return '#faad14';
    return '#ff4d4f';
  };

  const getHealthIcon = (health) => {
    if (health === 'HEALTHY') return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
    return <ExclamationCircleOutlined style={{ color: '#faad14' }} />;
  };

  if (loading && !systemData) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <Spin size="large" />
        <Text style={{ marginLeft: 16, color: 'white', fontSize: 18 }}>
          AI Sistemi Yükleniyor...
        </Text>
      </div>
    );
  }

  return (
    <Layout style={{ minHeight: '100vh', background: '#f0f2f5' }}>
      <Header style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <RobotOutlined style={{ fontSize: 32, color: 'white', marginRight: 16 }} />
          <Title level={2} style={{ color: 'white', margin: 0 }}>
            🤖 Multi-Agent Finans AI Sistemi
          </Title>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ textAlign: 'center' }}>
            {getHealthIcon(systemHealth)}
            <Text style={{ color: 'white', marginLeft: 8 }}>
              {systemHealth}
            </Text>
          </div>
          
          <Button 
            type="primary" 
            ghost 
            icon={<ThunderboltOutlined />}
            onClick={loadDashboardData}
            loading={loading}
          >
            Yenile
          </Button>
        </div>
      </Header>

      <Content style={{ padding: '24px', maxWidth: 1400, margin: '0 auto', width: '100%' }}>
        {/* Sistem Metrikleri */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="Aktif Agent'lar"
                value={systemData?.status?.total_agents || 0}
                prefix={<RobotOutlined style={{ color: '#1890ff' }} />}
                suffix="/ 7"
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="Toplam Görev"
                value={systemData?.summary?.system_overview?.total_tasks_completed || 0}
                prefix={<BarChartOutlined style={{ color: '#52c41a' }} />}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="Sistem Durumu"
                value={systemHealth === 'HEALTHY' ? 'Sağlıklı' : 'Uyarı'}
                prefix={getHealthIcon(systemHealth)}
                valueStyle={{ color: getHealthColor(systemHealth) }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={12} lg={6}>
            <Card>
              <Statistic
                title="Son Güncelleme"
                value={lastUpdate.toLocaleTimeString('tr-TR')}
                prefix={<ThunderboltOutlined style={{ color: '#faad14' }} />}
                valueStyle={{ color: '#faad14' }}
              />
            </Card>
          </Col>
        </Row>

        {/* Ana Dashboard Content */}
        <Row gutter={[16, 16]}>
          {/* Sol Panel - Agent Status */}
          <Col xs={24} lg={8}>
            <AgentStatus 
              systemData={systemData} 
              onRefresh={loadDashboardData}
            />
          </Col>

          {/* Orta Panel - Analysis */}
          <Col xs={24} lg={10}>
            <AnalysisPanel onRefresh={loadDashboardData} />
          </Col>

          {/* Sağ Panel - Trading */}
          <Col xs={24} lg={6}>
            <TradingPanel />
          </Col>
        </Row>

        {/* Alt Panel - Charts */}
        <Row style={{ marginTop: 16 }}>
          <Col span={24}>
            <Charts systemData={systemData} />
          </Col>
        </Row>

        {/* Footer */}
        <div style={{ 
          textAlign: 'center', 
          marginTop: 32, 
          padding: 16,
          borderTop: '1px solid #f0f0f0'
        }}>
          <Text type="secondary">
            🚀 AI Multi-Agent Sistemi v4.0 | 
            7 Uzman Agent | 
            Gerçek Zamanlı Analiz | 
            {lastUpdate.toLocaleString('tr-TR')}
          </Text>
        </div>
      </Content>
    </Layout>
  );
};

export default Dashboard;