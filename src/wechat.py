"""
企业微信机器人通知模块
"""

import os
import requests


def send_wechat_summary(summary, report_path=None):
    """
    发送日报摘要到企业微信群机器人。
    未配置 WECHAT_WEBHOOK_URL 时静默跳过，避免影响日报生成。
    """
    webhook_url = os.environ.get("WECHAT_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("[WECHAT] 未配置 WECHAT_WEBHOOK_URL，跳过推送")
        return False

    lines = ["孟加拉商业情报日报已生成", ""]
    lines.extend(summary)
    if report_path:
        lines.extend(["", f"报告路径: {report_path}"])

    payload = {
        "msgtype": "text",
        "text": {
            "content": "\n".join(lines)
        },
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("errcode") == 0:
            print("[WECHAT] 推送成功")
            return True
        print(f"[WECHAT] 推送失败: {data}")
    except Exception as e:
        print(f"[WECHAT] 推送异常: {str(e)[:80]}")
    return False
