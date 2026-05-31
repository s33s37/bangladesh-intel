"""
网页直接抓取插件
针对没有 RSS 的网站，通过 requests + BeautifulSoup 抓取列表页
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from src.fetchers.base import BaseFetcher


class WebScraperFetcher(BaseFetcher):
    """网页列表页抓取器"""

    source_type = "scraper"

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    def fetch(self, config: dict, hours: int = 24) -> list:
        """
        抓取网页列表页
        config 示例：
        {
            "type": "scraper",
            "name": "NBR-News",
            "url": "https://nbr.gov.bd/",
            "item_selector": ".news-item h3 a",      # CSS 选择器定位每条新闻
            "title_attr": "text",                    # "text" 或属性名如 "title"
            "link_attr": "href",                     # 链接来源：href 或拼接前缀
            "link_prefix": "",                       # 如果 href 是相对路径，加前缀
            "summary_selector": "",                  # 可选：摘要的选择器
            "encoding": "utf-8"                      # 页面编码
        }
        """
        url = config.get("url", "")
        source_name = config.get("name", "WebScraper")
        encoding = config.get("encoding", "utf-8")

        try:
            resp = requests.get(url, headers=self.DEFAULT_HEADERS, timeout=30)
            resp.encoding = encoding
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            item_selector = config.get("item_selector", "")
            if not item_selector:
                print(f"  [WARN] [{source_name}] 未配置 item_selector")
                return []

            items = soup.select(item_selector)
            entries = []
            for item in items[:15]:  # 最多取 15 条
                title_element = item
                if config.get("title_selector"):
                    title_element = item.select_one(config["title_selector"]) or item

                link_element = item
                if config.get("link_selector"):
                    link_element = item.select_one(config["link_selector"]) or item

                title = self._extract_text(
                    title_element,
                    config.get("title_attr", "text"),
                )
                link = self._extract_link(link_element, config)
                summary = ""
                if config.get("summary_selector"):
                    sum_elem = item.select_one(config["summary_selector"])
                    if sum_elem:
                        summary = sum_elem.get_text(strip=True)

                if title and link:
                    entries.append({
                        "title": title,
                        "link": link,
                        "summary": summary[:1500],
                        "source": source_name,
                        "pub_date": self._now_str(),
                        "raw_date": datetime.utcnow(),
                    })

            return entries

        except Exception as e:
            print(f"  [ERROR] [{source_name}] {str(e)[:60]}")
            return []

    def _extract_text(self, element, attr: str) -> str:
        """从元素中提取文本"""
        if attr == "text":
            return element.get_text(strip=True)
        return element.get(attr, "").strip()

    def _extract_link(self, element, config: dict) -> str:
        """提取并补全链接"""
        link_attr = config.get("link_attr", "href")
        link = element.get(link_attr, "") if element.name == "a" else ""
        if not link:
            # 尝试在子元素中找 a 标签
            a_tag = element.find("a")
            if a_tag:
                link = a_tag.get(link_attr, "")
        prefix = config.get("link_prefix", "")
        if link and not link.startswith(("http://", "https://")):
            link = prefix + link
        return link
