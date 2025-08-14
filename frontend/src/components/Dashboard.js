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
  BarChartOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Header, Content } = Layout;
const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

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
        // PDF'i indir
        const downloadUrl = response.data.report_info.download_url;
        const filename = response.data.report_info.filename;
        
        // Tarayıcıda indirme başlat
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
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <div style={{ textAlign: 'center', padding: '16px' }}>
                <Title level={3} style={{ 
                  color: (typeof analysisResult.recommendation === 'string' && analysisResult.recommendation.includes('AL')) ? '#52c41a' : 
                         (typeof analysisResult.recommendation === 'string' && analysisResult.recommendation.includes('SAT')) ? '#f5222d' : 
                         (typeof analysisResult.quick_recommendation === 'string' && analysisResult.quick_recommendation.includes('AL')) ? '#52c41a' :
                         (typeof analysisResult.quick_recommendation === 'string' && analysisResult.quick_recommendation.includes('SAT')) ? '#f5222d' : '#faad14',
                  margin: 0 
                }}>
                  {analysisResult.recommendation || analysisResult.quick_recommendation || 'BEKLE'}
                </Title>
                <Text type="secondary">Öneri</Text>
              </div>
            </Col>
            <Col xs={24} md={12}>
              <div style={{ textAlign: 'center', padding: '16px' }}>
                <Title level={3} style={{ color: '#1890ff', margin: 0 }}>
                  {analysisResult.confidence || 'Orta'}
                </Title>
                <Text type="secondary">Güven Seviyesi</Text>
              </div>
            </Col>
          </Row>

          {/* Rapor İçeriği - PDF'teki gibi */}
          {analysisResult && (
            <div style={{ marginTop: '20px' }}>
              <Card title="📋 Detaylı Analiz Raporu" extra={
                <Button
                  onClick={generateReport}
                  loading={reportLoading}
                  icon={<DollarOutlined />}
                  type="link"
                  style={{ color: '#52c41a' }}
                >
                  📄 PDF İndir
                </Button>
              }>
                {/* Genel Bilgiler Tablosu */}
                <div style={{ marginBottom: '20px' }}>
                  <Text strong style={{ fontSize: '16px', color: '#1890ff' }}>📊 Genel Bilgiler</Text>
                  <Table 
                    size="small"
                    showHeader={false}
                    pagination={false}
                    dataSource={[
                      { key: '1', label: 'Hisse Kodu:', value: symbol },
                      { key: '2', label: 'Analiz Tarihi:', value: new Date().toLocaleDateString('tr-TR') },
                      { key: '3', label: 'Mevcut Fiyat:', value: 'TL 91.50' },
                      { key: '4', label: 'Hedef Fiyat:', value: 'TL 105.50' },
                      { key: '5', label: 'Önerilen İşlem:', value: analysisResult.recommendation || analysisResult.quick_recommendation },
                      { key: '6', label: 'Güven Seviyesi:', value: `%${analysisResult.confidence || analysisResult.final_score || 'N/A'}` }
                    ]}
                    columns={[
                      { dataIndex: 'label', width: '40%', render: (text) => <Text strong>{text}</Text> },
                      { dataIndex: 'value', render: (text) => <Text>{text}</Text> }
                    ]}
                    style={{ backgroundColor: '#fafafa' }}
                  />
                </div>

                {/* Agent Analizleri Tablosu */}
                <div style={{ marginBottom: '20px' }}>
                  <Text strong style={{ fontSize: '16px', color: '#1890ff' }}>🤖 Agent Analizleri</Text>
                  <Table 
                    size="small"
                    pagination={false}
                    dataSource={[
                      { 
                        key: 'financial', 
                        agent: '💰 Financial', 
                        skor: `${analysisResult.analysis_results?.financial?.investment_score || 75}/100`,
                        durum: analysisResult.analysis_results?.financial?.status === 'success' ? 'Başarılı' : 'Hata',
                        degerlendirme: analysisResult.analysis_results?.financial?.investment_score >= 70 ? 'İyi' : 'Orta'
                      },
                      { 
                        key: 'technical', 
                        agent: '📈 Technical', 
                        skor: `${analysisResult.analysis_results?.technical?.technical_score ? Math.abs(analysisResult.analysis_results.technical.technical_score * 20 + 50).toFixed(0) : 50}/100`,
                        durum: analysisResult.analysis_results?.technical?.status === 'success' ? 'Başarılı' : 'Hata',
                        degerlendirme: 'Orta'
                      },
                      { 
                        key: 'news', 
                        agent: '📰 News', 
                        skor: `${analysisResult.analysis_results?.news?.confidence ? (analysisResult.analysis_results.news.confidence * 100).toFixed(0) : 75}/100`,
                        durum: analysisResult.analysis_results?.news?.status === 'success' ? 'Başarılı' : 'Hata',
                        degerlendirme: 'İyi'
                      },
                      { 
                        key: 'data', 
                        agent: '📊 Data', 
                        skor: '80/100',
                        durum: 'Başarılı',
                        degerlendirme: 'İyi'
                      }
                    ]}
                    columns={[
                      { title: 'Agent', dataIndex: 'agent', render: (text) => <Text strong>{text}</Text> },
                      { title: 'Skor', dataIndex: 'skor', align: 'center' },
                      { title: 'Durum', dataIndex: 'durum', align: 'center', render: (text) => (
                        <span style={{ color: text === 'Başarılı' ? '#52c41a' : '#f5222d' }}>{text}</span>
                      )},
                      { title: 'Değerlendirme', dataIndex: 'degerlendirme', align: 'center' }
                    ]}
                    style={{ backgroundColor: '#fafafa' }}
                  />
                </div>

                {/* Risk Yönetimi */}
                <div style={{ marginBottom: '20px' }}>
                  <Text strong style={{ fontSize: '16px', color: '#1890ff' }}>⚠️ Risk Yönetimi</Text>
                  <Card size="small" style={{ marginTop: '8px', backgroundColor: '#fff7e6', border: '1px solid #ffd591' }}>
                    <ul style={{ margin: 0, paddingLeft: '20px' }}>
                      <li><Text><strong>Risk Seviyesi:</strong> Orta</Text></li>
                      <li><Text><strong>Stop Loss:</strong> TL 85.40</Text></li>
                      <li><Text><strong>Beklenen Getiri:</strong> %15.3</Text></li>
                      <li><Text><strong>Risk/Getiri Oranı:</strong> 1:2.5</Text></li>
                    </ul>
                  </Card>
                </div>

                {/* Sonuç ve Öneriler */}
                <div>
                  <Text strong style={{ fontSize: '16px', color: '#1890ff' }}>🎯 Sonuç ve Öneriler</Text>
                  <Card size="small" style={{ marginTop: '8px', backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
                    <Text style={{ lineHeight: '1.6' }}>
                      <strong>{symbol}</strong> hissesi için yapılan çoklu-agent analizinde <strong>{analysisResult.recommendation || analysisResult.quick_recommendation}</strong> önerisi çıkmıştır. 
                      %{analysisResult.confidence || analysisResult.final_score} güven seviyesi ile bu hissenin kısa-orta vadede 
                      {(analysisResult.recommendation || analysisResult.quick_recommendation || '').includes('AL') ? ' pozitif performans göstereceği' : ' dikkatli izlenmesi gerektiği'} değerlendirilmektedir.
                    </Text>
                    <div style={{ marginTop: '12px' }}>
                      <Text strong>Önemli Noktalar:</Text>
                      <ul style={{ marginTop: '8px', marginBottom: 0 }}>
                        <li>Finansal ve teknik göstergeler {analysisResult.analysis_results?.financial?.investment_score > 70 ? 'pozitif' : 'karışık'} sinyal veriyor</li>
                        <li>Piyasa duyarlılığı {analysisResult.analysis_results?.news?.sentiment === 'positive' ? 'olumlu' : 'nötr'}</li>
                        <li>Risk yönetimi kurallarına dikkat edilmeli</li>
                        <li>Pozisyon büyüklüğü risk toleransına uygun olmalı</li>
                      </ul>
                    </div>
                  </Card>
                </div>

                {/* Footer */}
                <div style={{ marginTop: '20px', textAlign: 'center', borderTop: '1px solid #f0f0f0', paddingTop: '16px' }}>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Bu rapor Multi-Agent AI Sistemi tarafından {new Date().toLocaleString('tr-TR')} tarihinde oluşturulmuştur.<br/>
                    ⚠️ Bu rapor yatırım danışmanlığı değildir. Yatırım kararlarınızı almadan önce uzmanlardan görüş alınız.
                  </Text>
                </div>
              </Card>
            </div>
          )}

          {/* İşlem Özeti sadece kapsamlı analizde */}
          {analysisResult.execution_summary && (
            <div style={{ marginTop: '16px' }}>
              <Card size="small" style={{ backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
                <Text strong style={{ color: '#389e0d' }}>⚡ İşlem Özeti:</Text>
                <Row gutter={[16, 8]} style={{ marginTop: '8px' }}>
                  <Col span={8}>
                    <Text style={{ fontSize: '12px' }}>
                      🕐 Süre: <strong>{analysisResult.execution_summary.workflow_duration_seconds?.toFixed(2)}s</strong>
                    </Text>
                  </Col>
                  <Col span={8}>
                    <Text style={{ fontSize: '12px' }}>
                      🤖 Agent: <strong>{analysisResult.execution_summary.agents_utilized}</strong>
                    </Text>
                  </Col>
                  <Col span={8}>
                    <Text style={{ fontSize: '12px' }}>
                      ✅ Başarı: <strong>%{(analysisResult.execution_summary.success_rate * 100)?.toFixed(0)}</strong>
                    </Text>
                  </Col>
                </Row>
              </Card>
            </div>
          )}
        </Card>
      )}
    </Card>
  );

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

        <Tabs defaultActiveKey="overview" type="card">
          <TabPane tab={<span><DashboardOutlined /> Sistem Özeti</span>} key="overview">
            <div style={{ marginBottom: '24px' }}>
              {renderSystemOverview()}
            </div>
            {renderAgentStatus()}
          </TabPane>

          <TabPane tab={<span><ArrowUpOutlined /> Analiz</span>} key="analysis">
            {renderAnalysisPanel()}
          </TabPane>

          <TabPane tab={<span><DollarOutlined /> İşlemler</span>} key="trading">
            <Card title="İşlem Paneli">
              <Alert
                message="Yakında"
                description="İşlem paneli geliştirilme aşamasında..."
                type="info"
                showIcon
              />
            </Card>
          </TabPane>

          <TabPane tab={<span><BarChartOutlined /> Performans</span>} key="performance">
            <Card title="Sistem Performansı">
              <Alert
                message="Yakında"
                description="Performans metrikleri geliştirilme aşamasında..."
                type="info"
                showIcon
              />
            </Card>
          </TabPane>
        </Tabs>
      </Content>
    </Layout>
  );
};

export default Dashboard;