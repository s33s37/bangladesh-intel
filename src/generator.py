
"""
孟加拉商业情报日报 - 报告生成模块
将AI分析结果填入HTML模板，生成最终网页
"""

import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from src.config import SECTORS


def generate_html(intel_items, output_dir="output", model_name="deepseek-chat"):
    """
    生成HTML日报报告
    intel_items: processor返回的结构化情报列表
    output_dir: 输出目录
    model_name: 使用的AI模型名（用于页脚展示）
    """
    # 加载模板
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    # 统计数据
    total = len(intel_items)
    red_flags = [i for i in intel_items if i.get("red_flag")]
    policy_radar = [i for i in intel_items if i.get("intel_type") == "政策变动"]
    positive_count = len([i for i in intel_items if i.get("impact_cn") == "正面"])

    # 按产业分组
    sectors_data = {}
    for item in intel_items:
        sec = item.get("sector", "其他")
        if sec not in sectors_data:
            sectors_data[sec] = []
        sectors_data[sec].append(item)

    # 按重要性排序：高 > 中 > 低
    priority = {"高": 0, "中": 1, "低": 2}
    for sec in sectors_data:
        sectors_data[sec].sort(key=lambda x: priority.get(x.get("importance", "低"), 3))

    # 只保留有数据的产业，按预设顺序排列
    sector_list = [s for s in SECTORS if s in sectors_data and sectors_data[s]]

    # 计算期数（基于日期）
    issue_no = datetime.now().strftime("%Y%m%d")[2:]  # 例如 260528

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
        sectors=sectors_data,
        sector_list=sector_list,
        model_name=model_name
    )

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[GEN] Report generated: {output_path} ({total} items, {len(red_flags)} red flags)")
    return output_path
        .footer { text-align: center; padding: 24px 16px; font-size: 0.75rem; color: var(--text-light); }
        .footer a { color: var(--info); text-decoration: none; }
        @media (max-width: 480px) { .stats-panel { grid-template-columns: repeat(3, 1fr); } .header h1 { font-size: 1.2rem; } }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #bdc3c7; border-radius: 3px; }
        """

        # 构建完整HTML
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="zh-CN">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
            '    <title>孟加拉商业情报日报 | ' + date_str + '</title>',
            '    <style>' + css + '</style>',
            '</head>',
            '<body>',
            '    <div class="header">',
            '        <h1>孟加拉商业情报日报 <span class="badge-live">LIVE</span></h1>',
            '        <div class="subtitle">服务中国政策制定者 · 智库学者 · 跨境电商从业者</div>',
            '        <div class="date">' + date_str + ' | 共采集 ' + str(stats['total']) + ' 条情报 | 置信度 ' + str(int(stats.get('avg_confidence', 0) * 100)) + '%</div>',
            '    </div>',
            '    <div class="container">',
            stats_panel,
            risk_section,
            policy_section,
            positive_section,
            '        <div style="margin: 20px 0; text-align: center; font-size: 0.85rem; color: var(--text-light);">',
            '            —— 分产业详细动态 ——',
            '        </div>',
            industry_sections,
            '        <div class="footer">',
            '            <p>孟加拉商业情报日报系统 | 自动生成于 ' + datetime.now().strftime("%Y-%m-%d %H:%M") + '</p>',
            '            <p>数据来源: 50+孟加拉及国际媒体RSS | AI分析模型: GPT-4o-mini / DeepSeek</p>',
            '            <p>本站仅供研究参考，不构成投资建议</p>',
            '        </div>',
            '    </div>',
            '</body>',
            '</html>'
        ]

        return "\n".join(html_parts)

    def _build_section(self, title, section_class, items, max_items=10, empty_msg="暂无数据"):
        """构建区域HTML"""
        if not items:
            return '<div class="section ' + section_class + '"><div class="section-header">' + title + '</div><div class="section-content"><div class="empty-msg">' + empty_msg + '</div></div></div>'

        cards = ""
        for item in items[:max_items]:
            cards += self._build_card(item)

        return '<div class="section ' + section_class + '"><div class="section-header">' + title + ' (' + str(len(items[:max_items])) + ')</div><div class="section-content">' + cards + '</div></div>'

    def _build_industry_section(self, ind_id, ind_name, ind_color, items):
        """构建产业分区HTML"""
        cards = ""
        for item in items[:5]:
            cards += self._build_card(item)

        return '<div class="section industry-section"><div class="section-header" style="border-left-color: ' + ind_color + ';"><span style="color: ' + ind_color + ';">●</span> ' + ind_name + ' (' + str(len(items)) + ')</div><div class="section-content">' + cards + '</div></div>'

    def _build_card(self, item):
        """构建单条情报卡片"""
        original = item.get("original", {})
        title = original.get("title", "未知标题")
        link = original.get("link", "#")
        source = original.get("source_name", "未知来源")
        pub_date = original.get("published", "")[:10]

        summary = item.get("chinese_summary", "")
        impact = item.get("impact", "neutral")
        importance = item.get("importance", "low")
        risk_level = item.get("risk_level", "none")
        industries = item.get("industries", ["others"])
        intel_type = item.get("intelligence_type", "general")
        entities = item.get("entities", {})
        evidence = item.get("evidence", [])
        confidence = item.get("confidence", 0)

        impact_badge, _ = self._get_impact_badge(impact)
        importance_badge = self._get_importance_badge(importance)
        risk_badge = self._get_risk_badge(risk_level)

        # 产业标签
        industry_badges = ""
        for ind in industries[:2]:
            ind_name = self._get_industry_name(ind)
            industry_badges += '<span class="badge badge-industry">' + ind_name + '</span>'

        type_name = self._get_type_name(intel_type)
        type_badge = '<span class="badge badge-type">' + type_name + '</span>'

        # 中国相关标记
        china_badge = ""
        if any(kw in summary.lower() for kw in ["中国", "中方", "北京", "上海", "深圳", "一带一路", "bri", "china", "chinese"]):
            china_badge = '<span class="badge badge-china">涉华</span>'

        # 实体标签
        entity_html = ""
        all_entities = []
        for key in ["companies", "organizations", "people", "projects", "amounts", "locations"]:
            all_entities.extend(entities.get(key, [])[:3])
        if all_entities:
            entity_html = '<div class="card-entities">'
            for e in all_entities[:6]:
                entity_html += '<span class="entity-tag">' + str(e) + '</span>'
            entity_html += '</div>'

        # 证据
        evidence_html = ""
        if evidence:
            evidence_html = '<div class="card-evidence">依据: ' + "; ".join(evidence[:2]) + '</div>'

        return '<div class="intel-card"><div class="card-header"><div class="card-title">' + title + '</div><div class="card-badges">' + impact_badge + importance_badge + risk_badge + china_badge + '</div></div><div class="card-summary">' + summary + '</div>' + entity_html + evidence_html + '<div class="card-meta"><div class="card-meta-left"><span class="card-source">' + source + '</span><span>' + pub_date + '</span>' + industry_badges + type_badge + '<span style="color: #95a5a6;">置信度 ' + str(int(confidence * 100)) + '%</span></div><a href="' + link + '" target="_blank" class="card-link">原文 →</a></div></div>'


if __name__ == "__main__":
    gen = ReportGenerator()
    test_analyses = [
        {
            "industries": ["garment"],
            "intelligence_type": "market",
            "entities": {"companies": ["BGMEA"], "amounts": ["$28.4B"]},
            "chinese_summary": "孟加拉国成衣出口连续6个月负增长，主要受欧盟市场需求下滑影响。中国企业在孟投资纺织业面临订单减少风险。",
            "impact": "negative",
            "impact_reason": "出口下滑影响产业信心",
            "importance": "high",
            "risk_level": "medium",
            "risk_tags": ["出口下滑", "需求疲软"],
            "evidence": ["连续6个月负增长", "欧盟订单减少"],
            "confidence": 0.88,
            "original": {"title": "RMG exports fall for 6th month", "link": "#", "source_name": "The Daily Star", "published": "2026-05-29"}
        }
    ]
    test_stats = {"total": 1, "risk_count": 1, "policy_count": 0, "by_impact": {"positive": 0, "neutral": 0, "negative": 1}, "china_related": 1, "avg_confidence": 0.88}
    gen.generate_html(test_analyses, test_stats, output_dir="test_docs")
