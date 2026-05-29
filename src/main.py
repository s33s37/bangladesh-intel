#!/usr/bin/env python3
"""
孟加拉商业情报日报 - 主程序入口
完整流程：采集 -> AI分析 -> 生成报告
"""

import sys
import os
import time
from datetime import datetime

# 确保项目根目录在 sys.path 中（兼容 python src/main.py 和 python -m src.main 两种方式）
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.fetcher import fetch_all_sources, fetch_for_test
from src.processor import batch_analyze, get_top_signals
from src.generator import generate_html


def run_daily(test_mode=False):
    print("=" * 60)
    print(f"🇧🇩 孟加拉商业情报日报 - 开始生成")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"模式: {'测试模式' if test_mode else '正式模式'}")
    print("=" * 60)

    # Step 1: 数据采集
    print("\n[STEP 1/3] 数据采集...")
    if test_mode:
        entries = fetch_for_test()
    else:
        entries = fetch_all_sources(hours=24)

    if not entries:
        print("[WARN] 未采集到任何新闻，生成空报告")
        # 即使为空也生成报告，避免GitHub Pages断更
        generate_html([], model_name="deepseek-chat")
        print("\n[COMPLETE] 空报告已生成")
        return

    print(f"[OK] 采集完成: {len(entries)} 条原始新闻")

    # Step 2: AI分析
    print("\n[STEP 2/3] AI分析处理...")
    start_time = time.time()
    analyzed = batch_analyze(entries)
    elapsed = time.time() - start_time
    print(f"[OK] AI分析完成: {len(analyzed)} 条，耗时 {elapsed:.1f} 秒")

    # 打印Top信号预览
    top = get_top_signals(analyzed, n=3)
    print(f"\n[TOP SIGNALS] 今日Top {len(top)} 信号:")
    for i, t in enumerate(top, 1):
        flag_icon = "🔴" if t.get("red_flag") else "⚡"
        print(f"  {flag_icon} [{t['sector']}] {t['summary_cn'][:50]}... ({t['importance']})")

    # Step 3: 生成报告
    print("\n[STEP 3/3] 生成HTML报告...")
    output_path = generate_html(analyzed, model_name="deepseek-chat")
    print(f"[OK] 报告已生成: {output_path}")

    # 统计摘要
    red_count = len([x for x in analyzed if x.get("red_flag")])
    policy_count = len([x for x in analyzed if x.get("intel_type") == "政策变动"])
    pos_count = len([x for x in analyzed if x.get("impact_cn") == "正面"])

    print("\n" + "=" * 60)
    print("[DAILY SUMMARY]")
    print(f"  总条目:     {len(analyzed)}")
    print(f"  风险预警:   {red_count} 🔴")
    print(f"  政策变动:   {policy_count} 📜")
    print(f"  正面信号:   {pos_count} ✅")
    print(f"  报告路径:   {output_path}")
    print("=" * 60)
    print("[COMPLETE] 日报生成完毕\n")


if __name__ == "__main__":
    # 支持命令行参数
    import argparse
    parser = argparse.ArgumentParser(description="Bangladesh Intel Daily")
    parser.add_argument("--test", action="store_true", help="测试模式（少量数据快速验证）")
    args = parser.parse_args()

    run_daily(test_mode=args.test)
