"""
孟加拉商业情报日报 - 报告生成模块
将AI分析结果填入HTML模板，生成最终网页
"""

import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from src.config import SECTORS


def generate_html(intel_items, output_dir="output", model_name="qwen-plus"):
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


if __name__ == "__main__":
    # 本地测试
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
