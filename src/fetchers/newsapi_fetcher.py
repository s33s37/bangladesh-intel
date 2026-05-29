"""
NewsAPI 抓取插件
通过 newsapi.org 获取结构化新闻，作为 RSS 的补充
免费额度：100 请求/天
"""
import os
from datetime import datetime, timedelta

import requests

from src.fetchers.base import BaseFetcher


class NewsAPIFetcher(BaseFetcher):
    """NewsAPI 新闻聚合抓取器"""

    source_type = "newsapi"
    BASE_URL = "https://newsapi.org/v2/everything"

    def fetch(self, config: dict, hours: int = 24) -> list:
        """
        抓取 NewsAPI
        config 示例：
        {
            "type": "newsapi",
            "name": "NewsAPI-BD-Business",
            "query": "bangladesh business",
            "lang": "en",
            "api_key_env": "NEWSAPI_KEY"  # 从环境变量读取 API Key
        }
        """
        api_key = self._get_api_key(config)
        if not api_key:
            print(f"  [SKIP] [{config.get('name')}] NEWSAPI_KEY 未配置")
            return []

        query = config.get("query", "bangladesh")
        lang = config.get("lang", "en")
        source_name = config.get("name", "NewsAPI")
        from_date = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S")

        try:
            params = {
                "q": query,
                "language": lang,
                "from": from_date,
                "sortBy": "publishedAt",
                "pageSize": 20,
                "apiKey": api_key,
            }
            resp = requests.get(self.BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if data.get("status") != "ok":
                print(f"  [ERROR] [{source_name}] API 错误: {data.get('message', 'unknown')}")
                return []

            entries = []
            for article in data.get("articles", []):
                pub_str = article.get("publishedAt", "")
                try:
                    pub_date = datetime.strptime(pub_str, "%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    pub_date = datetime.utcnow()

                entries.append({
                    "title": article.get("title", "").strip(),
                    "link": article.get("url", ""),
                    "summary": article.get("description", "") or article.get("content", "")[:1500],
                    "source": article.get("source", {}).get("name", source_name),
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                })

            return entries

        except Exception as e:
            print(f"  [ERROR] [{source_name}] {str(e)[:60]}")
            return []

    def _get_api_key(self, config: dict) -> str:
        """从环境变量或配置中获取 API Key"""
        env_var = config.get("api_key_env", "NEWSAPI_KEY")
        api_key = os.environ.get(env_var, "")
        if not api_key:
            api_key = config.get("api_key", "")
        return api_key
