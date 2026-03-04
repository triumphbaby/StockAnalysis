"""
News Article Data Model
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Date, Index
from sqlalchemy.sql import func
from app.database import Base


class NewsArticle(Base):
    """
    News article table for storing collected financial news.
    """
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, comment="新闻标题")
    description = Column(Text, comment="新闻摘要")
    content = Column(Text, comment="新闻正文")
    source = Column(String(100), comment="来源名称")
    author = Column(String(200), comment="作者")
    url = Column(String(1000), unique=True, comment="原文链接")
    image_url = Column(String(1000), comment="封面图片URL")

    # Classification
    category = Column(String(50), index=True, default="未分类", comment="分类(宏观经济/行业动态/公司公告/市场评论/政策法规/国际财经)")
    sentiment = Column(String(20), comment="情感倾向(positive/negative/neutral)")
    keywords = Column(Text, comment="关键词(JSON数组)")
    importance_score = Column(Float, default=50.0, comment="重要度评分(0-100)")

    # Timestamps
    published_at = Column(DateTime(timezone=True), index=True, comment="发布时间")
    collected_at = Column(DateTime(timezone=True), server_default=func.now(), comment="采集时间")

    __table_args__ = (
        Index('idx_news_published_at', 'published_at'),
        Index('idx_news_category', 'category'),
        Index('idx_news_source', 'source'),
        Index('idx_news_category_published', 'category', 'published_at'),
        {'comment': '新闻资讯表'}
    )

    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title={self.title[:30]}...)>"

    def to_dict(self):
        """Convert to dictionary for API response."""
        import json
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "source": self.source,
            "author": self.author,
            "url": self.url,
            "image_url": self.image_url,
            "category": self.category,
            "sentiment": self.sentiment,
            "keywords": json.loads(self.keywords) if self.keywords else [],
            "importance_score": self.importance_score,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "collected_at": self.collected_at.isoformat() if self.collected_at else None,
        }

    def to_list_dict(self):
        """Compact dict for list views (omits full content)."""
        import json
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "author": self.author,
            "url": self.url,
            "image_url": self.image_url,
            "category": self.category,
            "sentiment": self.sentiment,
            "keywords": json.loads(self.keywords) if self.keywords else [],
            "importance_score": self.importance_score,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }
