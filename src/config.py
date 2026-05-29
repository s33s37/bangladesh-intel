# ============================================
# 孟加拉商业情报日报 - 监控矩阵配置
# 插件化架构：每个源通过 type 字段声明抓取方式
# ============================================

# === RSS 源（通用媒体 + Google News）===
RSS_SOURCES = [
    # 核心四大媒体
    {"type": "rss", "name": "The Daily Star", "url": "https://www.thedailystar.net/frontpage/rss.xml"},
    {"type": "rss", "name": "The Daily Star - Business", "url": "https://www.thedailystar.net/business/rss.xml"},
    {"type": "rss", "name": "BDNews24", "url": "https://bdnews24.com/?widgetName=rssfeed&widgetId=1150&getXmlFeed=true"},
    {"type": "rss", "name": "The Business Standard", "url": "https://www.tbsnews.net/rss.xml"},
    {"type": "rss", "name": "Dhaka Tribune", "url": "https://www.dhakatribune.com/feed/"},

    # 其他英文媒体
    {"type": "rss", "name": "New Age", "url": "https://www.newagebd.net/rss.xml"},
    {"type": "rss", "name": "The Financial Express", "url": "https://thefinancialexpress.com.bd/rss"},
    {"type": "rss", "name": "Prothom Alo English", "url": "https://www.prothomalo.com/feed/"},
    {"type": "rss", "name": "Bangladesh Post", "url": "https://bangladeshpost.net/rss.xml"},
    {"type": "rss", "name": "The Dhaka Post", "url": "https://thedhakapost.com/rss.xml"},
    {"type": "rss", "name": "Daily Sun", "url": "https://www.daily-sun.com/rss"},
    {"type": "rss", "name": "The Independent", "url": "https://www.theindependentbd.com/rss"},
    {"type": "rss", "name": "The Bangladesh Today", "url": "https://www.thebangladeshtoday.com/rss"},
    {"type": "rss", "name": "United News of Bangladesh", "url": "https://unb.com.bd/rss"},
    {"type": "rss", "name": "Bangladesh Sangbad Sangstha", "url": "https://bssnews.net/rss"},

    # 孟语媒体（可能有英文内容）
    {"type": "rss", "name": "Jugantor", "url": "https://www.jugantor.com/feed/rss.xml"},
    {"type": "rss", "name": "Jagonews24", "url": "https://www.jagonews24.com/rss/rss.xml"},
    {"type": "rss", "name": "Kaler Kantho", "url": "https://www.kalerkantho.com/rss.xml"},
    {"type": "rss", "name": "Bangla News 24", "url": "https://www.banglanews24.com/rss/rss.xml"},
    {"type": "rss", "name": "BD Pratidin", "url": "https://bd-pratidin.com/rss.xml"},
    {"type": "rss", "name": "Samakal", "url": "https://www.samakal.com/rss.xml"},
    {"type": "rss", "name": "Manab Zamin", "url": "https://www.mzamin.com/rss.xml"},
    {"type": "rss", "name": "Daily Naya Diganta", "url": "https://dailynayadiganta.com/rss.xml"},
    {"type": "rss", "name": "Inqilab", "url": "https://dailyinqilab.com/rss.xml"},
    {"type": "rss", "name": "Jaijaidin", "url": "https://www.jaijaidinbd.com/rss.xml"},
    {"type": "rss", "name": "Bhorer Kagoj", "url": "https://www.bhorerkagoj.com/rss.xml"},

    # 能源垂直媒体
    {"type": "rss", "name": "Energy Bangla", "url": "https://energybangla.com/feed"},

    # 外交/国际视角
    {"type": "rss", "name": "Bangladesh Diplomat", "url": "https://bangladeshdiplomat.com/feed"},

    # Google News RSS（关键词搜索，稳定可靠）
    {"type": "rss", "name": "Google News - Bangladesh", "url": "https://news.google.com/rss/search?q=bangladesh&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Business", "url": "https://news.google.com/rss/search?q=bangladesh+business&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Economy", "url": "https://news.google.com/rss/search?q=bangladesh+economy&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh China", "url": "https://news.google.com/rss/search?q=bangladesh+china&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Solar", "url": "https://news.google.com/rss/search?q=bangladesh+solar+energy&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Textile", "url": "https://news.google.com/rss/search?q=bangladesh+textile+garment&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Investment", "url": "https://news.google.com/rss/search?q=bangladesh+investment&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Infrastructure", "url": "https://news.google.com/rss/search?q=bangladesh+infrastructure&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh RMG", "url": "https://news.google.com/rss/search?q=bangladesh+RMG+garment+export&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Pharma", "url": "https://news.google.com/rss/search?q=bangladesh+pharmaceutical&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Shipbreaking", "url": "https://news.google.com/rss/search?q=bangladesh+ship+breaking&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Leather", "url": "https://news.google.com/rss/search?q=bangladesh+leather+tannery&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh Jute", "url": "https://news.google.com/rss/search?q=bangladesh+jute&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh ICT", "url": "https://news.google.com/rss/search?q=bangladesh+ICT+technology&hl=en-US&gl=US&ceid=US:en"},
    {"type": "rss", "name": "Google News - Bangladesh EV", "url": "https://news.google.com/rss/search?q=bangladesh+electric+vehicle&hl=en-US&gl=US&ceid=US:en"},

    # 孟加拉语关键词 Google News RSS
    {"type": "rss", "name": "Google News - BD Business (Bangla)", "url": "https://news.google.com/rss/search?q=%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6+%E0%A6%AC%E0%A7%8D%E0%A6%AF%E0%A6%AC%E0%A6%B8%E0%A6%BE&hl=bn&gl=BD&ceid=BD:bn"},
    {"type": "rss", "name": "Google News - BD China (Bangla)", "url": "https://news.google.com/rss/search?q=%E0%A6%9A%E0%A7%80%E0%A6%A8+%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6&hl=bn&gl=BD&ceid=BD:bn"},
]

