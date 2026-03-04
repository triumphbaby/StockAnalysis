import React, { useEffect, useState, useCallback } from 'react';
import { Layout, Input, Spin, Empty, Pagination, Typography, Tag, Space } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import NewsCard from '../components/NewsCard';
import NewsDetailModal from '../components/NewsDetailModal';
import {
  fetchNewsList,
  fetchNewsCategories,
  type NewsArticle,
  type NewsCategory,
} from '../services/api';
import './NewsPage.css';

const { Content } = Layout;
const { Title } = Typography;

const NewsPage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [categories, setCategories] = useState<NewsCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(15);
  const [selectedCategory, setSelectedCategory] = useState<string>('全部');
  const [keyword, setKeyword] = useState('');
  const [searchValue, setSearchValue] = useState('');
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [modalVisible, setModalVisible] = useState(false);

  const loadNews = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, any> = {
        page,
        page_size: pageSize,
      };
      if (selectedCategory && selectedCategory !== '全部') {
        params.category = selectedCategory;
      }
      if (keyword) {
        params.keyword = keyword;
      }

      const result = await fetchNewsList(params);
      setArticles(result.data);
      setTotal(result.total);
    } catch (error) {
      console.error('Failed to load news:', error);
      setArticles([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, selectedCategory, keyword]);

  const loadCategories = async () => {
    try {
      const result = await fetchNewsCategories();
      setCategories(result.data || []);
    } catch {
      setCategories([{ name: '全部', count: 0 }]);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadNews();
  }, [loadNews]);

  const handleSearch = () => {
    setKeyword(searchValue);
    setPage(1);
  };

  const handleCategoryClick = (name: string) => {
    setSelectedCategory(name);
    setPage(1);
  };

  const handleArticleClick = (article: NewsArticle) => {
    setSelectedArticle(article);
    setModalVisible(true);
  };

  return (
    <Content className="news-page">
      <div className="news-container">
        {/* Page Header */}
        <div className="news-header">
          <Title level={3} style={{ margin: 0 }}>财经资讯</Title>
          <div className="news-search-box">
            <Input
              placeholder="搜索新闻标题或内容..."
              prefix={<SearchOutlined />}
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              onPressEnter={handleSearch}
              allowClear
              onClear={() => { setSearchValue(''); setKeyword(''); setPage(1); }}
              style={{ width: 300 }}
            />
          </div>
        </div>

        {/* Category Filter Bar */}
        <div className="news-categories">
          <Space wrap size={[8, 8]}>
            {categories.map((cat) => (
              <Tag
                key={cat.name}
                className={`category-filter-tag ${selectedCategory === cat.name ? 'active' : ''}`}
                onClick={() => handleCategoryClick(cat.name)}
              >
                {cat.name}
                <span className="category-count">{cat.count}</span>
              </Tag>
            ))}
          </Space>
          <div
            className="news-refresh"
            onClick={() => { loadNews(); loadCategories(); }}
            title="刷新"
          >
            <ReloadOutlined spin={loading} />
          </div>
        </div>

        {/* News List */}
        <div className="news-list">
          {loading ? (
            <div className="news-loading">
              <Spin size="large" />
              <div style={{ marginTop: 16 }}>加载资讯中...</div>
            </div>
          ) : articles.length > 0 ? (
            <>
              {articles.map((article) => (
                <NewsCard
                  key={article.id}
                  article={article}
                  onClick={handleArticleClick}
                />
              ))}

              {/* Pagination */}
              {total > pageSize && (
                <div className="news-pagination">
                  <Pagination
                    current={page}
                    total={total}
                    pageSize={pageSize}
                    onChange={(p) => setPage(p)}
                    showSizeChanger={false}
                    showTotal={(t) => `共 ${t} 条资讯`}
                  />
                </div>
              )}
            </>
          ) : (
            <Empty
              description={keyword ? '未找到相关资讯' : '暂无资讯数据，请先采集新闻'}
              style={{ padding: '80px 0' }}
            />
          )}
        </div>
      </div>

      {/* Detail Modal */}
      <NewsDetailModal
        article={selectedArticle}
        visible={modalVisible}
        onClose={() => { setModalVisible(false); setSelectedArticle(null); }}
      />
    </Content>
  );
};

export default NewsPage;
