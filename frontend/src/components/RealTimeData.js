import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Badge, Table } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const RealTimeData = () => {
  const [marketData, setMarketData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock real-time data
    const interval = setInterval(() => {
      const mockData = [
        { symbol: 'THYAO', price: 91.50 + (Math.random() - 0.5) * 2, change: Math.random() * 4 - 2 },
        { symbol: 'AKBNK', price: 45.20 + (Math.random() - 0.5) * 1, change: Math.random() * 3 - 1.5 },
        { symbol: 'BIMAS', price: 185.30 + (Math.random() - 0.5) * 5, change: Math.random() * 5 - 2.5 },
      ];
      setMarketData(mockData);
      setLoading(false);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const columns = [
    {
      title: 'Sembol',
      dataIndex: 'symbol',
      key: 'symbol',
      render: (text) => <strong>{text}</strong>
    },
    {
      title: 'Fiyat',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `₺${price.toFixed(2)}`
    },
    {
      title: 'Değişim',
      dataIndex: 'change',
      key: 'change',
      render: (change) => (
        <span style={{ color: change >= 0 ? '#52c41a' : '#f5222d' }}>
          {change >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          {' '}{change >= 0 ? '+' : ''}{change.toFixed(2)}%
        </span>
      )
    },
    {
      title: 'Durum',
      key: 'status',
      render: () => <Badge status="processing" text="Canlı" />
    }
  ];

  return (
    <Card title="📈 Canlı Piyasa Verileri" loading={loading}>
      <Table 
        dataSource={marketData} 
        columns={columns} 
        pagination={false}
        rowKey="symbol"
        size="small"
      />
    </Card>
  );
};

export default RealTimeData;