# === NewsAPI 源（需配置 NEWSAPI_KEY 环境变量）===
NEWSAPI_SOURCES = [
    {
        "type": "newsapi",
        "name": "NewsAPI-BD-Business",
        "query": "bangladesh business",
        "lang": "en",
        "api_key_env": "NEWSAPI_KEY",
    },
    {
        "type": "newsapi",
        "name": "NewsAPI-BD-Economy",
        "query": "bangladesh economy OR bangladesh investment",
        "lang": "en",
        "api_key_env": "NEWSAPI_KEY",
    },
    {
        "type": "newsapi",
        "name": "NewsAPI-BD-China",
        "query": "bangladesh china OR bangladesh BRI",
        "lang": "en",
        "api_key_env": "NEWSAPI_KEY",
    },
]

# === API 金融/贸易数据接口 ===
# 通过 REST API 获取宏观经济指标、汇率等结构化数据
API_SOURCES = [
    # --- 世界银行 API（免费，无需 Key） ---
    {
        "type": "api",
        "name": "WorldBank - GDP Growth",
        "api_type": "worldbank",
        "indicator": "NY.GDP.MKTP.KD.ZG",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Inflation",
        "api_type": "worldbank",
        "indicator": "FP.CPI.TOTL.ZG",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Current Account",
        "api_type": "worldbank",
        "indicator": "BN.CAB.XOKA.GD.ZS",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - FDI Inflow",
        "api_type": "worldbank",
        "indicator": "BX.KLT.DINV.WD.GD.ZS",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - External Debt",
        "api_type": "worldbank",
        "indicator": "DT.DOD.DECT.GN.ZS",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Export Growth",
        "api_type": "worldbank",
        "indicator": "NE.EXP.GNFS.KD.ZG",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Import Growth",
        "api_type": "worldbank",
        "indicator": "NE.IMP.GNFS.KD.ZG",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - GDP (USD)",
        "api_type": "worldbank",
        "indicator": "NY.GDP.MKTP.CD",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Foreign Reserves",
        "api_type": "worldbank",
        "indicator": "FI.RES.TOTL.CD",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Merchandise Exports",
        "api_type": "worldbank",
        "indicator": "BX.GSR.MRCH.CD",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Merchandise Imports",
        "api_type": "worldbank",
        "indicator": "BM.GSR.MRCH.CD",
        "country": "BD",
    },
    {
        "type": "api",
        "name": "WorldBank - Unemployment",
        "api_type": "worldbank",
        "indicator": "SL.UEM.TOTL.ZS",
        "country": "BD",
    },
    # --- 孟加拉央行汇率 ---
    {
        "type": "api",
        "name": "Bangladesh Bank - Exchange Rate",
        "api_type": "bangladesh_bank",
    },
    # --- Trading Economics（预留，需配置 TRADING_ECONOMICS_KEY） ---
    # {
    #     "type": "api",
    #     "name": "TE - Bangladesh GDP",
    #     "api_type": "trading_economics",
    #     "indicator": "gdp",
    #     "country": "bangladesh",
    # },
]

