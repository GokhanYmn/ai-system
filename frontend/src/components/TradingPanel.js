import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Button, 
  Input, 
  Space, 
  Statistic, 
  Alert, 
  Typography,
  Divider,
  List,
  Tag,
  Progress,
  Tooltip
} from 'antd';
import { 
  DollarOutlined, 
  TrophyOutlined, 
  ThunderboltOutlined,
  LineChartOutlined,
  InfoCircleOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Title, Text } = Typography;

const TradingPanel = () => {
  const [learningData, setLearningData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mockPortfolio] = useState({
    totalValue: 1250000,
    todayChange: 15750,
    todayChangePercent: 1.28,
    positions: [
      { symbol: 'THYAO', value: 327500, change: 2.5, weight: 26.2 },
      { symbol: 'AKBNK', value: 195000, change: -1.2, weight: 15.6 },
      { symbol: 'BIMAS', value: 156250, change: 0.8, weight: 12.5 },
      { symbol: 'ASELS', value: 143750, change: 3.2, weight: 11.5 },
      { symbol: 'CASH', value: 427500, change: 0, weight: 34.2 }
    ]
  });

  useEffect(() => {
    loadLearningData();
  }, []);

  const loadLearningData = async () => {
    setLoading(true);
    try {
      const response = await apiService.getLearningPerformance();
      setLearningData(response.data);
    } catch (error) {
      console.error('Learning data error:', error);
    } finally {
      setLoading(false);
    }
  };

  const executeMockTrade = async () => {
    // Mock trade execution
    alert('Demo modunda! Gerçek işlem yapılmadı.\nProfesyonel kullanım için broker entegrasyonu gereklidir.');
  };

  const getChangeColor = (change) => {
    if (change > 0) return '#52c41a';
    if (change < 0) return '#ff4d4f';
    return '#666';
  };

  const getChangeIcon = (change) => {
    if (change > 0) return <RiseOutlined />;
    if (change < 0) return <FallOutlined />;
    return null;
  };

  return (
    <Card 
      title={
        <Space>
          <DollarOutlined style={{ color: '#faad14' }} />
          <Title level={4} style={{ margin: 0 }}>İşlem Paneli</Title>
        </Space>
      }
      extra={
        <Button 
          type="text" 
          icon={<ThunderboltOutlined />} 
          onClick={loadLearningData}
          loading={loading}
          size="small"
        >
          Yenile
        </Button>
      }
      style={{ height: 600 }}
      bodyStyle={{ padding: 16, height: 'calc(100% - 60px)', overflow: 'auto' }}
    >
      {/* Portfolio Summary */}
      <div style={{ marginBottom: 16 }}>
        <Alert
          message={
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Text strong style={{ fontSize: 16 }}>
                  {mockPortfolio.totalValue.toLocaleString('tr-TR')} TL
                </Text>
                <Space>
                  {getChangeIcon(mockPortfolio.todayChange)}
                  <Text 
                    strong 
                    style={{ 
                      color: getChangeColor(mockPortfolio.todayChange),
                      fontSize: 14 
                    }}
                  >
                    {mockPortfolio.todayChange > 0 ? '+' : ''}
                    {mockPortfolio.todayChange.toLocaleString('tr-TR')} TL
                    ({mockPortfolio.todayChangePercent > 0 ? '+' : ''}{mockPortfolio.todayChangePercent}%)
                  </Text>
                </Space>
              </div>
            </div>
          }
          description="Toplam Portföy Değeri"
          type={mockPortfolio.todayChange >= 0 ? 'success' : 'error'}
        />
      </div>

      {/* Positions */}
      <Card size="small" title="Pozisyonlar" style={{ marginBottom: 16 }}>
        <List
          size="small"
          dataSource={mockPortfolio.positions}
          renderItem={(position) => (
            <List.Item style={{ padding: '8px 0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                <div>
                  <Text strong>{position.symbol}</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: 11 }}>
                    %{position.weight}
                  </Text>
                </div>
                
                <div style={{ textAlign: 'right' }}>
                  <Text strong style={{ fontSize: 12 }}>
                    {position.value.toLocaleString('tr-TR')} TL
                  </Text>
                  <br />
                  <Text 
                    style={{ 
                      fontSize: 11, 
                      color: getChangeColor(position.change) 
                    }}
                  >
                    {position.change > 0 ? '+' : ''}{position.change}%
                  </Text>
                </div>
              </div>
            </List.Item>
          )}
        />
      </Card>

      {/* Learning Performance */}
      {learningData && (
        <Card size="small" title="AI Öğrenme Durumu" style={{ marginBottom: 16 }}>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text type="secondary">Durum:</Text>
              <Tag color="blue">{learningData.learning_status}</Tag>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text type="secondary">Epsilon:</Text>
              <Text strong>
                {learningData.agent_metrics?.epsilon?.toFixed(3) || 'N/A'}
              </Text>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Text type="secondary">Trend:</Text>
              <Tag color="green">{learningData.performance_trend}</Tag>
            </div>
            
            <Progress 
              percent={85} 
              size="small"
              strokeColor="#52c41a"
              format={() => 'Öğrenme İlerlemesi'}
            />
          </Space>
        </Card>
      )}

      {/* Quick Trade */}
      <Card size="small" title="Hızlı İşlem">
        <Space direction="vertical" style={{ width: '100%' }}>
          <Input placeholder="Hisse Kodu" defaultValue="THYAO" />
          <Input placeholder="Miktar (TL)" defaultValue="50000" />
          
          <Space style={{ width: '100%', justifyContent: 'space-between' }}>
            <Button 
              type="primary" 
              danger 
              style={{ width: '48%' }}
              onClick={executeMockTrade}
            >
              SAT
            </Button>
            <Button 
              type="primary" 
              style={{ width: '48%' }}
              onClick={executeMockTrade}
            >
              AL
            </Button>
          </Space>
          
          <Alert
            message={
              <Space>
                <InfoCircleOutlined />
                <Text style={{ fontSize: 11 }}>
                  Demo modunda çalışıyorsunuz
                </Text>
              </Space>
            }
            type="info"
            showIcon={false}
          />
        </Space>
      </Card>

      {/* Performance Metrics */}
      <div style={{ marginTop: 16 }}>
        <Divider style={{ margin: '12px 0' }} />
        <Space split={<Divider type="vertical" />} style={{ width: '100%', justifyContent: 'center' }}>
          <Tooltip title="Günlük Getiri">
            <Statistic
              value={mockPortfolio.todayChangePercent}
              precision={2}
              suffix="%"
              valueStyle={{ 
                color: getChangeColor(mockPortfolio.todayChange),
                fontSize: 14 
              }}
              prefix={getChangeIcon(mockPortfolio.todayChange)}
            />
          </Tooltip>
          
          <Tooltip title="Aktif Pozisyon">
            <Statistic
              value={mockPortfolio.positions.length - 1}
              suffix="adet"
              valueStyle={{ fontSize: 14 }}
              prefix={<LineChartOutlined />}
            />
          </Tooltip>
        </Space>
      </div>
    </Card>
  );
};

export default TradingPanel;