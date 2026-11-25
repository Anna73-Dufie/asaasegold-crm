"""
AsaaseGold Cocoa CRM: synthetic dataset generator
Author: Anna Afriyie Dufie, MSc · Marketing & Data Analyst · Accra, Ghana

Builds one linked, fictional dataset for a made-in-Ghana cocoa brand that turns
Ghanaian cocoa into chocolate, cocoa powder and cocoa butter at home, and sells
retail (website, social shops, WhatsApp, pop-ups) and wholesale (supermarkets,
hotels, cafés, airlines, corporate gifting, export distributors).
Period: 1 Jan 2025 to 24 Nov 2026.

All names, companies and figures are synthetic. Patterns are built in on
purpose so the analysis has something to find (see STORIES at the bottom).
Run:  python generate_asaasegold_crm.py   -> writes ./data/*.csv
"""
import random, math, csv, os, bisect, datetime as dt
random.seed(2026)
START = dt.date(2025, 1, 1); END = dt.date(2026, 11, 24)
DAYS = (END - START).days + 1
D = lambda i: START + dt.timedelta(days=i)
def pick(seq, w): return random.choices(seq, weights=w)[0]
def clamp(x, a, b): return max(a, min(b, x))
os.makedirs('data', exist_ok=True)

def season(d):
    m, dd = d.month, d.day; f = 1.0
    if m == 12: f = 1.6 if dd <= 24 else 1.05
    if m == 2 and dd <= 14: f = 1.75   # National Chocolate Day (14 Feb)
    if m == 4 and dd <= 20: f = 1.15
    if m == 3 and dd <= 10: f = 1.15
    if m == 5 and dd <= 11: f = 1.35
    if m == 11 and dd >= 20: f = 1.7
    if m in (6, 7): f *= .9
    return f
def growth(i): return 0.55 + 0.9 * (i / DAYS)          # business roughly 2.5x over the period

FIRST_F = ['Akosua','Abena','Efua','Ama','Esi','Adwoa','Yaa','Afua','Akua','Naa','Dede','Selorm','Elikem','Nana','Maame','Kukua','Araba','Mansa','Dzifa','Edem','Gifty','Priscilla','Linda','Sandra','Vida','Joyce','Rita','Belinda','Nadia','Zainab','Fatima','Hawa','Ewurabena','Adjoa','Mawusi','Sena','Delali','Aseye','Korkor','Lamisi']
FIRST_M = ['Kwame','Kofi','Kojo','Yaw','Kwabena','Kweku','Nii','Fiifi','Delali','Bright','Emmanuel','Daniel','Ebo','Kwesi','Selasi','Mawuli','Issah','Ibrahim']
LAST = ['Mensah','Owusu','Boateng','Asante','Osei','Agyei','Addo','Quaye','Tetteh','Ansah','Appiah','Darko','Amoah','Frimpong','Badu','Sarpong','Acheampong','Opoku','Lartey','Adjei','Bonsu','Kumi','Antwi','Ofori','Dogbe','Agbeko','Yeboah','Wiredu','Issah','Mahama','Abdulai','Nyarko','Kyei','Gyamfi','Ankrah','Okine','Sowah','Aryee']
def person(f=.82): return (random.choice(FIRST_F) if random.random() < f else random.choice(FIRST_M)) + ' ' + random.choice(LAST)
CITIES = [('Accra', .46), ('Kumasi', .16), ('Tema', .10), ('Takoradi', .06), ('Cape Coast', .04), ('Kasoa', .05), ('Koforidua', .03), ('Ho', .03), ('Tamale', .04), ('Sunyani', .03)]
CITY = lambda: pick([c for c, _ in CITIES], [w for _, w in CITIES])

# ---------------- team, products
TEAM = [
 ('T01','Esi Mensah','Head of Sales'),('T02','Kwame Owusu','Sales Rep'),('T03','Ama Serwaa','Sales Rep'),('T04','Yaw Boateng','Sales Rep'),
 ('T05','Dede Quaye','Sales Rep'),('T06','Selorm Agbeko','Account Manager'),('T07','Nadia Issah','Account Manager'),
 ('T08','Gifty Ansah','Support Agent'),('T09','Kojo Tetteh','Support Agent'),('T10','Afua Darko','Support Agent'),
 ('T11','Naa Lartey','Marketing Lead'),('T12','Fiifi Appiah','Social Media Manager')]
REPS = ['T01','T02','T03','T04','T05','T06','T07']
REP_SKILL = {'T01':1.15,'T02':1.0,'T03':1.08,'T04':.85,'T05':.95,'T06':1.05,'T07':1.0}
REP_SPEED = {'T01':3,'T02':6,'T03':4,'T04':14,'T05':8,'T06':5,'T07':6}     # median hours to first contact
AGENTS = ['T08','T09','T10']
PRODUCTS = [
 ('P01','70% Dark Chocolate Bar','Chocolate bars',45,30,14),('P02','85% Extra Dark Bar','Chocolate bars',48,32,15),('P03','Creamy Milk Chocolate Bar','Chocolate bars',40,27,12),
 ('P04','Dark Chocolate with Coconut','Chocolate bars',48,32,15),('P05','Milk Chocolate with Groundnut','Chocolate bars',45,30,14),('P06','Dark Chocolate with Ginger & Pepper','Chocolate bars',50,33,15),
 ('P07','Mini Bars Pack (10)','Chocolate bars',85,56,26),('P08','Natural Cocoa Powder 500g','Cocoa powder & drinks',65,44,22),('P09','Drinking Chocolate 400g','Cocoa powder & drinks',70,47,23),
 ('P10','Cocoa Tea (shell infusion)','Cocoa powder & drinks',55,36,14),('P11','Roasted Cocoa Nibs 250g','Baking',60,40,19),('P12','Chocolate Spread 350g','Spreads',75,50,24),
 ('P13','Baking Chocolate Chips 1kg','Baking',140,95,52),('P14','Pure Cocoa Butter 250g','Cocoa butter care',90,60,28),('P15','Cocoa Butter Body Lotion','Cocoa butter care',85,57,25),
 ('P16','Truffle Box (9)','Gifts',180,120,62),('P17','Kente Gift Box','Gifts',320,215,110),('P18','Christmas Hamper','Gifts',650,440,240),
 ('P19','Valentine Heart Box','Gifts',220,148,72),('P20','Farm-to-Bar Tasting Set','Gifts',260,175,85),('P21','Corporate Gift Pack (12)','Gifts',540,380,190),
 ('P22','Hotel Turndown Chocolates (100)','Hospitality',0,420,180),('P23','In-flight Mini Bars (200)','Hospitality',0,760,330),('P24','Couverture 70% (5kg)','Bulk & export',0,980,520)]
PW = [10,6,9,6,7,4,7,8,8,4,4,7,3,6,5,5,3,2,3,3,2,0,0,0]
WHOLESALE_P = list(range(23)) + [23]

