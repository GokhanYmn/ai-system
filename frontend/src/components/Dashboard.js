import React, { useState, useEffect } from 'react';
import { Layout, Card, Row, Col, Statistic, Button, Select, Alert, Spin, Typography, Tabs, Table } from 'antd';
import { 
  RobotOutlined, 
  DashboardOutlined, 
  ArrowUpOutlined,
  DollarOutlined,
  ReloadOutlined,
  ThunderboltOutlined,
  GlobalOutlined,
  BarChartOutlined,
  BellOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';
import NotificationPanel from './NotificationPanel';
import PerformanceDashboard from './PerformanceDashboard';

const { Header, Content } = Layout;
const { Title, Text } = Typography;
const { Option } = Select;

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [symbol, setSymbol] = useState('THYAO');
  const [error, setError] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);

  // System status'u yükle
  useEffect(() => {
    loadSystemStatus();
  }, []);

  const loadSystemStatus = async () => {
    setLoading(true);
    try {
      const response = await apiService.getSystemStatus();
      setSystemStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Sistem durumu yüklenemedi: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const runAnalysis = async (analysisType = 'comprehensive') => {
    setAnalysisLoading(true);
    setError(null);
    
    try {
      let response;
      if (analysisType === 'quick') {
        response = await apiService.quickAnalysis(symbol);
      } else {
        response = await apiService.comprehensiveAnalysis(symbol);
      }
      
      setAnalysisResult(response.data);
    } catch (err) {
      setError('Analiz başarısız: ' + err.message);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const generateReport = async () => {
    setReportLoading(true);
    setError(null);
    
    try {
      const response = await apiService.generateReport(symbol);
      
      if (response.data.success) {
        const downloadUrl = response.data.report_info.download_url;
        const filename = response.data.report_info.filename;
        
        const link = document.createElement('a');
        link.href = `http://localhost:8003${downloadUrl}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        alert(`📄 ${symbol} analiz raporu başarıyla indirildi!`);
      }
    } catch (err) {
      setError('Rapor oluşturma hatası: ' + err.message);
    } finally {
      setReportLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'ready': 
      case 'operational': 
      case 'active': 
        return '#52c41a';
      case 'working': 
      case 'processing': 
        return '#1890ff';
      case 'idle': 
        return '#faad14';
      default: 
        return '#f5222d';
    }
  };

  const renderSystemOverview = () => (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} md={6}>
        <Card>
          <Statistic
            title="Aktif Agent'lar"
            value={systemStatus?.total_agents || 0}
            prefix={<RobotOutlined style={{ color: '#1890ff' }} />}
            valueStyle={{ color: '#1890ff' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card>
          <Statistic
            title="Sistem Durumu"
            value={systemStatus?.system_status || 'Unknown'}
            prefix={<ThunderboltOutlined style={{ color: getStatusColor(systemStatus?.system_status) }} />}
            valueStyle={{ color: getStatusColor(systemStatus?.system_status) }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card>
          <Statistic
            title="Çalışan Agent'lar"
            value={systemStatus?.active_agents || 0}
            prefix={<GlobalOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card>
          <Statistic
            title="Toplam Workflow"
            value={systemStatus?.total_workflows || 0}
            prefix={<BarChartOutlined style={{ color: '#faad14' }} />}
            valueStyle={{ color: '#faad14' }}
          />
        </Card>
      </Col>
    </Row>
  );

  const renderAgentStatus = () => (
    <Card 
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span><RobotOutlined /> Agent Durumları</span>
          <Button 
            icon={<ReloadOutlined />} 
            onClick={loadSystemStatus}
            loading={loading}
            size="small"
          >
            Yenile
          </Button>
        </div>
      }
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          {systemStatus?.agents && Object.entries(systemStatus.agents).map(([agentName, agentInfo]) => (
            <Col xs={24} sm={12} md={8} lg={6} key={agentName}>
              <Card 
                size="small"
                style={{ 
                  borderLeft: `4px solid ${getStatusColor(agentInfo.status)}`,
                  height: '100%'
                }}
              >
                <div style={{ textAlign: 'center' }}>
                  <Title level={5} style={{ margin: '0 0 8px 0' }}>
                    {agentName.replace('_agent', '').toUpperCase()}
                  </Title>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {agentInfo.type || 'Unknown Type'}
                  </Text>
                  <div style={{ margin: '8px 0' }}>
                    <span 
                      style={{ 
                        padding: '2px 8px', 
                        borderRadius: '12px', 
                        backgroundColor: getStatusColor(agentInfo.status),
                        color: 'white',
                        fontSize: '11px',
                        fontWeight: 'bold'
                      }}
                    >
                      {agentInfo.status?.toUpperCase() || 'UNKNOWN'}
                    </span>
                  </div>
                  <Text style={{ fontSize: '11px' }}>
                    Görevler: {agentInfo.task_count || 0} | 
                    Başarı: %{agentInfo.success_rate || 0}
                  </Text>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Card>
  );

  const renderAnalysisPanel = () => (
    <Card title={<span><ArrowUpOutlined /> Finansal Analiz</span>}>
      <Row gutter={[16, 16]} style={{ marginBottom: '16px' }}>
        <Col xs={24} sm={12} md={8}>
          <Select
            value={symbol}
            onChange={setSymbol}
            style={{ width: '100%' }}
            placeholder="Hisse seçin"
          >
            <Option value="THYAO">Türk Hava Yolları (THYAO)</Option>
            <Option value="AKBNK">Akbank (AKBNK)</Option>
            <Option value="BIMAS">BİM (BIMAS)</Option>
            <Option value="ASELS">Aselsan (ASELS)</Option>
            <Option value="KCHOL">Koç Holding (KCHOL)</Option>
            <Option value="TCELL">Turkcell (TCELL)</Option>
          </Select>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Button
            type="primary"
            onClick={() => runAnalysis('comprehensive')}
            loading={analysisLoading}
            icon={<BarChartOutlined />}
            style={{ width: '100%' }}
          >
            Kapsamlı Analiz
          </Button>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Button
            onClick={() => runAnalysis('quick')}
            loading={analysisLoading}
            icon={<ThunderboltOutlined />}
            style={{ width: '100%' }}
          >
            Hızlı Analiz
          </Button>
        </Col>
      </Row>

      {analysisResult && (
        <Card 
          size="small" 
          title={`${symbol} Analiz Sonucu`}
          style={{ marginTop: '16px' }}
        >
          <Alert
            message={analysisResult.recommendation || analysisResult.quick_recommendation || 'BEKLE'}
            description={`Güven seviyesi: ${analysisResult.confidence || 'Orta'}`}
            type="info"
            showIcon
          />
        </Card>
      )}
    </Card>
  );

  // Modern Tabs items
  const tabItems = [
    {
      key: 'overview',
      label: (
        <span>
          <DashboardOutlined />
          Sistem Özeti
        </span>
      ),
      children: (
        <div>
          <div style={{ marginBottom: '24px' }}>
            {renderSystemOverview()}
          </div>
          {renderAgentStatus()}
        </div>
      ),
    },
    {
      key: 'analysis',
      label: (
        <span>
          <ArrowUpOutlined />
          Analiz
        </span>
      ),
      children: renderAnalysisPanel(),
    },
    {
      key: 'notifications',
      label: (
        <span>
          <BellOutlined />
          Bildirimler
        </span>
      ),
      children: <NotificationPanel />,
    },
    {
      key: 'trading',
      label: (
        <span>
          <DollarOutlined />
          İşlemler
        </span>
      ),
      children: (
        <Card title="İşlem Paneli">
          <Alert
            message="Yakında"
            description="İşlem paneli geliştirilme aşamasında..."
            type="info"
            showIcon
          />
        </Card>
      ),
    },
    {
      key: 'performance',
      label: (
        <span>
          <BarChartOutlined />
          Performans
        </span>
      ),
      children: (
        <Card title="Sistem Performansı">
          <Alert
            message="Yakında"
            description="Performans metrikleri geliştirilme aşamasında..."
            type="info"
            showIcon
          />
        </Card>
      ),
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        background: '#fff', 
        padding: '0 24px', 
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <RobotOutlined style={{ fontSize: '24px', color: '#1890ff', marginRight: '12px' }} />
          <Title level={3} style={{ margin: 0, color: '#1890ff' }}>
            🤖 Multi-Agent Finans AI Sistemi
          </Title>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ 
            padding: '4px 12px', 
            borderRadius: '12px', 
            backgroundColor: systemStatus?.system_status === 'operational' ? '#52c41a' : '#faad14',
            color: 'white',
            fontSize: '12px',
            fontWeight: 'bold'
          }}>
            {systemStatus?.system_status?.toUpperCase() || 'LOADING'}
          </span>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            v4.0.0
          </Text>
        </div>
      </Header>

      <Content style={{ padding: '24px' }}>
        {error && (
          <Alert
            message="Hata"
            description={error}
            type="error"
            showIcon
            closable
            onClose={() => setError(null)}
            style={{ marginBottom: '16px' }}
          />
        )}

        <Tabs
          defaultActiveKey="overview"
          type="card"
          items={tabItems}
        />
      </Content>
    </Layout>
  );
};

export default Dashboard;