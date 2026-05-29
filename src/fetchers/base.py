"""
抓取器插件基类
所有数据源抓取插件必须继承此类并实现接口
"""
from abc import ABC, abstractmethod
from datetime import datetime


class BaseFetcher(ABC):
    """抓取插件抽象基类"""

    @property
    @abstractmethod
    def source_type(self) -> str:
        """返回插件类型标识，如 'rss', 'api', 'scraper'"""
        pass

    @abstractmethod
    def fetch(self, config: dict, hours: int = 24) -> list:
        """
        抓取新闻的通用接口

        Args:
            config: 该源的配置字典
            hours: 只返回最近 N 小时的新闻

        Returns:
            标准化的新闻条目列表，每条格式：
            [
                {
                    "title": str,
                    "link": str,
                    "summary": str,
                    "source": str,
                    "pub_date": str,  # 格式: "MM-DD HH:MM"
                    "raw_date": datetime,
                }
            ]
        """
        pass

    def _now_str(self) -> str:
        """返回当前时间的字符串格式"""
        return datetime.now().strftime("%m-%d %H:%M")