# ---------------- channels
SOCIAL = ['Instagram','TikTok','Facebook','X','LinkedIn','YouTube']
SOC_START = {'Instagram':9200,'TikTok':2100,'Facebook':6400,'X':1300,'LinkedIn':800,'YouTube':350}
SOC_GROWTH = {'Instagram':.0016,'TikTok':.0029,'Facebook':.0008,'X':.0004,'LinkedIn':.0024,'YouTube':.0024}   # daily follower growth
SOC_POSTS = {'Instagram':1.1,'TikTok':1.3,'Facebook':.7,'X':1.2,'LinkedIn':.35,'YouTube':.08}
SOC_REACH = {'Instagram':.55,'TikTok':2.4,'Facebook':.35,'X':.25,'LinkedIn':.9,'YouTube':6}                     # reach per post / follower
SOC_ENG = {'Instagram':.055,'TikTok':.072,'Facebook':.021,'X':.012,'LinkedIn':.034,'YouTube':.045}
SOC_CLICK = {'Instagram':.009,'TikTok':.005,'Facebook':.008,'X':.004,'LinkedIn':.012,'YouTube':.006}
LEAD_SOURCES = ['Instagram','TikTok','Facebook','X','LinkedIn','YouTube','Website','Email','Google Ads','Event','Referral','WhatsApp']

social_daily = []; foll = dict(SOC_START); soc_leads_by_day = {}
for i in range(DAYS):
    d = D(i)
    for p in SOCIAL:
        g = SOC_GROWTH[p] * (1 + random.gauss(0, .5)) * season(d)
        if p == 'TikTok' and d >= dt.date(2025, 8, 1): g *= 1.35           # TikTok takes off mid-2025
        if p == 'X' and d >= dt.date(2026, 3, 1): g *= .3                 # X stalls
        new = max(0, round(foll[p] * g)); lost = round(foll[p] * .00035 * random.random())
        foll[p] += new - lost
        posts = sum(1 for _ in range(3) if random.random() < SOC_POSTS[p] / 3) if p != 'YouTube' else int(random.random() < SOC_POSTS[p])
        reach = int(foll[p] * SOC_REACH[p] * (posts + .25) * random.uniform(.6, 1.5))
        impressions = int(reach * random.uniform(1.3, 1.9))
        eng = int(reach * SOC_ENG[p] * random.uniform(.7, 1.3))
        clicks = int(reach * SOC_CLICK[p] * random.uniform(.6, 1.4))
        social_daily.append(dict(date=d, platform=p, followers=foll[p], new_followers=new, posts=posts, reach=reach, impressions=impressions, engagements=eng, link_clicks=clicks))

social_posts = []; pid = 1
POST_TYPES = {'Instagram':['Reel','Carousel','Photo','Story'],'TikTok':['Video','Live'],'Facebook':['Photo','Video','Link'],'X':['Text','Photo','Thread'],'LinkedIn':['Article','Photo','Text'],'YouTube':['Video','Short']}
TOPICS = ['Farm to bar','Meet the farmers','Tasting notes','Behind the scenes','Recipe in 60 seconds','Gift ideas','New flavour','Giveaway','Why Ghana cocoa','National Chocolate Day','Unboxing','Cocoa butter tips']
for r in social_daily:
    for k in range(r['posts']):
        if random.random() > .35: continue
        t = random.choice(POST_TYPES[r['platform']]); top = random.choice(TOPICS)
        base = r['reach'] / max(r['posts'], 1) * random.lognormvariate(0, .6)
        if top in ('Farm to bar', 'Recipe in 60 seconds') and t in ('Reel', 'Video', 'Short'): base *= 2.2
        likes = int(base * SOC_ENG[r['platform']] * .75); com = int(likes * random.uniform(.03, .09)); sh = int(likes * random.uniform(.02, .12)); sv = int(likes * random.uniform(.03, .15))
        social_posts.append(dict(id=f'SP{pid:05d}', date=r['date'], platform=r['platform'], type=t, topic=top, reach=int(base), likes=likes, comments=com, shares=sh, saves=sv, link_clicks=int(base * SOC_CLICK[r['platform']] * random.uniform(.5, 1.6))))
        pid += 1

# ---------------- ad campaigns
AD_PLAT = [('Meta (Instagram/Facebook)', .36), ('TikTok Ads', .26), ('Google Ads', .2), ('YouTube Ads', .07), ('LinkedIn Ads', .07), ('X Ads', .04)]
AD_OBJ = ['Sales', 'Leads', 'Awareness', 'Traffic']
AD_THEMES = ['National Chocolate Day','Eat Ghana chocolate','Corporate gifting','Christmas hampers','Valentine box','Farm-to-bar story','New flavour','Easter treats','Hotel & airline partners','Cocoa butter care','Back to school snacks','Diaspora gifting']
ad_campaigns = []; aid = 1
for m in range(23):
    y, mo = 2025 + m // 12, m % 12 + 1
    for k in range(random.randint(4, 7)):
        p = pick([a for a, _ in AD_PLAT], [w for _, w in AD_PLAT]); obj = random.choice(AD_OBJ)
        s = dt.date(y, mo, random.randint(1, 20)); e = s + dt.timedelta(days=random.choice([7, 10, 14, 21, 28]))
        if s > END: continue
        e = min(e, END)
        budget = {'Meta (Instagram/Facebook)': 4200, 'TikTok Ads': 3800, 'Google Ads': 3500, 'YouTube Ads': 3000, 'LinkedIn Ads': 3200, 'X Ads': 1800}[p] * random.uniform(.5, 1.6) * growth((s - START).days)
        cpm = {'Meta (Instagram/Facebook)': 14, 'TikTok Ads': 9, 'Google Ads': 30, 'YouTube Ads': 18, 'LinkedIn Ads': 75, 'X Ads': 16}[p]
        ctr = {'Meta (Instagram/Facebook)': .011, 'TikTok Ads': .009, 'Google Ads': .038, 'YouTube Ads': .006, 'LinkedIn Ads': .007, 'X Ads': .005}[p] * random.uniform(.7, 1.3)
        cvr = {'Meta (Instagram/Facebook)': .035, 'TikTok Ads': .028, 'Google Ads': .05, 'YouTube Ads': .02, 'LinkedIn Ads': .06, 'X Ads': .012}[p] * random.uniform(.6, 1.4)
        imp = int(budget / cpm * 1000); clk = int(imp * ctr); leads = int(clk * cvr * (1.6 if obj == 'Leads' else 1)); conv = int(leads * random.uniform(.25, .45))
        aov = 900 if p == 'LinkedIn Ads' else random.uniform(260, 420)
        rev = round(conv * aov)
        ad_campaigns.append(dict(id=f'AD{aid:03d}', name=f'{random.choice(AD_THEMES)} · {obj.lower()}', platform=p, objective=obj, start=s, end=e, spend=round(budget), impressions=imp, clicks=clk, leads=leads, conversions=conv, revenue=rev, status='Active' if e >= END - dt.timedelta(days=2) else 'Completed'))
        aid += 1

