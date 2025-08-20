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
  InputNumber,
  DatePicker,
  Alert,
  Statistic,
  Tag,
  Typography,
  Space,
  Modal,
  Tabs,
  Progress,
  List,
  Spin
} from 'antd';
import { 
  PlusOutlined, 
  DollarOutlined, 
  ArrowUpOutlined,
  ArrowDownOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
  LineChartOutlined,
  PieChartOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const PersonalPortfolioPanel = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [portfolioData, setPortfolioData] = useState(null);
  const [addPositionModal, setAddPositionModal] = useState(false);
  const [performanceData, setPerformanceData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [userId] = useState('user123'); // Mock user ID

  useEffect(() => {
    loadPortfolioData();
  }, []);

  const loadPortfolioData = async () => {
    setLoading(true);
    try {
      const response = await apiService.getPortfolioPerformance(userId);
      setPortfolioData(response.data);
    } catch (error) {
      console.error('Portfolio data loading error:', error);
      // Set mock data if API fails
      setPortfolioData({
        portfolio_performance: {
          total_positions: 0,
          total_invested: 0,
          current_portfolio_value: 0,
          total_unrealized_pnl: 0,
          total_return_pct: 0,
          best_performer: null,
          worst_performer: null
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const addPosition = async (values) => {
    setLoading(true);
    try {
      const positionData = {
        symbol: values.symbol,
        quantity: values.quantity,
        purchase_price: values.purchase_price,
        purchase_date: values.purchase_date?.toISOString(),
        asset_type: values.asset_type
      };

      await apiService.addPortfolioPosition(userId, positionData);
      setAddPositionModal(false);
      form.resetFields();
      loadPortfolioData();
      
      // Update prices after adding
      updatePrices();
    } catch (error) {
      console.error('Add position error:', error);
    } finally {
      setLoading(false);
    }
  };

  const updatePrices = async () => {
    try {
      const mockPrices = {
        'THYAO': 92.30,
        'AKBNK': 46.80,
        'BIMAS': 188.50,
        'ASELS': 95.20,
        'KCHOL': 87.60
      };

      await apiService.updatePortfolioPrices(userId, mockPrices);
      loadPortfolioData();
    } catch (error) {
      console.error('Price update error:', error);
    }
  };

  const analyzePortfolio = async () => {
    setLoading(true);
    try {
      const response = await apiService.analyzePersonalPortfolio(userId);
      setPerformanceData(response.data);
    } catch (error) {
      console.error('Portfolio analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendations = async () => {
    setLoading(true);
    try {
      const response = await apiService.getPersonalRecommendations(userId);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Recommendations error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderPortfolioSummary = () => {
    // Guard clause for null/undefined data
    if (!portfolioData || !portfolioData.portfolio_performance) {
      return (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={24}>
            <Alert
              message="Portföy verisi yükleniyor..."
              description="Lütfen bekleyin veya bir pozisyon ekleyin."
              type="info"
              showIcon
            />
          </Col>
        </Row>
      );
    }

    const { portfolio_performance } = portfolioData;
    const isProfit = (portfolio_performance.total_unrealized_pnl || 0) >= 0;

    return (
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Toplam Yatırım"
              value={portfolio_performance.total_invested || 0}
              precision={2}
              suffix="TL"
              prefix={<DollarOutlined />}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Güncel Değer"
              value={portfolio_performance.current_portfolio_value || 0}
              precision={2}
              suffix="TL"
              valueStyle={{ color: isProfit ? '#3f8600' : '#cf1322' }}
              prefix={isProfit ? <RiseOutlined /> : <FallOutlined />}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Toplam K/Z"
              value={portfolio_performance.total_unrealized_pnl || 0}
              precision={2}
              suffix="TL"
              valueStyle={{ color: isProfit ? '#3f8600' : '#cf1322' }}
              prefix={isProfit ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Toplam Getiri"
              value={portfolio_performance.total_return_pct || 0}
              precision={2}
              suffix="%"
              valueStyle={{ color: isProfit ? '#3f8600' : '#cf1322' }}
            />
          </Card>
        </Col>
      </Row>
    );
  };

  const renderPositionsTable = () => {
    // Mock positions data (normally would come from API)
    const positions = [
      {
        key: '1',
        symbol: 'THYAO',
        quantity: 1000,
        purchase_price: 85.50,
        current_price: 92.30,
        total_cost: 85500,
        current_value: 92300,
        unrealized_pnl: 6800,
        unrealized_pnl_pct: 7.95
      },
      {
        key: '2',
        symbol: 'AKBNK', 
        quantity: 2000,
        purchase_price: 48.20,
        current_price: 46.80,
        total_cost: 96400,
        current_value: 93600,
        unrealized_pnl: -2800,
        unrealized_pnl_pct: -2.90
      }
    ];

    const columns = [
      {
        title: 'Sembol',
        dataIndex: 'symbol',
        key: 'symbol',
        render: (text) => <Text strong>{text}</Text>
      },
      {
        title: 'Miktar',
        dataIndex: 'quantity',
        key: 'quantity',
        render: (value) => value.toLocaleString('tr-TR')
      },
      {
        title: 'Alış Fiyatı',
        dataIndex: 'purchase_price',
        key: 'purchase_price',
        render: (value) => `${value.toFixed(2)} TL`
      },
      {
        title: 'Güncel Fiyat',
        dataIndex: 'current_price',
        key: 'current_price',
        render: (value) => `${value.toFixed(2)} TL`
      },
      {
        title: 'Toplam Maliyet',
        dataIndex: 'total_cost',
        key: 'total_cost',
        render: (value) => `${value.toLocaleString('tr-TR')} TL`
      },
      {
        title: 'Güncel Değer',
        dataIndex: 'current_value',
        key: 'current_value',
        render: (value) => `${value.toLocaleString('tr-TR')} TL`
      },
      {
        title: 'K/Z',
        dataIndex: 'unrealized_pnl',
        key: 'unrealized_pnl',
        render: (value, record) => (
          <div>
            <Text style={{ color: value >= 0 ? '#3f8600' : '#cf1322' }}>
              {value >= 0 ? '+' : ''}{value.toLocaleString('tr-TR')} TL
            </Text>
            <div>
              <Text 
                size="small" 
                style={{ color: record.unrealized_pnl_pct >= 0 ? '#3f8600' : '#cf1322' }}
              >
                ({record.unrealized_pnl_pct >= 0 ? '+' : ''}{record.unrealized_pnl_pct.toFixed(2)}%)
              </Text>
            </div>
          </div>
        )
      },
      {
        title: 'İşlemler',
        key: 'actions',
        render: (_, record) => (
          <Space>
            <Button size="small" icon={<EyeOutlined />} />
            <Button size="small" icon={<EditOutlined />} />
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Space>
        )
      }
    ];

    return (
      <Card 
        title="Pozisyonlarım" 
        size="small"
        extra={
          <Space>
            <Button 
              type="primary" 
              icon={<PlusOutlined />}
              onClick={() => setAddPositionModal(true)}
            >
              Pozisyon Ekle
            </Button>
            <Button 
              icon={<LineChartOutlined />}
              onClick={updatePrices}
              loading={loading}
            >
              Fiyat Güncelle
            </Button>
          </Space>
        }
      >
        <Table 
          dataSource={positions}
          columns={columns}
          pagination={false}
          size="small"
          scroll={{ x: true }}
        />
      </Card>
    );
  };

  const renderPerformanceAnalysis = () => {
    if (!performanceData) {
      return (
        <Alert
          message="Performans analizi için butona tıklayın"
          type="info"
          showIcon
        />
      );
    }

    const { personal_portfolio_analysis } = performanceData;

    return (
      <Card title="Portföy Analizi" size="small">
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Card size="small" title="Risk Analizi">
              <div style={{ marginBottom: 8 }}>
                <Text>Konsantrasyon Riski: </Text>
                <Tag color={
                  personal_portfolio_analysis?.risk_analysis?.concentration_risk === 'LOW' ? 'green' :
                  personal_portfolio_analysis?.risk_analysis?.concentration_risk === 'MEDIUM' ? 'orange' : 'red'
                }>
                  {personal_portfolio_analysis?.risk_analysis?.concentration_risk || 'N/A'}
                </Tag>
              </div>
              <div style={{ marginBottom: 8 }}>
                <Text>En Büyük Pozisyon: </Text>
                <Text strong>{personal_portfolio_analysis?.risk_analysis?.largest_position_weight || 0}%</Text>
              </div>
              <div>
                <Text>Pozisyon Sayısı: </Text>
                <Text strong>{personal_portfolio_analysis?.risk_analysis?.number_of_positions || 0}</Text>
              </div>
            </Card>
          </Col>
          
          <Col xs={24} md={12}>
            <Card size="small" title="Öneriler">
              <List
                size="small"
                dataSource={personal_portfolio_analysis?.portfolio_recommendations || []}
                renderItem={(item) => (
                  <List.Item>
                    <Text>{item}</Text>
                  </List.Item>
                )}
              />
            </Card>
          </Col>
        </Row>
      </Card>
    );
  };

  const renderRecommendations = () => {
    if (!recommendations) {
      return (
        <Alert
          message="Kişisel öneriler için butona tıklayın"
          type="info"
          showIcon
        />
      );
    }

    const { personal_recommendations } = recommendations;

    return (
      <Row gutter={16}>
        <Col xs={24} md={12}>
          <Card title="Pozisyon Önerileri" size="small">
            <List
              dataSource={personal_recommendations?.position_specific || []}
              renderItem={(item) => (
                <List.Item>
                  <div style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                      <Text strong>{item.symbol}</Text>
                      <Tag color={
                        item.action === 'PARTIAL_SELL' ? 'orange' :
                        item.action === 'HOLD' ? 'blue' :
                        item.action === 'REVIEW_STOP_LOSS' ? 'red' : 'default'
                      }>
                        {item.action}
                      </Tag>
                    </div>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {item.reason}
                    </Text>
                    <div style={{ marginTop: 4 }}>
                      <Text>Getiri: </Text>
                      <Text style={{ color: item.current_return >= 0 ? '#3f8600' : '#cf1322' }}>
                        {item.current_return >= 0 ? '+' : ''}{item.current_return?.toFixed(2) || 0}%
                      </Text>
                    </div>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        
        <Col xs={24} md={12}>
          <Card title="Genel Öneriler" size="small">
            <List
              dataSource={personal_recommendations?.general_recommendations || []}
              renderItem={(item) => (
                <List.Item>
                  <div>
                    <Tag color={
                      item.priority === 'HIGH' ? 'red' :
                      item.priority === 'MEDIUM' ? 'orange' : 'blue'
                    }>
                      {item.priority}
                    </Tag>
                    <Text style={{ marginLeft: 8 }}>{item.message}</Text>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    );
  };

  const renderAddPositionModal = () => (
    <Modal
      title="Yeni Pozisyon Ekle"
      open={addPositionModal}
      onCancel={() => setAddPositionModal(false)}
      footer={null}
      width={600}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={addPosition}
      >
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item 
              label="Sembol" 
              name="symbol" 
              rules={[{ required: true, message: 'Sembol gerekli' }]}
            >
              <Select placeholder="Hisse seçin">
                <Option value="THYAO">THYAO - Türk Hava Yolları</Option>
                <Option value="AKBNK">AKBNK - Akbank</Option>
                <Option value="BIMAS">BIMAS - BİM</Option>
                <Option value="ASELS">ASELS - Aselsan</Option>
                <Option value="KCHOL">KCHOL - Koç Holding</Option>
                <Option value="TCELL">TCELL - Turkcell</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item 
              label="Varlık Türü" 
              name="asset_type" 
              initialValue="stock"
            >
              <Select>
                <Option value="stock">Hisse Senedi</Option>
                <Option value="fund">Fon</Option>
                <Option value="bond">Tahvil</Option>
                <Option value="crypto">Kripto</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item 
              label="Miktar" 
              name="quantity" 
              rules={[{ required: true, message: 'Miktar gerekli' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                min={1}
                placeholder="Adet"
              />
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item 
              label="Alış Fiyatı (TL)" 
              name="purchase_price" 
              rules={[{ required: true, message: 'Alış fiyatı gerekli' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                min={0.01}
                step={0.01}
                placeholder="Fiyat"
              />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item 
          label="Alış Tarihi" 
          name="purchase_date"
        >
          <DatePicker style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              Pozisyon Ekle
            </Button>
            <Button onClick={() => setAddPositionModal(false)}>
              İptal
            </Button>
          </Space>
        </Form.Item>
      </Form>
    </Modal>
  );

  if (loading && !portfolioData) {
    return (
      <div style={{ textAlign: 'center', padding: 50 }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text>Portföy verileri yükleniyor...</Text>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <PieChartOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Kişisel Portföy</Title>
        </Space>
      </div>

      <Tabs defaultActiveKey="positions">
        <TabPane tab="Pozisyonlarım" key="positions">
          {renderPortfolioSummary()}
          {renderPositionsTable()}
        </TabPane>
        
        <TabPane tab="Performans Analizi" key="performance">
          <div style={{ marginBottom: 16 }}>
            <Button 
              type="primary" 
              onClick={analyzePortfolio}
              loading={loading}
            >
              Portföy Analizi Yap
            </Button>
          </div>
          {renderPerformanceAnalysis()}
        </TabPane>
        
        <TabPane tab="Öneriler" key="recommendations">
          <div style={{ marginBottom: 16 }}>
            <Button 
              type="primary" 
              onClick={getRecommendations}
              loading={loading}
            >
              Kişisel Öneriler Al
            </Button>
          </div>
          {renderRecommendations()}
        </TabPane>
      </Tabs>

      {renderAddPositionModal()}

      <Card 
        title="Kişisel Portföy Hakkında" 
        size="small" 
        style={{ marginTop: 24 }}
      >
        <Alert
          message="Kişisel Portföy Özellikleri"
          description={
            <ul style={{ marginBottom: 0 }}>
              <li>Kendi alış fiyatlarınızla kar/zarar takibi</li>
              <li>Pozisyon bazlı öneriler ve uyarılar</li>
              <li>Risk analizi ve portföy optimizasyon önerileri</li>
              <li>Gerçek zamanlı fiyat güncellemeleri</li>
              <li>Vergi optimizasyonu fırsatları</li>
            </ul>
          }
          type="info"
          showIcon
        />
      </Card>
    </div>
  );
};

export default PersonalPortfolioPanel;