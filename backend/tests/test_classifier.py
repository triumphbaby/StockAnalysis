"""
Tests for News Classifier Service
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.classifier import (
    RuleBasedClassifier,
    ClassifierFactory,
    analyze_sentiment,
    extract_keywords,
    CATEGORIES,
)


class TestRuleBasedClassifier:
    """Test rule-based news classification."""

    def setup_method(self):
        self.classifier = RuleBasedClassifier()

    def test_policy_classification(self):
        result = self.classifier.classify("央行宣布降准0.5个百分点", "中国人民银行决定下调存款准备金率")
        assert result == "政策法规"

    def test_company_announcement(self):
        result = self.classifier.classify("贵州茅台发布年报：净利润增长15%", "公司公告显示营收创新高")
        assert result == "公司公告"

    def test_macro_economy(self):
        result = self.classifier.classify("中国GDP同比增长5.2%", "国家统计局公布经济增长数据")
        assert result == "宏观经济"

    def test_international_finance(self):
        result = self.classifier.classify("美股三大指数收涨，纳斯达克创新高", "华尔街分析师看好后市")
        assert result == "国际财经"

    def test_industry_dynamics(self):
        result = self.classifier.classify("新能源汽车销量创新高", "电动车行业迎来产业链升级")
        assert result == "行业动态"

    def test_market_commentary(self):
        result = self.classifier.classify("大盘震荡走低，后市如何走", "市场分析人士认为短期需要震荡整理")
        assert result == "市场评论"

    def test_english_classification(self):
        result = self.classifier.classify("S&P 500 hits new high", "Wall Street rally continues")
        assert result == "国际财经"

    def test_unclassified(self):
        result = self.classifier.classify("天气预报", "明天有雨")
        assert result == "未分类"

    def test_batch_classify(self):
        articles = [
            {"title": "央行降息", "description": "货币政策调整", "content": ""},
            {"title": "特斯拉股价上涨", "description": "美股科技股反弹", "content": ""},
        ]
        results = self.classifier.batch_classify(articles)
        assert results[0]["category"] == "政策法规"
        assert results[1]["category"] in ("国际财经", "行业动态")


class TestSentimentAnalysis:
    """Test sentiment analysis."""

    def test_positive_sentiment(self):
        assert analyze_sentiment("股市大涨，牛市来了") == "positive"

    def test_negative_sentiment(self):
        assert analyze_sentiment("股市暴跌，投资者亏损严重") == "negative"

    def test_neutral_sentiment(self):
        assert analyze_sentiment("今日市场成交活跃") == "neutral"


class TestKeywordExtraction:
    """Test keyword extraction."""

    def test_extract_keywords(self):
        keywords = extract_keywords("A股新能源板块大涨，宁德时代领涨", "新能源汽车销量持续增长")
        assert len(keywords) > 0
        assert "新能源" in keywords or "A股" in keywords

    def test_empty_text(self):
        keywords = extract_keywords("", "")
        assert isinstance(keywords, list)


class TestClassifierFactory:
    """Test classifier factory."""

    def test_create_rule_classifier(self):
        classifier = ClassifierFactory.create("rule")
        assert isinstance(classifier, RuleBasedClassifier)

    def test_create_unknown_fallback(self):
        classifier = ClassifierFactory.create("nonexistent")
        assert isinstance(classifier, RuleBasedClassifier)
