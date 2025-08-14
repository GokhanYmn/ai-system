import React, { useState } from 'react';
import { Card, List, Badge, Button, Tooltip, Progress, Space, Typography, Divider } from 'antd';
import { 
  RobotOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  ThunderboltOutlined,
  BarChartOutlined
} from '@ant-design/icons';

const { Text, Title } = Typography;

const AgentStatus = ({ systemData, onRefresh }) => {
  const [selectedAgent, setSelectedAgent] = useState(null);

  const getAgentIcon = (agentType) => {
    const icons = {
      'news_analyzer': '📰',
      'financial_analyzer': '📊',
      'technical_analyzer': '📈',
      'data_processor': '🔄',
      'decision_maker': '🧠',
      'trading_executor': '💼',
      'reinforcement_learner': '📚',
      'orchestrator': '🎯'
    };
    return icons[agentType] || '🤖';
  };

  const getStatusColor = (status) => {
    const colors = {
      'idle': 'success',
      'working': 'processing',
      'error': 'error',
      'registered': 'default'
    };
    return colors[status] || 'default';
  };

  const getSuccessRateColor = (rate) => {
    if (rate >= 90) return '#52c41a';
    if (rate >= 70) return '#faad14';
    return '#ff4d4f';
  };

  const agents = systemData?.status?.agents || {};
  const agentList = Object.entries(agents).map(([name, data]) => ({
    name,
    ...data,
    displayName: name.replace('_agent', '').toUpperCase()
  }));

  return (
    <Card 
      title={
        <Space>
          <RobotOutlined style={{ color: '#1890ff' }} />
          <Title level={4} style={{ margin: 0 }}>Agent Durumları</Title>
        </Space>
      }
      extra={
        <Button 
          type="text" 
          icon={<ThunderboltOutlined />} 
          onClick={onRefresh}
          size="small"
        >
          Yenile
        </Button>
      }
      style={{ height: 600, overflow: 'hidden' }}
      bodyStyle={{ padding: 0, height: 'calc(100% - 60px)', overflow: 'auto' }}
    >
      <List
        dataSource={agentList}
        renderItem={(agent) => (
          <List.Item 
            style={{ 
              padding: '12px 16px',
              cursor: 'pointer',
              background: selectedAgent === agent.name ? '#f6ffed' : 'white'
            }}
            onClick={() => setSelectedAgent(selectedAgent === agent.name ? null : agent.name)}
          >
            <List.Item.Meta
              avatar={
                <div style={{ 
                  fontSize: 24, 
                  display: 'flex', 
                  alignItems: 'center',
                  marginRight: 8
                }}>
                  {getAgentIcon(agent.type)}
                </div>
              }
              title={
                <Space>
                  <Text strong>{agent.displayName}</Text>
                  <Badge 
                    status={getStatusColor(agent.status)} 
                    text={agent.status?.toUpperCase()} 
                  />
                </Space>
              }
              description={
                <Space direction="vertical" size={4} style={{ width: '100%' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      Görev: {agent.task_count || 0}
                    </Text>
                    <Text 
                      style={{ 
                        fontSize: 12, 
                        color: getSuccessRateColor(agent.success_rate) 
                      }}
                    >
                      ✓ {agent.success_rate}%
                    </Text>
                  </div>
                  
                  <Progress 
                    percent={agent.success_rate} 
                    size="small" 
                    strokeColor={getSuccessRateColor(agent.success_rate)}
                    showInfo={false}
                  />
                  
                  {selectedAgent === agent.name && (
                    <div style={{ marginTop: 8, padding: 8, background: '#fafafa', borderRadius: 4 }}>
                      <Divider style={{ margin: '8px 0' }} />
                      <Space direction="vertical" size={4}>
                        <Text style={{ fontSize: 11 }}>
                          <strong>Tip:</strong> {agent.type}
                        </Text>
                        <Text style={{ fontSize: 11 }}>
                          <strong>Yetenekler:</strong> {agent.capabilities?.join(', ') || 'Yükleniyor...'}
                        </Text>
                        <Text style={{ fontSize: 11 }}>
                          <strong>Durum:</strong> {
                            agent.status === 'idle' ? 'Beklemede' :
                            agent.status === 'working' ? 'Çalışıyor' :
                            agent.status === 'registered' ? 'Kayıtlı' : 'Bilinmiyor'
                          }
                        </Text>
                      </Space>
                    </div>
                  )}
                </Space>
              }
            />
          </List.Item>
        )}
      />
      
      {/* Summary Footer */}
      <div style={{ 
        padding: 16, 
        background: '#fafafa', 
        borderTop: '1px solid #f0f0f0',
        position: 'sticky',
        bottom: 0
      }}>
        <Space split={<Divider type="vertical" />}>
          <Tooltip title="Toplam Agent Sayısı">
            <Space>
              <RobotOutlined style={{ color: '#1890ff' }} />
              <Text strong>{agentList.length}</Text>
            </Space>
          </Tooltip>
          
          <Tooltip title="Aktif Agent Sayısı">
            <Space>
              <CheckCircleOutlined style={{ color: '#52c41a' }} />
              <Text strong>
                {agentList.filter(a => a.status !== 'error').length}
              </Text>
            </Space>
          </Tooltip>
          
          <Tooltip title="Ortalama Başarı Oranı">
            <Space>
              <BarChartOutlined style={{ color: '#faad14' }} />
              <Text strong>
                {Math.round(agentList.reduce((acc, a) => acc + (a.success_rate || 0), 0) / agentList.length)}%
              </Text>
            </Space>
          </Tooltip>
        </Space>
      </div>
    </Card>
  );
};

export default AgentStatus;