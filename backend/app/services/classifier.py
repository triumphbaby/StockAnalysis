"""
News Classifier - Strategy Pattern

Phase 1: Rule-based keyword matching
Phase 2: AI-assisted classification (future)
Phase 3: Autonomous classification (future)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)

# Category definitions
CATEGORIES = [
    "宏观经济",
    "行业动态",
    "公司公告",
    "市场评论",
    "政策法规",
    "国际财经",
]

DEFAULT_CATEGORY = "未分类"


class BaseClassifier(ABC):
    """Abstract base class for news classifiers."""

    @abstractmethod
    def classify(self, title: str, content: str = "") -> str:
        """
        Classify a single article.

        Args:
            title: Article title
            content: Article content/description

        Returns:
            Category string
        """
        pass

    def batch_classify(self, articles: List[Dict]) -> List[Dict]:
        """
        Classify multiple articles.

        Args:
            articles: List of article dicts with 'title' and 'description'/'content'

        Returns:
            Same list with 'category' field added
        """
        for article in articles:
            title = article.get("title", "")
            content = article.get("description", "") + " " + article.get("content", "")
            article["category"] = self.classify(title, content)
        return articles


class RuleBasedClassifier(BaseClassifier):
    """
    Rule-based classifier using keyword matching.
    Fast and reliable for clear-cut categorization.
    """

    # Keywords mapped to categories, ordered by priority
    RULES: List[Tuple[str, List[str]]] = [
        ("政策法规", [
            "政策", "法规", "监管", "央行", "证监会", "银保监",
            "regulation", "policy", "SEC", "federal reserve",
            "央行", "国务院", "人民银行", "发改委", "财政部",
            "法案", "条例", "通知", "意见", "办法",
        ]),
        ("公司公告", [
            "公告", "年报", "季报", "财报", "分红", "配股", "增发",
            "并购", "收购", "重组", "上市", "IPO", "退市",
            "earnings", "dividend", "acquisition", "merger", "IPO",
            "营收", "利润", "业绩", "盈利", "亏损",
        ]),
        ("宏观经济", [
            "GDP", "CPI", "PPI", "PMI", "通胀", "通缩",
            "利率", "汇率", "就业", "失业", "贸易",
            "inflation", "interest rate", "unemployment", "trade",
            "经济增长", "货币政策", "财政政策", "宏观",
        ]),
        ("国际财经", [
            "美股", "纳斯达克", "道琼斯", "标普", "华尔街",
            "NASDAQ", "S&P", "Dow Jones", "Wall Street",
            "欧洲", "日本", "亚太", "全球", "国际",
            "global", "international", "European", "Asian",
            "美联储", "欧央行", "日央行",
        ]),
        ("行业动态", [
            "行业", "板块", "赛道", "产业链", "供应链",
            "新能源", "半导体", "芯片", "AI", "人工智能",
            "医药", "房地产", "消费", "科技", "银行",
            "industry", "sector", "technology", "energy",
            "电动车", "光伏", "储能", "锂电",
        ]),
        ("市场评论", [
            "大盘", "走势", "分析", "预测", "展望",
            "涨停", "跌停", "牛市", "熊市", "震荡",
            "market", "analysis", "outlook", "forecast",
            "策略", "观点", "研报", "评论", "解读",
        ]),
    ]

    def classify(self, title: str, content: str = "") -> str:
        """Classify by keyword matching. Title matches weighted higher."""
        text_lower = (title + " " + content).lower()
        title_lower = title.lower()

        best_category = DEFAULT_CATEGORY
        best_score = 0

        for category, keywords in self.RULES:
            score = 0
            for keyword in keywords:
                kw = keyword.lower()
                # Title match: 3 points, content match: 1 point
                if kw in title_lower:
                    score += 3
                elif kw in text_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_category = category

        return best_category


class ClassifierFactory:
    """Factory to create classifier instances based on configuration."""

    _classifiers = {
        "rule": RuleBasedClassifier,
        # "ai": AIClassifier,  # Phase 2
        # "autonomous": AutonomousClassifier,  # Phase 3
    }

    @classmethod
    def create(cls, classifier_type: str = "rule") -> BaseClassifier:
        """
        Create a classifier instance.

        Args:
            classifier_type: Type of classifier ("rule", "ai", "autonomous")

        Returns:
            BaseClassifier instance
        """
        classifier_cls = cls._classifiers.get(classifier_type)
        if not classifier_cls:
            logger.warning(f"Unknown classifier type '{classifier_type}', falling back to rule-based")
            classifier_cls = RuleBasedClassifier

        return classifier_cls()

    @classmethod
    def register(cls, name: str, classifier_cls):
        """Register a new classifier type."""
        cls._classifiers[name] = classifier_cls


def analyze_sentiment(title: str, content: str = "") -> str:
    """
    Simple rule-based sentiment analysis.

    Returns: "positive", "negative", or "neutral"
    """
    text = (title + " " + content).lower()

    positive_words = [
        "上涨", "涨停", "利好", "增长", "突破", "新高", "反弹", "回升",
        "surge", "rise", "gain", "bullish", "record", "growth", "profit",
        "牛市", "繁荣", "强劲", "超预期",
    ]
    negative_words = [
        "下跌", "跌停", "利空", "下滑", "暴跌", "新低", "崩盘", "亏损",
        "decline", "fall", "drop", "bearish", "crash", "loss", "recession",
        "熊市", "衰退", "疲软", "不及预期",
    ]

    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def extract_keywords(title: str, content: str = "", max_keywords: int = 5) -> List[str]:
    """
    Simple keyword extraction based on predefined financial terms.
    """
    text = title + " " + content
    # Financial term dictionary
    terms = [
        "A股", "港股", "美股", "沪深", "创业板", "科创板", "北交所",
        "GDP", "CPI", "PPI", "PMI", "利率", "汇率",
        "新能源", "半导体", "人工智能", "AI", "芯片", "光伏", "锂电",
        "医药", "房地产", "消费", "银行", "保险", "证券",
        "茅台", "平安", "宁德", "比亚迪", "腾讯", "阿里",
        "央行", "证监会", "美联储",
        "IPO", "并购", "分红", "回购", "减持", "增持",
    ]

    found = []
    for term in terms:
        if term.lower() in text.lower():
            found.append(term)
            if len(found) >= max_keywords:
                break

    return found
