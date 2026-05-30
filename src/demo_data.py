"""
离线验收样本数据
用于无网络/无 API key 环境验证完整日报链路，不用于生产采集。
"""

from datetime import datetime, timedelta


def get_demo_entries():
    now = datetime.utcnow()
    return [
        {
            "title": "Bangladesh garment exports face new tariff pressure in key market",
            "link": "https://example.com/demo/garment-tariff",
            "summary": "Exporters warned that new duty and tariff pressure may affect RMG shipments and buyer orders over the coming quarter.",
            "source": "Demo Business News",
            "pub_date": now.strftime("%m-%d %H:%M"),
            "raw_date": now,
            "item_type": "news",
            "source_type": "demo",
        },
        {
            "title": "Chinese-backed solar park reaches financial close in Bangladesh",
            "link": "https://example.com/demo/solar-project",
            "summary": "A 100MW solar power project reached investment close with Chinese equipment suppliers and local grid connection support.",
            "source": "Demo Energy Desk",
            "pub_date": (now - timedelta(hours=1)).strftime("%m-%d %H:%M"),
            "raw_date": now - timedelta(hours=1),
            "item_type": "news",
            "source_type": "demo",
        },
        {
            "title": "Bangladesh port logistics delay raises supply chain concerns",
            "link": "https://example.com/demo/port-logistics",
            "summary": "Importers reported shipment delays at a major port, creating supply chain risk for machinery and textile raw materials.",
            "source": "Demo Logistics Monitor",
            "pub_date": (now - timedelta(hours=2)).strftime("%m-%d %H:%M"),
            "raw_date": now - timedelta(hours=2),
            "item_type": "news",
            "source_type": "demo",
        },
        {
            "title": "[央行汇率] BDT/USD demo observation",
            "link": "https://example.com/demo/exchange-rate",
            "summary": "孟加拉塔卡(BDT)兑USD汇率待观察，进口成本敏感行业需关注汇率波动。",
            "source": "Demo Macro Data",
            "pub_date": now.strftime("%m-%d %H:%M"),
            "raw_date": now,
            "item_type": "indicator",
            "source_type": "demo",
        },
    ]
