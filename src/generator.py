
"""
孟加拉商业情报日报 - 报告生成模块
将AI分析结果填入HTML模板，生成最终网页
"""

import os
import re
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from src.config import SECTORS


def _cn_digraphs(text):
    """提取中文摘要中的2字重叠词作为特征"""
    tokens = set()
    parts = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    for part in parts:
        for i in range(len(part) - 1):
            tokens.add(part[i:i+2])
    return tokens


def _dedup_items(items):
    """基于中文摘要相似度合并同一事件的多个来源报道"""
    if not items:
        return items

    # 预计算所有 token 集（仅基于中文摘要，不含英文标题）
    item_tokens = []
    for item in items:
        reason = item.get("reason", "")
        if reason == "无AI密钥" or reason.startswith("AI失败"):
            item_tokens.append({f"fallback:{item.get('title', '')}:{item.get('source', '')}"})
            continue
        text = item.get('summary_cn', '')
        tokens = _cn_digraphs(text)
        # 加入摘要整体指纹
        fp = text.replace(' ', '')[:15]
        if len(fp) >= 6:
            tokens.add(fp)
        item_tokens.append(tokens)

    # 按重要性排序（高>中>低），优先保留高质量条目
    priority = {"高": 0, "中": 1, "低": 2}
    ranked = sorted(enumerate(items), key=lambda x: priority.get(x[1].get("importance", "低"), 3))

    kept = []
    kept_tokens = []
    for idx, item in ranked:
        tokens = item_tokens[idx]
        is_dup = False
        for kt in kept_tokens:
            if not tokens or not kt:
                continue
            # Jaccard 相似度 = 交集 / 并集
            overlap = len(tokens & kt) / len(tokens | kt)
            if overlap > 0.30:
                is_dup = True
                break
        if not is_dup:
            kept.append(item)
            kept_tokens.append(tokens)

    # 恢复原始顺序
    return kept


def generate_html(intel_items, output_dir="docs", model_name="deepseek-chat"):
    """
    生成HTML日报报告
    intel_items: processor返回的结构化情报列表
    output_dir: 输出目录
    model_name: 使用的AI模型名（用于页脚展示）
    """
    # 语义去重：合并同一事件的多来源重复报道
    before_dedup = len(intel_items)
    intel_items = _dedup_items(intel_items)
    deduped = before_dedup - len(intel_items)
    if deduped:
        print(f"[GEN] 语义去重: 合并 {deduped} 条重复报道")

    # 加载模板
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    # 统计数据
    total = len(intel_items)
    red_flags = [i for i in intel_items if i.get("red_flag")]
    policy_radar = [i for i in intel_items if i.get("intel_type") == "政策变动"]
    positive_count = len([i for i in intel_items if i.get("impact_cn") == "正面"])

    # 已在顶部固定板块显示的条目ID（避免下方重复）
    top_section_ids = set()
    for e in intel_items:
        if e.get("intel_type") in ("政策变动", "风险事件", "市场数据") or e.get("red_flag"):
            top_section_ids.add(id(e))

    # 按产业分组
    sectors_data = {}
    other_by_type = {}  # "其他"板块按情报类型再分组
    for item in intel_items:
        sec = item.get("sector", "其他")

        # 已在顶部政策雷达/风险预警/风险事件显示的，下方不再重复
        if id(item) in top_section_ids:
            continue

        # "其他"板块只保留重要条目（高/中重要度，或结构化指标数据）
        if sec == "其他":
            imp = item.get("importance", "低")
            is_indicator = item.get("item_type") == "indicator"
            if imp not in ("高", "中") and not is_indicator:
                continue
            # 同时按情报类型分组
            itype = item.get("intel_type", "其他")
            if itype not in other_by_type:
                other_by_type[itype] = []
            other_by_type[itype].append(item)

        if sec not in sectors_data:
            sectors_data[sec] = []
        sectors_data[sec].append(item)

    # 按重要性排序：高 > 中 > 低
    priority = {"高": 0, "中": 1, "低": 2}
    for sec in sectors_data:
        sectors_data[sec].sort(key=lambda x: priority.get(x.get("importance", "低"), 3))
    for itype in other_by_type:
        other_by_type[itype].sort(key=lambda x: priority.get(x.get("importance", "低"), 3))

    # 情报类型排序：市场数据 > 风险事件 > 政策变动 > 其他
    type_order = {"市场数据": 0, "风险事件": 1, "政策变动": 2, "项目中标": 3, "投融资": 4, "供应链": 5, "人事变动": 6, "其他": 7}
    other_type_list = sorted(other_by_type.keys(), key=lambda t: type_order.get(t, 99))

    # 只保留有数据的产业，按预设顺序排列
    sector_list = [s for s in SECTORS if s in sectors_data and sectors_data[s]]

    # 计算期数（基于日期）
    issue_no = datetime.now().strftime("%Y%m%d")[2:]  # 例如 260528

    # 情报类型图标映射
    TYPE_ICONS = {
        "市场数据": "📊", "风险事件": "⚠️", "政策变动": "📜",
        "项目中标": "🏆", "投融资": "💰", "供应链": "🔗",
        "人事变动": "👤", "其他": "📋",
    }

    # 渲染HTML
    html = template.render(
        date=datetime.now().strftime("%Y年%m月%d日"),
        issue_no=issue_no,
        total=total,
        red_count=len(red_flags),
        policy_count=len(policy_radar),
        positive_count=positive_count,
        red_flags=red_flags[:5],  # 最多显示5条预警
        policy_radar=policy_radar[:8],  # 最多显示8条政策
        risk_events=[i for i in intel_items if i.get("intel_type") == "风险事件" and i.get("importance") in ("高", "中")][:10],  # 最多显示10条风险事件
        market_data=[i for i in intel_items if i.get("intel_type") == "市场数据" and (i.get("importance") in ("高", "中") or i.get("item_type") == "indicator")][:10],  # 最多显示10条市场数据
        sectors=sectors_data,
        sector_list=sector_list,
        other_by_type=other_by_type,
        other_type_list=other_type_list,
        type_icons=TYPE_ICONS,
        model_name=model_name
    )

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 写入首页和日期归档
    output_path = os.path.join(output_dir, "index.html")
    archive_path = os.path.join(output_dir, f"report_{datetime.now().strftime('%Y-%m-%d')}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[GEN] Report generated: {output_path}, {archive_path} ({total} items, {len(red_flags)} red flags)")
    return output_path


if __name__ == "__main__":
    test_items = [
        {
            "title": "Test News 1",
            "link": "https://example.com/1",
            "source": "Test",
            "pub_date": "05-28 10:00",
            "sector": "太阳能",
            "intel_type": "政策变动",
            "entities": ["NBR", "IDCOL"],
            "summary_cn": "太阳能设备进口关税全免延期两年",
            "impact_cn": "正面",
            "importance": "高",
            "red_flag": False,
            "reason": "政策红利"
        },
        {
            "title": "Test News 2",
            "link": "https://example.com/2",
            "source": "Test",
            "pub_date": "05-28 09:30",
            "sector": "能源",
            "intel_type": "风险事件",
            "entities": ["BPDB", "达卡工业区"],
            "summary_cn": "达卡工业区限电4小时，纺织企业成本上升",
            "impact_cn": "负面",
            "importance": "高",
            "red_flag": True,
            "reason": "停电危机"
        }
    ]
    generate_html(test_items)
