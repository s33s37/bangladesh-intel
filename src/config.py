# ============================================
# 孟加拉商业情报日报 - 全网监控矩阵配置
# ============================================

# ============================================
# 一、通用主流媒体（宏观政策、政治风险）
# ============================================
GENERAL_RSS = [
    {"name": "The Daily Star", "url": "https://www.thedailystar.net/rss.xml"},
    {"name": "The Business Standard", "url": "https://www.tbsnews.net/rss.xml"},
    {"name": "BDNews24", "url": "https://bdnews24.com/rss/english/"},
    {"name": "Dhaka Tribune", "url": "https://www.dhakatribune.com/feed/"},
    {"name": "New Age", "url": "https://www.newagebd.net/rss.xml"},
    {"name": "The Financial Express", "url": "https://thefinancialexpress.com.bd/rss.xml"},
    {"name": "Prothom Alo English", "url": "https://en.prothomalo.com/rss.xml"},
]

# ============================================
# 二、官方机构与政策（政策雷达核心）
# ============================================
OFFICIAL_SOURCES = [
    {"name": "BIDA News", "url": "https://bida.gov.bd/news", "type": "web"},
    {"name": "BIDA Notices", "url": "https://bida.gov.bd/notices", "type": "web"},
    {"name": "NBR SRO Archive", "url": "https://nbr.gov.bd/sro", "type": "web"},
    {"name": "NBR Circulars", "url": "https://nbr.gov.bd/circulars", "type": "web"},
    {"name": "EPB Export Data", "url": "https://epb.gov.bd/export-statistics", "type": "web"},
    {"name": "Bangladesh Bank", "url": "https://www.bb.org.bd/en/index.php/publication/publicationcategory/1", "type": "web"},
    {"name": "BRTA Notices", "url": "https://brta.gov.bd/notice", "type": "web"},
    {"name": "BPDB Tender", "url": "https://bpdb.gov.bd/site/view/tenders", "type": "web"},
    {"name": "IDCOL Projects", "url": "https://idcol.org/project", "type": "web"},
    {"name": "BEZA EZ", "url": "https://beza.gov.bd/news", "type": "web"},
    {"name": "DGDA Drug Alert", "url": "https://dgda.gov.bd/alert", "type": "web"},
    {"name": "Power Division", "url": "https://powerdivision.gov.bd/site/view/notices", "type": "web"},
    {"name": "Petrobangla", "url": "https://petrobangla.org.bd/notice", "type": "web"},
    {"name": "Ministry of Commerce", "url": "https://mincom.gov.bd/notice", "type": "web"},
    {"name": "Ministry of Finance", "url": "https://mof.gov.bd/site/view/notices", "type": "web"},
]

# ============================================
# 三、成衣纺织（RMG）
# ============================================
TEXTILE_SOURCES = [
    {"name": "BGMEA News", "url": "https://bgmea.com.bd/news", "type": "web"},
    {"name": "BTMA News", "url": "https://btma.com.bd/news", "type": "web"},
    {"name": "BKMEA News", "url": "https://bkmea.com.bd/news", "type": "web"},
    {"name": "TBS Textile", "url": "https://www.tbsnews.net/economy/textile", "type": "web"},
    {"name": "Apparel Resources BD", "url": "https://apparelresources.com/business-news/sourcing/bangladesh/", "type": "web"},
    {"name": "Just Style Bangladesh", "url": "https://www.just-style.com/country/bangladesh/", "type": "web"},
    {"name": "Textile Today BD", "url": "https://www.textiletoday.com.bd/", "type": "web"},
    {"name": "Fashion Network BD", "url": "https://us.fashionnetwork.com/news/list/bangladesh/", "type": "web"},
]

