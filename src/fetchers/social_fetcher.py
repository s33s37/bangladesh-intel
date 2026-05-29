"""
社交媒体/即时新闻插件
从 X/Twitter、Telegram 等平台实时抓取孟加拉商业情报

依赖：
  - X/Twitter: pip install tweepy
  - Telegram: pip install telethon
"""
import os
import re
import time as time_module
from datetime import datetime, timedelta

from src.fetchers.base import BaseFetcher


class SocialFetcher(BaseFetcher):
    """
    社交媒体情报抓取器

    支持平台：
      - twitter/x: 通过 Tweepy API v2 抓取指定账号的最新推文
      - telegram: 通过 Telethon 抓取公开频道消息

    config 参数：
      platform: "twitter" | "telegram"
      accounts/channels: 要监控的账号/频道列表
      keywords: 过滤关键词（可选，不填则全部抓取）
      max_items: 每个源最多抓取条数（默认 20）
    """

    source_type = "social"

    # 孟加拉商业情报相关 X/Twitter 账号
    TWITTER_ACCOUNTS = {
        # 媒体/新闻机构
        "dailystar_news": {"name": "The Daily Star", "user_id": "16292291"},
        "tbsnews": {"name": "The Business Standard", "user_id": "3046348613"},
        "bdnews24": {"name": "bdnews24.com", "user_id": "16611208"},
        "dhakatribune": {"name": "Dhaka Tribune", "user_id": "21427723"},
        "financialexpress": {"name": "The Financial Express", "user_id": "22877118"},
        # 财经/商业
        "bgmea": {"name": "BGMEA", "user_id": "289032256"},
        "bgmea_updates": {"name": "BGMEA Updates", "user_id": "123574249"},
        "dsbusiness": {"name": "DS Business", "user_id": "188932684"},
        "tbs_business": {"name": "TBS Business", "user_id": "983763234"},
        "beza_bd": {"name": "BEZA Bangladesh", "user_id": "860746307"},
        "bida_bd": {"name": "BIDA Bangladesh", "user_id": "285282439"},
    }

    # 孟加拉商业情报 Telegram 频道
    TELEGRAM_CHANNELS = {
        "bd_business_news": {"name": "BD Business News", "username": "bd_business_news"},
        "bd_stock_market": {"name": "BD Stock Market", "username": "bdstockmarket"},
        "bgmea_official": {"name": "BGMEA Official", "username": "bgmea_official"},
        "beza_bd": {"name": "BEZA Updates", "username": "beza_bd"},
    }

    # 商业情报相关过滤关键词
    RELEVANT_KEYWORDS = [
        # 中文
        "关税", "投资", "政策", "出口", "进口", "贸易", "招标", "投标",
        "合作", "一带一路", "基建", "能源", "纺织", "成衣", "制造",
        # English
        "tariff", "duty", "investment", "policy", "export", "import",
        "trade", "tender", "bid", "project", "infrastructure", "energy",
        "garment", "textile", "RMG", "manufacturing", "China", "Chinese",
        "BRI", "Bangladesh", "economic", "growth", "GDP", "inflation",
        "market", "stock", "crisis", "shortage", "supply chain",
        "renewable", "solar", "power", "FDI", "joint venture",
        # 孟加拉语关键词
        "বাংলাদেশ", "ব্যবসা", "বাণিজ্য", "অর্থনীতি", "রপ্তানি", "আমদানি",
        "বিনিয়োগ", "শুল্ক", "পোশাক", "তৈরী পোশাক", "শক্তি", "বিদ্যুৎ",
    ]

    def fetch(self, config: dict, hours: int = 24) -> list:
        """根据平台类型分发"""
        platform = config.get("platform", "twitter")
        source_name = config.get("name", "SocialFetcher")

        if platform == "twitter":
            return self._fetch_twitter(config, hours, source_name)
        elif platform == "telegram":
            return self._fetch_telegram(config, hours, source_name)
        else:
            print(f"  [ERROR] [Social] 未知平台: {platform}")
            return []

    # ==================== X / Twitter ====================

    def _fetch_twitter(self, config: dict, hours: int, source_name: str) -> list:
        """通过 Tweepy API v2 抓取推文"""
        try:
            import tweepy
        except ImportError:
            print(f"  [SKIP] [Twitter] tweepy 未安装，请执行: pip install tweepy")
            return []

        bearer_token = os.environ.get("TWITTER_BEARER_TOKEN", "")
        if not bearer_token:
            print(f"  [SKIP] [Twitter] 未配置 TWITTER_BEARER_TOKEN")
            return []

        # 获取目标账号
        account_keys = config.get("accounts", [])
        accounts = []
        for key in account_keys:
            if key in self.TWITTER_ACCOUNTS:
                accounts.append(self.TWITTER_ACCOUNTS[key])
            else:
                accounts.append({"name": key, "user_id": key})

        if not accounts:
            # 默认使用预设账号列表的前 5 个
            accounts = list(self.TWITTER_ACCOUNTS.values())[:5]

        keywords = config.get("keywords", self.RELEVANT_KEYWORDS)
        max_items = config.get("max_items", 20)

        try:
            client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        except Exception as e:
            print(f"  [ERROR] [Twitter] 客户端初始化失败: {str(e)[:60]}")
            return []

        entries = []
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        for account in accounts:
            account_name = account["name"]
            user_id = account["user_id"]

            try:
                # 先通过用户名获取用户 ID（如果 user_id 不是数字而是 @用户名）
                if not user_id.isdigit():
                    user = client.get_user(username=user_id.lstrip("@"))
                    if not user.data:
                        continue
                    user_id = user.data.id

                # 获取用户最近推文
                tweets = client.get_users_tweets(
                    id=user_id,
                    max_results=10,
                    tweet_fields=["created_at", "public_metrics"],
                )

                if not tweets.data:
                    continue

                for tweet in tweets.data:
                    tweet_text = tweet.text.strip()
                    created = tweet.created_at
                    if created.tzinfo:
                        created = created.replace(tzinfo=None)

                    # 时间过滤
                    if created < cutoff:
                        continue

                    # 关键词过滤（如果配置了关键词）
                    if keywords and not any(
                        kw.lower() in tweet_text.lower() for kw in keywords
                    ):
                        continue

                    # 跳过回复和转发
                    if tweet_text.startswith("@") or tweet_text.startswith("RT @"):
                        continue

                    entry = {
                        "title": f"[X/{account_name}] {tweet_text[:80]}...",
                        "link": f"https://x.com/i/web/status/{tweet.id}",
                        "summary": tweet_text[:500],
                        "source": f"X/{account_name}",
                        "pub_date": created.strftime("%m-%d %H:%M"),
                        "raw_date": created,
                    }
                    entries.append(entry)

                    if len(entries) >= max_items:
                        break

            except Exception as e:
                print(f"  [WARN] [Twitter] @{account_name}: {str(e)[:50]}")
                continue

            if len(entries) >= max_items:
                break

        if entries:
            print(f"  [OK] [Twitter] 获取 {len(entries)} 条推文")
        else:
            print(f"  [WARN] [Twitter] 未获取到相关推文")
        return entries

    # ==================== Telegram ====================

    def _fetch_telegram(self, config: dict, hours: int, source_name: str) -> list:
        """通过 Telethon 抓取 Telegram 公开频道消息"""
        try:
            from telethon import TelegramClient
        except ImportError:
            print(f"  [SKIP] [Telegram] telethon 未安装，请执行: pip install telethon")
            return []

        api_id = os.environ.get("TELEGRAM_API_ID", "")
        api_hash = os.environ.get("TELEGRAM_API_HASH", "")
        session_file = os.environ.get("TELEGRAM_SESSION", "social_fetcher.session")

        if not api_id or not api_hash:
            print(f"  [SKIP] [Telegram] 未配置 TELEGRAM_API_ID / TELEGRAM_API_HASH")
            return []

        # 获取目标频道
        channel_keys = config.get("channels", [])
        channels = []
        for key in channel_keys:
            if key in self.TELEGRAM_CHANNELS:
                channels.append(self.TELEGRAM_CHANNELS[key])
            else:
                channels.append({"name": key, "username": key})

        if not channels:
            channels = list(self.TELEGRAM_CHANNELS.values())[:3]

        keywords = config.get("keywords", self.RELEVANT_KEYWORDS)
        max_items = config.get("max_items", 20)
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        entries = []

        try:
            client = TelegramClient(session_file, int(api_id), api_hash)
            await_client = hasattr(client, 'start')

            if await_client:
                # 异步模式
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(client.start())
                    entries = loop.run_until_complete(
                        self._telegram_fetch_messages(client, channels, keywords, cutoff, max_items)
                    )
                    loop.run_until_complete(client.disconnect())
                finally:
                    loop.close()
            else:
                # 同步模式（旧版 Telethon）
                client.start()
                entries = self._telegram_fetch_messages_sync(
                    client, channels, keywords, cutoff, max_items
                )
                client.disconnect()

        except Exception as e:
            print(f"  [ERROR] [Telegram] 连接失败: {str(e)[:80]}")

        if entries:
            print(f"  [OK] [Telegram] 获取 {len(entries)} 条消息")
        else:
            print(f"  [WARN] [Telegram] 未获取到相关消息（需首次交互登录）")
        return entries

    async def _telegram_fetch_messages(self, client, channels, keywords, cutoff, max_items):
        """异步抓取 Telegram 消息"""
        entries = []
        for channel in channels:
            try:
                entity = await client.get_entity(channel["username"])
                async for msg in client.iter_messages(
                    entity, limit=15, offset_date=datetime.utcnow()
                ):
                    if not msg.text:
                        continue
                    created = msg.date.replace(tzinfo=None) if msg.date.tzinfo else msg.date
                    if created < cutoff:
                        continue
                    if keywords and not any(kw.lower() in msg.text.lower() for kw in keywords):
                        continue

                    entries.append({
                        "title": f"[Telegram/{channel['name']}] {msg.text[:80]}...",
                        "link": f"https://t.me/{channel['username']}/{msg.id}",
                        "summary": msg.text[:500],
                        "source": f"Telegram/{channel['name']}",
                        "pub_date": created.strftime("%m-%d %H:%M"),
                        "raw_date": created,
                    })
                    if len(entries) >= max_items:
                        break
            except Exception as e:
                print(f"  [WARN] [Telegram] {channel['name']}: {str(e)[:50]}")
                continue
            if len(entries) >= max_items:
                break
        return entries

    def _telegram_fetch_messages_sync(self, client, channels, keywords, cutoff, max_items):
        """同步方式抓取（兼容旧版 Telethon）"""
        entries = []
        for channel in channels:
            try:
                entity = client.get_entity(channel["username"])
                for msg in client.iter_messages(entity, limit=15):
                    if not msg.text:
                        continue
                    created = msg.date.replace(tzinfo=None) if msg.date.tzinfo else msg.date
                    if created < cutoff:
                        continue
                    if keywords and not any(kw.lower() in msg.text.lower() for kw in keywords):
                        continue
                    entries.append({
                        "title": f"[Telegram/{channel['name']}] {msg.text[:80]}...",
                        "link": f"https://t.me/{channel['username']}/{msg.id}",
                        "summary": msg.text[:500],
                        "source": f"Telegram/{channel['name']}",
                        "pub_date": created.strftime("%m-%d %H:%M"),
                        "raw_date": created,
                    })
                    if len(entries) >= max_items:
                        break
            except Exception:
                continue
            if len(entries) >= max_items:
                break
        return entries


if __name__ == "__main__":
    # 本地测试
    fetcher = SocialFetcher()

    print("=" * 60)
    print("[TEST] Twitter 模式")
    print("=" * 60)
    result = fetcher.fetch({
        "platform": "twitter",
        "name": "Twitter-Test",
        "accounts": ["tbsnews", "dailystar_news"],
        "keywords": ["Bangladesh", "economy", "trade"],
        "max_items": 5,
    })
    print(f"  结果: {len(result)} 条")

    print("\n" + "=" * 60)
    print("[TEST] Telegram 模式")
    print("=" * 60)
    result = fetcher.fetch({
        "platform": "telegram",
        "name": "Telegram-Test",
        "channels": ["bd_business_news"],
        "max_items": 5,
    })
    print(f"  结果: {len(result)} 条")
