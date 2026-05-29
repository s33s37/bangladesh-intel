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

# Prompt模板：把孟加拉新闻转化为结构化商业情报
PROMPT_TEMPLATE = """你是一名资深的孟加拉国商业情报分析师，精通中英美产业术语。

任务：对以下新闻进行结构化分析，提取关键商业情报。

可选产业（必须严格从以下列表选择，**请使用中文名称输出**）：
{sectors}

可选情报类型（必须严格从以下列表选择）：
{types}

可选影响判断：正面、中性、负面、待观察
可选重要性：高、中、低

分析要求：
1. 产业判断：根据新闻内容匹配最相关的产业，若无明确匹配则选"其他"
2. 实体提取：提取所有公司名、政府机构名、项目名称、人名
3. 中文摘要：用一句话中文概括核心商业要点（含具体金额/数据）
4. 影响判断：评估对中国企业的潜在影响（正面=机会，负面=风险）
5. 风险标记：若新闻含关税、禁令、罢工、事故、召回、制裁等负面事件，red_flag=true
6. 重要性：高=需24小时内关注，中=需本周关注，低=背景信息

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


def analyze_one(title, content, source_name):
    """
    调用 DeepSeek 分析单条新闻
    """
    try:
        # 构建Prompt
        prompt = PROMPT_TEMPLATE.format(
            sectors="、".join(SECTORS),
            types="、".join(TYPES),
            title=title,
            source=source_name,
            content=content[:2000]  # 限制长度，避免超长
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

        result = analyze_one(
            title=entry["title"],
            content=entry["summary"],
            source_name=entry["source"]
        )

        # 回填链接和时间
        result["link"] = entry["link"]
        result["pub_date"] = entry["pub_date"]

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
