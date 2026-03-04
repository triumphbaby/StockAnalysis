import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Layout, Typography, Card, Row, Col, Space, Tag, Spin, Menu, ConfigProvider, theme } from 'antd';
import {
  StockOutlined,
  LineChartOutlined,
  FileTextOutlined,
  ApiOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  HomeOutlined,
  BarChartOutlined,
  RocketOutlined,
} from '@ant-design/icons';
import './App.css';
import { fetchAPIInfo, fetchHealthCheck } from './services/api';
import StockAnalysisPage from './pages/StockAnalysisPage';

const { Header, Content, Footer } = Layout;
const { Title, Text, Paragraph } = Typography;

interface APIInfo {
  api_name: string;
  version: string;
  environment: string;
  features: string[];
  documentation: string;
  timestamp: string;
}

interface HealthStatus {
  status: string;
  database: string;
  redis: string;
  timestamp: string;
}

const HomePage: React.FC<{ apiInfo: APIInfo | null; healthStatus: HealthStatus | null; loading: boolean }> = ({
  apiInfo,
  healthStatus,
  loading
}) => {
  return (
    <Content style={{ padding: '50px' }}>
      <div className="fade-in" style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '100px 0' }}>
            <Spin size="large" />
            <Paragraph style={{ marginTop: '20px' }}>正在连接后端服务...</Paragraph>
          </div>
        ) : (
          <>
            {/* Welcome Section */}
            <Card className="glass-card" style={{ marginBottom: '24px', textAlign: 'center' }}>
              <RocketOutlined style={{ fontSize: '48px', color: '#1890ff', marginBottom: '16px' }} />
              <Title level={2} className="text-gradient">欢迎使用股票分析平台</Title>
              <Paragraph>
                智能化股票研究辅助工具，提供全球股市资讯的自动化采集、智能分析和可视化报告功能
              </Paragraph>
              <Space size="large" style={{ marginTop: '16px' }}>
                <Tag color="blue" icon={<ApiOutlined />}>
                  版本: {apiInfo?.version || '0.1.0'}
                </Tag>
                <Tag color="green" icon={<CheckCircleOutlined />}>
                  环境: {apiInfo?.environment || 'development'}
                </Tag>
                {healthStatus?.status === 'healthy' ? (
                  <Tag color="success" icon={<CheckCircleOutlined />}>
                    服务状态: 正常运行
                  </Tag>
                ) : (
                  <Tag color="error" icon={<CloseCircleOutlined />}>
                    服务状态: 异常
                  </Tag>
                )}
              </Space>
            </Card>

            {/* System Status */}
            <Card className="glass-card" title="系统状态" style={{ marginBottom: '24px' }}>
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={8}>
                  <Card className="glass-card" size="small">
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Text type="secondary">数据库</Text>
                      <Text strong>
                        {healthStatus?.database === 'connected' ? (
                          <Tag color="success">已连接</Tag>
                        ) : (
                          <Tag color="error">未连接</Tag>
                        )}
                      </Text>
                    </Space>
                  </Card>
                </Col>
                <Col xs={24} sm={8}>
                  <Card className="glass-card" size="small">
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Text type="secondary">Redis 缓存</Text>
                      <Text strong>
                        {healthStatus?.redis === 'connected' ? (
                          <Tag color="success">已连接</Tag>
                        ) : (
                          <Tag color="error">未连接</Tag>
                        )}
                      </Text>
                    </Space>
                  </Card>
                </Col>
                <Col xs={24} sm={8}>
                  <Card className="glass-card" size="small">
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Text type="secondary">后端 API</Text>
                      <Text strong>
                        <Tag color="success">运行中</Tag>
                      </Text>
                    </Space>
                  </Card>
                </Col>
              </Row>
            </Card>

            {/* Features Section */}
            <Card className="glass-card" title="核心功能" style={{ marginBottom: '24px' }}>
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} md={8}>
                  <Link to="/analysis" style={{ textDecoration: 'none' }}>
                    <Card
                      className="glass-card glow-effect"
                      size="small"
                      hoverable
                      style={{ textAlign: 'center', height: '100%', position: 'relative', overflow: 'hidden' }}
                    >
                      <StockOutlined style={{ fontSize: '56px', color: '#1890ff', marginBottom: '8px' }} />
                      <Title level={4} style={{ marginTop: '16px', marginBottom: '8px' }}>
                        股票分析
                      </Title>
                      <Text type="secondary">
                        实时行情、K线图、技术指标
                      </Text>
                      <div style={{ marginTop: '12px' }}>
                        <Tag color="success">已上线</Tag>
                      </div>
                    </Card>
                  </Link>
                </Col>
                <Col xs={24} sm={12} md={8}>
                  <Card
                    className="glass-card"
                    size="small"
                    hoverable
                    style={{ textAlign: 'center', height: '100%', opacity: 0.7 }}
                  >
                    <LineChartOutlined style={{ fontSize: '56px', color: '#52c41a', marginBottom: '8px' }} />
                    <Title level={4} style={{ marginTop: '16px', marginBottom: '8px' }}>
                      智能分析
                    </Title>
                    <Text type="secondary">
                      技术面、基本面、综合评分
                    </Text>
                    <div style={{ marginTop: '12px' }}>
                      <Tag color="warning">开发中</Tag>
                    </div>
                  </Card>
                </Col>
                <Col xs={24} sm={12} md={8}>
                  <Card
                    className="glass-card"
                    size="small"
                    hoverable
                    style={{ textAlign: 'center', height: '100%', opacity: 0.7 }}
                  >
                    <FileTextOutlined style={{ fontSize: '56px', color: '#faad14', marginBottom: '8px' }} />
                    <Title level={4} style={{ marginTop: '16px', marginBottom: '8px' }}>
                      研究报告
                    </Title>
                    <Text type="secondary">
                      自动生成、PDF导出
                    </Text>
                    <div style={{ marginTop: '12px' }}>
                      <Tag color="default">规划中</Tag>
                    </div>
                  </Card>
                </Col>
              </Row>
            </Card>

            {/* Available Features List */}
            {apiInfo?.features && (
              <Card className="glass-card" title="已实现功能" style={{ marginBottom: '24px' }}>
                <Space direction="vertical" style={{ width: '100%' }} size="middle">
                  {apiInfo.features.map((feature, index) => (
                    <Text key={index} style={{ fontSize: '15px' }}>
                      <CheckCircleOutlined style={{ color: '#52c41a', marginRight: '12px', fontSize: '16px' }} />
                      {feature}
                    </Text>
                  ))}
                  <Text style={{ fontSize: '15px' }}>
                    <CheckCircleOutlined style={{ color: '#52c41a', marginRight: '12px', fontSize: '16px' }} />
                    股票搜索功能
                  </Text>
                  <Text style={{ fontSize: '15px' }}>
                    <CheckCircleOutlined style={{ color: '#52c41a', marginRight: '12px', fontSize: '16px' }} />
                    K线图可视化
                  </Text>
                </Space>
              </Card>
            )}

            {/* API Documentation Link */}
            <Card className="glass-card" style={{ marginTop: '24px', textAlign: 'center' }}>
              <Space direction="vertical" size="large">
                <ApiOutlined style={{ fontSize: '40px', color: '#1890ff' }} />
                <Title level={4}>API 文档</Title>
                <Paragraph style={{ fontSize: '15px' }}>
                  访问 <a href="/docs" target="_blank" style={{ color: '#1890ff', textDecoration: 'underline' }}>Swagger API 文档</a> 查看完整的 API 接口说明
                </Paragraph>
              </Space>
            </Card>
          </>
        )}
      </div>
    </Content>
  );
};