# ============================================
# 四、基建与工程
# ============================================
INFRA_SOURCES = [
    {"name": "TBS Infrastructure", "url": "https://www.tbsnews.net/economy/infrastructure", "type": "web"},
    {"name": "Roads and Highways", "url": "https://rhd.gov.bd/notice", "type": "web"},
    {"name": "Bangladesh Bridge Authority", "url": "https://bba.gov.bd/notice", "type": "web"},
    {"name": "Dhaka Mass Transit", "url": "https://dmtcl.gov.bd/notice", "type": "web"},
    {"name": "Chittagong Port", "url": "https://cPA.gov.bd/notice", "type": "web"},
    {"name": "Matarbari Port", "url": "https://matarbarideepseaport.com/news", "type": "web"},
    {"name": "Railway Bangladesh", "url": "https://railway.gov.bd/notice", "type": "web"},
    {"name": "ADB Bangladesh Projects", "url": "https://www.adb.org/countries/bangladesh/projects", "type": "web"},
    {"name": "World Bank BD Projects", "url": "https://projects.worldbank.org/en/country/bangladesh", "type": "web"},
    {"name": "JICA Bangladesh", "url": "https://www.jica.go.jp/bangladesh/english/office/topics.html", "type": "web"},
    {"name": "AIIB Projects", "url": "https://www.aiib.org/en/projects/list/approved/Bangladesh/index.html", "type": "web"},
    {"name": "Construction Today BD", "url": "https://www.constructiontoday.com.bd/", "type": "web"},
]

# ============================================
# 五、能源与电力
# ============================================
ENERGY_SOURCES = [
    {"name": "TBS Energy", "url": "https://www.tbsnews.net/economy/energy", "type": "web"},
    {"name": "Energy Bangla", "url": "https://energybangla.com/", "type": "web"},
    {"name": "Power Division Tender", "url": "https://powerdivision.gov.bd/site/view/tenders", "type": "web"},
    {"name": "Petrobangla News", "url": "https://petrobangla.org.bd/news", "type": "web"},
    {"name": "Bangladesh Energy Reg", "url": "https://berc.org.bd/notice", "type": "web"},
    {"name": "Summit Power", "url": "https://summitpower.com.bd/news", "type": "web"},
    {"name": "United Power", "url": "https://unitedpowerbd.com/news", "type": "web"},
    {"name": "Orion Power", "url": "https://oriongroup.com.bd/news", "type": "web"},
    {"name": "North West Power", "url": "https://nwpgcl.org.bd/notice", "type": "web"},
    {"name": "Ashuganj Power", "url": "https://apscl.gov.bd/notice", "type": "web"},
]

# ============================================
# 六、太阳能与可再生能源
# ============================================
SOLAR_SOURCES = [
    {"name": "IDCOL Solar", "url": "https://idcol.org/renewable-energy", "type": "web"},
    {"name": "SREDA News", "url": "https://sreda.gov.bd/notice", "type": "web"},
    {"name": "Solar Bangladesh", "url": "https://solarbangladesh.com/news", "type": "web"},
    {"name": "PV Tech Asia", "url": "https://www.pv-tech.org/region/asia/", "type": "web"},
    {"name": "Energy Storage News", "url": "https://www.energy-storage.news/region/asia/", "type": "web"},
    {"name": "Renewables Now BD", "url": "https://renewablesnow.com/news/search/?q=bangladesh", "type": "web"},
    {"name": "PV Magazine International", "url": "https://www.pv-magazine.com/?s=bangladesh", "type": "web"},
    {"name": "Solar Quarter", "url": "https://solarquarter.com/?s=bangladesh", "type": "web"},
]

# ============================================
# 七、电动两轮车与电动汽车
# ============================================
EV_SOURCES = [
    {"name": "BRTA EV Notices", "url": "https://brta.gov.bd/notice", "type": "web"},
    {"name": "TBS Auto", "url": "https://www.tbsnews.net/economy/auto", "type": "web"},
    {"name": "Runner Automobiles", "url": "https://runnerbd.com/news", "type": "web"},
    {"name": "Walton Digi-Tech", "url": "https://waltonbd.com/news", "type": "web"},
    {"name": "Akij Motors", "url": "https://akijmotors.com/news", "type": "web"},
    {"name": "Electrive Asia", "url": "https://www.electrive.com/?s=bangladesh", "type": "web"},
    {"name": "Inside EVs Asia", "url": "https://insideevs.com/tags/bangladesh/", "type": "web"},
    {"name": "Auto News BD", "url": "https://www.autonews.com.bd/", "type": "web"},
    {"name": "BikeBD", "url": "https://www.bikebd.com/", "type": "web"},
]

