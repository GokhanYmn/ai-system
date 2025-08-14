import React from 'react';
import { Card, List, Badge, Progress, Tooltip } from 'antd';
import { RobotOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';

const AgentStatus = ({ agents }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
      case 'ready':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'working':
        return <ClockCircleOutlined style={{ color: '#1890ff' }} />;
      default:
        return <RobotOutlined style={{ color: '#faad14' }} />;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
      case 'ready':
        return 'success';
      case 'working':
        return 'processing';
      default:
        return 'default';
    }
  };

  return (
    <Card title="🤖 Agent Durumları" size="small">
      <List
        itemLayout="horizontal"
        dataSource={Object.entries(agents || {})}
        renderItem={([agentName, agentInfo]) => (
          <List.Item>
            <List.Item.Meta
              avatar={getStatusIcon(agentInfo.status)}
              title={
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span>{agentName.replace('_agent', '').toUpperCase()}</span>
                  <Badge status={getStatusBadge(agentInfo.status)} text={agentInfo.status} />
                </div>
              }
              description={
                <div>
                  <div style={{ marginBottom: 4 }}>
                    Görevler: {agentInfo.task_count || 0}
                  </div>
                  <Tooltip title={`Başarı Oranı: %${agentInfo.success_rate || 0}`}>
                    <Progress 
                      percent={agentInfo.success_rate || 0} 
                      size="small" 
                      status={agentInfo.success_rate > 80 ? 'success' : agentInfo.success_rate > 60 ? 'active' : 'exception'}
                    />
                  </Tooltip>
                </div>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  );
};

export default AgentStatus;