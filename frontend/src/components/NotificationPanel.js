import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Button, 
  Select, 
  Alert, 
  Statistic, 
  Row, 
  Col,
  Typography,
  Space,
  Tag,
  Modal,
  TimePicker,
  Checkbox,
  message
} from 'antd';
import { 
  BellOutlined, 
  MailOutlined, 
  MessageOutlined,
  ClockCircleOutlined,
  UserAddOutlined,
  SendOutlined,
  NotificationOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const NotificationPanel = () => {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadNotificationStats();
  }, []);

  const loadNotificationStats = async () => {
    try {
      // Demo stats
      setStats({
        notification_stats: {
          total_notifications: 5,
          email_notifications: 3,
          telegram_notifications: 2,
          active_subscribers: 1
        },
        features: {
          email_enabled: false,
          telegram_enabled: false,
          scheduler_active: false
        }
      });
    } catch (error) {
      console.error('Stats yüklenemedi:', error);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Space>
          <BellOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Bildirim Merkezi</Title>
        </Space>
      </div>

      {/* İstatistikler */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Toplam Bildirim"
              value={stats?.notification_stats?.total_notifications || 0}
              prefix={<BellOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="E-mail Gönderimi"
              value={stats?.notification_stats?.email_notifications || 0}
              prefix={<MailOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Telegram Mesajı"
              value={stats?.notification_stats?.telegram_notifications || 0}
              prefix={<MessageOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="Aktif Abone"
              value={stats?.notification_stats?.active_subscribers || 0}
              prefix={<UserAddOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Demo Bilgi */}
      <Card title="📧 Bildirim Sistemi">
        <Alert
          message="Demo Mode"
          description="Notification Agent başarıyla entegre edildi. SMTP ve Telegram ayarları yapıldığında gerçek bildirimler gönderilecek."
          type="info"
          showIcon
        />
        
        <div style={{ marginTop: 16 }}>
          <Space wrap>
            <Button type="primary" icon={<SendOutlined />}>
              Test E-mail
            </Button>
            <Button icon={<MessageOutlined />}>
              Test Telegram
            </Button>
            <Button icon={<UserAddOutlined />}>
              Abone Ekle
            </Button>
          </Space>
        </div>
      </Card>
    </div>
  );
};

export default NotificationPanel;