# ============================================
# 八、制药
# ============================================
PHARMA_SOURCES = [
    {"name": "DGDA News", "url": "https://dgda.gov.bd/news", "type": "web"},
    {"name": "Square Pharma", "url": "https://squarepharma.com.bd/news", "type": "web"},
    {"name": "Incepta Pharma", "url": "https://inceptapharma.com/news", "type": "web"},
    {"name": "Beximco Pharma", "url": "https://beximcopharma.com/news", "type": "web"},
    {"name": "ACI Pharma", "url": "https://aci-bd.com/news", "type": "web"},
    {"name": "Eskayef", "url": "https://eskayef.com/news", "type": "web"},
    {"name": "Pharma Mirror", "url": "https://pharmamirror.com/", "type": "web"},
    {"name": "Fierce Pharma Asia", "url": "https://www.fiercepharma.com/asia", "type": "web"},
    {"name": "Pharma Boardroom Asia", "url": "https://pharmaboardroom.com/country/bangladesh/", "type": "web"},
]

# ============================================
# 九、ICT与数字经济
# ============================================
ICT_SOURCES = [
    {"name": "BTRC Notices", "url": "https://btrc.gov.bd/notice", "type": "web"},
    {"name": "BCC News", "url": "https://bcc.gov.bd/notice", "type": "web"},
    {"name": "TBS Tech", "url": "https://www.tbsnews.net/economy/tech", "type": "web"},
    {"name": "Future Startup", "url": "https://futurestartup.com/", "type": "web"},
    {"name": "LightCastle Partners", "url": "https://www.lightcastlebd.com/insights", "type": "web"},
    {"name": "bKash News", "url": "https://www.bkash.com/news", "type": "web"},
    {"name": "Nagad News", "url": "https://nagad.com.bd/news", "type": "web"},
    {"name": "Daraz Bangladesh", "url": "https://www.daraz.com.bd/blog", "type": "web"},
    {"name": "Chaldal", "url": "https://chaldal.com/blog", "type": "web"},
    {"name": "Pathao News", "url": "https://pathao.com/news", "type": "web"},
    {"name": "TechCrunch Asia", "url": "https://techcrunch.com/category/asia/", "type": "web"},
    {"name": "Rest of World South Asia", "url": "https://restofworld.org/region/south-asia/", "type": "web"},
]

# ============================================
# 十、船舶拆解
# ============================================
SHIPBREAKING_SOURCES = [
    {"name": "BSBA News", "url": "https://bsba-bd.org/news", "type": "web"},
    {"name": "Shipbreaking Platform", "url": "https://www.shipbreakingplatform.org/news/", "type": "web"},
    {"name": "Lloyd's List", "url": "https://lloydslist.maritimeintelligence.informa.com/?s=bangladesh", "type": "web"},
    {"name": "Tradewinds", "url": "https://www.tradewindsnews.com/search?q=bangladesh", "type": "web"},
    {"name": "Splash247 Asia", "url": "https://splash247.com/?s=bangladesh", "type": "web"},
    {"name": "Maritime Executive", "url": "https://maritime-executive.com/search?query=bangladesh", "type": "web"},
]

# ============================================
# 十一、渔业与水产
# ============================================
FISHERY_SOURCES = [
    {"name": "DoF Bangladesh", "url": "https://fisheries.gov.bd/notice", "type": "web"},
    {"name": "BFDC News", "url": "https://bfdc.gov.bd/notice", "type": "web"},
    {"name": "Shrimp News International", "url": "https://www.shrimpnews.com/?s=bangladesh", "type": "web"},
    {"name": "Undercurrent News", "url": "https://www.undercurrentnews.com/?s=bangladesh", "type": "web"},
    {"name": "IntraFish", "url": "https://www.intrafish.com/?s=bangladesh", "type": "web"},
    {"name": "Seafood Source", "url": "https://www.seafoodsource.com/search?query=bangladesh", "type": "web"},
]

# ============================================
# 十二、黄麻、皮革、陶瓷、家具、轻工
# ============================================
TRADITIONAL_SOURCES = [
    {"name": "BJMC News", "url": "https://bjmc.gov.bd/notice", "type": "web"},
    {"name": "BJRI News", "url": "https://bjri.gov.bd/notice", "type": "web"},
    {"name": "BFLLFEA News", "url": "https://bfllfea-bd.org/news", "type": "web"},
    {"name": "BCMA News", "url": "https://bcma-bd.org/news", "type": "web"},
    {"name": "BIFMA News", "url": "https://bifma-bd.org/news", "type": "web"},
    {"name": "BTMA General", "url": "https://btma.com.bd/news", "type": "web"},
]

