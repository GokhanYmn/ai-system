import React, { useState } from 'react';
import { 
  Card, 
  Input, 
  Button, 
  Space, 
  Alert, 
  Descriptions, 
  Tag, 
  Progress, 
  Typography,
  Spin,
  Result,
  Divider
} from 'antd';
import { 
  SearchOutlined, 
  ThunderboltOutlined, 
  DollarOutlined,
  TrophyOutlined,
  ClockCircleOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Title, Text } = Typography;

const AnalysisPanel = ({ onRefresh }) => {
  const [symbol, setSymbol] = useState('THYAO');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [quickMode, setQuickMode] = useState(false);

  const runAnalysis = async (isQuick = false) => {
    if (!symbol) return;
    
    setLoading(true);
    setQuickMode(isQuick);
    
    try {
      const response = isQuick 
        ? await apiService.quickAnalysis(symbol.toUpperCase())
        : await apiService.comprehensiveAnalysis(symbol.toUpperCase());
      
      setAnalysisData(response.data);
      if (onRefresh) onRefresh();
    } catch (error) {
      console.error('Analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationColor = (signal) => {
    if (signal?.includes('AL')) return 'success';
    if (signal?.includes('SAT')) return 'error';
    return 'warning';
  };

  const getRecommendationIcon = (signal) => {
    if (signal?.includes('AL')) return '🚀';
    if (signal?.includes('SAT')) return '⬇️';
    return '⏳';
  };

  const formatDuration = (seconds) => {
    if (seconds < 1) return `${Math.round(seconds * 1000)}ms`;
    return `${seconds.toFixed(2)}s`;
  };

  return (
    <Card 
      title={
        <Space>
          <SearchOutlined style={{ color: '#52c41a' }} />
          <Title level={4} style={{ margin: 0 }}>Finansal Analiz</Title>
        </Space>
      }
      style={{ height: 600 }}
      bodyStyle={{ padding: 16, height: 'calc(100% - 60px)', overflow: 'auto' }}
    >
      {/* Arama ve Butonlar */}
      <Space.Compact style={{ width: '100%', marginBottom: 16 }}>
        <Input
          placeholder="Hisse kodu (örn: THYAO)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          onPressEnter={() => runAnalysis(false)}
          style={{ flex: 1 }}
        />
        <Button 
          type="primary" 
          icon={<ThunderboltOutlined />}
          onClick={() => runAnalysis(false)}
          loading={loading && !quickMode}
        >
          Tam Analiz
        </Button>
      </Space.Compact>

      <Button 
        type="default" 
        block
        onClick={() => runAnalysis(true)}
        loading={loading && quickMode}
        style={{ marginBottom: 16 }}
      >
        Hızlı Analiz
      </Button>

      {/* Loading State */}
      {loading && (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>
            <Text type="secondary">
              {quickMode ? 'Hızlı analiz yapılıyor...' : '7 AI Agent koordine ediliyor...'}
            </Text>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {!loading && analysisData && (
        <div>
          {/* Ana Öneri */}
          <Alert
            message={
              <Space>
                <span style={{ fontSize: 20 }}>
                  {getRecommendationIcon(analysisData.recommendation?.overall_signal || analysisData.quick_recommendation)}
                </span>
                <strong>
                  {analysisData.recommendation?.overall_signal || analysisData.quick_recommendation}
                </strong>
              </Space>
            }
            description={analysisData.recommendation?.reasoning?.[0] || 'Hızlı analiz tamamlandı'}
            type={getRecommendationColor(analysisData.recommendation?.overall_signal || analysisData.quick_recommendation)}
            style={{ marginBottom: 16 }}
          />

          {/* Detaylı Bilgiler - Kapsamlı Analiz */}
          {analysisData.recommendation && (
            <>
              <Descriptions title="Analiz Detayları" bordered size="small" column={1}>
                <Descriptions.Item label="Güven Seviyesi">
                  <Progress 
                    percent={analysisData.recommendation.confidence || 0} 
                    size="small"
                    status={analysisData.recommendation.confidence > 70 ? 'success' : 'normal'}
                  />
                </Descriptions.Item>
                
                <Descriptions.Item label="Önerilen Pozisyon">
                  <Space>
                    <Tag color="blue">%{analysisData.recommendation.suggested_allocation}</Tag>
                    <Text type="secondary">portföy ağırlığı</Text>
                  </Space>
                </Descriptions.Item>
                
                <Descriptions.Item label="İşlem Tutarı">
                  <Space>
                    <DollarOutlined style={{ color: '#faad14' }} />
                    <Text strong>
                      {analysisData.recommendation.optimal_trade_amount?.toLocaleString('tr-TR')} TL
                    </Text>
                  </Space>
                </Descriptions.Item>
                
                <Descriptions.Item label="Risk Yönetimi">
                  <Space split={<Divider type="vertical" />}>
                    <Text>
                      <span style={{ color: '#ff4d4f' }}>SL:</span> %{analysisData.recommendation.stop_loss}
                    </Text>
                    <Text>
                      <span style={{ color: '#52c41a' }}>TP:</span> %{analysisData.recommendation.take_profit}
                    </Text>
                  </Space>
                </Descriptions.Item>
                
                <Descriptions.Item label="Zaman Ufku">
                  <Tag color="purple">{analysisData.recommendation.time_horizon}</Tag>
                </Descriptions.Item>
              </Descriptions>

              {/* Execution Summary */}
              {analysisData.execution_summary && (
                <Card 
                  size="small" 
                  title="İşlem Özeti" 
                  style={{ marginTop: 16 }}
                >
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text type="secondary">Süre:</Text>
                      <Text strong>
                        <ClockCircleOutlined style={{ marginRight: 4 }} />
                        {formatDuration(analysisData.execution_summary.workflow_duration_seconds)}
                      </Text>
                    </div>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text type="secondary">Agent'lar:</Text>
                      <Text strong>
                        <TrophyOutlined style={{ marginRight: 4, color: '#52c41a' }} />
                        {analysisData.execution_summary.agents_utilized}/6
                      </Text>
                    </div>
                    
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text type="secondary">Başarı Oranı:</Text>
                      <Progress 
                        percent={Math.round(analysisData.execution_summary.success_rate * 100)} 
                        size="small"
                        style={{ width: 100 }}
                      />
                    </div>
                  </Space>
                </Card>
              )}
            </>
          )}

          {/* Hızlı Analiz Sonuçları */}
          {analysisData.quick_recommendation && !analysisData.recommendation && (
            <Descriptions title="Hızlı Analiz" bordered size="small" column={1}>
              <Descriptions.Item label="Öneri">
                {analysisData.quick_recommendation}
              </Descriptions.Item>
              
              <Descriptions.Item label="Güven">
                <Tag color="blue">{analysisData.confidence}</Tag>
              </Descriptions.Item>
              
              <Descriptions.Item label="Not">
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {analysisData.note}
                </Text>
              </Descriptions.Item>
            </Descriptions>
          )}
        </div>
      )}

      {/* İlk Durum */}
      {!loading && !analysisData && (
        <Result
          icon={<BarChartOutlined style={{ color: '#1890ff' }} />}
          title="Finansal Analiz"
          subTitle="Hisse senedi kodu girin ve AI agent'larının kapsamlı analizini başlatın"
          extra={
            <Space direction="vertical">
              <Text type="secondary">
                • 7 uzman AI agent koordineli çalışır
              </Text>
              <Text type="secondary">
                • Gerçek zamanlı veri analizi
              </Text>
              <Text type="secondary">
                • Risk yönetimi ve strateji önerileri
              </Text>
            </Space>
          }
        />
      )}
    </Card>
  );
};

export default AnalysisPanel;