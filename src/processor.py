"""
孟加拉商业情报日报 - AI处理模块
调用 DeepSeek/OpenAI API 对新闻进行结构化分析
"""

import os
import json
from openai import OpenAI
from src.config import SECTORS, TYPES

# 模型选择：
# - deepseek-chat: DeepSeek 通用对话，速度快，性价比高（推荐）
# - gpt-4o-mini: OpenAI fallback
MODEL_NAME = None
client = None


def _read_optional_key(path):
    try:
        with open(os.path.expanduser(path), "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def get_ai_client():
    """
    延迟初始化 AI 客户端，避免 import 阶段因缺少密钥直接崩溃。
    优先 DeepSeek，其次 OpenAI。
    """
    global client, MODEL_NAME
    if client:
        return client

    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "") or _read_optional_key("~/.deepseek_key")
    if deepseek_key:
        MODEL_NAME = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")
        return client

    openai_key = os.environ.get("OPENAI_API_KEY", "") or _read_optional_key("~/.openai_key")
    if openai_key:
        MODEL_NAME = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        client = OpenAI(api_key=openai_key)
        return client

    raise ValueError("未设置 AI 密钥。请配置 DEEPSEEK_API_KEY 或 OPENAI_API_KEY。")


def get_model_name():
    if MODEL_NAME:
        return MODEL_NAME
    try:
        get_ai_client()
    except ValueError:
        return "unconfigured"
    return MODEL_NAME

# AI返回英文产业名 → 中文产业名 映射表
SECTOR_NAME_MAP = {
    "garment": "成衣纺织", "textile": "成衣纺织", "apparel": "成衣纺织", "rmg": "成衣纺织", "clothing": "成衣纺织",
    "infrastructure": "基建", "construction": "基建", "bridge": "基建", "road": "基建",
    "energy": "能源", "power": "能源", "electricity": "能源", "gas": "能源", "lng": "能源",
    "solar": "太阳能", "photovoltaic": "太阳能", "renewable": "太阳能",
    "e-bike": "电动两轮车", "electric two-wheeler": "电动两轮车", "e-motorcycle": "电动两轮车",
    "ev": "电动汽车", "electric vehicle": "电动汽车", "electric car": "电动汽车",
    "pharma": "制药", "pharmaceutical": "制药", "drug": "制药", "medicine": "制药",
    "ict": "ICT电商", "e-commerce": "ICT电商", "software": "ICT电商", "it": "ICT电商", "digital": "ICT电商",
    "jute": "黄麻",
    "leather": "皮革", "tannery": "皮革", "footwear": "皮革",
    "shipbreaking": "船舶拆解", "ship breaking": "船舶拆解", "ship recycling": "船舶拆解",
    "fisheries": "渔业", "fish": "渔业", "aquaculture": "渔业", "shrimp": "渔业",
    "agro": "农产品加工", "agriculture": "农产品加工", "food processing": "农产品加工",
    "ceramic": "陶瓷", "ceramics": "陶瓷", "tile": "陶瓷",
    "furniture": "家具", "wood": "家具",
    "light manufacturing": "轻工制造", "light mfg": "轻工制造", "sm": "轻工制造",
    "shipbuilding": "造船", "ship building": "造船", "vessel": "造船",
    "medical": "医疗器械", "medical device": "医疗器械", "healthcare": "医疗器械",
    "plastic": "塑料", "plastics": "塑料", "polymer": "塑料",
    "appliance": "家电", "appliances": "家电", "electronics": "家电",
    "digital economy": "数字经济", "digital_economy": "数字经济", "blockchain": "数字经济", "ai": "数字经济",
    "others": "其他", "other": "其他", "general": "其他",
}

