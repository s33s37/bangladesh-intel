# 孟加拉商业情报日报系统

> 每日自动生成孟加拉国商业情报中文日报，服务中国政策制定者、智库学者和跨境电商从业者。

## 项目结构

```
.
├── .github/workflows/daily.yml    # GitHub Actions 自动工作流
├── config/
│   ├── industries.json            # 22个产业分类配置
│   └── sources.json               # 50+ RSS源配置
├── src/
│   ├── main.py                    # 主程序入口
│   ├── crawler.py                 # RSS采集器
│   ├── analyzer.py                # AI分析器
│   ├── generator.py               # HTML报告生成器
│   └── wechat.py                  # 微信通知模块
├── data/                          # 采集数据存储
├── docs/                          # GitHub Pages 输出目录
├── requirements.txt
└── README.md
```

## 核心功能

- **自动采集**：从50+个孟加拉国及国际媒体RSS源抓取新闻
- **AI分析**：自动分类产业、提取实体、判断影响、标记风险
- **中文报告**：生成带颜色标签的网页日报，支持手机/电脑访问
- **自动发布**：每日早7点（北京时间）自动更新
- **微信推送**：自动发送日报摘要到微信

## 监控产业（22个）

成衣纺织、基建、能源、太阳能、电动两轮车、电动汽车、制药、ICT电商、黄麻、皮革、船舶拆解、渔业、农产品加工、陶瓷、家具、轻工制造、造船、医疗器械、塑料、家电、数字经济、其他

## 部署步骤

### 第一步：Fork/创建GitHub仓库

1. 登录 GitHub，创建新仓库，命名为 `bangladesh-intelligence-daily`
2. 设置为 **Public**（GitHub Pages免费版需要公开仓库）

### 第二步：上传代码

将本项目所有文件上传到仓库根目录：

```bash
git clone https://github.com/你的用户名/bangladesh-intelligence-daily.git
cd bangladesh-intelligence-daily
# 复制所有项目文件到此目录
git add .
git commit -m "init: 孟加拉商业情报日报系统"
git push origin main
```

### 第三步：配置GitHub Pages

1. 进入仓库 **Settings → Pages**
2. **Source** 选择 **GitHub Actions**
3. 保存

### 第四步：配置API密钥（Secrets）

进入仓库 **Settings → Secrets and variables → Actions → New repository secret**，添加以下密钥：

| Secret名称 | 说明 | 获取方式 |
|-----------|------|---------|
| `OPENAI_API_KEY` | OpenAI API密钥 | [platform.openai.com](https://platform.openai.com) |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥（可选，优先使用） | [platform.deepseek.com](https://platform.deepseek.com) |
| `WECHAT_WEBHOOK_URL` | 企业微信机器人Webhook | 企业微信群 → 添加机器人 → 复制Webhook地址 |

> **成本提示**：使用 DeepSeek API 成本约为 OpenAI 的 1/10，推荐优先配置 `DEEPSEEK_API_KEY`。

### 第五步：手动触发测试

1. 进入仓库 **Actions** 标签页
2. 点击左侧 **"孟加拉商业情报日报生成"**
3. 点击右侧 **Run workflow** → 选择分支 → **Run workflow**
4. 等待约3-5分钟，查看运行日志

### 第六步：验证报告

1. 运行成功后，访问 `https://你的用户名.github.io/bangladesh-intelligence-daily/`
2. 检查报告是否正常显示
3. 检查微信是否收到推送

### 第七步：设置定时运行（自动）

工作流已配置为每日 UTC 23:00 运行（北京时间 07:00），无需额外设置。

如需调整时间，修改 `.github/workflows/daily.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 23 * * *'  # UTC 23:00 = 北京时间 07:00
```

## 验收标准

| 标准 | 要求 |
|-----|------|
| 每日自动运行 | GitHub Actions 定时触发成功 |
| 采集数量 | ≥30条多源新闻 |
| 产业分类准确率 | AI分析产业分类≥70% |
| 中文摘要 | 通顺可读，信息完整 |
| 移动端显示 | 网页在手机浏览器正常显示 |
| 微信推送 | 每日早7点收到摘要消息 |

## 自定义配置

### 修改RSS源
编辑 `config/sources.json`，添加或删除RSS源。

### 修改产业分类
编辑 `config/industries.json`，调整产业关键词和别名。

### 调整采集数量
修改 `src/main.py` 中的 `target_count` 参数（默认50条）。

### 切换AI模型
系统优先使用 `DEEPSEEK_API_KEY`，如未配置则使用 `OPENAI_API_KEY`（默认gpt-4o-mini）。

## 常见问题

**Q: 运行失败，提示API密钥错误？**
A: 检查 Settings → Secrets 中是否正确配置了 `OPENAI_API_KEY` 或 `DEEPSEEK_API_KEY`。

**Q: 采集不到新闻？**
A: 部分RSS源可能失效，检查 `src/crawler.py` 运行日志，在 `config/sources.json` 中更新源地址。

**Q: 微信收不到消息？**
A: 检查 `WECHAT_WEBHOOK_URL` 是否正确，且机器人未被踢出群聊。

**Q: 如何查看历史报告？**
A: 报告归档在 `docs/report_YYYY-MM-DD.html`，可通过 `https://你的用户名.github.io/bangladesh-intelligence-daily/report_YYYY-MM-DD.html` 访问。

## 技术栈

- Python 3.11
- GitHub Actions（定时任务 + Pages部署）
- OpenAI API / DeepSeek API（AI分析）
- feedparser + BeautifulSoup（RSS采集）
- 纯HTML/CSS（移动端适配）

## 免责声明

本项目仅供研究参考，不构成投资建议。情报内容由AI自动生成，可能存在误差，请结合原文核实。

---

**生成日期**: 2026-05-29