# === 网页直接抓取源（无 RSS / RSS 更新慢的网站）===
# 使用 requests + BeautifulSoup 抓取首页/栏目列表页
# 注意：部分网站有 Cloudflare 防护（如 gov.bd 域名），requests 无法直接抓取
SCRAPER_SOURCES = [
    # --- 四大媒体商业版（补充 RSS 未覆盖的文章） ---
    {
        "type": "scraper",
        "name": "The Daily Star - Business (Scraper)",
        "url": "https://www.thedailystar.net/business",
        "item_selector": ".card-content .card-title a",
        "title_attr": "text",
        "link_attr": "href",
        "link_prefix": "https://www.thedailystar.net",
        "summary_selector": "",
        "encoding": "utf-8",
    },
    {
        "type": "scraper",
        "name": "TBS - Economy (Scraper)",
        "url": "https://www.tbsnews.net/economy",
        "item_selector": ".card-title a",
        "title_attr": "text",
        "link_attr": "href",
        "link_prefix": "https://www.tbsnews.net",
        "summary_selector": ".card-intro",
        "encoding": "utf-8",
    },
    # --- Prothom Alo 英文/孟语商业版 ---
    # 孟语版：https://www.prothomalo.com/business
    # 使用 .title-link a 选择器，链接为完整 URL
    {
        "type": "scraper",
        "name": "Prothom Alo - Business (Scraper)",
        "url": "https://www.prothomalo.com/business",
        "item_selector": ".title-link a",
        "title_attr": "text",
        "link_attr": "href",
        "link_prefix": "",
        "summary_selector": "",
        "encoding": "utf-8",
    },
    # --- 政府/政策网站（注意：部分 gov.bd 域名有 Cloudflare 防护） ---
    # 孟加拉经济区管理局 - 招标/政策公告
    # ⚠️ https://www.beza.gov.bd/ 有 Cloudflare 防护，以下配置仅作模板
    # {
    #     "type": "scraper",
    #     "name": "BEZA - News",
    #     "url": "https://www.beza.gov.bd/",
    #     "item_selector": ".news-item h3 a",
    #     "link_prefix": "https://www.beza.gov.bd",
    # },
    # 国家税务局 - 关税政策
    # ⚠️ https://www.nbr.gov.bd/ 有 Cloudflare 防护
    # {
    #     "type": "scraper",
    #     "name": "NBR - News",
    #     "url": "https://www.nbr.gov.bd/",
    #     "item_selector": ".news-item h3 a",
    #     "link_prefix": "https://www.nbr.gov.bd",
    # },
    # 孟加拉投资发展局 - 投资政策/激励措施（有 RSS，补充抓取）
    # {
    #     "type": "scraper",
    #     "name": "BIDA - Investment News (Scraper)",
    #     "url": "https://www.bida.gov.bd/investment-news",
    #     "item_selector": ".views-field-title a",
    #     "link_prefix": "https://www.bida.gov.bd",
    # },
]

# === Headless 浏览器抓取源（突破 Cloudflare 防护）===
# 使用 Playwright 启动 Chromium，绕过 JS 挑战
# 安装依赖：pip install playwright && playwright install chromium
BROWSER_SOURCES = [
    {
        "type": "browser",
        "name": "BEZA - 经济区招标",
        "site": "beza",
        "url": "https://www.beza.gov.bd/",
    },
    {
        "type": "browser",
        "name": "NBR - 关税政策",
        "site": "nbr",
        "url": "https://www.nbr.gov.bd/",
    },
    {
        "type": "browser",
        "name": "BIDA - 投资激励",
        "site": "bida",
        "url": "https://www.bida.gov.bd/",
    },
    {
        "type": "browser",
        "name": "Bangladesh Bank - 货币政策",
        "site": "bb",
        "url": "https://www.bb.org.bd/",
    },
]

