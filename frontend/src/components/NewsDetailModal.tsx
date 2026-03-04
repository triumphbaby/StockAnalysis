import React, { useEffect, useState } from 'react';
import { Modal, Tag, Typography, Space, Button, Spin, Divider } from 'antd';
import {
  ClockCircleOutlined,
  UserOutlined,
  LinkOutlined,
  TagsOutlined,
} from '@ant-design/icons';
import type { NewsArticle } from '../services/api';
import { fetchNewsDetail } from '../services/api';

const { Title, Text, Paragraph } = Typography;

interface NewsDetailModalProps {
  article: NewsArticle | null;
  visible: boolean;
  onClose: () => void;
}

const CATEGORY_COLORS: Record<string, string> = {
  '宏观经济': '#1890ff',
  '行业动态': '#52c41a',
  '公司公告': '#faad14',
  '市场评论': '#722ed1',
  '政策法规': '#eb2f96',
  '国际财经': '#13c2c2',
  '未分类': '#666',
};

const SENTIMENT_LABELS: Record<string, { color: string; label: string }> = {
  positive: { color: '#52c41a', label: '利好' },
  negative: { color: '#ff4d4f', label: '利空' },
  neutral: { color: '#999', label: '中性' },
};

const formatDateTime = (dateStr: string): string => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const NewsDetailModal: React.FC<NewsDetailModalProps> = ({ article, visible, onClose }) => {
  const [detail, setDetail] = useState<NewsArticle | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (article && visible) {
      loadDetail(article.id);
    }
  }, [article, visible]);

  const loadDetail = async (id: number) => {
    setLoading(true);
    try {
      const data = await fetchNewsDetail(id);
      setDetail(data);
    } catch {
      // Fall back to the list data
      setDetail(article);
    } finally {
      setLoading(false);
    }
  };

  const data = detail || article;
  if (!data) return null;

  const sentimentInfo = SENTIMENT_LABELS[data.sentiment] || SENTIMENT_LABELS.neutral;

  return (
    <Modal
      open={visible}
      onCancel={onClose}
      footer={null}
      width={720}
      style={{ top: 40 }}
      styles={{
        body: { maxHeight: '75vh', overflowY: 'auto', padding: '24px' },
      }}
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          {/* Category + Sentiment */}
          <Space wrap style={{ marginBottom: 12 }}>
            <Tag color={CATEGORY_COLORS[data.category] || '#666'}>{data.category}</Tag>
            <Tag color={sentimentInfo.color}>{sentimentInfo.label}</Tag>
            <Tag color="blue">
              重要度: {data.importance_score?.toFixed(0) || '--'}
            </Tag>
          </Space>

          {/* Title */}
          <Title level={4} style={{ marginBottom: 16 }}>{data.title}</Title>

          {/* Meta info */}
          <Space split={<Divider type="vertical" />} wrap style={{ marginBottom: 16 }}>
            <Text type="secondary">
              <UserOutlined style={{ marginRight: 4 }} />
              {data.author || data.source || '未知来源'}
            </Text>
            <Text type="secondary">
              <ClockCircleOutlined style={{ marginRight: 4 }} />
              {formatDateTime(data.published_at)}
            </Text>
            <Text type="secondary">{data.source}</Text>
          </Space>

          {/* Image */}
          {data.image_url && (
            <div style={{ marginBottom: 16, borderRadius: 8, overflow: 'hidden' }}>
              <img
                src={data.image_url}
                alt=""
                style={{ width: '100%', maxHeight: 300, objectFit: 'cover' }}
                onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
              />
            </div>
          )}

          {/* Content */}
          <Paragraph style={{ fontSize: 15, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
            {data.content || data.description || '暂无详细内容'}
          </Paragraph>

          {/* Keywords */}
          {data.keywords && data.keywords.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <Text type="secondary"><TagsOutlined style={{ marginRight: 4 }} />关键词: </Text>
              {data.keywords.map((kw, i) => (
                <Tag key={i} color="blue" style={{ marginBottom: 4 }}>{kw}</Tag>
              ))}
            </div>
          )}

          {/* External link */}
          {data.url && (
            <div style={{ marginTop: 20, textAlign: 'center' }}>
              <Button
                type="primary"
                icon={<LinkOutlined />}
                href={data.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                查看原文
              </Button>
            </div>
          )}
        </>
      )}
    </Modal>
  );
};

export default NewsDetailModal;