# 行业关键词提示（帮助AI精准匹配产业）
SECTOR_HINTS = {
    "成衣纺织": "RMG, garment, textile, apparel, clothing, fabric, yarn, knitwear, BGMEA, 服装, 纺织, 成衣, 面料, 出口订单",
    "基建": "bridge, road, highway, metro, railway, port, tunnel, dam, EPC, contractor, tender, 基建, 桥梁, 港口, 铁路, 公路, 隧道, 地铁, 工程, 招标",
    "能源": "power, electricity, gas, LNG, petroleum, BPDB, Petrobangla, blackout, load shedding, power plant, 能源, 电力, 天然气, 电网, 发电, 停电",
    "太阳能": "solar, photovoltaic, PV, renewable, panel, inverter, module, IDCOL, SREDA, 太阳能, 光伏, 新能源, 可再生能源",
    "电动两轮车": "e-bike, electric motorcycle, e-motorcycle, scooter, e-scooter, battery bike, Yadea, AIMA, Walton, BRTA, 电动自行车, 电动车, 电摩, 两轮车",
    "电动汽车": "EV, electric vehicle, charging station, battery, electric car, 电动汽车, 新能源汽车, 充电桩",
    "制药": "pharma, pharmaceutical, drug, medicine, API, generic, vaccine, Square Pharma, Incepta, Beximco, DGDA, 制药, 医药, 药品, 疫苗",
    "ICT电商": "ICT, software, IT, e-commerce, fintech, digital, startup, bKash, Nagad, Daraz, 电商, 互联网, 软件, 信息技术, 科技, 数字化",
    "黄麻": "jute, golden fiber, hessian, sacking, jute bag, 黄麻, 麻制品",
    "皮革": "leather, tannery, footwear, shoe, hide, skin, 皮革, 制鞋, 皮具",
    "船舶拆解": "ship breaking, ship recycling, shipyard, scrap, Chittagong, 拆船, 船舶回收",
    "渔业": "fisheries, fish, shrimp, prawn, aquaculture, seafood, hilsa, 渔业, 水产, 海鲜, 养虾",
    "农产品加工": "agriculture, agro, food processing, rice, sugar, tea, dairy, poultry, frozen food, 农业, 农产品, 食品加工, 粮食",
    "陶瓷": "ceramic, tile, sanitary ware, porcelain, 陶瓷, 瓷砖",
    "家具": "furniture, wood, timber, home decor, 家具, 木材, 家居",
    "轻工制造": "light engineering, manufacturing, SME, machinery, tools, hardware, 轻工, 制造, 五金, 中小企业",
    "造船": "shipbuilding, vessel, naval, shipyard, boat, 造船",
    "医疗器械": "medical device, diagnostic, hospital equipment, surgical, healthcare, 医疗器械, 医疗设备",
    "塑料": "plastic, polymer, PVC, PET, packaging, molding, 塑料, 包装",
    "家电": "appliance, electronics, TV, refrigerator, AC, washing machine, Walton, 家电, 电器",
    "数字经济": "digital economy, AI, blockchain, data center, cloud, smart city, IoT, 5G, 数字经济, 人工智能, 区块链, 智慧城市",
}

# Prompt模板：把孟加拉新闻转化为结构化商业情报
PROMPT_TEMPLATE = """你是一名资深的孟加拉国商业情报分析师，精通中英文产业术语。

任务：对以下新闻进行结构化分析，提取关键商业情报。

可选产业（请从以下列表中选择最匹配的一个，**必须使用中文名称输出**）：
{sectors}

各产业关键词对照（辅助判断）：
{sector_hints}

可选情报类型：
{types}

可选影响判断：正面、中性、负面、待观察
可选重要性：高、中、低

分析要求：
1. **产业判断**：根据新闻标题和内容，匹配最相关的产业。请积极匹配——只要新闻内容与某个产业相关就选该产业，**只有完全无法匹配时才选"其他"**。
2. 实体提取：提取所有公司名、政府机构名、项目名称、人名
3. 中文摘要：用一句话中文概括核心商业要点（含具体金额/数据，50字以内）
4. 影响判断：评估对中国企业的潜在影响（正面=机会，负面=风险）
5. 风险标记：若新闻含关税、禁令、罢工、事故、召回、制裁等负面事件，red_flag=true
6. 重要性：高=需24小时内关注，中=需本周关注，低=背景信息

{sector_hint}

请严格按以下JSON格式输出，不要有任何其他文字：
{{
  "sector": "产业名称",
  "intel_type": "情报类型",
  "entities": ["实体A", "实体B"],
  "summary_cn": "一句话中文摘要（50字以内）",
  "impact_cn": "正面/中性/负面/待观察",
  "importance": "高/中/低",
  "red_flag": true/false,
  "reason": "判断依据（15字以内）"
}}

新闻标题：{title}
新闻来源：{source}
新闻内容：{content}
"""


def _keyword_suggest_sector(title, content):
    """关键词预判产业：返回 (sector_name, confidence) 或 (None, 0)"""
    text = f"{title} {content}".lower()
    best_sector = None
    best_score = 0
    for sector, keywords_str in SECTOR_HINTS.items():
        keywords = [k.strip().lower() for k in keywords_str.replace("，", ",").split(",")]
        score = sum(1 for kw in keywords if kw and kw in text)
        if score > best_score:
            best_score = score
            best_sector = sector
    return best_sector, best_score