# === PDF 文档解析源（政府公报 / SRO / 政策文件）===
# 下载 PDF 并用 pdfplumber 提取文本，自动识别 SRO/公报/政策等类型
# 安装依赖：pip install pdfplumber
PDF_SOURCES = [
    {
        "type": "pdf",
        "name": "NBR - SRO法规",
        "site": "nbr_sro",
    },
    {
        "type": "pdf",
        "name": "Bangladesh Gazette",
        "site": "bangladesh_gazette",
    },
    {
        "type": "pdf",
        "name": "央行 - 政策文件",
        "site": "bb_policy",
    },
    {
        "type": "pdf",
        "name": "财政部 - 预算文件",
        "site": "mof_budget",
    },
]

# === 统一数据源列表（所有插件共用）===
SOURCES = RSS_SOURCES + NEWSAPI_SOURCES + API_SOURCES + BROWSER_SOURCES + PDF_SOURCES + SCRAPER_SOURCES


# === 产业分类标签 ===
SECTORS = [
    "成衣纺织", "基建", "能源", "太阳能", "电动两轮车", "电动汽车",
    "制药", "ICT电商", "黄麻", "皮革", "船舶拆解", "渔业",
    "农产品加工", "陶瓷", "家具", "轻工制造", "造船", "医疗器械",
    "塑料", "家电", "数字经济", "其他"
]

# === 情报类型 ===
TYPES = [
    "政策变动", "项目中标", "投融资", "供应链", "人事变动",
    "风险事件", "市场数据", "其他"
]

# === 高优先级关键词（出现即标红预警）===
RED_FLAG_KEYWORDS = [
    "tariff", "duty", "tax", "SRO", "ban", "suspend", "cancel",
    "protest", "strike", "blackout", "fire", "accident", "corruption",
    "shortage", "crisis", "default", "bankruptcy", "recall", "embargo",
    "fraud", "lawsuit", "litigation", "penalty", "fine", "shutdown",
    "closure", "layoff", "withdrawal", "restriction",
    "quota", "dumping", "anti-dumping", "safeguard", "countervailing"
]

