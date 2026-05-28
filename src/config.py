# ============================================
# 孟加拉商业情报日报 - 监控矩阵配置
# ============================================

# 确认有效的RSS源（经过测试）
GENERAL_RSS = [
    {"name": "The Daily Star", "url": "https://www.thedailystar.net/rss.xml"},
    {"name": "The Business Standard", "url": "https://www.tbsnews.net/rss.xml"},
    {"name": "BDNews24", "url": "https://bdnews24.com/rss/english/"},
    {"name": "Dhaka Tribune", "url": "https://www.dhakatribune.com/feed/"},
    {"name": "New Age", "url": "https://www.newagebd.net/rss.xml"},
    {"name": "The Financial Express", "url": "https://thefinancialexpress.com.bd/rss.xml"},
    {"name": "Prothom Alo English", "url": "https://en.prothomalo.com/rss.xml"},
    {"name": "Bangladesh Post", "url": "https://bangladeshpost.net/rss.xml"},
    {"name": "Observer BD", "url": "https://www.observerbd.com/rss.xml"},
    {"name": "Daily Sun", "url": "https://www.daily-sun.com/rss.xml"},
    {"name": "UNB English", "url": "https://unb.com.bd/rss.xml"},
    {"name": "Jugantor English", "url": "https://english.jugantor.com/rss.xml"},
    {"name": "Kaler Kantho English", "url": "https://english.kalerkantho.com/rss.xml"},
    {"name": "Ittefaq English", "url": "https://english.ittefaq.com.bd/rss.xml"},
    {"name": "Inqilab English", "url": "https://english.dailyinqilab.com/rss.xml"},
    {"name": "Naya Diganta English", "url": "https://enayadiganta.com/rss.xml"},
    {"name": "Manab Zamin English", "url": "https://mzamin.com/rss.xml"},
    {"name": "Samakal English", "url": "https://en.samakal.com/rss.xml"},
    {"name": "Jaijaidin", "url": "https://www.jaijaidinbd.com/rss.xml"},
    {"name": "Bhorer Kagoj", "url": "https://www.bhorerkagoj.com/rss.xml"},
]

# Google Alerts RSS（后续步骤生成，先留空）
GOOGLE_ALERTS_RSS = [
    # 示例（后续填入真实链接）：
    # "https://www.google.com/alerts/feeds/xxxx/xxxx",
]

# 产业分类标签
SECTORS = [
    "成衣纺织", "基建", "能源", "太阳能", "电动两轮车", "电动汽车",
    "制药", "ICT电商", "黄麻", "皮革", "船舶拆解", "渔业",
    "农产品加工", "陶瓷", "家具", "轻工制造", "造船", "医疗器械",
    "塑料", "家电", "数字经济", "其他"
]

# 情报类型
TYPES = [
    "政策变动", "项目中标", "投融资", "供应链", "人事变动",
    "风险事件", "市场数据", "其他"
]

# 高优先级关键词（出现即标红预警）
RED_FLAG_KEYWORDS = [
    "tariff", "duty", "tax", "SRO", "ban", "suspend", "cancel",
    "protest", "strike", "blackout", "fire", "accident", "corruption",
    "shortage", "crisis", "default", "bankruptcy", "recall", "embargo",
    "fraud", "lawsuit", "litigation", "penalty", "fine", "shutdown",
    "closure", "layoff", "recall", "withdrawal", "restriction",
    "quota", "dumping", "anti-dumping", "safeguard", "countervailing"
]

# 产业关键词映射（用于AI分类时的辅助判断）
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
