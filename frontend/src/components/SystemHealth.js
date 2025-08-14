import React from 'react';
import { Card, Row, Col, Progress, Statistic, Timeline, Badge } from 'antd';
import { HeartOutlined, ThunderboltOutlined, CloudOutlined } from '@ant-design/icons';

const SystemHealth = ({ healthData }) => {
  const getHealthColor = (value) => {
    if (value >= 90) return '#52c41a';
    if (value >= 70) return '#faad14';
    return '#f5222d';
  };

  return (
    <Card title={<span><HeartOutlined /> Sistem Sağlığı</span>}>
      <Row gutter={[16, 16]}>
        <Col xs={24} md={8}>
          <Card size="small">
            <Statistic
              title="CPU Kullanımı"
              value={75}
              suffix="%"
              valueStyle={{ color: getHealthColor(75) }}
              prefix={<ThunderboltOutlined />}
            />
            <Progress percent={75} size="small" />
          </Card>
        </Col>
        
        <Col xs={24} md={8}>
          <Card size="small">
            <Statistic
              title="Bellek Kullanımı"
              value={60}
              suffix="%"
              valueStyle={{ color: getHealthColor(60) }}
              prefix={<CloudOutlined />}
            />
            <Progress percent={60} size="small" />
          </Card>
        </Col>
        
        <Col xs={24} md={8}>
          <Card size="small">
            <Statistic
              title="API Yanıt Süresi"
              value={245}
              suffix="ms"
              valueStyle={{ color: getHealthColor(85) }}
            />
            <Progress percent={85} size="small" />
          </Card>
        </Col>
      </Row>

      <Card size="small" title="Son Aktiviteler" style={{ marginTop: 16 }}>
        <Timeline size="small">
          <Timeline.Item color="green">
            <Badge status="success" /> NewsAgent başarıyla KAP verisi aldı
          </Timeline.Item>
          <Timeline.Item color="blue">
            <Badge status="processing" /> TechnicalAgent fiyat analizi yapıyor
          </Timeline.Item>
          <Timeline.Item color="orange">
            <Badge status="warning" /> DataAgent cache yeniliyor
          </Timeline.Item>
        </Timeline>
      </Card>
    </Card>
  );
};

export default SystemHealth;