# ============================================
# 十三、招标与采购平台（全产业）
# ============================================
TENDER_SOURCES = [
    {"name": "dgMarket BD", "url": "https://www.dgmarket.com/tenders/search?noticeType=1&country=16", "type": "web"},
    {"name": "TenderTiger BD", "url": "https://www.tendertiger.com/bangladesh-tenders", "type": "web"},
    {"name": "UNDP Procurement", "url": "https://procurement-notices.undp.org/view_notice.cfm?notice_id=", "type": "web"},
    {"name": "World Bank Procurement", "url": "https://www.worldbank.org/en/projects-operations/procurement/debarred-firms", "type": "web"},
    {"name": "ADB Procurement", "url": "https://www.adb.org/work-with-us/business-opportunities", "type": "web"},
    {"name": "AIIB Procurement", "url": "https://www.aiib.org/en/opportunities/business/procurement.html", "type": "web"},
]

# ============================================
# 十四、中国视角（中资动态）
# ============================================
CHINA_SOURCES = [
    {"name": "China Daily Asia", "url": "https://www.chinadaily.com.cn/world/asia_pacific/", "type": "web"},
    {"name": "Xinhua Bangladesh", "url": "https://www.news.cn/english/2024-05/27/c_1129681234.htm", "type": "web"},
    {"name": "CGTN South Asia", "url": "https://www.cgtn.com/search?keyword=bangladesh", "type": "web"},
    {"name": "Global Times", "url": "https://www.globaltimes.cn/search/?q=bangladesh", "type": "web"},
    {"name": "China Commerce Ministry", "url": "https://www.mofcom.gov.cn/article/i/jyjl/m/", "type": "web"},
    {"name": "Embassy of China BD", "url": "http://bd.china-embassy.gov.cn/chn/zbgx/zcwj/", "type": "web"},
    {"name": "CRI Online", "url": "https://english.cri.cn/search?keyword=bangladesh", "type": "web"},
]

# ============================================
# 十五、Google Alerts RSS（后续步骤生成）
# ============================================
GOOGLE_ALERTS_RSS = [
    # 示例格式（后续填入真实RSS链接）：
    # "https://www.google.com/alerts/feeds/xxxx/xxxx",
]

# ============================================
# 合并所有源（供采集器遍历）
# ============================================
ALL_SOURCES = (
    GENERAL_RSS + OFFICIAL_SOURCES + TEXTILE_SOURCES + INFRA_SOURCES +
    ENERGY_SOURCES + SOLAR_SOURCES + EV_SOURCES + PHARMA_SOURCES +
    ICT_SOURCES + SHIPBREAKING_SOURCES + FISHERY_SOURCES +
    TRADITIONAL_SOURCES + TENDER_SOURCES + CHINA_SOURCES
)

# ============================================
# 产业分类标签
# ============================================
SECTORS = [
    "成衣纺织", "基建", "能源", "太阳能", "电动两轮车", "电动汽车",
    "制药", "ICT电商", "黄麻", "皮革", "船舶拆解", "渔业",
    "农产品加工", "陶瓷", "家具", "轻工制造", "造船", "医疗器械",
    "塑料", "家电", "数字经济", "其他"
]

# ============================================
# 情报类型
# ============================================
TYPES = [
    "政策变动", "项目中标", "投融资", "供应链", "人事变动",
    "风险事件", "市场数据", "其他"
]

# ============================================
# 高优先级关键词（出现即标红预警）
# ============================================
RED_FLAG_KEYWORDS = [
    "tariff", "duty", "tax", "SRO", "ban", "suspend", "cancel",
    "protest", "strike", "blackout", "fire", "accident", "corruption",
    "shortage", "crisis", "default", "bankruptcy", "recall", "embargo",
    "fraud", "lawsuit", "litigation", "penalty", "fine", "shutdown",
    "closure", "layoff", "recall", "withdrawal", "restriction",
    "quota", "dumping", "anti-dumping", "safeguard", "countervailing"
]

# ============================================
# 产业关键词映射（AI分类辅助）
# ============================================
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