const AppContent: React.FC = () => {
  const [apiInfo, setApiInfo] = useState<APIInfo | null>(null);
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [info, health] = await Promise.all([
          fetchAPIInfo(),
          fetchHealthCheck(),
        ]);
        setApiInfo(info);
        setHealthStatus(health);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const getSelectedKey = () => {
    if (location.pathname === '/analysis') return 'analysis';
    return 'home';
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '100%' }}>
          <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
            <StockOutlined className="pulse-animation" style={{ fontSize: '32px', color: '#1890ff', marginRight: '16px' }} />
            <Title level={3} className="text-gradient" style={{ margin: 0 }}>
              股票分析平台
            </Title>
          </Link>
          <Menu
            theme="dark"
            mode="horizontal"
            selectedKeys={[getSelectedKey()]}
            style={{ background: 'transparent', flex: 1, justifyContent: 'flex-end', borderBottom: 'none' }}
          >
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">首页</Link>
            </Menu.Item>
            <Menu.Item key="analysis" icon={<BarChartOutlined />}>
              <Link to="/analysis">股票分析</Link>
            </Menu.Item>
          </Menu>
        </div>
      </Header>

      <Routes>
        <Route path="/" element={<HomePage apiInfo={apiInfo} healthStatus={healthStatus} loading={loading} />} />
        <Route path="/analysis" element={<StockAnalysisPage />} />
      </Routes>

      <Footer>
        Stock Analysis Platform ©2026 | 智能化股票研究辅助工具
      </Footer>
    </Layout>
  );
};

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: '#1890ff',
          colorBgBase: '#0a0e27',
          colorBgContainer: 'rgba(26, 31, 58, 0.6)',
          colorBorder: 'rgba(255, 255, 255, 0.1)',
          borderRadius: 8,
          fontSize: 14,
          fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
        },
        components: {
          Layout: {
            headerBg: 'rgba(26, 31, 58, 0.6)',
            footerBg: 'rgba(26, 31, 58, 0.6)',
            bodyBg: 'transparent',
          },
          Card: {
            colorBgContainer: 'rgba(26, 31, 58, 0.6)',
          },
          Menu: {
            darkItemBg: 'transparent',
            darkItemSelectedBg: 'rgba(24, 144, 255, 0.2)',
          },
        },
      }}
    >
      <Router>
        <AppContent />
      </Router>
    </ConfigProvider>
  );
};

export default App;
