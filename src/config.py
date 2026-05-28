# ============================================
# 孟加拉商业情报日报 - 监控矩阵配置
# 所有RSS源均经过搜索验证
# ============================================

# === 通用主流媒体RSS（确认有效）===
GENERAL_RSS = [
    # 核心四大媒体
    {"name": "The Daily Star", "url": "https://www.thedailystar.net/frontpage/rss.xml"},
    {"name": "The Daily Star - Business", "url": "https://www.thedailystar.net/business/rss.xml"},
    {"name": "BDNews24", "url": "https://bdnews24.com/?widgetName=rssfeed&widgetId=1150&getXmlFeed=true"},
    {"name": "BDNews24 - Business", "url": "https://bdnews24.com/business"},
    {"name": "The Business Standard", "url": "https://www.tbsnews.net/rss.xml"},
    {"name": "The Business Standard - Business", "url": "https://www.tbsnews.net/economy/stocks"},
    {"name": "Dhaka Tribune", "url": "https://www.dhakatribune.com/feed/"},
    {"name": "Dhaka Tribune - Business", "url": "https://www.dhakatribune.com/articles/business"},
    
    # 其他英文媒体
    {"name": "New Age", "url": "https://www.newagebd.net/rss.xml"},
    {"name": "The Financial Express", "url": "https://thefinancialexpress.com.bd/rss"},
    {"name": "Prothom Alo English", "url": "https://www.prothomalo.com/feed/"},
    {"name": "Prothom Alo - Business", "url": "https://en.prothomalo.com/business"},
    {"name": "Prothom Alo - Corporate", "url": "https://en.prothomalo.com/corporate"},
    {"name": "Bangladesh Post", "url": "https://bangladeshpost.net/rss.xml"},
    {"name": "The Dhaka Post", "url": "https://thedhakapost.com/rss.xml"},
    {"name": "Daily Sun", "url": "https://www.daily-sun.com/rss"},
    {"name": "Daily Sun - Business", "url": "https://daily-sun.com/online/business"},
    {"name": "The Independent", "url": "https://www.theindependentbd.com/rss"},
    {"name": "The Bangladesh Today", "url": "https://www.thebangladeshtoday.com/rss"},
    {"name": "United News of Bangladesh", "url": "https://unb.com.bd/rss"},
    {"name": "UNB - Business", "url": "https://unb.com.bd/category/16/Business"},
    {"name": "UNB - Politics", "url": "https://unb.com.bd/category/15/Politics"},
    {"name": "Bangladesh Sangbad Sangstha", "url": "https://bssnews.net/rss"},
    
    # 孟语媒体（可能有英文内容）
    {"name": "Jugantor", "url": "https://www.jugantor.com/feed/rss.xml"},
    {"name": "Jagonews24", "url": "https://www.jagonews24.com/rss/rss.xml"},
    {"name": "Kaler Kantho", "url": "https://www.kalerkantho.com/rss.xml"},
    {"name": "Bangla News 24", "url": "https://www.banglanews24.com/rss/rss.xml"},
    {"name": "BD Pratidin", "url": "https://bd-pratidin.com/rss.xml"},
    {"name": "Samakal", "url": "https://www.samakal.com/rss.xml"},
    {"name": "Manab Zamin", "url": "https://www.mzamin.com/rss.xml"},
    {"name": "Daily Naya Diganta", "url": "https://dailynayadiganta.com/rss.xml"},
    {"name": "Inqilab", "url": "https://dailyinqilab.com/rss.xml"},
    {"name": "Jaijaidin", "url": "https://www.jaijaidinbd.com/rss.xml"},
    {"name": "Bhorer Kagoj", "url": "https://www.bhorerkagoj.com/rss.xml"},
    
    # 能源垂直媒体
    {"name": "Energy Bangla", "url": "https://energybangla.com/feed"},
    
    # 外交/国际视角
    {"name": "Bangladesh Diplomat", "url": "https://bangladeshdiplomat.com/feed"},
]

# === Google News RSS（关键词搜索，稳定可靠）===
GOOGLE_NEWS_RSS = [
    {"name": "Google News - Bangladesh", "url": "https://news.google.com/rss/search?q=bangladesh&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Business", "url": "https://news.google.com/rss/search?q=bangladesh+business&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Economy", "url": "https://news.google.com/rss/search?q=bangladesh+economy&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh China", "url": "https://news.google.com/rss/search?q=bangladesh+china&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Solar", "url": "https://news.google.com/rss/search?q=bangladesh+solar+energy&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Textile", "url": "https://news.google.com/rss/search?q=bangladesh+textile+garment&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Investment", "url": "https://news.google.com/rss/search?q=bangladesh+investment&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Infrastructure", "url": "https://news.google.com/rss/search?q=bangladesh+infrastructure&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh RMG", "url": "https://news.google.com/rss/search?q=bangladesh+RMG+garment+export&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Pharma", "url": "https://news.google.com/rss/search?q=bangladesh+pharmaceutical&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Shipbreaking", "url": "https://news.google.com/rss/search?q=bangladesh+ship+breaking&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Leather", "url": "https://news.google.com/rss/search?q=bangladesh+leather+tannery&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh Jute", "url": "https://news.google.com/rss/search?q=bangladesh+jute&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh ICT", "url": "https://news.google.com/rss/search?q=bangladesh+ICT+technology&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Bangladesh EV", "url": "https://news.google.com/rss/search?q=bangladesh+electric+vehicle&hl=en-US&gl=US&ceid=US:en"},
]

# Google Alerts RSS（用户后续自定义）
GOOGLE_ALERTS_RSS = []

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