def analyze_one(title, content, source_name):
    """
    调用 DeepSeek 分析单条新闻
    """
    try:
        # 关键词预判：给AI提供一个产业建议
        suggested_sector, kw_score = _keyword_suggest_sector(title, content)
        if suggested_sector and kw_score >= 2:
            sector_hint = f"【关键词提示】本条新闻疑似与「{suggested_sector}」相关，请重点确认。"
        else:
            sector_hint = "无"

        # 构建提示文本
        hints_lines = []
        for sec in SECTORS:
            kw = SECTOR_HINTS.get(sec, "")
            hints_lines.append(f"  - {sec}: {kw}")
        hints_str = "\n".join(hints_lines)

        # 构建Prompt
        prompt = PROMPT_TEMPLATE.format(
            sectors="、".join(SECTORS),
            sector_hints=hints_str,
            types="、".join(TYPES),
            title=title,
            source=source_name,
            content=content[:2000],  # 限制长度，避免超长
            sector_hint=sector_hint
        )

        # 调用API
        ai_client = get_ai_client()
        response = ai_client.chat.completions.create(
            model=get_model_name(),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},  # 强制JSON输出
            temperature=0.1,  # 低温度，减少幻觉
            max_tokens=512,
            timeout=30
        )

        # 解析JSON
        result = json.loads(response.choices[0].message.content)

        # 数据校验与清洗
        raw_sector = result.get("sector", "其他")
        if raw_sector not in SECTORS:
            # 尝试通过英文名映射到中文
            mapped = SECTOR_NAME_MAP.get(raw_sector.strip().lower(), "其他")
            result["sector"] = mapped if mapped in SECTORS else "其他"
        if result.get("intel_type") not in TYPES:
            result["intel_type"] = "其他"
        if result.get("impact_cn") not in ["正面", "中性", "负面", "待观察"]:
            result["impact_cn"] = "待观察"
        if result.get("importance") not in ["高", "中", "低"]:
            result["importance"] = "中"
        if not isinstance(result.get("red_flag"), bool):
            result["red_flag"] = False
        if not isinstance(result.get("entities"), list):
            result["entities"] = []

        # 补充字段（供后续使用）
        result["title"] = title
        result["link"] = ""  # 外部填入
        result["source"] = source_name
        result["pub_date"] = ""

        return result

    except Exception as e:
        # 任何异常都返回默认结构，保证流程不中断
        return {
            "sector": "其他",
            "intel_type": "其他",
            "entities": [],
            "summary_cn": f"AI解析异常: {str(e)[:30]}",
            "impact_cn": "待观察",
            "importance": "低",
            "red_flag": False,
            "reason": "解析失败",
            "title": title,
            "link": "",
            "source": source_name,
            "pub_date": ""
        }


def analyze_indicator(entry):
    """
    宏观/汇率等结构化指标不需要再调用大模型，直接转成日报字段。
    """
    return {
        "sector": "其他",
        "intel_type": "市场数据",
        "entities": [entry.get("source", "")],
        "summary_cn": entry.get("summary") or entry.get("title", ""),
        "impact_cn": "待观察",
        "importance": "低",
        "red_flag": False,
        "reason": "结构化数据",
        "title": entry.get("title", ""),
        "link": entry.get("link", ""),
        "source": entry.get("source", ""),
        "pub_date": entry.get("pub_date", ""),
        "item_type": "indicator",
    }


def batch_analyze(entries):
    """
    批量分析新闻条目
    entries: fetcher返回的列表
    """
    results = []
    total = len(entries)

    print(f"[AI] Starting batch analysis: {total} entries")

    for i, entry in enumerate(entries, 1):
        print(f"  [{i}/{total}] Processing: {entry['title'][:50]}...")

        if entry.get("item_type") == "indicator":
            result = analyze_indicator(entry)
        else:
            result = analyze_one(
                title=entry["title"],
                content=entry["summary"],
                source_name=entry["source"]
            )

        # 回填链接和时间
        result["link"] = entry["link"]
        result["pub_date"] = entry["pub_date"]
        result["item_type"] = entry.get("item_type", "news")

        results.append(result)

        # DeepSeek 限速：约 30 RPM，加延迟避免触发
        if i < total and i % 5 == 0:
            print("  [AI] Rate limit protection: sleeping 2s...")
            import time
            time.sleep(2)

    print(f"[AI] Batch complete: {len(results)} entries analyzed")
    return results


def get_top_signals(results, n=3):
    """
    提取Top N重要信号（用于报告头部高亮）
    """
    # 按重要性排序：高 > 中 > 低
    priority = {"高": 0, "中": 1, "低": 2}
    sorted_results = sorted(results, key=lambda x: priority.get(x.get("importance", "低"), 3))

    # 取前N条，且优先取 red_flag=true 或 impact_cn=负面的
    top = []
    for r in sorted_results:
        if r.get("importance") == "高" or r.get("red_flag") or r.get("impact_cn") == "负面":
            top.append(r)
        if len(top) >= n:
            break

    # 如果高优先级不够N条，补中性/正面
    if len(top) < n:
        for r in sorted_results:
            if r not in top:
                top.append(r)
            if len(top) >= n:
                break

    return top[:n]


if __name__ == "__main__":
    # 本地测试
    test_entry = {
        "title": "Bangladesh announces new solar import duty exemption for Chinese panels",
        "summary": "The government has decided to waive all import duties on solar photovoltaic panels and inverters imported from China for the next two years to boost renewable energy capacity.",
        "source": "Test",
        "link": "https://example.com",
        "pub_date": "05-28 10:00"
    }
    result = analyze_one(test_entry["title"], test_entry["summary"], test_entry["source"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
