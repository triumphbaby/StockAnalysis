import React, { useState } from 'react';
import { Layout, Card, Row, Col, Descriptions, Typography, Tag, Spin } from 'antd';
import StockSearch from '../components/StockSearch';
import StockChart from '../components/StockChart';
import { get } from '../services/api';

const { Content } = Layout;
const { Title } = Typography;

interface StockInfo {
  stock_code: string;
  name: string;
  fullname?: string;
  market?: string;
  exchange?: string;
  industry?: string;
  area?: string;
  listing_date?: string;
  status?: string;
}

const StockAnalysisPage: React.FC = () => {
  const [selectedStock, setSelectedStock] = useState<StockInfo | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStockSelect = async (stockCode: string) => {
    setLoading(true);
    try {
      const stockInfo = await get(`/api/stocks/${stockCode}`);
      setSelectedStock(stockInfo);
    } catch (error) {
      console.error('获取股票信息失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusTag = (status?: string) => {
    if (!status) return null;

    const statusMap: Record<string, { color: string; text: string }> = {
      active: { color: 'success', text: '正常' },
      suspended: { color: 'warning', text: '停牌' },
      delisted: { color: 'error', text: '退市' }
    };

    const config = statusMap[status] || { color: 'default', text: status };
    return <Tag color={config.color}>{config.text}</Tag>;
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Content style={{ padding: '24px' }}>
        <div className="fade-in" style={{ maxWidth: '1400px', margin: '0 auto' }}>
          {/* Header */}
          <div style={{ marginBottom: '24px' }}>
            <Title level={2} className="text-gradient" style={{ fontSize: '32px' }}>
              📈 股票分析
            </Title>
          </div>

          {/* Search Box */}
          <div style={{ marginBottom: '24px' }}>
            <StockSearch
              onSelect={handleStockSelect}
              placeholder="请输入股票代码或名称进行搜索（如：000001 或 平安银行）"
            />
          </div>

          {/* Stock Info and Chart */}
          {loading ? (
            <Card className="glass-card" style={{ textAlign: 'center', padding: '80px 0' }}>
              <Spin size="large" />
              <div style={{ marginTop: '20px', fontSize: '16px' }}>加载股票信息中...</div>
            </Card>
          ) : selectedStock ? (
            <Row gutter={[16, 16]}>
              {/* Stock Basic Info */}
              <Col span={24}>
                <Card className="glass-card" title="📊 基本信息">
                  <Descriptions column={3} bordered style={{ background: 'transparent' }}>
                    <Descriptions.Item label="股票代码">
                      {selectedStock.stock_code}
                    </Descriptions.Item>
                    <Descriptions.Item label="股票名称">
                      {selectedStock.name}
                    </Descriptions.Item>
                    <Descriptions.Item label="状态">
                      {getStatusTag(selectedStock.status)}
                    </Descriptions.Item>
                    {selectedStock.fullname && (
                      <Descriptions.Item label="公司全称" span={3}>
                        {selectedStock.fullname}
                      </Descriptions.Item>
                    )}
                    <Descriptions.Item label="市场">
                      {selectedStock.market || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="交易所">
                      {selectedStock.exchange || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="行业">
                      {selectedStock.industry || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="地域">
                      {selectedStock.area || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="上市日期">
                      {selectedStock.listing_date || '-'}
                    </Descriptions.Item>
                  </Descriptions>
                </Card>
              </Col>

              {/* K-Line Chart */}
              <Col span={24}>
                <StockChart
                  stockCode={selectedStock.stock_code}
                  stockName={selectedStock.name}
                />
              </Col>
            </Row>
          ) : (
            <Card className="glass-card">
              <div style={{ textAlign: 'center', padding: '100px 0' }}>
                <div style={{ fontSize: '64px', marginBottom: '24px', opacity: 0.6 }}>
                  🔍
                </div>
                <Title level={4} type="secondary">
                  请在上方搜索框中输入股票代码或名称开始分析
                </Title>
                <p style={{ fontSize: '15px', marginTop: '12px', opacity: 0.7 }}>
                  例如：输入 "000001" 或 "平安银行"
                </p>
              </div>
            </Card>
          )}
        </div>
      </Content>
    </Layout>
  );
};

export default StockAnalysisPage;