# === 产业关键词映射 ===
SECTOR_KEYWORDS = {
    "成衣纺织": ["RMG", "garment", "textile", "apparel", "BGMEA", "BTMA", "BKMEA", "knitwear", "woven", "denim", "spinning", "dyeing", "fabric", "yarn", "cotton", "readymade", "clothing", "fashion", "buyer", "order", "FOB", "C&F"],
    "基建": ["bridge", "road", "highway", "metro", "rail", "port", "power plant", "EPC", "contractor", "infrastructure", "construction", "engineering", "tender", "bid", "award", "contract", "development", "project", "milestone", "inauguration", "completion", "Padma", "Matarbari", "Dhaka Metro", "elevated expressway", "tunnel", "dam", "airport"],
    "能源": ["power", "electricity", "gas", "LNG", "petroleum", "BPDB", "Petrobangla", "fuel", "blackout", "load shedding", "generation", "transmission", "distribution", "substation", "grid", "pipeline", "import", "price hike", "subsidy", "IPP", "RPP", "rental", "quick rental", "captive power"],
    "太阳能": ["solar", "photovoltaic", "PV", "IDCOL", "renewable", "green energy", "panel", "inverter", "module", "cell", "watt", "MW", "GW", "grid-tie", "off-grid", "rooftop", "floating solar", "solar park", "solar farm", "FIT", "feed-in tariff", "net metering", "SREDA", "clean energy", "carbon neutral"],
    "电动两轮车": ["e-bike", "electric motorcycle", "e-motorcycle", "EV two wheeler", "BRTA", "scooter", "moped", "battery bike", "lithium-ion", "lead acid", "charging station", "swap station", "Yadea", "AIMA", "Walton", "Runner", "Akij", "registration", "homologation", "emission", "EV policy"],
    "电动汽车": ["EV", "electric vehicle", "charging station", "battery", "lithium", "Walton EV", "Nitol", "BAIL", "SUV", "sedan", "bus", "truck", "commercial vehicle", "EV policy", "EV roadmap", "incentive", "subsidy", "import duty", "CKD", "SKD", "battery swapping", "range", "kWh"],
    "制药": ["pharma", "drug", "medicine", "API", "DGDA", "Square Pharma", "Incepta", "Beximco", "ACI", "Eskayef", "generic", "formulation", "tablet", "capsule", "vaccine", "biotech", "clinical trial", "GMP", "WHO prequalification", "USFDA", "ANDA", "patent", "export", "pharmacy"],
    "ICT电商": ["ICT", "software", "IT", "e-commerce", "digital", "fintech", "bKash", "Nagad", "Daraz", "Chaldal", "Pathao", "Foodpanda", "startup", "venture capital", "unicorn", "app", "platform", "online", "payment gateway", "mobile banking", "digital wallet", "blockchain", "AI", "data center", "cloud", "SaaS", "BPO", "call center"],
    "黄麻": ["jute", "golden fiber", "hessian", "sacking", "bag", "carpet backing", "yarn", "BJMC", "BJRI", "raw jute", "jute goods", "export", "Golden Jubilee", "environment friendly", "biodegradable", "composite"],
    "皮革": ["leather", "tannery", "hide", "skin", "footwear", "bag", "belt", "wallet", "garment leather", "finished leather", "wet blue", "crust", "BFLLFEA", "Hazaribagh", "Savar tannery", "chrome", "vegetable tanning", "export"],
    "船舶拆解": ["ship breaking", "ship recycling", "HKC", "Hong Kong Convention", "yard", "scrap", "Alang", "Chittagong ship", "beaching", "plate", "re-rolling mill", "BSBA", "green yard", "certification", "IMO", "VLCC", "tanker", "bulk carrier", "hazardous waste", "asbestos"],
    "渔业": ["fish", "shrimp", "prawn", "aquaculture", "seafood", "frozen fish", "HACCP", "DoF", "BFDC", "export", "processing plant", "cold storage", "feed", "hatchery", "vannamei", "black tiger", "EU approval", "FDA", "depot", "landing center"],
    "农产品加工": ["agro", "food processing", "rice", "sugar", "tea", "spice", "flour", "oil", "dairy", "meat", "poultry", "egg", "fruit", "vegetable", "juice", "snack", "biscuit", "noodle", "frozen food", "canning", "packaging", "BADC", "BSCIC"],
    "陶瓷": ["ceramic", "tile", "sanitaryware", "pottery", "porcelain", "wall tile", "floor tile", "vitrified", "glazed", "BCMA", "furnace", "kiln", "natural gas", "clay", "feldspar", "export", "domestic market"],
    "家具": ["furniture", "wood", "wooden", "home decor", "interior", "office furniture", "BIFMA", "timber", "particle board", "MDF", "plywood", "rattan", "bamboo", "handicraft", "export", "EU market", "USA market"],
    "轻工制造": ["plastic", "polymer", "PET", "molding", "injection", "toy", "cosmetic", "battery", "paper", "packaging", "stationery", "sports goods", "bicycle", "leather goods", "synthetic", "polypropylene", "polyethylene", "BSCIC", "SME"],
    "造船": ["shipbuilding", "vessel", "naval", "shipyard", "Khulna Shipyard", "Ananda Shipyard", "coastal vessel", "inland vessel", "fishing trawler", "barge", "tugboat", "Bangladesh Navy", "coast guard", "IMO compliance"],
    "医疗器械": ["medical device", "hospital equipment", "diagnostic", "healthcare", "X-ray", "MRI", "CT scan", "ultrasound", "ventilator", "PPE", "mask", "glove", "syringe", "IV set", "stent", "implant", "DGDA approval", "ISO 13485"],
    "塑料": ["plastic", "polymer", "PET", "molding", "injection", "blow molding", "extrusion", "PVC", "HDPE", "LDPE", "PP", "PS", "recycling", "bioplastic", "degradable", "packaging", "bottle", "container", "film", "pipe"],
    "家电": ["appliance", "refrigerator", "TV", "AC", "washing machine", "microwave", "fan", "iron", "blender", "rice cooker", "Walton", "Samsung", "LG", "Transtec", "Haier", "Midea", "Gree", "CKD", "SKD", "assembly", "local manufacturing"],
    "数字经济": ["digital economy", "blockchain", "AI", "cloud", "data center", "smart city", "IoT", "5G", "broadband", "fiber optic", "digital payment", "e-governance", "cybersecurity", "data protection", "Digital Bangladesh", "Smart Bangladesh", "ICT Division"],
}
