import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Form, 
  Input, 
  Select, 
  Button, 
  Table,
  Alert,
  Statistic,
  Tag,
  Typography,
  Space,
  Tabs,
  Progress,
  List,
  Spin,
  Divider
} from 'antd';
import { 
  HeartOutlined, 
  TwitterOutlined, 
  RedditOutlined,
  LineChartOutlined,
  ThunderboltOutlined,
  TrendingUpOutlined,
  TrendingDownOutlined,
  EyeOutlined,
  WarningOutlined
} from '@ant-design/icons';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { apiService } from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const SentimentPanel = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [socialSentiment, setSocialSentiment] = useState(null);
  const [marketSentiment, setMarketSentiment] = useState(null);
  const [fearGreedIndex, setFearGreedIndex] = useState(null);
  const [sentimentSignals, setSentimentSignals] = useState(null);
  const [sentimentTrends, setSentimentTrends] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('THYAO');

  useEffect(() => {
    loadFearGreedIndex();
    loadMarketSentiment();
  }, []);

  const analyzeSocialSentiment = async (values) => {
    setLoading(true);
    try {
      const response = await apiService.analyzeSocialSentiment(
        values.symbol || selectedSymbol, 
        values.platform || 'twitter'
      );
      setSocialSentiment(response.data);
    } catch (error) {
      console.error('Social sentiment error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadFearGreedIndex = async () => {
    try {
      const response = await apiService.getFearGreedIndex();
      setFearGreedIndex(response.data);
    } catch (error) {
      console.error('Fear & Greed index error:', error);
    }
  };

  const loadMarketSentiment = async () => {
    try {
      const response = await apiService.getMarketSentiment();
      setMarketSentiment(response.data);
    } catch (error) {
      console.error('Market sentiment error:', error);
    }
  };

  const getSentimentSignals = async (symbol) => {
    setLoading(true);
    try {
      const response = await apiService.getSentimentSignals(symbol || selectedSymbol);
      setSentimentSignals(response.data);
    } catch (error) {
      console.error('Sentiment signals error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentTrends = async (symbol, timeframe = '7d') => {
    setLoading(true);
    try {
      const response = await apiService.getSentimentTrends(symbol || selectedSymbol, timeframe);
      setSentimentTrends(response.data);
    } catch (error) {
      console.error('Sentiment trends error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.4) return '#52c41a';
    if (sentiment > 0.1) return '#faad14';
    if (sentiment > -0.1) return '#d9d9d9';
    if (sentiment > -0.4) return '#faad14';
    return '#f5222d';
  };

  const getFearGreedColor = (index) => {
    if (index >= 75) return '#f5222d';
    if (index >= 55) return '#faad14';
    if (index >= 45) return '#d9d9d9';
    if (index >= 25) return '#faad14';
    return '#52c41a';
  };

  const renderFearGreedIndex = () => {
    if (!fearGreedIndex) return null;

    const { fear_greed_index } = fearGreedIndex;

    return (
      <Card title="Korku & Açgözlülük Endeksi" size="small">
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <div style={{ textAlign: 'center' }}>
              <Progress
                type="circle"
                percent={fear_greed_index.index_value}
                width={120}
                strokeColor={getFearGreedColor(fear_greed_index.index_value)}
                format={() => (
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 'bold' }}>
                      {fear_greed_index.index_value}
                    </div>
                    <div style={{ fontSize: 12 }}>
                      {fear_greed_index.category}
                    </div>
                  </div>
                )}
              />
              
              <div style={{ marginTop: 16 }}>
                <Tag 
                  color={getFearGreedColor(fear_greed_index.index_value)}
                  style={{ fontSize: 14, padding: '4px 12px' }}
                >
                  {fear_greed_index.signal}
                </Tag>
              </div>
            </div>
          </Col>
          
          <Col xs={24} md={12}>
            <div>
              <Text strong>Bileşenler:</Text>
              <div style={{ marginTop: 8 }}>
                {Object.entries(fear_greed_index.components).map(([key, value]) => (
                  <div key={key} style={{ marginBottom: 4 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text>{key.replace('_', ' ').toUpperCase()}</Text>
                      <Text strong>{value}</Text>
                    </div>
                    <Progress 
                      percent={value} 
                      size="small" 
                      strokeColor={getFearGreedColor(value)}
                      showInfo={false}
                    />
                  </div>
                ))}
              </div>
            </div>
          </Col>
        </Row>
        
        <Alert
          style={{ marginTop: 16 }}
          message={fear_greed_index.interpretation}
          type={fear_greed_index.contrarian_opportunity ? 'warning' : 'info'}
          showIcon
        />
      </Card>
    );
  };

  const renderSocialSentimentForm = () => (
    <Card title="Sosyal Medya Duygu Analizi" size="small">
      <Form
        form={form}
        layout="inline"
        onFinish={analyzeSocialSentiment}
        style={{ marginBottom: 16 }}
      >
        <Form.Item name="symbol" initialValue={selectedSymbol}>
          <Select style={{ width: 120 }} onChange={setSelectedSymbol}>
            <Option value="THYAO">THYAO</Option>
            <Option value="AKBNK">AKBNK</Option>
            <Option value="BIMAS">BIMAS</Option>
            <Option value="ASELS">ASELS</Option>
            <Option value="KCHOL">KCHOL</Option>
          </Select>
        </Form.Item>
        
        <Form.Item name="platform" initialValue="twitter">
          <Select style={{ width: 100 }}>
            <Option value="twitter">Twitter</Option>
            <Option value="reddit">Reddit</Option>
          </Select>
        </Form.Item>
        
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Analiz Et
          </Button>
        </Form.Item>
        
        <Form.Item>
          <Button onClick={() => getSentimentSignals(selectedSymbol)}>
            Sinyaller
          </Button>
        </Form.Item>
        
        <Form.Item>
          <Button onClick={() => getSentimentTrends(selectedSymbol)}>
            Trendler
          </Button>
        </Form.Item>
      </Form>

      {socialSentiment && renderSocialSentimentResults()}
    </Card>
  );

  const renderSocialSentimentResults = () => {
    const { social_sentiment_analysis } = socialSentiment;
    
    return (
      <div>
        <Row gutter={16}>
          <Col xs={24} sm={6}>
            <Card size="small">
              <Statistic
                title="Genel Duygu"
                value={social_sentiment_analysis.overall_sentiment}
                precision={3}
                valueStyle={{ 
                  color: getSentimentColor(social_sentiment_analysis.overall_sentiment) 
                }}
                suffix={
                  <Tag color={getSentimentColor(social_sentiment_analysis.overall_sentiment)}>
                    {social_sentiment_analysis.sentiment_label}
                  </Tag>
                }
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={6}>
            <Card size="small">
              <Statistic
                title="Güven Seviyesi"
                value={social_sentiment_analysis.reliability_score * 100}
                precision={1}
                suffix="%"
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={6}>
            <Card size="small">
              <Statistic
                title="Toplam Bahsetme"
                value={social_sentiment_analysis.total_mentions}
                valueStyle={{ color: '#722ed1' }}
                prefix={<TwitterOutlined />}
              />
            </Card>
          </Col>
          
          <Col xs={24} sm={6}>
            <Card size="small">
              <Statistic
                title="Duygu Gücü"
                value={social_sentiment_analysis.sentiment_strength * 100}
                precision={1}
                suffix="%"
                valueStyle={{ color: '#faad14' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={16} style={{ marginTop: 16 }}>
          <Col xs={24} md={12}>
            <Card title="Duygu Dağılımı" size="small">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={Object.entries(social_sentiment_analysis.sentiment_distribution).map(([key, value]) => ({
                      name: key.replace('_', ' ').toUpperCase(),
                      value: value
                    }))}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {Object.entries(social_sentiment_analysis.sentiment_distribution).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#f5222d', '#faad14', '#d9d9d9', '#52c41a', '#1890ff'][index]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          
          <Col xs={24} md={12}>
            <Card title="Etkili Postlar" size="small">
              <List
                size="small"
                dataSource={social_sentiment_analysis.influential_posts}
                renderItem={(item) => (
                  <List.Item>
                    <div style={{ width: '100%' }}>
                      <Text style={{ fontSize: 12 }}>{item.text}</Text>
                      <div style={{ marginTop: 4 }}>
                        <Space>
                          <Text type="secondary" style={{ fontSize: 10 }}>
                            👍 {item.likes}
                          </Text>
                          <Text type="secondary" style={{ fontSize: 10 }}>
                            🔄 {item.retweets}
                          </Text>
                        </Space>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>
      </div>
    );
  };

  const renderMarketSentiment = () => {
    if (!marketSentiment) return null;

    const { market_sentiment } = marketSentiment;
    
    return (
      <Card title="Genel Piyasa Duyarlılığı" size="small">
        <Row gutter={16}>
          <Col xs={24} md={8}>
            <Card size="small">
              <Statistic
                title="Piyasa Duyarlılığı"
                value={market_sentiment.overall_market_sentiment}
                precision={3}
                valueStyle={{ 
                  color: getSentimentColor(market_sentiment.overall_market_sentiment) 
                }}
                suffix={
                  <Tag color={getSentimentColor(market_sentiment.overall_market_sentiment)}>
                    {market_sentiment.sentiment_label}
                  </Tag>
                }
              />
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small">
              <Statistic
                title="Fikir Birliği"
                value={market_sentiment.market_consensus}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small">
              <Statistic
                title="Piyasa Ruh Hali"
                value={market_sentiment.market_mood}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
        </Row>

        <Card title="Hisse Bazlı Duyarlılık" size="small" style={{ marginTop: 16 }}>
          <Table
            size="small"
            pagination={false}
            dataSource={Object.entries(market_sentiment.symbol_sentiments).map(([symbol, data], index) => ({
              key: index,
              symbol,
              sentiment: data.sentiment_score,
              label: data.sentiment_label,
              volume: data.mention_volume
            }))}
            columns={[
              {
                title: 'Hisse',
                dataIndex: 'symbol',
                key: 'symbol',
                render: (text) => <Text strong>{text}</Text>
              },
              {
                title: 'Duygu Skoru',
                dataIndex: 'sentiment',
                key: 'sentiment',
                render: (value) => (
                  <Progress 
                    percent={((value + 1) / 2) * 100} 
                    size="small" 
                    strokeColor={getSentimentColor(value)}
                    format={() => value.toFixed(3)}
                  />
                )
              },
              {
                title: 'Etiket',
                dataIndex: 'label',
                key: 'label',
                render: (text, record) => (
                  <Tag color={getSentimentColor(record.sentiment)}>
                    {text}
                  </Tag>
                )
              },
              {
                title: 'Bahsetme',
                dataIndex: 'volume',
                key: 'volume'
              }
            ]}
          />
        </Card>
      </Card>
    );
  };

  const renderSentimentSignals = () => {
    if (!sentimentSignals) return null;

    const { sentiment_signals } = sentimentSignals;

    return (
      <Card title="Duygu Bazlı Sinyaller" size="small">
        <Row gutter={16}>
          <Col xs={24} md={8}>
            <Card size="small">
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>
                  {sentiment_signals.overall_signal === 'STRONG_BUY' ? '🚀' :
                   sentiment_signals.overall_signal === 'BUY' ? '📈' :
                   sentiment_signals.overall_signal === 'HOLD' ? '⏳' :
                   sentiment_signals.overall_signal === 'SELL' ? '📉' : '🔻'}
                </div>
                <Text strong style={{ fontSize: 16 }}>
                  {sentiment_signals.overall_signal}
                </Text>
                <div style={{ marginTop: 8 }}>
                  <Text>Güç: {sentiment_signals.signal_strength}</Text>
                </div>
              </div>
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small">
              <div>
                <Text strong>Güven: </Text>
                <Text>{sentiment_signals.confidence}%</Text>
                <Progress 
                  percent={sentiment_signals.confidence} 
                  size="small" 
                  style={{ marginTop: 4 }}
                />
              </div>
            </Card>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small">
              <div>
                <Text strong>Risk: </Text>
                <Tag color={
                  sentiment_signals.risk_assessment.risk_level === 'LOW' ? 'green' :
                  sentiment_signals.risk_assessment.risk_level === 'MEDIUM' ? 'orange' : 'red'
                }>
                  {sentiment_signals.risk_assessment.risk_level}
                </Tag>
              </div>
            </Card>
          </Col>
        </Row>

        <Card title="Detaylı Sinyaller" size="small" style={{ marginTop: 16 }}>
          <List
            dataSource={sentiment_signals.individual_signals}
            renderItem={(item) => (
              <List.Item>
                <div style={{ width: '100%' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <Text strong>{item.type}</Text>
                    <Tag color={
                      item.strength === 'HIGH' ? 'red' :
                      item.strength === 'MEDIUM' ? 'orange' : 'blue'
                    }>
                      {item.strength}
                    </Tag>
                  </div>
                  <Text type="secondary">{item.reason}</Text>
                  <div style={{ marginTop: 4 }}>
                    <Text style={{ fontSize: 12 }}>Zaman: {item.timeframe}</Text>
                  </div>
                </div>
              </List.Item>
            )}
          />
        </Card>
      </Card>
    );
  };

  const renderSentimentTrends = () => {
    if (!sentimentTrends) return null;

    const { sentiment_trends } = sentimentTrends;

    return (
      <Card title="Duygu Trendleri" size="small">
        <Row gutter={16}>
          <Col xs={24} md={16}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={sentiment_trends.sentiment_history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[-1, 1]} />
                <Tooltip 
                  formatter={(value) => [value.toFixed(3), 'Duygu']}
                />
                <Line 
                  type="monotone" 
                  dataKey="sentiment" 
                  stroke="#1890ff" 
                  strokeWidth={2}
                  dot={{ fill: '#1890ff', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Col>
          
          <Col xs={24} md={8}>
            <Card size="small" title="Trend Analizi">
              <div style={{ marginBottom: 8 }}>
                <Text>Yön: </Text>
                <Tag color={
                  sentiment_trends.trend_analysis.direction === 'Improving' ? 'green' :
                  sentiment_trends.trend_analysis.direction === 'Deteriorating' ? 'red' : 'blue'
                }>
                  {sentiment_trends.trend_analysis.direction}
                </Tag>
              </div>
              
              <div style={{ marginBottom: 8 }}>
                <Text>Güç: </Text>
                <Progress 
                  percent={sentiment_trends.trend_analysis.strength * 100} 
                  size="small"
                />
              </div>
              
              <div style={{ marginBottom: 8 }}>
                <Text>Volatilite: </Text>
                <Text>{sentiment_trends.trend_analysis.volatility.toFixed(3)}</Text>
              </div>
              
              <div>
                <Text>Momentum: </Text>
                <Text style={{ 
                  color: sentiment_trends.momentum >= 0 ? '#52c41a' : '#f5222d' 
                }}>
                  {sentiment_trends.momentum >= 0 ? '+' : ''}{sentiment_trends.momentum.toFixed(3)}
                </Text>
              </div>
            </Card>
          </Col>
        </Row>
      </Card>
    );
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <HeartOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Piyasa Duyarlılığı</Title>
        </Space>
      </div>

      <Tabs defaultActiveKey="fear-greed">
        <TabPane tab="Korku & Açgözlülük" key="fear-greed">
          {renderFearGreedIndex()}
        </TabPane>
        
        <TabPane tab="Sosyal Medya" key="social">
          {renderSocialSentimentForm()}
        </TabPane>
        
        <TabPane tab="Piyasa Genel" key="market">
          <div style={{ marginBottom: 16 }}>
            <Button 
              type="primary" 
              onClick={loadMarketSentiment}
              loading={loading}
            >
              Piyasa Duyarlılığı Yenile
            </Button>
          </div>
          {renderMarketSentiment()}
        </TabPane>
        
        <TabPane tab="Sinyaller" key="signals">
          {renderSentimentSignals()}
        </TabPane>
        
        <TabPane tab="Trendler" key="trends">
          {renderSentimentTrends()}
        </TabPane>
      </Tabs>

      <Card 
        title="Duygu Analizi Hakkında" 
        size="small" 
        style={{ marginTop: 24 }}
      >
        <Alert
          message="Piyasa Duyarlılığı Özellikleri"
          description={
            <ul style={{ marginBottom: 0 }}>
              <li>Sosyal medya platformlarından gerçek zamanlı duygu analizi</li>
              <li>Korku & Açgözlülük endeksi ile piyasa ruh hali ölçümü</li>
              <li>Duygu bazlı alım/satım sinyalleri</li>
              <li>Trend takibi ve momentum analizi</li>
              <li>Kontrarian yatırım fırsatlarının belirlenmesi</li>
            </ul>
          }
          type="info"
          showIcon
        />
      </Card>
    </div>
  );
};

export default SentimentPanel;