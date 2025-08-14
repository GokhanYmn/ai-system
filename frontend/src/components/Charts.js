import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Select, Typography, Space } from 'antd';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BarChartOutlined, LineChartOutlined, PieChartOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

const Charts = ({ systemData }) => {
  const [timeRange, setTimeRange] = useState('24h');
  
  // Mock performance data
  const performanceData = [
    { time: '09:00', value: 1200000, agents: 6, success: 95 },
    { time: '10:00', value: 1205000, agents: 7, success: 98 },
    { time: '11:00', value: 1198000, agents: 7, success: 92 },
    { time: '12:00', value: 1215000, agents: 6, success: 89 },
    { time: '13:00', value: 1225000, agents: 7, success: 96 },
    { time: '14:00', value: 1210000, agents: 7, success: 94 },
    { time: '15:00', value: 1235000, agents: 6, success: 91 },
    { time: '16:00', value: 1250000, agents: 7, success: 97 }
  ];

  // Agent task distribution
  const agentTaskData = [
    { name: 'News', value: 15, color: '#8884d8' },
    { name: 'Financial', value: 25, color: '#82ca9d' },
    { name: 'Technical', value: 20, color: '#ffc658' },
    { name: 'Data', value: 18, color: '#ff7300' },
    { name: 'Decision', value: 12, color: '#00ff00' },
    { name: 'Trading', value: 10, color: '#ff0000' }
  ];

  // Success rate data
  const successRateData = [
    { agent: 'News', rate: 98 },
    { agent: 'Financial', rate: 95 },
    { agent: 'Technical', rate: 92 },
    { agent: 'Data', rate: 97 },
    { agent: 'Decision', rate: 89 },
    { agent: 'Trading', rate: 94 }
  ];

  // Market sectors data
  const sectorData = [
    { sector: 'Teknoloji', performance: 5.2 },
    { sector: 'Finans', performance: -2.1 },
    { sector: 'Enerji', performance: 3.8 },
    { sector: 'Sanayi', performance: 1.5 },
    { sector: 'Tüketim', performance: -0.8 }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Space>
          <BarChartOutlined style={{ color: '#1890ff', fontSize: 20 }} />
          <Title level={4} style={{ margin: 0 }}>Performans Grafikleri</Title>
        </Space>
        
        <Select 
          value={timeRange} 
          onChange={setTimeRange}
          style={{ width: 120 }}
        >
          <Option value="1h">Son 1 Saat</Option>
          <Option value="24h">Son 24 Saat</Option>
          <Option value="7d">Son 7 Gün</Option>
          <Option value="30d">Son 30 Gün</Option>
        </Select>
      </div>

      <Row gutter={[16, 16]}>
        {/* Portfolio Performance */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <LineChartOutlined style={{ color: '#52c41a' }} />
                <Text>Portföy Performansı</Text>
              </Space>
            }
            size="small"
          >
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#52c41a" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#52c41a" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis tickFormatter={(value) => `${(value/1000000).toFixed(1)}M`} />
                <Tooltip 
                  formatter={(value) => [`${value.toLocaleString('tr-TR')} TL`, 'Değer']}
                  labelFormatter={(label) => `Saat: ${label}`}
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#52c41a" 
                  fillOpacity={1} 
                  fill="url(#colorValue)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* Agent Success Rates */}
        <Col xs={24} lg={12}>
          <Card 
            title={
              <Space>
                <BarChartOutlined style={{ color: '#1890ff' }} />
                <Text>Agent Başarı Oranları</Text>
              </Space>
            }
            size="small"
          >
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={successRateData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="agent" />
                <YAxis domain={[0, 100]} />
                <Tooltip formatter={(value) => [`${value}%`, 'Başarı Oranı']} />
                <Bar dataKey="rate" fill="#1890ff" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* Task Distribution */}
        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <PieChartOutlined style={{ color: '#faad14' }} />
                <Text>Görev Dağılımı</Text>
              </Space>
            }
            size="small"
          >
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={agentTaskData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {agentTaskData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* Sector Performance */}
        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <BarChartOutlined style={{ color: '#722ed1' }} />
                <Text>Sektör Performansı</Text>
              </Space>
            }
            size="small"
          >
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={sectorData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[-5, 10]} />
                <YAxis dataKey="sector" type="category" width={60} />
                <Tooltip formatter={(value) => [`${value}%`, 'Performans']} />
                <Bar 
                  dataKey="performance" 
                  fill={(entry) => entry.performance >= 0 ? '#52c41a' : '#ff4d4f'}
                  radius={[0, 4, 4, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* System Activity */}
        <Col xs={24} lg={8}>
          <Card 
            title={
              <Space>
                <LineChartOutlined style={{ color: '#eb2f96' }} />
                <Text>Sistem Aktivitesi</Text>
              </Space>
            }
            size="small"
          >
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="agents" 
                  stroke="#eb2f96" 
                  strokeWidth={2}
                  dot={{ fill: '#eb2f96', strokeWidth: 2, r: 4 }}
                  name="Aktif Agent"
                />
                <Line 
                  type="monotone" 
                  dataKey="success" 
                  stroke="#52c41a" 
                  strokeWidth={2}
                  dot={{ fill: '#52c41a', strokeWidth: 2, r: 4 }}
                  name="Başarı %"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Charts;