import React, { useState } from 'react';
import { Card, Form, Input, Select, Button, Radio, Row, Col, Alert, InputNumber } from 'antd';
import { DollarOutlined, ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const { Option } = Select;

const TradingPanel = () => {
  const [form] = Form.useForm();
  const [orderType, setOrderType] = useState('market');
  const [side, setSide] = useState('buy');

  const onFinish = (values) => {
    console.log('Trading order:', values);
    // API call to execute trade
  };

  return (
    <Card title={<span><DollarOutlined /> İşlem Paneli</span>}>
      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
        initialValues={{
          symbol: 'THYAO',
          orderType: 'market',
          side: 'buy'
        }}
      >
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item label="Sembol" name="symbol">
              <Select>
                <Option value="THYAO">THYAO</Option>
                <Option value="AKBNK">AKBNK</Option>
                <Option value="BIMAS">BIMAS</Option>
              </Select>
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item label="İşlem Tipi" name="side">
              <Radio.Group onChange={(e) => setSide(e.target.value)}>
                <Radio.Button value="buy">
                  <ArrowUpOutlined /> AL
                </Radio.Button>
                <Radio.Button value="sell">
                  <ArrowDownOutlined /> SAT
                </Radio.Button>
              </Radio.Group>
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col xs={24} md={12}>
            <Form.Item label="Miktar" name="quantity">
              <InputNumber 
                style={{ width: '100%' }} 
                min={1} 
                placeholder="Adet"
              />
            </Form.Item>
          </Col>
          
          <Col xs={24} md={12}>
            <Form.Item label="Emir Tipi" name="orderType">
              <Select onChange={setOrderType}>
                <Option value="market">Piyasa Emri</Option>
                <Option value="limit">Limitli Emir</Option>
                <Option value="stop">Stop Emir</Option>
              </Select>
            </Form.Item>
          </Col>
        </Row>

        {orderType !== 'market' && (
          <Form.Item label="Fiyat" name="price">
            <InputNumber 
              style={{ width: '100%' }} 
              min={0} 
              step={0.01}
              placeholder="₺"
            />
          </Form.Item>
        )}

        <Alert
          message="Demo Mod"
          description="Bu işlem simülasyon amaçlıdır. Gerçek para hareket etmez."
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Form.Item>
          <Button 
            type="primary" 
            htmlType="submit" 
            size="large"
            style={{ 
              width: '100%',
              backgroundColor: side === 'buy' ? '#52c41a' : '#f5222d',
              borderColor: side === 'buy' ? '#52c41a' : '#f5222d'
            }}
          >
            {side === 'buy' ? 'AL' : 'SAT'} Emri Ver
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default TradingPanel;