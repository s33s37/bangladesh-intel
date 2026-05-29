"""
API 数据抓取插件
从金融/贸易/宏观经济数据接口获取结构化数据
支持：世界银行 API、孟加拉央行汇率、Trading Economics（预留）
"""
import os
from datetime import datetime

import requests

from src.fetchers.base import BaseFetcher


class APIFetcher(BaseFetcher):
    """API 数据源抓取器"""

    source_type = "api"

    # 世界银行 API 指标代码（孟加拉国）
    WORLD_BANK_INDICATORS = {
        "NY.GDP.MKTP.KD.ZG": "GDP增长率(年%)",
        "FP.CPI.TOTL.ZG": "通胀率(年%)",
        "BN.CAB.XOKA.GD.ZS": "经常账户余额(占GDP%)",
        "BX.KLT.DINV.WD.GD.ZS": "FDI净流入(占GDP%)",
        "DT.DOD.DECT.GN.ZS": "外债总额(占GNI%)",
        "NE.EXP.GNFS.KD.ZG": "出口增长率(年%)",
        "NE.IMP.GNFS.KD.ZG": "进口增长率(年%)",
        "NY.GNP.PCAP.KD": "人均GNI(现价美元)",
        "SL.UEM.TOTL.ZS": "失业率(%)",
        "EG.USE.ELEC.KH.PC": "人均用电量(kWh)",
        "FB.BNK.CAPA.ZS": "银行资本充足率(%)",
        "NY.GDP.MKTP.CD": "GDP(现价美元)",
        "BX.GSR.MRCH.CD": "商品出口额(美元)",
        "BM.GSR.MRCH.CD": "商品进口额(美元)",
        "FI.RES.TOTL.CD": "外汇储备总额(美元)",
    }

    # 孟加拉央行汇率 API
    BB_EXCHANGE_API = "https://www.bb.org.bd/api/v1/exchange-rate"

    # Trading Economics（预留，需 API Key）
    TE_BASE_URL = "https://api.tradingeconomics.com"

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    def fetch(self, config: dict, hours: int = 24) -> list:
        """
        根据 api_type 分发到不同的数据接口
        config 示例：
        {
            "type": "api",
            "name": "WorldBank-GDP",
            "api_type": "worldbank",
            "indicator": "NY.GDP.MKTP.KD.ZG",
            "country": "BD",
        }
        """
        api_type = config.get("api_type", "worldbank")

        if api_type == "worldbank":
            return self._fetch_worldbank(config)
        elif api_type == "bangladesh_bank":
            return self._fetch_bangladesh_bank(config)
        elif api_type == "trading_economics":
            return self._fetch_trading_economics(config)
        else:
            print(f"  [ERROR] [APIFetcher] 未知 api_type: {api_type}")
            return []

    # ==================== 世界银行 API ====================

    def _fetch_worldbank(self, config: dict) -> list:
        """抓取世界银行指标数据"""
        indicator = config.get("indicator", "NY.GDP.MKTP.KD.ZG")
        country = config.get("country", "BD")
        source_name = config.get("name", f"WorldBank-{indicator}")
        label = self.WORLD_BANK_INDICATORS.get(indicator, indicator)

        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=20"

        try:
            resp = requests.get(url, headers=self.DEFAULT_HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if not isinstance(data, list) or len(data) < 2:
                print(f"  [WARN] [WorldBank] {label}: 无数据")
                return []

            entry = None
            for item in data[1]:  # data[1] 包含实际数据，按年份倒序返回
                value = item.get("value")
                year = item.get("date", "")
                if value is None:
                    continue

                # 构建可读的摘要
                try:
                    val_float = float(value)
                    if abs(val_float) < 1000:
                        summary = f"孟加拉{label}为 {val_float:.2f}%（{year}年）"
                    else:
                        summary = f"孟加拉{label}为 {val_float:,.0f}（{year}年）"
                except (ValueError, TypeError):
                    summary = f"孟加拉{label}: {value}（{year}年）"

                entry = {
                    "title": f"[世行数据] 孟加拉{label} ({year})",
                    "link": f"https://data.worldbank.org/indicator/{indicator}?locations={country}",
                    "summary": summary,
                    "source": source_name,
                    "pub_date": f"{year}-12-31 00:00",
                    "raw_date": datetime(int(year), 12, 31) if year.isdigit() else datetime.utcnow(),
                    "item_type": "indicator",
                }
                break

            if entry:
                print(f"  [OK] [WorldBank] {label}: 最新年度数据 1 条")
                return [entry]
            return []

        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] [WorldBank] {label}: {str(e)[:60]}")
            return []

    # ==================== 孟加拉央行汇率 ====================

    def _fetch_bangladesh_bank(self, config: dict) -> list:
        """抓取孟加拉央行汇率数据"""
        source_name = config.get("name", "Bangladesh Bank - Exchange Rate")

        try:
            resp = requests.get(self.BB_EXCHANGE_API, headers=self.DEFAULT_HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            entries = []
            today = datetime.utcnow()

            # 解析汇率数据（格式因 API 版本而异）
            if isinstance(data, list):
                for item in data[:30]:
                    currency = item.get("currency", item.get("code", ""))
                    buy_rate = item.get("buy", item.get("buy_rate", ""))
                    sell_rate = item.get("sell", item.get("sell_rate", ""))
                    cross_rate = item.get("cross", item.get("cross_rate", ""))
                    date_str = item.get("date", item.get("updated", ""))[:10]

                    if not currency:
                        continue

                    pub_date = today
                    if date_str:
                        try:
                            pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                        except ValueError:
                            pass

                    # 构建汇率摘要
                    rate_parts = []
                    if buy_rate:
                        rate_parts.append(f"买入 {buy_rate}")
                    if sell_rate:
                        rate_parts.append(f"卖出 {sell_rate}")
                    if cross_rate:
                        rate_parts.append(f"中间价 {cross_rate}")

                    rate_str = " / ".join(rate_parts) if rate_parts else str(item)
                    summary = f"孟加拉塔卡(BDT)兑{currency}汇率: {rate_str}"

                    entry = {
                        "title": f"[央行汇率] BDT/{currency} ({pub_date.strftime('%m-%d')})",
                        "link": "https://www.bb.org.bd/en/index.php/investor/exchangerate",
                        "summary": summary,
                        "source": source_name,
                        "pub_date": pub_date.strftime("%m-%d %H:%M"),
                        "raw_date": pub_date,
                        "item_type": "indicator",
                    }
                    entries.append(entry)

            elif isinstance(data, dict):
                # 嵌套字典格式
                for key, value in data.items():
                    if isinstance(value, (int, float, str)):
                        if key in ("last_update", "status", "message"):
                            continue
                        entry = {
                            "title": f"[央行数据] {key}: {value}",
                            "link": "https://www.bb.org.bd/",
                            "summary": f"孟加拉央行 {key}: {value}",
                            "source": source_name,
                            "pub_date": today.strftime("%m-%d %H:%M"),
                            "raw_date": today,
                            "item_type": "indicator",
                        }
                        entries.append(entry)

            if entries:
                print(f"  [OK] [Bangladesh Bank] 汇率: {len(entries)} 条")
            else:
                print(f"  [WARN] [Bangladesh Bank] 未解析到汇率数据")
            return entries[:20]

        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] [Bangladesh Bank] 请求失败: {str(e)[:60]}")
            return []

    # ==================== Trading Economics（预留） ====================

    def _fetch_trading_economics(self, config: dict) -> list:
        """抓取 Trading Economics 数据（需 API Key）"""
        api_key = os.environ.get("TRADING_ECONOMICS_KEY", "")
        if not api_key:
            print(f"  [SKIP] [TradingEconomics] 未配置 TRADING_ECONOMICS_KEY")
            return []

        indicator = config.get("indicator", "gdp")
        country = config.get("country", "bangladesh")
        source_name = config.get("name", f"TE-{indicator}")

        url = f"{self.TE_BASE_URL}/country/{country}/indicator/{indicator}?c={api_key}"

        try:
            resp = requests.get(url, headers=self.DEFAULT_HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            entries = []
            for item in data if isinstance(data, list) else [data]:
                title = item.get("Title", item.get("title", indicator))
                value = item.get("Value", item.get("value", ""))
                date_str = item.get("DateTime", item.get("date", ""))[:10]
                summary = f"孟加拉{title}: {value}"

                pub_date = datetime.utcnow()
                if date_str:
                    try:
                        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        pass

                entry = {
                    "title": f"[TE] 孟加拉{title}: {value}",
                    "link": f"https://tradingeconomics.com/bangladesh/{indicator.lower()}",
                    "summary": summary,
                    "source": source_name,
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                    "item_type": "indicator",
                }
                entries.append(entry)

            print(f"  [OK] [TradingEconomics] {indicator}: {len(entries)} 条")
            return entries

        except requests.exceptions.RequestException as e:
            print(f"  [ERROR] [TradingEconomics] {str(e)[:60]}")
            return []
