import React from 'react';
import { Tag, Typography } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';
import type { NewsArticle } from '../services/api';
import './NewsCard.css';

const { Text, Paragraph } = Typography;

interface NewsCardProps {
  article: NewsArticle;
  onClick: (article: NewsArticle) => void;
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

const SENTIMENT_CONFIG: Record<string, { color: string; label: string }> = {
  positive: { color: '#52c41a', label: '利好' },
  negative: { color: '#ff4d4f', label: '利空' },
  neutral: { color: '#999', label: '中性' },
};

const formatTime = (dateStr: string): string => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 60) return `${minutes}分钟前`;
  if (hours < 24) return `${hours}小时前`;
  if (days < 7) return `${days}天前`;
  return date.toLocaleDateString('zh-CN');
};

const NewsCard: React.FC<NewsCardProps> = ({ article, onClick }) => {
  const sentimentInfo = SENTIMENT_CONFIG[article.sentiment] || SENTIMENT_CONFIG.neutral;
  const categoryColor = CATEGORY_COLORS[article.category] || CATEGORY_COLORS['未分类'];

  return (
    <div className="news-card" onClick={() => onClick(article)}>
      <div className="news-card-content">
        <div className="news-card-header">
          <Tag color={categoryColor} style={{ marginRight: 8, borderRadius: 4 }}>
            {article.category}
          </Tag>
          {article.sentiment && article.sentiment !== 'neutral' && (
            <Tag color={sentimentInfo.color} style={{ borderRadius: 4 }}>
              {sentimentInfo.label}
            </Tag>
          )}
        </div>

        <Text className="news-card-title" strong>
          {article.title}
        </Text>

        {article.description && (
          <Paragraph className="news-card-desc" ellipsis={{ rows: 2 }}>
            {article.description}
          </Paragraph>
        )}

        <div className="news-card-footer">
          <Text className="news-card-source">{article.source}</Text>
          <Text className="news-card-time">
            <ClockCircleOutlined style={{ marginRight: 4 }} />
            {formatTime(article.published_at)}
          </Text>
        </div>

        {article.keywords && article.keywords.length > 0 && (
          <div className="news-card-keywords">
            {article.keywords.slice(0, 3).map((kw, i) => (
              <Tag key={i} className="keyword-tag">{kw}</Tag>
            ))}
          </div>
        )}
      </div>

      {article.image_url && (
        <div className="news-card-image">
          <img
            src={article.image_url}
            alt=""
            onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
          />
        </div>
      )}
    </div>
  );
};

export default NewsCard;