# ---------------- email campaigns
EM_TYPES = [('Newsletter', 2), ('Promotion', 3), ('Product launch', 1), ('Abandoned cart', 2), ('Win-back', 1), ('Wholesale update', 1)]
email_campaigns = []; eid = 1; listsize = 3800
for w in range(DAYS // 7):
    d = D(w * 7 + random.randint(0, 4))
    listsize = int(listsize * (1 + random.uniform(.004, .012)))
    for k in range(1 if random.random() < .7 else 2):
        if random.random() < .45 and k == 0: continue
        t = pick([a for a, _ in EM_TYPES], [w_ for _, w_ in EM_TYPES])
        sends = listsize if t in ('Newsletter', 'Promotion', 'Product launch') else (int(listsize * .08) if t == 'Abandoned cart' else int(listsize * .25) if t == 'Win-back' else 320)
        o = {'Newsletter': .38, 'Promotion': .33, 'Product launch': .42, 'Abandoned cart': .52, 'Win-back': .24, 'Wholesale update': .55}[t] * random.uniform(.85, 1.15)
        c = {'Newsletter': .045, 'Promotion': .07, 'Product launch': .08, 'Abandoned cart': .16, 'Win-back': .05, 'Wholesale update': .12}[t] * random.uniform(.8, 1.2)
        opens = int(sends * o); clicks = int(opens * c / o * o * 1.0); clicks = int(sends * o * c * 2.2)
        orders = int(clicks * {'Abandoned cart': .32, 'Promotion': .14, 'Product launch': .12, 'Newsletter': .06, 'Win-back': .1, 'Wholesale update': .2}[t])
        aov = 1800 if t == 'Wholesale update' else random.uniform(280, 380)
        email_campaigns.append(dict(id=f'EM{eid:03d}', name={'Newsletter': 'From the farm', 'Promotion': random.choice(['Payday treat', 'Weekend 15% off', 'Gift box week', 'Free delivery Friday']), 'Product launch': random.choice(['Meet our ginger & pepper bar', 'Cocoa tea is here', 'New Kente gift box']), 'Abandoned cart': 'You left something behind', 'Win-back': 'We miss you', 'Wholesale update': 'Partner price list'}[t] + f' · {d.strftime("%d %b %Y")}', type=t, sent=d, sends=sends, delivered=int(sends * random.uniform(.97, .99)), opens=opens, clicks=clicks, unsubscribes=int(sends * random.uniform(.001, .005)), orders=orders, revenue=round(orders * aov), cost=round(sends * .05 + 420)))
        eid += 1

# ---------------- web analytics (daily by source) + geo + pages
WEB_SRC = {'Organic search': 210, 'Direct': 160, 'Social': 240, 'Email': 70, 'Paid ads': 120, 'Referral': 40}
web_daily = []
for i in range(DAYS):
    d = D(i)
    for s, b in WEB_SRC.items():
        g = growth(i) * season(d) * (1.25 if s == 'Social' and d >= dt.date(2025, 8, 1) else 1)
        ses = int(b * g * random.uniform(.8, 1.2) * (1.1 if d.weekday() in (4, 5) else 1))
        users = int(ses * random.uniform(.78, .86)); new = int(users * random.uniform(.45, .7))
        bounce = clamp({'Organic search': .48, 'Direct': .38, 'Social': .62, 'Email': .33, 'Paid ads': .58, 'Referral': .42}[s] + random.gauss(0, .04), .2, .85)
        t = clamp({'Organic search': 140, 'Direct': 175, 'Social': 70, 'Email': 190, 'Paid ads': 85, 'Referral': 150}[s] + random.gauss(0, 20), 20, 400)
        cvr = {'Organic search': .022, 'Direct': .034, 'Social': .012, 'Email': .041, 'Paid ads': .018, 'Referral': .026}[s]
        mob = clamp(.74 if s == 'Social' else .62 + random.gauss(0, .03), .4, .9)
        web_daily.append(dict(date=d, source=s, sessions=ses, users=users, new_users=new, bounce_rate=round(bounce, 3), avg_time_sec=int(t), mobile_share=round(mob, 3), conversions=int(ses * cvr * random.uniform(.8, 1.2))))
tot_ses = sum(r['sessions'] for r in web_daily)
web_geo = [dict(country=c, sessions=int(tot_ses * s)) for c, s in [('Ghana', .58), ('United Kingdom', .1), ('United States', .09), ('Nigeria', .06), ('Canada', .04), ('Germany', .025), ('Netherlands', .02), ('Côte d’Ivoire', .015), ('South Africa', .012), ('Other', .048)]]
web_pages = [dict(page=p, views=int(tot_ses * v), avg_time_sec=t, exit_rate=e) for p, v, t, e in [('/ (home)', .62, 48, .28), ('/shop', .41, 95, .22), ('/product/70-dark-chocolate-bar', .19, 110, .31), ('/gifting', .16, 132, .29), ('/our-farmers', .12, 205, .35), ('/product/kente-gift-box', .11, 118, .27), ('/blog/why-ghana-cocoa', .08, 190, .52), ('/wholesale', .06, 150, .33), ('/cart', .12, 60, .41), ('/checkout', .07, 140, .36)]]

# ---------------- events + registrations
EVENTS = [('National Chocolate Day Market · Accra Mall', 'Pop-up', 'Accra'), ('Chocolate Tasting Masterclass', 'Masterclass', 'Accra'), ('Hospitality Buyers Breakfast', 'Trade event', 'Accra'), ('New Flavour Launch Night', 'Product launch', 'Accra'),
          ('Kumasi Chocolate Pop-up', 'Pop-up', 'Kumasi'), ('Made-in-Ghana Expo', 'Trade fair', 'Accra'), ('Export Buyers Webinar', 'Webinar', 'Online'), ('Farm-to-Bar Tour · Suhum', 'Masterclass', 'Suhum'),
          ('Chocolate & Wine Pairing Evening', 'Masterclass', 'Accra'), ('Cocoa Origins Webinar', 'Webinar', 'Online'), ('Corporate Gifting Showcase', 'Trade event', 'Accra'), ('December in GH Gift Market', 'Pop-up', 'Accra'), ('Kente Gift Box Launch', 'Product launch', 'Accra')]
events = []; evid = 1
for yr in (2025, 2026):
    for k, (n, t, c) in enumerate(EVENTS):
        d = dt.date(yr, [2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10, 12, 11][k], random.randint(3, 26))
        if d > END + dt.timedelta(days=40): continue
        cap = {'Pop-up': 400, 'Masterclass': 60, 'Trade event': 45, 'Product launch': 150, 'Trade fair': 600, 'Webinar': 300}[t]
        price = {'Pop-up': 0, 'Masterclass': 250, 'Trade event': 0, 'Product launch': 100, 'Trade fair': 0, 'Webinar': 0}[t]
        cost = {'Pop-up': 6500, 'Masterclass': 4000, 'Trade event': 5200, 'Product launch': 12000, 'Trade fair': 15000, 'Webinar': 600}[t] * random.uniform(.85, 1.2)
        events.append(dict(id=f'EV{evid:02d}', name=f'{n} {yr}', type=t, city=c, date=d, capacity=cap, ticket_price=price, cost=round(cost), status='Upcoming' if d > END else 'Completed'))
        evid += 1

# ---------------- accounts (wholesale)
ACC_TYPES = [('Supermarket', .26), ('Hotel', .18), ('Café & bakery', .2), ('Corporate gifting', .16), ('Airline & airport', .06), ('Export distributor', .14)]
ACC_WORDS = {'Supermarket': ['Unity', 'Goodway', 'Freshmart', 'CityShop', 'Family', 'Palace', 'Royal', 'Value'], 'Hotel': ['Palm Court', 'Lagoon', 'Coastline', 'Volta View', 'Golden Sands', 'Ridge', 'Labadi Bay'], 'Café & bakery': ['Kwaku', 'Morning Glory', 'Sweet Crumb', 'Bean & Bake', 'Akwaaba', 'Oven Fresh', 'Brew'], 'Corporate gifting': ['Adinkra', 'Gye Nyame', 'Prestige', 'Sankofa', 'Heritage', 'Bold'], 'Airline & airport': ['SkyGold', 'Kotoka', 'Volta Air', 'Coastal Wings'], 'Export distributor': ['Afro Foods', 'Diaspora Pantry', 'West Africa Trade', 'Gold Coast Imports', 'Accra Link', 'Akan Foods', 'Adinkra Trading', 'Ebony Foods', 'Motherland Pantry', 'Sahel & Coast', 'Cocoa Route', 'Black Star Imports']}
ACC_SUF = {'Supermarket': ['Supermarket', 'Mart', 'Stores'], 'Hotel': ['Hotel', 'Resort', 'Hotel & Suites'], 'Café & bakery': ['Café', 'Bakery', 'Coffee House'], 'Corporate gifting': ['Gifts', 'Gifting Co.', 'Hampers'], 'Airline & airport': ['Airways', 'Lounges', 'Duty Free'], 'Export distributor': ['(UK) Ltd', '(USA) Inc.', '(Canada)', 'BV (Netherlands)', 'GmbH']}
ACC_SRC = [('Event', .2), ('Referral', .18), ('LinkedIn', .17), ('Instagram', .12), ('Website', .11), ('Email', .07), ('Cold outreach', .1), ('Google Ads', .05)]
accounts = []; used = set()
for k in range(310):
    t = pick([a for a, _ in ACC_TYPES], [w for _, w in ACC_TYPES]); c = CITY()
    while True:
        suf = random.choice(ACC_SUF[t])
        if t == 'Export distributor':
            c = {'(UK) Ltd': 'London', '(USA) Inc.': random.choice(['Houston', 'New York', 'Atlanta']), '(Canada)': 'Toronto', 'BV (Netherlands)': 'Amsterdam', 'GmbH': 'Hamburg'}[suf]
        areas = {'Accra': ['East Legon', 'Osu', 'Airport City', 'Spintex', 'Cantonments', 'Labone', 'Dzorwulu'], 'Kumasi': ['Adum', 'Ahodwo', 'Asokwa'], 'Tema': ['Community 25', 'Harbour']}.get(c, [])
        n = f"{random.choice(ACC_WORDS[t])} {suf}" + (f" {random.choice(areas)}" if areas and t != 'Export distributor' and random.random() < .4 else '')
        if n in used: n = n + ' ' + random.choice(['North', 'South', 'East', 'West', 'Central', 'Plus'])
        if n not in used: used.add(n); break
    accounts.append(dict(id=f'AC{k+1:03d}', name=n, type=t, city=c, owner=random.choice(REPS), source=pick([a for a, _ in ACC_SRC], [w for _, w in ACC_SRC]), created=None, status='Prospect', tier='', lifetime_value=0))
contacts = []; ctid = 1
TITLES = {'Supermarket': ['Category Buyer', 'Store Manager', 'Owner'], 'Hotel': ['F&B Manager', 'Procurement Manager', 'GM'], 'Café & bakery': ['Owner', 'Head Baker', 'Manager'], 'Corporate gifting': ['Founder', 'Account Director', 'Procurement Lead'], 'Airline & airport': ['Catering Manager', 'Procurement Officer', 'Retail Manager'], 'Export distributor': ['Managing Director', 'Import Manager', 'Buyer']}
for a in accounts:
    for k in range(random.choice([2, 3, 3, 4, 5])):
        n = person(.7)
        contacts.append(dict(id=f'CT{ctid:04d}', account=a['id'], name=n, title=TITLES[a['type']][k % 3] if k < 3 else random.choice(['Assistant Manager', 'Accounts Officer', 'Front Desk Lead']), email=(n.split()[0][0] + n.split()[1]).lower() + '@' + a['name'].split()[0].lower() + '.example', phone=f"+233 {random.choice(['24','54','55','20','50','27'])} *** {random.randint(1000,9999)}", primary=int(k == 0)))
        ctid += 1

# ---------------- leads, deals, proposals, contracts
STAGES = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Won', 'Lost']
SRC_RETAIL_W = {'Instagram': .2, 'TikTok': .24, 'Facebook': .1, 'X': .03, 'LinkedIn': .01, 'YouTube': .03, 'Website': .14, 'Email': .07, 'Google Ads': .07, 'Event': .04, 'Referral': .04, 'WhatsApp': .03}
SRC_QUAL = {'Instagram': 1.0, 'TikTok': .72, 'Facebook': .9, 'X': .55, 'LinkedIn': 1.25, 'YouTube': .8, 'Website': 1.1, 'Email': 1.5, 'Google Ads': 1.05, 'Event': 1.45, 'Referral': 1.6, 'WhatsApp': 1.3}
leads = []; deals = []; proposals = []; contracts = []; lid = 1; did = 1; prid = 1; coid = 1
acc_queue = accounts[:]; random.shuffle(acc_queue); active_acc = []; one_off = []
acc_contacts = {}
for c_ in contacts: acc_contacts.setdefault(c_['account'], []).append(c_)
def resp_factor(h):
    return 1.35 if h <= 1 else 1.15 if h <= 4 else .95 if h <= 24 else .7 if h <= 72 else .45
for i in range(DAYS):
    d = D(i)
    n = int(random.gauss(11 * growth(i) * season(d), 2.4))
    for _ in range(max(n, 0)):
        wholesale = random.random() < .2
        if wholesale:
            if len(acc_queue) > 26 and (random.random() < .55 or not active_acc):
                a = acc_queue.pop(); a['created'] = d
            elif active_acc:
                a = random.choice(active_acc)
            else:
                a = None
        if wholesale and a:
            src = a['source'] if a['source'] != 'Cold outreach' else 'Referral'
            name = random.choice(acc_contacts[a['id']])['name']
        else:
            src = pick(list(SRC_RETAIL_W), list(SRC_RETAIL_W.values())); name = person(); a = None
        if src == 'TikTok' and d < dt.date(2025, 8, 1) and random.random() < .4: src = 'Instagram'
        if not wholesale or not a: a = None
        owner = a['owner'] if a else random.choice(REPS[1:6])
        resp = round(random.lognormvariate(math.log(REP_SPEED[owner]), .9), 1)
        q = SRC_QUAL.get(src, 1) * resp_factor(resp) * REP_SKILL[owner]
        score = int(clamp(random.gauss(48 * q, 14), 1, 99))
        age = (END - d).days
        p_conv = clamp((.24 if not a else .45) * q, 0, .9)
        if age < 5: status = random.choice(['New', 'New', 'Contacted'])
        elif age < 21 and random.random() < .5: status = random.choice(['Contacted', 'Qualified'])
        else: status = 'Converted' if random.random() < p_conv else random.choice(['Unqualified', 'Unqualified', 'Contacted', 'Lost interest'])
        est = (int(random.uniform(2500, 11000)) if a['status'] == 'Active' else int(random.uniform(9000, 38000) * (2.2 if src == 'Event' else 1.3 if src == 'LinkedIn' else 1))) if a else int(random.uniform(150, 900))
        ld = dict(id=f'LD{lid:05d}', created=d, name=name, type='Wholesale' if a else 'Retail', source=src, account=a['id'] if a else '', owner=owner, first_response_hrs=resp, score=score, status=status, est_value=est, campaign='')
        leads.append(ld); lid += 1
        if a:
            # deal
            stage_p = clamp(.36 * q, .06, .8)
            cdate = d + dt.timedelta(days=int(random.uniform(14, 75)))
            if cdate > END:
                stage = random.choice(['Prospecting', 'Qualification', 'Proposal', 'Negotiation']); close = cdate
            else:
                stage = 'Won' if random.random() < stage_p else 'Lost'; close = cdate
            reached = {'Prospecting': 0, 'Qualification': 1, 'Proposal': 2, 'Negotiation': 3, 'Won': 4, 'Lost': random.choice([0, 1, 2, 2, 3])}[stage]
            lost_r = random.choice(['Price', 'Chose a competitor', 'No budget', 'Went silent', 'Timing', 'Product fit']) if stage == 'Lost' else ''
            if stage == 'Lost' and resp > 24 and random.random() < .5: lost_r = 'Went silent'
            dl = dict(id=f'DL{did:04d}', name=f"{a['name']} · {(random.choice(['Opening order', 'Shelf listing', 'Annual supply', 'Gift range for season']) if a['status'] != 'Active' else random.choice(['Reorder', 'Range expansion', 'Christmas gift order', 'New branch supply', 'Valentine stock']))}", account=a['id'], owner=owner, source=src, value=est, stage=stage, probability={'Prospecting': 10, 'Qualification': 25, 'Proposal': 50, 'Negotiation': 75, 'Won': 100, 'Lost': 0}[stage], created=d, close_date=close, lost_reason=lost_r, first_response_hrs=resp, lead=ld['id'])
            deals.append(dl); did += 1
            if reached >= 2 or stage == 'Won':
                sd = d + dt.timedelta(days=int((close - d).days * .45))
                pst = 'Accepted' if stage == 'Won' else 'Declined' if stage == 'Lost' else random.choice(['Sent', 'Viewed', 'Viewed', 'Draft'])
                proposals.append(dict(id=f'PR{prid:04d}', deal=dl['id'], account=a['id'], owner=owner, title=f"Supply proposal · {a['name']}", value=int(est * random.uniform(.95, 1.1)), sent=sd, valid_until=sd + dt.timedelta(days=30), status=pst)); prid += 1
            if stage == 'Won' and a['status'] == 'Active':
                one_off.append((close, a['id'], dl['value'], dl['id']))
            elif stage == 'Won':
                active_acc.append(a)
                a['status'] = 'Active'
                s = close; e = s + dt.timedelta(days=365)
                contracts.append(dict(id=f'CO{coid:04d}', account=a['id'], deal=dl['id'], owner=owner, title=f"Wholesale supply agreement · {a['name']}", value=int(est * random.uniform(1.0, 1.25)), start=s, end=e, billing='Monthly', auto_renew=int(random.random() < .55), status='')); coid += 1
            elif stage == 'Lost' and a['status'] == 'Prospect':
                a['status'] = 'Lost'
# second deals (upsell / renewals) for active accounts
for c in list(contracts):
    if c['end'] <= END:
        a = next(x for x in accounts if x['id'] == c['account'])
        renew = random.random() < (.82 if c['auto_renew'] else .58)
        if renew:
            s = c['end']; contracts.append(dict(id=f'CO{coid:04d}', account=c['account'], deal='', owner=c['owner'], title=c['title'] + ' (renewal)', value=int(c['value'] * random.uniform(1.05, 1.3)), start=s, end=s + dt.timedelta(days=365), billing='Monthly', auto_renew=c['auto_renew'], status='')); coid += 1
            c['status'] = 'Renewed'
        else:
            c['status'] = 'Expired'
for c in contracts:
    if not c['status']:
        c['status'] = 'Expiring soon' if (c['end'] - END).days <= 60 else 'Active'
for a in accounts:
    if a['created'] is None: a['created'] = START + dt.timedelta(days=random.randint(0, 120)); a['status'] = 'Prospect'
    cs = [c for c in contracts if c['account'] == a['id']]
    if cs and all(c['status'] == 'Expired' for c in cs): a['status'] = 'Churned'

# ---------------- invoices + payments (monthly billing on contracts)
invoices = []; payments = []; inv = 1; pay = 1
for c in contracts:
    m = c['start']; acc = next(x for x in accounts if x['id'] == c['account'])
    slow = random.random() < .18
    while m < min(c['end'], END):
        amt = int(c['value'] / 12 * random.uniform(.85, 1.15)); due = m + dt.timedelta(days=30)
        days_to_pay = (int(random.uniform(45, 150)) if random.random() > .12 else 999) if slow else int(random.uniform(5, 40))
        paid_on = m + dt.timedelta(days=days_to_pay)
        if paid_on <= END:
            st = 'Paid'
            payments.append(dict(id=f'PY{pay:05d}', invoice=f'IN{inv:05d}', account=c['account'], date=paid_on, amount=amt, method=pick(['Bank transfer', 'Mobile Money', 'Cheque', 'Card'], [.55, .3, .1, .05]), days_to_pay=days_to_pay)); pay += 1
        else: st = 'Overdue' if due < END else 'Due'
        invoices.append(dict(id=f'IN{inv:05d}', account=c['account'], contract=c['id'], issued=m, due=due, amount=amt, status=st)); inv += 1
        acc['lifetime_value'] += amt if st == 'Paid' else 0
        m = m + dt.timedelta(days=30)
accmap = {a['id']: a for a in accounts}
for dte_, acc_id, val, dlid in one_off:
    days_to_pay = int(random.uniform(7, 45)); paid_on = dte_ + dt.timedelta(days=days_to_pay); due = dte_ + dt.timedelta(days=30)
    if paid_on <= END:
        st = 'Paid'; payments.append(dict(id=f'PY{pay:05d}', invoice=f'IN{inv:05d}', account=acc_id, date=paid_on, amount=val, method=pick(['Bank transfer', 'Mobile Money', 'Cheque', 'Card'], [.55, .3, .1, .05]), days_to_pay=days_to_pay)); pay += 1
        accmap[acc_id]['lifetime_value'] += val
    else: st = 'Overdue' if due < END else 'Due'
    invoices.append(dict(id=f'IN{inv:05d}', account=acc_id, contract='', issued=dte_, due=due, amount=val, status=st)); inv += 1
invoices.sort(key=lambda r: r['issued']); payments.sort(key=lambda r: r['date'])
for a in accounts:
    v = a['lifetime_value']; a['tier'] = 'Gold' if v >= 120000 else 'Silver' if v >= 40000 else 'Bronze' if v > 0 else '—'

# ---------------- retail customers + orders
customers = []; orders = []; cust_ix = []; oid = 1
ORDER_CH = {'Website': .34, 'Instagram shop': .2, 'WhatsApp': .2, 'TikTok shop': .12, 'Facebook shop': .06, 'Pop-up event': .08}
CH_FROM_SRC = {'Instagram': 'Instagram shop', 'TikTok': 'TikTok shop', 'Facebook': 'Facebook shop', 'WhatsApp': 'WhatsApp', 'Event': 'Pop-up event'}
for l in leads:
    if l['type'] == 'Retail' and l['status'] == 'Converted':
        customers.append(dict(id=f'CU{len(customers)+1:05d}', name=l['name'], source=l['source'], city=CITY(), joined=l['created'], orders=0, spend=0, last_order=None, segment='')); cust_ix.append(customers[-1])
ORG_SRC = {'Website': .3, 'Instagram': .2, 'TikTok': .17, 'Facebook': .07, 'Google Ads': .07, 'Email': .04, 'Referral': .08, 'WhatsApp': .05, 'YouTube': .02}
for i in range(DAYS):
    d = D(i)
    for _ in range(max(0, int(random.gauss(12 * growth(i) * season(d), 2.5)))):
        src = pick(list(ORG_SRC), list(ORG_SRC.values()))
        if src == 'TikTok' and d < dt.date(2025, 8, 1) and random.random() < .5: src = 'Instagram'
        customers.append(dict(id=f'CU{len(customers)+1:05d}', name=person(), source=src, city=CITY(), joined=d, orders=0, spend=0, last_order=None, segment='')); cust_ix.append(customers[-1])
cust_ix.sort(key=lambda c: c['joined']); joined_dates = [c['joined'] for c in cust_ix]
for i in range(DAYS):
    d = D(i)
    lo = bisect.bisect_left(joined_dates, d); hi = bisect.bisect_right(joined_dates, d); joined = cust_ix[lo:hi]
    for c in joined:
        ch = CH_FROM_SRC.get(c['source'], pick(list(ORDER_CH), list(ORDER_CH.values())))
        orders.append((d, c, ch))
    n = int(random.gauss(17 * growth(i) * season(d), 4))
    pool = cust_ix[:bisect.bisect_left(joined_dates, d)]
    for _ in range(max(n, 0)):
        if not pool: break
        c = random.choice(pool[-1500:]) if random.random() < .65 else random.choice(pool)
        orders.append((d, c, pick(list(ORDER_CH), list(ORDER_CH.values()))))
ord_rows = []
for d, c, ch in orders:
    k = random.choices([1, 2, 3, 4], weights=[.48, .3, .15, .07])[0]
    items = random.choices(PRODUCTS[:23], weights=PW[:23], k=k)
    sub = sum(p[3] for p in items); disc = round(sub * .15) if (d.month == 11 and d.day >= 20) else (round(sub * .1) if random.random() < .1 else 0)
    payme = pick(['Mobile Money', 'Card', 'Pay on delivery', 'Bank transfer'], [.56, .22, .18, .04])
    st = 'Delivered'; r = random.random()
    if payme == 'Pay on delivery' and r < .12: st = 'Cancelled'
    elif r < .025: st = 'Cancelled'
    elif r < .045: st = 'Returned'
    if (END - d).days <= 2 and st == 'Delivered': st = random.choice(['Processing', 'Shipped', 'Delivered'])
    ord_rows.append(dict(id=f'OR{oid:06d}', date=d, customer=c['id'], channel=ch, items='|'.join(p[0] for p in items), units=k, subtotal=sub, discount=disc, delivery_fee=random.choice([0, 25, 30, 35, 40]), amount=sub - disc, payment=payme, status=st)); oid += 1
    if st not in ('Cancelled', 'Returned'):
        c['orders'] += 1; c['spend'] += sub - disc; c['last_order'] = d
for c in customers:
    if not c['orders']: c['segment'] = 'No purchase'; continue
    rec = (END - c['last_order']).days
    c['segment'] = 'Champion' if c['orders'] >= 4 and rec <= 60 else 'Loyal' if c['orders'] >= 2 and rec <= 120 else 'At risk' if c['orders'] >= 2 and rec <= 240 else 'Lapsed' if c['orders'] >= 2 else 'New' if rec <= 45 else 'One-time' if rec <= 180 else 'Lapsed'

# ---------------- event registrations
registrations = []; rid = 1
for e in events:
    fill = random.uniform(.55, 1.05) * (1.15 if e['type'] in ('Masterclass', 'Product launch') else 1)
    n = int(e['capacity'] * fill) if e['status'] == 'Completed' else int(e['capacity'] * fill * random.uniform(.3, .7))
    for _ in range(n):
        att = int(e['status'] == 'Completed' and random.random() < (.62 if e['ticket_price'] == 0 else .86))
        spend = int(random.uniform(120, 650)) if att and e['type'] in ('Pop-up', 'Product launch', 'Masterclass') and random.random() < .55 else 0
        registrations.append(dict(id=f'RG{rid:05d}', event=e['id'], name=person(), source=pick(['Instagram', 'TikTok', 'Email', 'WhatsApp', 'Website', 'Referral', 'LinkedIn'], [.28, .2, .18, .12, .1, .07, .05 if e['type'] not in ('Trade event', 'Trade fair') else .4]), registered=e['date'] - dt.timedelta(days=random.randint(1, 30)), ticket_paid=e['ticket_price'], attended=att, spend_at_event=spend, became_lead=int(att and random.random() < (.35 if e['type'] in ('Trade event', 'Trade fair') else .12))))
        rid += 1
for e in events:
    rs = [r for r in registrations if r['event'] == e['id']]
    e['registered'] = len(rs); e['attended'] = sum(r['attended'] for r in rs); e['revenue'] = sum(r['ticket_paid'] + r['spend_at_event'] for r in rs if r['attended'] or r['ticket_paid'])
    e['leads'] = sum(r['became_lead'] for r in rs)
    e['wholesale_value'] = sum(d_['value'] for d_ in deals if d_['source'] == 'Event' and d_['stage'] == 'Won' and 0 <= (d_['created'] - e['date']).days <= 45)

# ---------------- helpdesk tickets
CATS = [('Delivery delay', .24), ('Product question', .17), ('Melted on arrival', .08), ('Wrong or missing item', .09), ('Refund request', .08), ('Allergen question', .05), ('Payment issue', .1), ('Wholesale order', .09), ('Export enquiry', .05), ('Corporate gifting enquiry', .05)]
tickets = []; tid = 1
for i in range(DAYS):
    d = D(i)
    for _ in range(max(0, int(random.gauss(4.6 * growth(i) * season(d), 1.6)))):
        cat = pick([a for a, _ in CATS], [w for _, w in CATS]); ag = pick(AGENTS, [.4, .35, .25])
        pri = 'Urgent' if cat in ('Allergen question', 'Melted on arrival') and random.random() < .5 else pick(['Low', 'Medium', 'High'], [.35, .45, .2])
        fr = round(random.lognormvariate(math.log({'T08': 1.2, 'T09': 2.4, 'T10': 4.5}[ag] * (.4 if pri == 'Urgent' else 1)), .8), 1)
        res = round(fr + random.lognormvariate(math.log(14 if cat in ('Product question', 'Account / login') else 36), .7), 1)
        age_h = (END - d).days * 24 + 12
        st = 'Resolved' if res < age_h else random.choice(['Open', 'Pending customer', 'In progress'])
        csat = '' if st != 'Resolved' or random.random() < .45 else int(clamp(round(random.gauss(4.7 - fr / 6 - (res / 72), .6)), 1, 5))
        tickets.append(dict(id=f'TK{tid:05d}', created=d, channel=pick(['WhatsApp', 'Email', 'Instagram DM', 'Phone', 'Website chat'], [.38, .22, .18, .1, .12]), category=cat, priority=pri, agent=ag, first_response_hrs=fr, resolution_hrs=res if st == 'Resolved' else '', status=st, csat=csat, customer=random.choice(customers)['id'] if customers else ''))
        tid += 1

# ---------------- messages (unified inbox, last 60 days)
MSG_TPL = {'Product question': ['Is the 70% dark bar dairy-free?', 'Do you have the ginger and pepper bar in stock?', 'Is your cocoa sourced from Ghanaian farmers?', 'How long does the chocolate keep in this heat?'],
 'Order': ['I want 3 Kente gift boxes delivered to East Legon', 'Please send 2 tins of drinking chocolate to Tema', 'Can I pay on delivery?', 'Do you ship to London? My mum loves your bars'],
 'Wholesale': ['Good afternoon, we run a supermarket in Kumasi and want to stock your bars', 'Please share your wholesale price list', 'We need 300 gift packs for our staff end-of-year party'],
 'Support': ['My parcel has not arrived yet', 'I was charged twice on MoMo', 'The bars arrived a bit melted', 'I need to change my delivery address'],
 'Collab': ['Hi! I’m a food creator with 40k followers, open to a collab?', 'We’d love to feature you at our Made-in-Ghana fair']}
messages = []; mid = 1
for i in range(DAYS - 60, DAYS):
    d = D(i)
    for _ in range(int(random.gauss(55 * season(d), 8))):
        ch = pick(['WhatsApp', 'Instagram', 'Facebook', 'TikTok', 'Email', 'X', 'LinkedIn'], [.34, .27, .1, .14, .1, .02, .03])
        topic = pick(list(MSG_TPL), [.34, .33, .08 if ch != 'LinkedIn' else .6, .2, .05])
        age = DAYS - 1 - i
        st = 'Unread' if age == 0 and random.random() < .5 else ('Open' if age <= 2 and random.random() < .4 else 'Replied')
        messages.append(dict(id=f'MS{mid:05d}', received=dt.datetime.combine(d, dt.time(random.choice(range(7, 24)), random.randint(0, 59))), channel=ch, sender=person(), topic=topic, text=random.choice(MSG_TPL[topic]), assigned_to=random.choice(REPS[1:6] if topic in ('Order', 'Wholesale') else AGENTS if topic == 'Support' else ['T11', 'T12']), status=st, reply_mins=int(random.lognormvariate(math.log(35), 1.1)) if st == 'Replied' else ''))
        mid += 1

# ---------------- tasks + calendar
tasks = []; tkid = 1
TASK_T = ['Follow up on proposal', 'Call to confirm order', 'Send price list', 'Arrange tasting', 'Chase overdue invoice', 'Prepare contract renewal', 'Plan event stand', 'Reply to collab request', 'Update lead notes', 'Check stock for hotel order']
for k in range(1500):
    d = END + dt.timedelta(days=random.randint(-120, 30))
    who = random.choice(REPS + ['T11', 'T12'])
    st = 'Done' if d < END - dt.timedelta(days=2) and random.random() < .88 else ('Overdue' if d < END else 'To do') if random.random() < .85 else 'In progress'
    rel = random.choice(deals)['id'] if random.random() < .5 else random.choice(accounts)['id']
    tasks.append(dict(id=f'TS{tkid:04d}', title=random.choice(TASK_T), due=d, owner=who, priority=pick(['Low', 'Medium', 'High'], [.3, .5, .2]), status=st, related_to=rel)); tkid += 1
calendar = []; cid = 1
MEET = ['Tasting session', 'Account review', 'Contract renewal call', 'Supermarket visit', 'Hotel buyer meeting', 'Team pipeline review', 'Content shoot', 'Farm visit · cooperative']
for k in range(620):
    d = END + dt.timedelta(days=random.randint(-90, 35))
    if d.weekday() == 6: continue
    t = random.choice(MEET); h = random.choice([9, 10, 11, 12, 14, 15, 16])
    calendar.append(dict(id=f'CA{cid:04d}', title=t + (f" · {random.choice(accounts)['name']}" if t in ('Tasting session', 'Account review', 'Contract renewal call', 'Supermarket visit', 'Hotel buyer meeting') else ''), date=d, start=f'{h:02d}:00', end=f'{h+1:02d}:00', owner=random.choice(REPS + ['T11', 'T12']), type='Meeting' if 'review' in t.lower() or 'Farm' in t else 'Client' if t != 'Content shoot' else 'Marketing')); cid += 1
for e in events:
    calendar.append(dict(id=f'CA{cid:04d}', title=e['name'], date=e['date'], start='10:00', end='16:00', owner='T11', type='Event')); cid += 1

# ---------------- expenses
expenses = []; xid = 1
for a in ad_campaigns:
    expenses.append(dict(id=f'EX{xid:05d}', date=a['start'], category='Advertising', vendor=a['platform'], description=a['name'], amount=a['spend'])); xid += 1
for e in email_campaigns:
    pass
for e in events:
    if e['status'] == 'Completed': expenses.append(dict(id=f'EX{xid:05d}', date=e['date'], category='Events', vendor='Venue & logistics', description=e['name'], amount=e['cost'])); xid += 1
for m in range(23):
    y, mo = 2025 + m // 12, m % 12 + 1; d = dt.date(y, mo, 1)
    if d > END: break
    g = growth((d - START).days)
    for cat, vend, base in [('Salaries', 'Payroll', 96000), ('Rent & utilities', 'Landlord / ECG', 14500), ('Software', 'Shopify, Google Workspace, Canva', 2600), ('Factory & energy', 'Processing plant, ECG, generator fuel', 22000), ('Website & SEO', 'Web agency retainer', 4800), ('Influencers', 'Creators', 9000), ('Email platform', 'Email service', 650)]:
        expenses.append(dict(id=f'EX{xid:05d}', date=d, category=cat, vendor=vend, description=f'{cat} · {d.strftime("%b %Y")}', amount=round(base * (g if cat in ('Salaries', 'Influencers', 'Website & SEO') else 1) * random.uniform(.95, 1.08)))); xid += 1
    for w in range(4):
        dd = d + dt.timedelta(days=w * 7 + 2)
        if dd > END: break
        expenses.append(dict(id=f'EX{xid:05d}', date=dd, category='Ingredients & packaging', vendor=random.choice(['Sugar & milk supplier', 'Packaging supplier', 'Foil & wrappers']), description='Ingredients and packaging', amount=round(25000 * g * random.uniform(.7, 1.3)))); xid += 1
        expenses.append(dict(id=f'EX{xid:05d}', date=dd, category='Cold-chain logistics', vendor=random.choice(['Dispatch riders', 'Refrigerated courier', 'Export freight']), description='Deliveries', amount=round(9000 * g * random.uniform(.8, 1.2)))); xid += 1

# ---------------- targets
targets = []
for m in range(23):
    y, mo = 2025 + m // 12, m % 12 + 1
    if dt.date(y, mo, 1) > END: break
    for r in REPS:
        targets.append(dict(month=f'{y}-{mo:02d}', rep=r, revenue_target=round(30000 * growth(m * 30.4) * (1.25 if r in ('T06', 'T07') else 1), -2), deals_target=6 if r in ('T06', 'T07') else 4))

# ---------------- cocoa sourcing from farmer cooperatives (national impact)
COOPS = [('Kuapa Union Group A', 'Ashanti'), ('Sefwi Farmers Co-op', 'Western North'), ('Suhum Cocoa Growers', 'Eastern'), ('Assin Fosu Farmers Assoc.', 'Central'), ('Goaso Growers Union', 'Ahafo'), ('Hohoe Cocoa Co-op', 'Volta')]
sourcing = []; sid = 1
for m in range(23):
    y, mo = 2025 + m // 12, m % 12 + 1; d = dt.date(y, mo, 5)
    if d > END: break
    g = growth((d - START).days)
    for k, (cp, reg) in enumerate(COOPS):
        kg = int(random.uniform(380, 720) * g * (1.15 if mo in (10, 11, 12, 1, 2) else .9))   # main crop Oct–Feb
        price = round((52 if y == 2025 else 58) * random.uniform(.97, 1.03), 2)                 # GH₵ per kg (illustrative)
        prem = 4.5 if k < 4 else 3.0
        farmers = int(kg / random.uniform(55, 80))
        sourcing.append(dict(id=f'SC{sid:04d}', date=d, cooperative=cp, region=reg, kg_beans=kg, price_per_kg=price, premium_per_kg=prem, total_paid=round(kg * (price + prem)), farmers_paid=farmers, certified='Rainforest Alliance' if k in (0, 1, 4) else 'Organic' if k == 5 else 'In progress')); sid += 1
        expenses.append(dict(id=f'EX{xid:05d}', date=d, category='Cocoa beans (farmers)', vendor=cp, description=f'Cocoa beans · {reg}', amount=round(kg * (price + prem)))); xid += 1

# ---------------- write
def w(fn, rows):
    if not rows: return
    cols = list(rows[0].keys())
    with open('data/' + fn + '.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(cols)
        for r in rows: wr.writerow([(r[c].isoformat(sep=' ', timespec='minutes') if isinstance(r[c], dt.datetime) else r[c].isoformat() if isinstance(r[c], dt.date) else r[c]) if r[c] is not None else '' for c in cols])
w('team', [dict(id=a, name=b, role=c) for a, b, c in TEAM])
w('products', [dict(id=p[0], name=p[1], category=p[2], retail_price=p[3], wholesale_price=p[4], unit_cost=p[5]) for p in PRODUCTS])
for n, rows in [('accounts', accounts), ('contacts', contacts), ('leads', leads), ('deals', deals), ('proposals', proposals), ('contracts', contracts), ('invoices', invoices), ('payments', payments),
                ('customers', customers), ('orders', ord_rows), ('social_daily', social_daily), ('social_posts', social_posts), ('ad_campaigns', ad_campaigns), ('email_campaigns', email_campaigns),
                ('web_daily', web_daily), ('web_geo', web_geo), ('web_pages', web_pages), ('events', events), ('event_registrations', registrations), ('tickets', tickets), ('messages', messages),
                ('tasks', tasks), ('calendar', calendar), ('expenses', expenses), ('targets', targets), ('sourcing', sourcing)]:
    w(n, rows); print(f'{n:22s}{len(rows):>8,}')

STORIES = """
0. Every bar starts with beans bought from six farmer cooperatives, with a premium paid on top of the market price.
1. TikTok grows followers fastest from Aug 2025, but its leads convert least; email and referrals convert best.
2. Email marketing has the highest return per cedi of any channel; LinkedIn Ads cost most per lead but bring wholesale.
3. Leads contacted within an hour convert far better than those left 3+ days; one rep is slow and loses deals.
4. Events (trade fairs, buyers' breakfasts) bring the biggest wholesale deals.
5. A slice of wholesale accounts pay invoices late, creating an overdue balance to chase.
6. X engagement stalls from March 2026.
7. Support: the slowest agent's tickets get lower satisfaction scores.
"""
