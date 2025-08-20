import React, { useState } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Form, 
  Input, 
  Select, 
  Button, 
  Slider, 
  InputNumber,
  Alert,
  Descriptions,
  Progress,
  Tag,
  Typography,
  Space,
  Spin,
  Divider,
  Table
} from 'antd';
import { 
  DollarOutlined, 
  PieChartOutlined, 
  BarChartOutlined,
  TrophyOutlined,
  SafetyOutlined,
  RocketOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const PortfolioPanel = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [allocationResult, setAllocationResult] = useState(null);
  const [activeTab, setActiveTab] = useState('optimize');

  const optimizePortfolio = async (values) => {
    setLoading(true);
    try {
      const userProfile = {
        risk_tolerance: values.risk_tolerance,
        investment_amount: values.investment_amount,
        age: values.age,
        investment_horizon: values.investment_horizon
      };

      const response = await apiService.optimizePortfolio(userProfile);
      setOptimizationResult(response.data);
    } catch (error) {
      console.error('Portfolio optimization error:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateAllocation = async (values) => {
    setLoading(true);
    try {
      const response = await apiService.calculateAssetAllocation(
        values.risk_tolerance,
        values.investment_amount
      );
      setAllocationResult(response.data);
    } catch (error) {
      console.error('Asset allocation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderOptimizationForm = () => (
    <Card title="Portföy Optimizasyonu" size="small">
      <Form
        form={form}
        layout="vertical"
        onFinish={optimizePortfolio}
        initialValues={{
          risk_tolerance: 'moderate',
          investment_amount: 100000,
          age: 35,
          investment_horizon: 'medium_term'
        }}
      >
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item label="Risk Toleransı" name="risk_tolerance">
              <Select>
                <Option value="conservative">İhtiyatlı risk</Option>
                <Option value="moderate">Orta Risk</Option>
                <Option value="aggressive">Agresif</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item label="Yatırım Tutarı (TL)" name="investment_amount">
              <InputNumber
                style={{ width: '100%' }}
                min={10000}
                max={10000000}
                step={10000}
                formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                parser={value => value.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item label="Yaş" name="age">
              <Slider
                min={18}
                max={70}
                marks={{
                  18: '18',
                  30: '30',
                  45: '45',
                  60: '60',
                  70: '70'
                }}
              />
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item label="Yatırım Vadesi" name="investment_horizon">
              <Select>
                <Option value="short_term">Kısa Vade (1-2 yıl)</Option>
                <Option value="medium_term">Orta Vade (2-5 yıl)</Option>
                <Option value="long_term">Uzun Vade (5+ yıl)</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

        <Form.Item>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={loading}
            block
            icon={<RocketOutlined />}
          >
            Portföyü Optimize Et
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );

  const renderOptimizationResults = () => {
    if (!optimizationResult) return null;

    const { optimized_portfolio, risk_metrics } = optimizationResult;

    const portfolioData = Object.entries(optimized_portfolio).map(([asset, data], index) => ({
      key: index,
      asset: asset.replace(/_/g, ' ').toUpperCase(),
      percentage: data.percentage,
      amount: data.amount,
      recommendation: data.recommendation
    }));

    const columns = [
      {
        title: 'Varlık',
        dataIndex: 'asset',
        key: 'asset',
        render: (text) => <Text strong>{text}</Text>
      },
      {
        title: 'Oran',
        dataIndex: 'percentage',
        key: 'percentage',
        render: (value) => (
          <div>
            <Progress 
              percent={value} 
              size="small" 
              strokeColor="#52c41a"
            />
            <Text>{value}%</Text>
          </div>
        )
      },
      {
        title: 'Tutar (TL)',
        dataIndex: 'amount',
        key: 'amount',
        render: (value) => (
          <Text strong>
            {value.toLocaleString('tr-TR')} TL
          </Text>
        )
      },
      {
        title: 'Öneri',
        dataIndex: 'recommendation',
        key: 'recommendation',
        render: (text) => <Text type="secondary">{text}</Text>
      }
    ];

    return (
      <div style={{ marginTop: 24 }}>
        <Card title="Optimize Edilmiş Portföy" size="small">
          <Table 
            dataSource={portfolioData}
            columns={columns}
            pagination={false}
            size="small"
          />
          
          <Divider />
          
          <Row gutter={16}>
            <Col xs={24} sm={6}>
              <Card size="small">
                <Text type="secondary">Beklenen Getiri</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#52c41a' }}>
                    {risk_metrics.expected_annual_return}
                  </Text>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={6}>
              <Card size="small">
                <Text type="secondary">Risk Skoru</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#faad14' }}>
                    {risk_metrics.risk_score}/5
                  </Text>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={6}>
              <Card size="small">
                <Text type="secondary">Sharpe Oranı</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#1890ff' }}>
                    {risk_metrics.sharpe_ratio.toFixed(2)}
                  </Text>
                </div>
              </Card>
            </Col>
            
            <Col xs={24} sm={6}>
              <Card size="small">
                <Text type="secondary">Çeşitlendirme</Text>
                <div>
                  <Text strong style={{ fontSize: 16, color: '#722ed1' }}>
                    {risk_metrics.diversification_score}/100
                  </Text>
                </div>
              </Card>
            </Col>
          </Row>
          
          <Alert
            style={{ marginTop: 16 }}
            message="Öneriler"
            description={
              <ul>
                {optimizationResult.recommendations?.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            }
            type="info"
            showIcon
          />
        </Card>
      </div>
    );
  };

  const renderQuickAllocation = () => (
    <Card title="Hızlı Varlık Dağılımı" size="small">
      <Form
        layout="inline"
        onFinish={calculateAllocation}
        style={{ marginBottom: 16 }}
      >
        <Form.Item name="risk_tolerance" initialValue="moderate">
          <Select style={{ width: 150 }}>
            <Option value="conservative">İhtiyatlı risk</Option>
            <Option value="moderate">Orta Risk</Option>
            <Option value="aggressive">Agresif</Option>
          </Select>
        </Form.Item>
        
        <Form.Item name="investment_amount" initialValue={50000}>
          <InputNumber
            placeholder="Tutar"
            min={10000}
            max={1000000}
            step={10000}
            formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
          />
        </Form.Item>
        
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Hesapla
          </Button>
        </Form.Item>
      </Form>

      {allocationResult && (
        <div>
          <Row gutter={16}>
            {Object.entries(allocationResult.investment_amounts).map(([asset, data]) => (
              <Col xs={24} sm={12} md={6} key={asset}>
                <Card size="small" style={{ marginBottom: 8 }}>
                  <div style={{ textAlign: 'center' }}>
                    <Text strong>{asset.toUpperCase()}</Text>
                    <div style={{ margin: '8px 0' }}>
                      <Progress
                        type="circle"
                        percent={data.percentage}
                        width={60}
                        strokeColor="#52c41a"
                      />
                    </div>
                    <Text>{data.amount.toLocaleString('tr-TR')} TL</Text>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
          
          <Alert
            message={`Risk Seviyesi: ${allocationResult.risk_level.toUpperCase()}`}
            description={`Beklenen Volatilite: ${allocationResult.expected_volatility}`}
            type="info"
            style={{ marginTop: 16 }}
          />
        </div>
      )}
    </Card>
  );

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <PieChartOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Portföy Yönetimi</Title>
        </Space>
      </div>

      <div style={{ marginBottom: 16 }}>
        <Button.Group>
          <Button 
            type={activeTab === 'optimize' ? 'primary' : 'default'}
            onClick={() => setActiveTab('optimize')}
          >
            Portföy Optimizasyonu
          </Button>
          <Button 
            type={activeTab === 'allocation' ? 'primary' : 'default'}
            onClick={() => setActiveTab('allocation')}
          >
            Hızlı Dağılım
          </Button>
        </Button.Group>
      </div>

      {activeTab === 'optimize' && (
        <div>
          {renderOptimizationForm()}
          {renderOptimizationResults()}
        </div>
      )}

      {activeTab === 'allocation' && renderQuickAllocation()}

      <Card 
        title="Portföy Yönetimi Hakkında" 
        size="small" 
        style={{ marginTop: 24 }}
      >
        <Row gutter={16}>
          <Col xs={24} md={8}>
            <div style={{ textAlign: 'center', padding: 16 }}>
              <TrophyOutlined style={{ fontSize: 32, color: '#faad14' }} />
              <div style={{ marginTop: 8 }}>
                <Text strong>Modern Portföy Teorisi</Text>
                <div style={{ fontSize: 12, color: '#666' }}>
                  Risk-getiri optimizasyonu
                </div>
              </div>
            </div>
          </Col>
          
          <Col xs={24} md={8}>
            <div style={{ textAlign: 'center', padding: 16 }}>
              <SafetyOutlined style={{ fontSize: 32, color: '#52c41a' }} />
              <div style={{ marginTop: 8 }}>
                <Text strong>Risk Yönetimi</Text>
                <div style={{ fontSize: 12, color: '#666' }}>
                  Yaş ve profil bazlı
                </div>
              </div>
            </div>
          </Col>
          
          <Col xs={24} md={8}>
            <div style={{ textAlign: 'center', padding: 16 }}>
              <BarChartOutlined style={{ fontSize: 32, color: '#1890ff' }} />
              <div style={{ marginTop: 8 }}>
                <Text strong>Çeşitlendirme</Text>
                <div style={{ fontSize: 12, color: '#666' }}>
                  Optimal varlık dağılımı
                </div>
              </div>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default PortfolioPanel;