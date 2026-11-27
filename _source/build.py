# -*- coding: utf-8 -*-
"""Nova Whisky Bar 官網產生器（淺色雜誌版）。
修改下方設定與文案後執行：python3 build.py  → 輸出到 ./site
"""
import json, re, os, html, shutil

# ---------------------------------------------------------------
# 基本設定
# ---------------------------------------------------------------
BASE = "https://nova-whisky-bar.github.io/"
HIDE_TODO = True   # True：未填資料直接不顯示（正式上線用）；False：顯示紅色【待填】（預覽用）
IG = "https://www.instagram.com/novawhisky/"
FB = "https://www.facebook.com/novawhiskybar"
THREADS = "https://www.threads.com/@novawhisky"
TEL = "+886-7-330-8050"
TEL_DISPLAY = "(07) 330-8050"
MAP = "https://www.google.com/maps/search/?api=1&query=" + "Nova%20Whisky%20Bar%20%E6%96%B0%E6%98%9F%E5%A8%81%E5%A3%AB%E5%BF%8C%E9%85%92%E9%A4%A8"
UPDATED = "2026-11-27"
GSC_VERIFY = "7rN2XwgvWpnXKgskS-hm6eu_E0YZMaUBgmdgYN8YGvY"   # Google Search Console 驗證碼，請勿刪除
OG_IMG = BASE + "assets/og.png"

# ---------------------------------------------------------------
# 待填事實：填好就把 None 換成文字，各語言分開填。
# 留 None 的地方，頁面上會顯示紅色【待填】標記。
# ---------------------------------------------------------------
FACTS = {
        "price":    {"zh": "低消每人 NT$500，另加 10% 服務費。",
                 "en": "Minimum spend NT$500 per person, plus a 10% service charge.",
                 "ja": "ミニマムチャージはお一人様 NT$500、別途サービス料10%がかかります。",
                 "ko": "1인 최소 주문 금액 NT$500, 서비스 요금 10% 별도입니다."},
    "bottles":  {"zh": "架上超過 500 瓶。",
                 "en": "There are more than 500 bottles on the back bar.",
                 "ja": "棚には500本以上のボトルが並んでいます。",
                 "ko": "500병이 넘는 위스키를 갖추고 있습니다."},
    "language": {"zh": "可以用英文點酒；目前沒有日文、韓文服務。",
                 "en": "Yes, we can serve you in English. Japanese and Korean aren't available at the moment.",
                 "ja": "英語での対応は可能です。現在、日本語での対応はできません。",
                 "ko": "영어로는 응대 가능합니다. 현재 한국어 응대는 어렵습니다."},
    "payment":  {"zh": "現金、信用卡", "en": "Cash and credit cards",
                 "ja": "現金・クレジットカード", "ko": "현금, 신용카드"},
}
TODO_LABEL = {
    "price":    {"zh": "低消、服務費、單杯價位", "en": "minimum charge, service charge, price per pour",
                 "ja": "ミニマムチャージ・サービス料・1杯の価格帯", "ko": "최소 주문, 서비스 요금, 한 잔 가격대"},
    "bottles":  {"zh": "架上約幾支酒", "en": "approx. number of bottles", "ja": "おおよその本数", "ko": "대략적인 보유 병 수"},
    "language": {"zh": "可否用英日韓語點酒", "en": "languages staff can serve in", "ja": "対応できる言語", "ko": "응대 가능한 언어"},
    "payment":  {"zh": "付款方式", "en": "payment methods", "ja": "支払い方法", "ko": "결제 수단"},
}
TODO_WORD = {"zh": "待填", "en": "TO FILL", "ja": "要記入", "ko": "기입 필요"}

def fact(key, lang):
    v = FACTS[key][lang]
    if v:
        return html.escape(v)
    if HIDE_TODO:
        return ""
    return f'<span class="todo" data-todo="{key}">【{TODO_WORD[lang]}：{TODO_LABEL[key][lang]}】</span>'

def fill(text, lang):
    return re.sub(r"\{(\w+)\}", lambda m: fact(m.group(1), lang) if m.group(1) in FACTS else m.group(0), text)

def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

def socials():
    out = [("Instagram", IG)]
    if FB: out.append(("Facebook", FB))
    if THREADS: out.append(("Threads", THREADS))
    return out

# ---------------------------------------------------------------
# 文案
# ---------------------------------------------------------------
L = {}

L["zh"] = dict(
    html_lang="zh-TW", og_locale="zh_TW", path="",
    fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+TC:wght@400;500;600&family=Noto+Sans+TC:wght@300;400;500",
    title="Nova Whisky Bar 新星威士忌酒館｜高雄苓雅威士忌酒吧・單杯品飲與獨立裝瓶",
    desc="Nova Whisky Bar 新星威士忌酒館是高雄苓雅區的威士忌酒吧，前身為高雄高地人小酒館（Highlander Inn Takao）。以蘇格蘭單一麥芽、獨立裝瓶與單桶為主，可點半杯，安靜適合一個人獨飲。",
    nav=[("#about", "關於"), ("#drink", "怎麼喝"), ("#visit", "來店資訊"), ("faq/", "常見問題"), ("journal/", "文章")],
    strap=("高雄苓雅區・威士忌酒吧", "單一麥芽・獨立裝瓶・安靜的夜晚"),
    h1_sub="新星威士忌酒館",
    lead="Nova Whisky Bar 新星威士忌酒館位於高雄市苓雅區林森二路，是一間安靜、適合一個人獨飲的威士忌酒吧。架上以蘇格蘭單一麥芽、獨立裝瓶與單桶為主，單杯超過 NT$500 的酒款可以點半杯。我們屬於醉俠 The Drunken Master 體系，和高雄建置中的南曜蒸餾所 NOVA Distillery 是同一個團隊。",
    formerly="前身為高雄高地人小酒館 Highlander Inn Takao・2026 年 4 月更名",
    side=["蘇格蘭單一麥芽／獨立裝瓶單桶", "單杯・半杯・Highball・調酒", "安靜獨飲・品牌品酒會"],
    btn_map="Google 地圖", btn_faq="第一次來看這裡",
    fig_caption="店內一景：四面燈光酒牆上，陳列超過 500 瓶威士忌。",
    photo_alt="Nova Whisky Bar 新星威士忌酒館店內，四面燈光酒牆陳列超過 500 瓶威士忌，中間是木桌與皮椅座位",
    about_k="About", about_h="關於 Nova",
    quote="一杯威士忌的距離，剛剛好的安靜。",
    about=[
        "Nova 的前身是高雄高地人小酒館（Highlander Inn Takao），2026 年 4 月更名為 Nova Whisky Bar 新星威士忌酒館。名字換了，做的事沒變：把一杯威士忌背後的酒廠、桶型與年份說清楚，讓你喝得懂，也喝得自在。",
        "座標 22.6°N，是高雄所在的緯度。",
        "店裡刻意保持安靜。一個人下班來喝一杯、放空也好，兩三個朋友輕聲聊天也好；想聊酒，隨時找我們，想要自己的空間，也沒人打擾。",
        "我們在社群上持續發表四語品飲紀錄【座標 22.6N｜新星亮這杯】，從 Gordon &amp; MacPhail 的老年份 Connoisseurs Choice，到 SMWS 與各家獨立裝瓶商的單桶，開過的酒都留下紀錄。",
    ],
    facts=[("地點", "高雄市苓雅區"), ("專長", "單一麥芽・獨立裝瓶單桶"), ("氣氛", "安靜・適合獨飲與輕聲交流")],
    drink_k="How to drink", drink_h="在 Nova 怎麼喝",
    drink=[
        ("單杯與半杯", "以單杯供應。單杯超過 NT$500 的酒款可以點半杯，想多試幾支高年份或稀有單桶時很方便。"),
        ("照你的口味挑酒", "說出你喜歡的味道或桶型，雪莉桶、波本桶、泥煤都可以，我們幫你配出一組並排比較。"),
        ("獨立裝瓶與單桶", "Gordon &amp; MacPhail、Douglas Laing、SMWS 等獨立裝瓶商的單桶酒款，很多是一桶只有兩、三百瓶的版本。"),
        ("安靜的獨飲空間", "不喧鬧、不趕人。一個人來很自在，兩三個朋友輕聲聊天也剛好。"),
        ("不喝純飲也可以", "有 Highball、調酒與無酒精飲料，同行朋友各自有選擇。"),
        ("新手也歡迎", "不用懂術語。告訴我們你平常喝什麼，我們從好入口的開始，一步一步帶。"),
    ],
    events_k="Tastings", events_h="品牌品酒會",
    events="不定期與酒商、品牌大使合作，在店裡舉辦小規模的主題品飲。場次與報名方式會在官方 Instagram、Facebook 與 Threads 公布。",
    visit_k="Visit", visit_h="來店資訊",
    visit=[
        ("店名", "Nova Whisky Bar 新星威士忌酒館<br><small>原 高雄高地人小酒館 Highlander Inn Takao</small>"),
        ("地址", "高雄市苓雅區林森二路128巷14號 2樓"),
        ("營業時間", "週日、週一、週三至週五 20:00–01:30<br>週六 20:00–02:00<br>週二公休"),
        ("電話", f'<a href="tel:{TEL}">{TEL_DISPLAY}</a>'),
        ("消費方式", "{price}"),
        ("外語服務", "{language}"),
        ("付款方式", "{payment}"),
    ],
    visit_note="公休與臨時異動以官方社群公告為準。人數較多或週末建議先來電或私訊訂位。",
    faq_k="FAQ", faq_h="常見問題", faq_more="看全部常見問題",
    family_k="Family", family_h="醉俠 The Drunken Master 體系",
    family=[
        ("醉俠 The Drunken Master", "高雄的威士忌品牌，長年推動在地威士忌文化。"),
        ("Nova Whisky Bar 新星威士忌酒館", "苓雅區的威士忌酒吧，也就是這裡。"),
        ("南曜蒸餾所 NOVA Distillery", "醉俠團隊在高雄建置中的精釀蒸餾所，從糖化、發酵到蒸餾都由團隊親手操作。"),
    ],
    journal_k="Journal", journal_h="文章", journal_more="看全部文章",
    warn_extra="",
    age_q="您是否已年滿 18 歲？", age_yes="是，我已滿 18 歲", age_no="否，離開",
    lang_name="繁體中文",
)

L["en"] = dict(
    html_lang="en", og_locale="en_US", path="en/",
    fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+TC:wght@400;500&family=Noto+Sans+TC:wght@300;400;500",
    title="Nova Whisky Bar | Quiet Whisky Bar in Kaohsiung, Taiwan (Lingya District)",
    desc="Nova Whisky Bar (新星威士忌酒館) is a quiet whisky bar in Lingya District, Kaohsiung, Taiwan, formerly Highlander Inn Takao. Scotch single malts, independent bottlings and single casks, with half pours available.",
    nav=[("#about", "About"), ("#drink", "Drinks"), ("#visit", "Visit"), ("#faq", "FAQ"), ("en/journal/", "Journal")],
    strap=("Lingya District, Kaohsiung · Whisky Bar", "Single malt · Independent bottlings · Quiet nights"),
    h1_sub="新星威士忌酒館",
    lead="Nova Whisky Bar (新星威士忌酒館) is a quiet whisky bar in Lingya District, Kaohsiung, Taiwan — a good place to drink on your own. The back bar is built around Scotch single malts, independent bottlings and single casks, and any dram over NT$500 can be ordered as a half pour. We are part of The Drunken Master (醉俠) family and share a team with NOVA Distillery (南曜蒸餾所), a craft distillery being built in Kaohsiung.",
    formerly="Formerly Highlander Inn Takao (高雄高地人小酒館) · Renamed April 2026",
    side=["Scotch single malts / independent single casks", "Full and half pours · Highballs · Cocktails", "Quiet solo drinking · Brand tastings"],
    btn_map="Google Maps", btn_faq="First visit? Start here",
    fig_caption="Inside Nova: lit shelves on every wall, holding more than 500 bottles of whisky.",
    photo_alt="Inside Nova Whisky Bar in Kaohsiung: illuminated whisky shelves on every wall with more than 500 bottles, wooden tables and leather chairs",
    about_k="About", about_h="About Nova",
    quote="Just the right amount of quiet, one dram at a time.",
    about=[
        "Nova opened as Highlander Inn Takao (高雄高地人小酒館) and became Nova Whisky Bar in April 2026. The name changed; the job didn't. We tell you where the whisky in your glass came from — the distillery, the cask, the vintage — so it makes sense as well as tastes good.",
        "22.6°N is the latitude of Kaohsiung.",
        "We keep the room quiet on purpose. Come alone after work and unwind, or bring a friend or two for a low-voiced chat. If you want to talk whisky, we're happy to; if you'd rather be left alone, you will be.",
        "On social media we keep a running tasting journal in four languages, 22.6°N | Nova in the Glass — from old Gordon &amp; MacPhail Connoisseurs Choice vintages to SMWS and other independent single casks.",
    ],
    facts=[("Location", "Lingya District, Kaohsiung"), ("Focus", "Single malts · IB single casks"), ("Atmosphere", "Quiet · solo-friendly")],
    drink_k="How to drink", drink_h="How to drink at Nova",
    drink=[
        ("Full and half pours", "Whisky is served by the glass. Any dram priced over NT$500 is also available as a half pour — an easy way to try older or rarer single casks."),
        ("Pick by taste", "Tell us what you like — sherry cask, bourbon cask, peat — and we'll line up a few drams side by side."),
        ("Independent single casks", "Single casks from bottlers such as Gordon &amp; MacPhail, Douglas Laing and SMWS, many of them a couple of hundred bottles from one cask."),
        ("A quiet room", "No loud music, no rush. Comfortable on your own, just right for two or three."),
        ("Not drinking neat?", "Highballs, cocktails and non-alcoholic drinks are on offer, so everyone at the table is covered."),
        ("New to whisky?", "No jargon needed. Tell us what you usually drink and we'll start somewhere easy."),
    ],
    events_k="Tastings", events_h="Brand tastings",
    events="We regularly host small tastings with importers and brand ambassadors. Dates and how to sign up are posted on our Instagram, Facebook and Threads.",
    visit_k="Visit", visit_h="Visit",
    visit=[
        ("Name", "Nova Whisky Bar 新星威士忌酒館<br><small>Formerly Highlander Inn Takao 高雄高地人小酒館</small>"),
        ("Address", "2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City, Taiwan<br><small lang=\"zh-TW\">高雄市苓雅區林森二路128巷14號 2樓</small>"),
        ("Hours", "Sun, Mon, Wed–Fri 20:00–01:30<br>Sat 20:00–02:00<br>Closed Tue"),
        ("Phone", f'<a href="tel:{TEL}">+886 7 330 8050</a>'),
        ("Prices", "{price}"),
        ("Languages", "{language}"),
        ("Payment", "{payment}"),
    ],
    visit_note="Closures and changes are announced on our social media. For larger groups or weekends, call or send a DM to book.",
    faq_k="FAQ", faq_h="FAQ", faq_more=None,
    family_k="Family", family_h="The Drunken Master family",
    family=[
        ("The Drunken Master (醉俠)", "A Kaohsiung whisky brand that has long championed the city's whisky culture."),
        ("Nova Whisky Bar (新星威士忌酒館)", "Our whisky bar in Lingya District — you're here."),
        ("NOVA Distillery (南曜蒸餾所)", "The team's craft distillery under construction in Kaohsiung, run hands-on from mashing to distillation."),
    ],
    journal_k="Journal", journal_h="Journal", journal_more="All articles",
    warn_extra="Please drink responsibly. No drink driving. Over 18s only.",
    age_q="Are you 18 or older?", age_yes="Yes, I am 18+", age_no="No, leave",
    lang_name="English",
)

L["ja"] = dict(
    html_lang="ja", og_locale="ja_JP", path="ja/",
    fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+JP:wght@400;500;600&family=Noto+Sans+JP:wght@300;400;500",
    title="Nova Whisky Bar 新星威士忌酒館｜台湾・高雄の静かなウイスキーバー（苓雅区）",
    desc="Nova Whisky Bar（新星威士忌酒館）は台湾・高雄市苓雅区の静かなウイスキーバー。旧店名 Highlander Inn Takao。スコッチのシングルモルト、独立瓶詰め、シングルカスクが中心で、ハーフショットも可能です。",
    nav=[("#about", "お店について"), ("#drink", "楽しみ方"), ("#visit", "アクセス"), ("#faq", "よくある質問"), ("ja/journal/", "記事")],
    strap=("高雄市苓雅区・ウイスキーバー", "シングルモルト・独立瓶詰め・静かな夜"),
    h1_sub="新星威士忌酒館",
    lead="Nova Whisky Bar（新星威士忌酒館）は、台湾・高雄市苓雅区にある静かなウイスキーバーです。お一人でも落ち着いて飲めます。スコッチのシングルモルト、独立瓶詰め、シングルカスクを中心に揃え、1杯 NT$500 を超えるウイスキーはハーフでも注文できます。高雄のウイスキーブランド「醉俠 The Drunken Master」のグループで、高雄で建設中のクラフト蒸溜所「南曜蒸餾所 NOVA Distillery」と同じチームが運営しています。",
    formerly="旧店名 Highlander Inn Takao（高雄高地人小酒館）・2026年4月改名",
    side=["スコッチのシングルモルト／独立瓶詰めシングルカスク", "1杯・ハーフ・ハイボール・カクテル", "静かなひとり飲み・テイスティング会"],
    btn_map="Googleマップ", btn_faq="初めての方へ",
    fig_caption="店内：四方の壁を照らす棚に、500本以上のウイスキーが並びます。",
    photo_alt="高雄 Nova Whisky Bar の店内。四方の壁一面に照明付きの棚があり、500本以上のウイスキーが並ぶ。木のテーブルと革張りの椅子",
    about_k="About", about_h="お店について",
    quote="ウイスキー一杯ぶんの、ちょうどいい静けさ。",
    about=[
        "Nova の前身は高雄高地人小酒館（Highlander Inn Takao）で、2026年4月に Nova Whisky Bar 新星威士忌酒館へ改名しました。名前は変わっても、やることは同じです。グラスの中のウイスキーが、どの蒸溜所の、どんな樽の、何年のものなのか。それを伝えて、分かって楽しめる一杯にすること。",
        "22.6°N は、高雄の緯度です。",
        "店内はあえて静かにしています。仕事帰りにお一人でぼんやり飲むのも、二、三人で小声で話すのも心地よい空間です。お酒の話をしたければいつでもどうぞ。一人の時間を過ごしたい方の邪魔はしません。",
        "SNS では4か国語のテイスティング記録「22.6°N | Nova in the Glass」を続けています。Gordon &amp; MacPhail の古いヴィンテージ Connoisseurs Choice から、SMWS をはじめとする独立瓶詰めのシングルカスクまで、開けたボトルを記録しています。",
    ],
    facts=[("場所", "高雄市苓雅区"), ("専門", "シングルモルト・独立瓶詰め"), ("雰囲気", "静か・ひとり飲み歓迎")],
    drink_k="How to drink", drink_h="Nova での楽しみ方",
    drink=[
        ("1杯とハーフ", "ウイスキーは1杯単位でご提供。1杯 NT$500 を超えるものはハーフも可能なので、高年数や希少なシングルカスクを何種類か試すのに便利です。"),
        ("好みで選ぶ", "シェリー樽、バーボン樽、ピートなど、好きな味や樽を教えてください。飲み比べできるよう何杯か並べて組み立てます。"),
        ("独立瓶詰めとシングルカスク", "Gordon &amp; MacPhail、Douglas Laing、SMWS などのシングルカスク。1樽から200〜300本ほどしか取れないものも多くあります。"),
        ("静かな空間", "騒がしくなく、急かされることもありません。お一人でも、二、三人でも心地よく過ごせます。"),
        ("ストレート以外も", "ハイボール、カクテル、ノンアルコールドリンクもあるので、お連れの方も楽しめます。"),
        ("初めての方も", "専門用語は要りません。普段飲んでいるものを教えていただければ、飲みやすい一杯から始めます。"),
    ],
    events_k="Tastings", events_h="テイスティング会",
    events="輸入元やブランドアンバサダーと組んだ少人数のテイスティング会を不定期に開いています。日程と申し込み方法は公式 Instagram、Facebook、Threads でお知らせします。",
    visit_k="Visit", visit_h="アクセス・営業時間",
    visit=[
        ("店名", "Nova Whisky Bar 新星威士忌酒館<br><small>旧店名 Highlander Inn Takao（高雄高地人小酒館）</small>"),
        ("住所", "高雄市苓雅区林森二路128巷14号 2階<br><small lang=\"zh-TW\">高雄市苓雅區林森二路128巷14號 2樓</small>"),
        ("営業時間", "日・月・水〜金 20:00–01:30<br>土 20:00–02:00<br>火曜定休"),
        ("電話", f'<a href="tel:{TEL}">+886 7 330 8050</a>'),
        ("料金", "{price}"),
        ("対応言語", "{language}"),
        ("お支払い", "{payment}"),
    ],
    visit_note="臨時休業や変更は公式SNSでお知らせします。大人数や週末は、お電話かDMでのご予約をおすすめします。",
    faq_k="FAQ", faq_h="よくある質問", faq_more=None,
    family_k="Family", family_h="醉俠 The Drunken Master グループ",
    family=[
        ("醉俠 The Drunken Master", "高雄のウイスキーブランド。長年、地元のウイスキー文化を盛り上げてきました。"),
        ("Nova Whisky Bar 新星威士忌酒館", "苓雅区のウイスキーバー。このお店です。"),
        ("南曜蒸餾所 NOVA Distillery", "チームが高雄で建設中のクラフト蒸溜所。糖化から蒸溜まで自分たちの手で行います。"),
    ],
    journal_k="Journal", journal_h="記事", journal_more="記事一覧へ",
    warn_extra="20歳未満の飲酒は日本の法律で禁止されています。台湾では18歳未満の飲酒は禁止です。飲酒運転は絶対にやめましょう。",
    age_q="18歳以上ですか？", age_yes="はい、18歳以上です", age_no="いいえ、退出します",
    lang_name="日本語",
)

L["ko"] = dict(
    html_lang="ko", og_locale="ko_KR", path="ko/",
    fonts="family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+KR:wght@400;500;600&family=Noto+Sans+KR:wght@300;400;500",
    title="Nova Whisky Bar 新星威士忌酒館｜대만 가오슝의 조용한 위스키 바 (링야구)",
    desc="Nova Whisky Bar(新星威士忌酒館)는 대만 가오슝 링야구의 조용한 위스키 바입니다. 옛 이름 Highlander Inn Takao. 스카치 싱글 몰트, 독립 병입, 싱글 캐스크 중심이며 하프 잔도 주문할 수 있습니다.",
    nav=[("#about", "소개"), ("#drink", "즐기는 법"), ("#visit", "찾아오는 길"), ("#faq", "자주 묻는 질문"), ("ko/journal/", "글")],
    strap=("가오슝 링야구 · 위스키 바", "싱글 몰트 · 독립 병입 · 조용한 밤"),
    h1_sub="新星威士忌酒館",
    lead="Nova Whisky Bar(新星威士忌酒館)는 대만 가오슝시 링야구에 있는 조용한 위스키 바로, 혼자 마시기에도 편안한 곳입니다. 스카치 싱글 몰트, 독립 병입, 싱글 캐스크를 중심으로 갖추고 있으며, 한 잔에 NT$500가 넘는 위스키는 하프 잔으로도 주문할 수 있습니다. 가오슝 위스키 브랜드 醉俠 The Drunken Master 소속이며, 가오슝에서 건설 중인 크래프트 증류소 南曜蒸餾所 NOVA Distillery와 같은 팀이 운영합니다.",
    formerly="옛 이름 Highlander Inn Takao(高雄高地人小酒館) · 2026년 4월 이름 변경",
    side=["스카치 싱글 몰트 / 독립 병입 싱글 캐스크", "한 잔 · 하프 잔 · 하이볼 · 칵테일", "조용한 혼술 · 브랜드 테이스팅"],
    btn_map="Google 지도", btn_faq="처음 오신다면",
    fig_caption="가게 안: 네 벽을 채운 조명 선반에 500병이 넘는 위스키가 진열되어 있습니다.",
    photo_alt="가오슝 Nova Whisky Bar 내부. 네 벽을 가득 채운 조명 선반에 500병이 넘는 위스키가 진열되어 있고, 나무 테이블과 가죽 의자가 놓여 있다",
    about_k="About", about_h="Nova 소개",
    quote="위스키 한 잔만큼의, 딱 알맞은 고요함.",
    about=[
        "Nova의 전신은 高雄高地人小酒館(Highlander Inn Takao)이며, 2026년 4월 Nova Whisky Bar 新星威士忌酒館로 이름을 바꿨습니다. 이름은 바뀌었지만 하는 일은 같습니다. 잔 속 위스키가 어느 증류소에서, 어떤 캐스크로, 몇 년에 만들어졌는지 들려드리고, 알고 마시는 즐거움을 드리는 것.",
        "22.6°N은 가오슝의 위도입니다.",
        "가게는 일부러 조용하게 유지합니다. 퇴근 후 혼자 들러 멍하니 한 잔 하셔도 좋고, 두세 명이 나지막이 이야기 나누기에도 좋습니다. 위스키 이야기가 하고 싶으면 언제든 말을 걸어 주세요. 혼자만의 시간을 원하시면 방해하지 않습니다.",
        "SNS에서는 4개 국어 테이스팅 기록 「22.6°N | Nova in the Glass」를 꾸준히 올리고 있습니다. Gordon &amp; MacPhail의 오래된 빈티지 Connoisseurs Choice부터 SMWS 등 독립 병입 싱글 캐스크까지, 열어 본 병은 모두 기록합니다.",
    ],
    facts=[("위치", "가오슝 링야구"), ("전문", "싱글 몰트 · 독립 병입"), ("분위기", "조용함 · 혼술 환영")],
    drink_k="How to drink", drink_h="Nova에서 즐기는 법",
    drink=[
        ("한 잔과 하프 잔", "위스키는 잔 단위로 제공합니다. 한 잔에 NT$500가 넘는 위스키는 하프 잔도 가능해서, 고숙성이나 희귀한 싱글 캐스크를 여러 종류 맛보기 좋습니다."),
        ("취향대로 고르기", "셰리 캐스크, 버번 캐스크, 피트 등 좋아하는 맛이나 캐스크를 말씀해 주세요. 몇 잔을 나란히 비교할 수 있게 골라 드립니다."),
        ("독립 병입과 싱글 캐스크", "Gordon &amp; MacPhail, Douglas Laing, SMWS 등의 싱글 캐스크. 한 캐스크에서 200~300병 정도만 나온 것도 많습니다."),
        ("조용한 공간", "시끄럽지 않고 재촉하지 않습니다. 혼자여도 편하고, 두세 명이어도 딱 좋습니다."),
        ("니트가 아니어도", "하이볼, 칵테일, 무알코올 음료도 있어 함께 온 일행도 즐길 수 있습니다."),
        ("위스키가 처음이라면", "전문 용어는 몰라도 됩니다. 평소 즐겨 마시는 술을 알려 주시면 마시기 편한 잔부터 시작합니다."),
    ],
    events_k="Tastings", events_h="브랜드 테이스팅",
    events="수입사, 브랜드 앰배서더와 함께 소규모 테이스팅을 비정기적으로 엽니다. 일정과 신청 방법은 공식 Instagram, Facebook, Threads에서 알려 드립니다.",
    visit_k="Visit", visit_h="찾아오는 길",
    visit=[
        ("상호", "Nova Whisky Bar 新星威士忌酒館<br><small>옛 이름 Highlander Inn Takao(高雄高地人小酒館)</small>"),
        ("주소", "2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City, Taiwan<br><small lang=\"zh-TW\">高雄市苓雅區林森二路128巷14號 2樓</small>"),
        ("영업시간", "일·월·수–금 20:00–01:30<br>토 20:00–02:00<br>화요일 휴무"),
        ("전화", f'<a href="tel:{TEL}">+886 7 330 8050</a>'),
        ("가격", "{price}"),
        ("응대 언어", "{language}"),
        ("결제", "{payment}"),
    ],
    visit_note="휴무와 변경 사항은 공식 SNS에서 공지합니다. 인원이 많거나 주말이라면 전화나 DM으로 예약하시길 권합니다.",
    faq_k="FAQ", faq_h="자주 묻는 질문", faq_more=None,
    family_k="Family", family_h="醉俠 The Drunken Master 패밀리",
    family=[
        ("醉俠 The Drunken Master", "가오슝의 위스키 브랜드로, 오랫동안 지역 위스키 문화를 이끌어 왔습니다."),
        ("Nova Whisky Bar 新星威士忌酒館", "링야구의 위스키 바, 바로 이곳입니다."),
        ("南曜蒸餾所 NOVA Distillery", "팀이 가오슝에 짓고 있는 크래프트 증류소. 당화부터 증류까지 직접 운영합니다."),
    ],
    journal_k="Journal", journal_h="글", journal_more="전체 글 보기",
    warn_extra="대만에서는 만 18세 미만 음주가 금지되어 있습니다. 음주운전은 절대 하지 마세요.",
    age_q="만 18세 이상이신가요?", age_yes="네, 18세 이상입니다", age_no="아니요, 나가기",
    lang_name="한국어",
)

FAQ = {
"zh": [
    ("Nova Whisky Bar 是什麼樣的酒吧？", "高雄苓雅區的威士忌酒吧，以蘇格蘭威士忌為主，特別是單一麥芽、獨立裝瓶與單桶酒款。店裡安靜、適合一個人獨飲，可以依你的口味和喜歡的桶型推薦，也能安排幾支酒並排比較。"),
    ("平常很少喝純飲，對威士忌不熟的新手適合來嗎？", "適合。不用懂術語，告訴我們你平常喝什麼、喜歡甜一點還是煙燻一點，我們會從好入口的酒開始帶。單杯超過 NT$500 的酒款可以點半杯，多試幾支也不會負擔太重。"),
    ("一個人來喝酒會不會尷尬？適合安靜獨飲嗎？", "很多客人都是一個人來。店裡刻意保持安靜，適合下班後自己喝一杯放空，也適合兩三個朋友輕聲聊天。想聊酒隨時找我們，想要自己的空間也沒人打擾。"),
    ("可以點半杯嗎？", "可以。單杯價格超過 NT$500 的酒款都可以點半杯，想多試幾支高年份或稀有單桶時很方便。"),
    ("同行朋友不喝威士忌純飲，有其他選擇嗎？", "有。店裡也有 Highball、調酒與無酒精飲料，同行朋友各自有選擇。"),
    ("店裡有哪些威士忌？", "以蘇格蘭威士忌為主，包含各產區的單一麥芽，以及 Gordon &amp; MacPhail、Douglas Laing、SMWS 等獨立裝瓶商的單桶酒款。{bottles}"),
    ("Nova 在哪裡？", "地址是高雄市苓雅區林森二路128巷14號 2樓。"),
    ("營業時間是幾點到幾點？", "週日、週一、週三至週五 20:00–01:30，週六 20:00–02:00，每週二公休。臨時異動以官方社群公告為準。"),
    ("大概的消費是多少？有低消嗎？", "{price}"),
    ("需要訂位嗎？", f"人數較多或週末建議先來電 {TEL_DISPLAY}，或私訊 Instagram @novawhisky。"),
    ("可以用英文、日文、韓文點酒嗎？", "{language}"),
    ("可以刷卡嗎？", "可以。接受{payment}。"),
    ("有舉辦品酒會嗎？", "有。我們不定期與酒商、品牌大使合作舉辦小規模的主題品飲，場次與報名方式會在官方 Instagram、Facebook 與 Threads 公布。"),
    ("Nova 和以前的高雄高地人小酒館（Highlander Inn Takao）是同一間店嗎？", "是。高雄高地人小酒館（Highlander Inn Takao）在 2026 年 4 月更名為 Nova Whisky Bar 新星威士忌酒館。"),
    ("Nova 和醉俠是什麼關係？", "Nova 屬於醉俠 The Drunken Master 體系，和高雄建置中的南曜蒸餾所 NOVA Distillery 是同一個團隊。"),
],
"en": [
    ("What kind of bar is Nova Whisky Bar?", "A quiet whisky bar in Lingya District, Kaohsiung, centred on Scotch — especially single malts, independent bottlings and single casks. It's comfortable for solo drinkers; we recommend by taste and cask style and can line up a few drams for comparison."),
    ("I rarely drink whisky neat. Is Nova OK for beginners?", "Yes. Tell us what you usually drink and whether you like it sweeter or smokier, and we'll start with something approachable. Drams over NT$500 come as half pours too, so trying several won't break the bank."),
    ("Is it awkward to come alone? Is it quiet?", "Plenty of guests come on their own. We keep the room quiet — good for unwinding by yourself or a low-voiced chat with a friend or two. Talk whisky with us if you like, or keep to yourself."),
    ("Can I order a half pour?", "Yes. Any dram priced over NT$500 is available as a half pour — handy for trying older or rarer single casks."),
    ("My friends don't drink whisky neat. Anything for them?", "Yes — Highballs, cocktails and non-alcoholic drinks."),
    ("What whiskies do you have?", "Mainly Scotch: single malts from across the regions, plus single casks from independent bottlers such as Gordon &amp; MacPhail, Douglas Laing and SMWS. {bottles}"),
    ("Where is Nova?", "2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City."),
    ("What are the opening hours?", "Sunday, Monday and Wednesday to Friday 20:00–01:30, Saturday 20:00–02:00. Closed on Tuesdays. Any other closures are announced on our social media."),
    ("How much does it cost? Is there a minimum charge?", "{price}"),
    ("Do I need a reservation?", "For larger groups or weekends, call +886 7 330 8050 or send a DM to @novawhisky on Instagram."),
    ("Can I order in English, Japanese or Korean?", "{language}"),
    ("Do you take cards?", "Yes. We accept cash and credit cards."),
    ("Do you host tastings?", "Yes. We hold small tastings with importers and brand ambassadors from time to time. Dates and sign-up details go up on our Instagram, Facebook and Threads."),
    ("Is Nova the same bar as Highlander Inn Takao?", "Yes. Highlander Inn Takao (高雄高地人小酒館) was renamed Nova Whisky Bar (新星威士忌酒館) in April 2026."),
    ("How is Nova related to The Drunken Master?", "Nova is part of The Drunken Master (醉俠) family and shares its team with NOVA Distillery (南曜蒸餾所), a craft distillery being built in Kaohsiung."),
],
"ja": [
    ("Nova Whisky Bar はどんなバーですか？", "高雄市苓雅区の静かなウイスキーバーで、スコッチが中心です。特にシングルモルト、独立瓶詰め、シングルカスクを揃えています。お一人でも落ち着いて飲め、好みの味や樽に合わせたお勧めや、数種類の飲み比べもご用意できます。"),
    ("ストレートはあまり飲みません。初心者でも大丈夫ですか？", "大丈夫です。普段飲んでいるものや、甘めかスモーキーかの好みを教えてください。飲みやすい一杯から始めます。1杯 NT$500 を超えるものはハーフもできるので、何種類か試しても負担になりにくいです。"),
    ("一人で行っても気まずくないですか？静かに飲めますか？", "お一人で来られる方も多いです。店内はあえて静かにしているので、仕事帰りに一人でぼんやり飲むのにも、二、三人で小声で話すのにも向いています。お酒の話がしたければいつでもどうぞ。"),
    ("ハーフで注文できますか？", "はい。1杯 NT$500 を超えるウイスキーはすべてハーフで注文できます。高年数や希少なシングルカスクを何種類か試したいときに便利です。"),
    ("連れがストレートを飲みません。他の選択肢はありますか？", "はい。ハイボール、カクテル、ノンアルコールドリンクもあります。"),
    ("どんなウイスキーがありますか？", "スコッチが中心で、各地域のシングルモルトと、Gordon &amp; MacPhail、Douglas Laing、SMWS などの独立瓶詰めシングルカスクがあります。{bottles}"),
    ("お店の場所は？", "住所は高雄市苓雅区林森二路128巷14号 2階です。"),
    ("営業時間は？", "日曜・月曜・水曜〜金曜 20:00–01:30、土曜 20:00–02:00。火曜日定休です。臨時休業は公式SNSでお知らせします。"),
    ("予算はどのくらいですか？ミニマムチャージはありますか？", "{price}"),
    ("予約は必要ですか？", "大人数や週末は、+886 7 330 8050 へのお電話か Instagram @novawhisky の DM でご連絡ください。"),
    ("日本語で注文できますか？", "{language}"),
    ("カードは使えますか？", "はい。お支払いは{payment}がご利用いただけます。"),
    ("テイスティング会はありますか？", "はい。輸入元やブランドアンバサダーと組んだ少人数のテイスティング会を不定期に開いています。日程と申し込み方法は公式 Instagram、Facebook、Threads でお知らせします。"),
    ("Highlander Inn Takao と同じお店ですか？", "はい。高雄高地人小酒館（Highlander Inn Takao）は2026年4月に Nova Whisky Bar（新星威士忌酒館）へ改名しました。"),
    ("醉俠（The Drunken Master）との関係は？", "Nova は醉俠 The Drunken Master グループの一員で、高雄で建設中の南曜蒸餾所 NOVA Distillery と同じチームです。"),
],
"ko": [
    ("Nova Whisky Bar는 어떤 바인가요?", "가오슝 링야구의 조용한 위스키 바로, 스카치가 중심입니다. 특히 싱글 몰트, 독립 병입, 싱글 캐스크를 많이 갖추고 있습니다. 혼자서도 편하게 마실 수 있고, 취향과 캐스크 스타일에 맞춰 추천하거나 몇 잔을 비교 시음할 수 있게 준비해 드립니다."),
    ("평소 니트로 잘 안 마시는데, 위스키 초보도 괜찮을까요?", "물론입니다. 평소 즐기는 술과 달콤한 쪽인지 스모키한 쪽인지 알려 주시면 마시기 편한 잔부터 시작합니다. 한 잔에 NT$500가 넘는 위스키는 하프 잔도 되니 여러 종류를 맛봐도 부담이 적습니다."),
    ("혼자 가도 어색하지 않을까요? 조용히 마실 수 있나요?", "혼자 오시는 분이 많습니다. 가게는 일부러 조용하게 유지해서, 퇴근 후 혼자 한 잔 하기에도, 두세 명이 나지막이 이야기 나누기에도 좋습니다. 위스키 이야기가 하고 싶으면 언제든 말을 걸어 주세요."),
    ("하프 잔으로 주문할 수 있나요?", "네. 한 잔 가격이 NT$500를 넘는 위스키는 모두 하프 잔으로 주문할 수 있습니다. 고숙성이나 희귀 싱글 캐스크를 여러 종류 맛볼 때 편리합니다."),
    ("일행이 위스키를 니트로 안 마시는데, 다른 선택지가 있나요?", "네. 하이볼, 칵테일, 무알코올 음료도 있습니다."),
    ("어떤 위스키가 있나요?", "스카치 위주로 지역별 싱글 몰트와 Gordon &amp; MacPhail, Douglas Laing, SMWS 등 독립 병입 싱글 캐스크가 있습니다. {bottles}"),
    ("위치가 어디인가요?", "주소는 2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City입니다."),
    ("영업시간은 어떻게 되나요?", "일요일, 월요일, 수요일~금요일 20:00–01:30, 토요일 20:00–02:00이며 매주 화요일은 휴무입니다. 임시 휴무는 공식 SNS에서 공지합니다."),
    ("가격대는 어느 정도인가요? 최소 주문이 있나요?", "{price}"),
    ("예약이 필요한가요?", "인원이 많거나 주말이라면 +886 7 330 8050으로 전화하시거나 Instagram @novawhisky로 DM 주세요."),
    ("한국어로 주문할 수 있나요?", "{language}"),
    ("카드 결제가 되나요?", "네. {payment} 모두 가능합니다."),
    ("테이스팅 행사가 있나요?", "네. 수입사, 브랜드 앰배서더와 함께 소규모 테이스팅을 비정기적으로 엽니다. 일정과 신청 방법은 공식 Instagram, Facebook, Threads에서 알려 드립니다."),
    ("Highlander Inn Takao와 같은 가게인가요?", "네. 高雄高地人小酒館(Highlander Inn Takao)는 2026년 4월 Nova Whisky Bar(新星威士忌酒館)로 이름을 바꿨습니다."),
    ("醉俠(The Drunken Master)와는 어떤 관계인가요?", "Nova는 醉俠 The Drunken Master 패밀리에 속하며, 가오슝에서 건설 중인 南曜蒸餾所 NOVA Distillery와 같은 팀입니다."),
],
}

# 文章清單（之後每篇品飲紀錄新增一筆）
ARTICLES = [
    dict(url="https://zerg1129.github.io/nova-GM-Old-Connoisseurs-Choice-/",
         title="Gordon & MacPhail Connoisseurs Choice 老年份四支：Dallas Dhu、Glen Albyn、Ardbeg、Port Ellen",
         summary="四支 Connoisseurs Choice 老年份單一麥芽，搭配各自酒廠的歷史與品飲紀錄。"),
    dict(url="https://zerg1129.github.io/nova-knowledge/",
         title="一篇看懂橡木桶如何改變威士忌",
         summary="美洲橡木、歐洲橡木、風乾與烘烤，如何一路影響杯中的風味。新手友善的入門指南。"),
]

# 站內品飲紀錄（四語，新的放最上面）。網址：journal/SLUG/、en/journal/SLUG/、ja/journal/SLUG/、ko/journal/SLUG/
# img：assets/ 裡的照片檔名前綴，需有 -720 與 -1080 的 .jpg／.webp（直式 1080×1350）
SERIES = {"zh": "座標 22.6°N｜新星亮這杯", "en": "22.6°N | Nova in the Glass",
          "ja": "22.6°N | Nova in the Glass", "ko": "22.6°N | Nova in the Glass"}
POST_UI = {
    "zh": dict(crumb="文章", by="醉郭", notes_h="品飲紀錄",
               closing="這杯在高雄苓雅的 Nova Whisky Bar 新星威士忌酒館喝得到，數量有限，以現場為準。"),
    "en": dict(crumb="Journal", by="Drunken Kuo", notes_h="Tasting notes",
               closing="You can drink this one at Nova Whisky Bar in Lingya District, Kaohsiung. Stock is limited — ask at the bar."),
    "ja": dict(crumb="記事", by="醉郭（Drunken Kuo）", notes_h="テイスティングノート",
               closing="このウイスキーは高雄・苓雅区の Nova Whisky Bar でお飲みいただけます。数量限定のため、在庫は店頭でご確認ください。"),
    "ko": dict(crumb="글", by="醉郭 (Drunken Kuo)", notes_h="테이스팅 노트",
               closing="이 위스키는 가오슝 링야구의 Nova Whisky Bar에서 맛보실 수 있습니다. 수량이 한정되어 있으니 재고는 매장에서 확인해 주세요."),
}
POSTS = [dict(
    slug="maoweiki-cosmos-autumn-aya023011", date="2026-11-27", img="maoweiki-cosmos-autumn",
    about="Maoweiki 2022/2026 Single Cask #AYA023011, Cosmos • Autumn (Ex-Rye Cask)",
    text={
        "zh": dict(
            title="貓尾崎《秋・波斯菊》2022/2026 單桶 #AYA023011",
            lead="2026 TWSC「最佳台灣蒸溜所」貓尾崎，以美國裸麥桶全程熟成約 4 年 4 個月的單桶。",
            desc="貓尾崎蒸溜所（Maoweiki Distillery）《秋・波斯菊》Cosmos・Autumn 單桶 #AYA023011，2022 年 6 月蒸餾、2026 年 10 月裝瓶，Ex-Rye Cask，153 瓶，56.2%。台灣新世代酒廠的單一麥芽，在高雄 Nova Whisky Bar 喝得到。",
            summary="台灣新世代酒廠貓尾崎的單桶，美國裸麥桶全程熟成，Ex-Rye Cask #AYA023011，153 瓶，56.2%。",
            alt="貓尾崎《秋・波斯菊》酒瓶，紫色波斯菊酒標，背景是 Nova Whisky Bar 的酒架",
            fig="Cosmos・Autumn《秋・波斯菊》，Ex-Rye Cask #AYA023011。",
            info=[("酒廠", "貓尾崎蒸溜所 Maoweiki Distillery"), ("蒸餾", "2022.06"), ("裝瓶", "2026.10"),
                  ("桶型", "Ex-Rye Cask（美國裸麥桶）"), ("桶號", "#AYA023011"), ("瓶數", "153 瓶"), ("酒精度", "56.2%")],
            body=["這兩天有看到台灣威士忌的國際捷報嗎？來自屏東的大武山威士忌，剛在英國 IWSC 拿下「世界產區威士忌冠軍」！",
                  "其實今年五月，另一間台灣新世代酒廠也在日本獲得肯定，就是貓尾崎蒸溜所（Maoweiki Distillery），在 2026 TWSC 東京威士忌與烈酒競賽中，獲頒「最佳台灣蒸溜所」。",
                  "台灣威士忌不再只有熟悉的大酒廠，一個百花齊放的新時代真的來了。",
                  "今天分享的這瓶《秋・波斯菊》正好呼應此刻，以美國裸麥桶（Ex-Rye Cask）全程熟成約 4 年 4 個月。清新明亮的花果香，帶有莓果、李子與柑橘的甜美氣息，入口柔順，交織著蜜糖、奶油與堅果，最後留下淡雅花香、木質與溫暖的辛香，宛如秋日午後的陽光。",
                  "對了，大家知道波斯菊的英文 Cosmos，也有「宇宙」的含義嗎？期許未來有越來越多台灣酒廠，一起進入威士忌宇宙發光發熱！",
                  "今晚，就來 Nova 喝一杯台灣新世代酒廠的味道吧！"],
            notes=[("香氣", "清新明亮的花果香、覆盆子、些許鹹甜蜜餞、李子與柳橙硬糖。接著是明亮的蜜糖漿、花香、堅果、香草與草本，後段是烘烤橡木、肉桂、小荳蔻與白胡椒"),
                   ("口感", "口感柔順。柑橘、莓果、果乾、鹹甜蜜餞、奶油、蜜糖漿、核桃、香草、草本、木質、肉桂與辛香料"),
                   ("尾韻", "中等尾韻。柑橘、李子、果乾、花香、奶油、核桃、椰子、木質、肉桂與白胡椒")]),
        "en": dict(
            title="Maoweiki 2022/2026 Single Cask #AYA023011, Cosmos • Autumn",
            lead="A single cask from Maoweiki, named Best Taiwanese Distillery at TWSC 2026, matured entirely in an American ex-rye cask for about 4 years and 4 months.",
            desc="Maoweiki Distillery Cosmos • Autumn, Single Cask #AYA023011: distilled June 2022, bottled October 2026, Ex-Rye Cask, 153 bottles, 56.2%. A single malt from Taiwan's new generation of distilleries, pouring at Nova Whisky Bar, Kaohsiung.",
            summary="A single cask from new-generation Taiwanese distillery Maoweiki, fully matured in American ex-rye: Ex-Rye Cask #AYA023011, 153 bottles, 56.2%.",
            alt="Bottle of Maoweiki Cosmos • Autumn with its purple cosmos-flower label, in front of the shelves at Nova Whisky Bar",
            fig="Cosmos • Autumn, Ex-Rye Cask #AYA023011.",
            info=[("Distillery", "Maoweiki Distillery"), ("Distilled", "June 2022"), ("Bottled", "October 2026"),
                  ("Cask type", "Ex-Rye Cask (American)"), ("Cask number", "#AYA023011"), ("Bottles", "153"), ("ABV", "56.2%")],
            body=["Have you heard the exciting news about Taiwanese whisky over the past few days? Dawu Whisky from Pingtung, Taiwan, has just won the Worldwide Whiskey Trophy at the UK's International Wine & Spirit Competition (IWSC)!",
                  "Earlier this May, another new-generation Taiwanese distillery also received international recognition in Japan. Maoweiki Distillery was named Best Taiwanese Distillery at the 2026 Tokyo Whisky & Spirits Competition (TWSC).",
                  "Taiwanese whisky is no longer defined solely by its familiar major distilleries. A new era of diverse styles and distinctive voices is truly in bloom.",
                  "Today's whisky, Maoweiki's Cosmos • Autumn, feels particularly fitting for this moment.",
                  "Matured entirely in an American ex-rye whiskey cask for approximately 4 years and 4 months, it opens with fresh, bright floral and fruity aromas, accompanied by the sweetness of berries, plums and citrus.",
                  "The palate is smooth, with honey, cream and nuts beautifully intertwined, leaving delicate floral notes, oak and warming spices on the finish — like the gentle sunlight of an autumn afternoon.",
                  "By the way, did you know that Cosmos is both the name of a flower and another word for the universe?",
                  "Here's to more Taiwanese distilleries finding their place and shining together in the whisky universe!",
                  "Tonight, discover the flavours of Taiwan's new generation of distilleries at Nova Whisky Bar."],
            notes=[("Nose", "Fresh, bright floral and fruity notes, raspberries, a hint of sweet-and-salty preserved fruit, plum and orange hard candies. Followed by bright honey syrup, florals, nuts, vanilla and herbs. Later, toasted oak, cinnamon, cardamom and white pepper."),
                   ("Palate", "Smooth mouthfeel. Citrus, berries, dried fruits, sweet-and-salty preserved fruit, cream, honey syrup, walnuts, vanilla, herbs, wood, cinnamon and spices."),
                   ("Finish", "Medium. Citrus, plum, dried fruits, florals, cream, walnuts, coconut, woody notes, cinnamon and white pepper.")]),
        "ja": dict(
            title="貓尾崎 2022/2026 シングルカスク #AYA023011「秋・コスモス」",
            lead="2026年TWSC「ベスト・タイワニーズ・ディスティラリー」の貓尾崎が、アメリカン・ライウイスキー樽で約4年4カ月全期間熟成させたシングルカスク。",
            desc="貓尾崎蒸溜所（Maoweiki Distillery）「秋・コスモス」Cosmos • Autumn シングルカスク #AYA023011。2022年6月蒸溜、2026年10月瓶詰め、Ex-Rye Cask、153本、56.2%。台湾の新世代蒸溜所のシングルモルトを高雄の Nova Whisky Bar で。",
            summary="台湾の新世代蒸溜所・貓尾崎のシングルカスク。アメリカン・ライ樽で全期間熟成、Ex-Rye Cask #AYA023011、153本、56.2%。",
            alt="紫のコスモスのラベルが付いた貓尾崎「秋・コスモス」のボトル。背景は Nova Whisky Bar のボトル棚",
            fig="Cosmos • Autumn「秋・コスモス」、Ex-Rye Cask #AYA023011。",
            info=[("蒸溜所", "貓尾崎蒸溜所 Maoweiki Distillery"), ("蒸溜", "2022年6月"), ("瓶詰め", "2026年10月"),
                  ("樽", "Ex-Rye Cask（アメリカン・ライウイスキー樽）"), ("樽番号", "#AYA023011"), ("本数", "153本"), ("アルコール度数", "56.2%")],
            body=["ここ数日、台湾ウイスキーのうれしい国際ニュースをご覧になりましたか？",
                  "台湾・屏東の大武山（Dawu）ウイスキーが、英国の国際ワイン＆スピリッツコンペティション（IWSC）で「ワールドワイド・ウイスキー・トロフィー」を受賞しました！",
                  "実は今年5月にも、台湾の新世代蒸溜所が日本で高い評価を受けています。2026年の東京ウイスキー＆スピリッツコンペティション（TWSC）で「ベスト・タイワニーズ・ディスティラリー」に選ばれた、貓尾崎蒸溜所（Maoweiki Distillery）です。",
                  "台湾ウイスキーは、もはやおなじみの大手蒸溜所だけではありません。それぞれの個性が花開く、百花繚乱の新時代が本当に訪れました。",
                  "本日ご紹介する貓尾崎の「秋・コスモス」は、まさに今の台湾ウイスキーを象徴するような一本です。",
                  "アメリカン・ライウイスキーの空き樽で、約4年4カ月にわたり全期間熟成されています。",
                  "爽やかで華やかな花と果実の香りに、ベリーやプラム、柑橘類の甘い香りが重なります。口当たりはなめらかで、蜂蜜、クリーム、ナッツが心地よく調和。余韻には繊細な花の香り、木のニュアンス、温かなスパイスが残ります。まるで秋の午後の陽だまりのようです。",
                  "ところで、コスモスの英語名「Cosmos」には、「宇宙」という意味もあることをご存じですか？",
                  "これからも、より多くの台湾の蒸溜所がウイスキーという宇宙で、それぞれの輝きを放つことを願っています！",
                  "今夜はNovaで、台湾の新世代蒸溜所が生み出すウイスキーを味わってみませんか？"],
            notes=[("香り", "爽やかで明るい花と果実、ラズベリー、ほのかな甘じょっぱい果物の砂糖漬け、プラムとオレンジのキャンディ。続いて明るいハニーシロップ、フローラル、ナッツ、バニラ、ハーブ。後半はトーストしたオーク、シナモン、カルダモン、ホワイトペッパー"),
                   ("味わい", "なめらかな口当たり。シトラス、ベリー、ドライフルーツ、甘じょっぱい果物の砂糖漬け、クリーム、ハニーシロップ、クルミ、バニラ、ハーブ、ウッド、シナモン、スパイス"),
                   ("余韻", "ミディアム。シトラス、プラム、ドライフルーツ、フローラル、クリーム、クルミ、ココナッツ、ウッディ、シナモン、ホワイトペッパー")]),
        "ko": dict(
            title="마오웨이키 2022/2026 싱글 캐스크 #AYA023011 ‘코스모스·어텀’",
            lead="2026 TWSC ‘최우수 대만 증류소’ 마오웨이키가 미국 라이 위스키 캐스크에서 약 4년 4개월 동안 숙성한 싱글 캐스크.",
            desc="마오웨이키 증류소(Maoweiki Distillery) ‘코스모스·어텀(Cosmos • Autumn)’ 싱글 캐스크 #AYA023011. 2022년 6월 증류, 2026년 10월 병입, Ex-Rye Cask, 153병, 56.2%. 대만 신세대 증류소의 싱글 몰트를 가오슝 Nova Whisky Bar에서 맛볼 수 있습니다.",
            summary="대만 신세대 증류소 마오웨이키의 싱글 캐스크. 미국 라이 캐스크 풀 숙성, Ex-Rye Cask #AYA023011, 153병, 56.2%.",
            alt="보라색 코스모스 라벨의 마오웨이키 ‘코스모스·어텀’ 보틀. 뒤로 Nova Whisky Bar의 술장이 보인다",
            fig="Cosmos • Autumn ‘코스모스·어텀’, Ex-Rye Cask #AYA023011.",
            info=[("증류소", "마오웨이키 증류소 Maoweiki Distillery"), ("증류", "2022년 6월"), ("병입", "2026년 10월"),
                  ("캐스크", "Ex-Rye Cask (미국 라이 위스키 캐스크)"), ("캐스크 번호", "#AYA023011"), ("병 수", "153병"), ("도수", "56.2%")],
            body=["최근 대만 위스키가 국제 무대에서 전해 온 반가운 소식, 보셨나요? 대만 핑둥의 다우(Dawu) 위스키가 영국 IWSC에서 ‘월드와이드 위스키 트로피’를 수상했습니다!",
                  "사실 올해 5월에도 대만의 또 다른 신세대 증류소가 일본에서 좋은 평가를 받았습니다. 바로 2026 도쿄 위스키 & 스피리츠 컴피티션(TWSC)에서 ‘최우수 대만 증류소’로 선정된 마오웨이키 증류소(Maoweiki Distillery)입니다.",
                  "이제 대만 위스키는 익숙한 대형 증류소에만 머물지 않습니다. 저마다의 개성을 지닌 새로운 증류소들이 활짝 꽃피우는 시대가 정말 찾아왔습니다.",
                  "오늘 소개하는 마오웨이키의 ‘코스모스·어텀(Cosmos • Autumn)’은 이런 순간과 참 잘 어울리는 위스키입니다.",
                  "미국 라이 위스키를 담았던 캐스크에서 약 4년 4개월 동안 숙성했습니다.",
                  "싱그럽고 화사한 꽃과 과일 향에 베리류, 자두, 감귤류의 달콤함이 더해집니다. 입안에서는 꿀, 크림, 견과류가 부드럽게 어우러지고, 은은한 꽃향기와 우디함, 따뜻한 향신료가 여운을 남깁니다. 마치 가을 오후의 햇살처럼 말이죠.",
                  "그런데 코스모스의 영어 이름인 Cosmos에는 ‘우주’라는 뜻도 있다는 사실, 알고 계셨나요?",
                  "앞으로 더 많은 대만 증류소가 위스키라는 우주에서 함께 빛나기를 기대합니다!",
                  "오늘 밤, Nova에서 대만 신세대 증류소의 위스키를 만나 보세요!"],
            notes=[("향", "싱그럽고 밝은 꽃과 과일, 라즈베리, 은은한 단짠 과일 절임, 자두와 오렌지 캔디. 이어서 밝은 꿀 시럽, 꽃, 견과류, 바닐라, 허브, 후반에는 토스트한 오크, 시나몬, 카다멈, 백후추"),
                   ("맛", "부드러운 질감. 시트러스, 베리, 말린 과일, 단짠 과일 절임, 크림, 꿀 시럽, 호두, 바닐라, 허브, 나무, 시나몬, 향신료"),
                   ("피니시", "미디엄. 시트러스, 자두, 말린 과일, 꽃, 크림, 호두, 코코넛, 우디함, 시나몬, 백후추")]),
    },
), dict(
    slug="glenrothes-2000-single-cask-2364", date="2026-11-22", img="glenrothes-2000-2364",
    about="The Glenrothes 2000 Single Cask #2364 (Sherry Butt)",
    text={
        "zh": dict(
            title="The Glenrothes 2000/2017 Single Cask #2364",
            lead="BBR 時代以蒸餾年份標示的 Glenrothes 單桶，2000 年蒸餾、2017 年裝瓶。",
            desc="The Glenrothes 2000 年蒸餾、2017 年裝瓶的單桶 #2364，Sherry Butt，575 瓶，58.7%，UK Exclusive Single Cask Series Batch #1。BBR 掌握品牌時期的年份酒標，在高雄 Nova Whisky Bar 喝得到。",
            summary="BBR 時代的年份酒標，2000 年蒸餾、2017 年裝瓶，Sherry Butt #2364，58.7%。",
            alt="The Glenrothes 2000 Single Cask #2364 酒瓶，金色酒標，背景是 Nova Whisky Bar 的酒架",
            fig="UK Exclusive Single Cask Series 第一批，Sherry Butt #2364。",
            info=[("酒廠", "Glenrothes"), ("系列", "UK Exclusive Single Cask Series, Batch #1"), ("蒸餾", "2000"), ("裝瓶", "2017"),
                  ("桶型", "Sherry Butt"), ("桶號", "#2364"), ("瓶數", "575 瓶"), ("酒精度", "58.7%")],
            body=["最近高雄的天氣瞬間轉涼了許多，好像該喝一杯溫暖的雪莉桶威士忌了。",
                  "這瓶 Glenrothes 跟現在的酒標怎麼長得不一樣呢？因為這時的 Glenrothes 酒廠雖然隸屬於 Edrington，但實際品牌所有權是在英國百年酒商 Berry Bros. & Rudd（BBR）手上，當時酒標是以 Vintage 蒸餾年份建立辨識度。",
                  "直到 2017 年 5 月，Edrington 買回品牌，酒廠與品牌再度合而為一；隔年，酒標也改成大家比較熟悉的熟成年數。",
                  "這瓶單桶蘊藏著兩段歷史故事。2000 年蒸餾時，酒廠恰逢「做半年、休半年」的減產期；裝瓶的 2017 年，則是品牌交接的那一年，有沒有很剛好？",
                  "58.7% 的原酒強度，喝起來就像在微涼空氣裡聞到明亮的葡萄乾與莓果軟糖，入口後則轉為中深焙咖啡豆的沉穩氣息。很適合在這樣轉涼的夜晚，來 Nova 慢慢喝一杯。"],
            notes=[("香氣", "明亮的葡萄乾、莓果軟糖、深色莓果、柑橘與果乾，接著是焦糖、堅果與香草，後段是橡木、甘草、肉桂與胡椒"),
                   ("口感", "中等口感。豐富的葡萄乾、莓果、柑橘、焦糖、黑巧克力、黑咖啡、堅果、烘烤橡木、小荳蔻與胡椒"),
                   ("尾韻", "中長尾韻。葡萄乾、果乾、柑橘、黑巧克力、些微焦糖、核桃、橡木、皮革、小荳蔻與胡椒")]),
        "en": dict(
            title="The Glenrothes 2000/2017 Single Cask #2364",
            lead="A Glenrothes single cask from the Berry Bros. & Rudd era, when the label led with the vintage.",
            desc="The Glenrothes Single Cask #2364, distilled 2000 and bottled 2017 (Sherry Butt, 575 bottles, 58.7%), UK Exclusive Single Cask Series, Batch #1, from the Berry Bros. & Rudd vintage era. Pouring at Nova Whisky Bar, Kaohsiung.",
            summary="A vintage-era Glenrothes from the BBR years: distilled 2000, bottled 2017, Sherry Butt #2364, 58.7%.",
            alt="Bottle of The Glenrothes 2000 Single Cask #2364 with its gold label, in front of the shelves at Nova Whisky Bar",
            fig="UK Exclusive Single Cask Series, Batch #1 — Sherry Butt #2364.",
            info=[("Distillery", "Glenrothes"), ("Series", "UK Exclusive Single Cask Series, Batch #1"), ("Distilled", "2000"), ("Bottled", "2017"),
                  ("Cask type", "Sherry Butt"), ("Cask number", "#2364"), ("Bottles", "575"), ("ABV", "58.7%")],
            body=["Kaohsiung just turned chilly—time for a sherry cask.",
                  "Under BBR, Glenrothes highlighted the vintage year. Edrington bought the brand back in May 2017, and the core range switched to age statements in 2018.",
                  "Distilled in 2000 (six months on, six off) and bottled in 2017. This 58.7% cask moves from raisins and berry gummies to medium-dark roast coffee. Come unwind at Nova."],
            notes=[("Nose", "Bright raisins, berry gummies, dark berries, citrus and dried fruits. Followed by caramel, nuts and vanilla. Later, oak, liquorice, cinnamon and pepper."),
                   ("Palate", "Medium mouthfeel. Rich raisins, berries, citrus, caramel, dark chocolate, black coffee, nuts, toasted oak, cardamom and pepper."),
                   ("Finish", "Medium-long. Raisins, dried fruits, citrus, dark chocolate, a hint of caramel, walnuts, oak, leather, cardamom and pepper.")]),
        "ja": dict(
            title="The Glenrothes 2000/2017 Single Cask #2364",
            lead="Berry Bros. & Rudd がブランドを持ち、蒸留年で名乗っていた時代の Glenrothes シングルカスク。",
            desc="2000年蒸留・2017年瓶詰めの The Glenrothes シングルカスク #2364（Sherry Butt、575本、58.7%）。UK Exclusive Single Cask Series Batch #1。BBR 時代のヴィンテージ表記ボトルを高雄の Nova Whisky Bar で。",
            summary="BBR 時代のヴィンテージ表記。2000年蒸留、2017年瓶詰め、Sherry Butt #2364、58.7%。",
            alt="金色ラベルの The Glenrothes 2000 Single Cask #2364 のボトル。背景は Nova Whisky Bar のボトル棚",
            fig="UK Exclusive Single Cask Series 第1弾、Sherry Butt #2364。",
            info=[("蒸溜所", "Glenrothes"), ("シリーズ", "UK Exclusive Single Cask Series, Batch #1"), ("蒸溜", "2000"), ("瓶詰め", "2017"),
                  ("樽", "Sherry Butt"), ("樽番号", "#2364"), ("本数", "575本"), ("アルコール度数", "58.7%")],
            body=["急に涼しくなった高雄。シェリー樽熟成のウイスキーが恋しくなる夜です。",
                  "蒸留年を大きく記したこのラベルは、英国の老舗酒商BBRがブランドを持っていた頃のもの。2017年5月にエドリントンが買い戻し、翌年、主力シリーズは熟成年数表記に変わりました。",
                  "半年稼働・半年休止で減産していた2000年に蒸留、ブランドが戻った2017年に瓶詰めされた一本です。58.7%の原酒はレーズンとベリーグミが香り、口に含むと中深煎りのコーヒーを思わせます。今夜はNovaでゆっくりどうぞ。"],
            notes=[("香り", "明るいレーズン、ベリーグミ、ダークベリー、シトラス、ドライフルーツ。続いてキャラメル、ナッツ、バニラ。後半はオーク、リコリス、シナモン、ペッパー"),
                   ("味わい", "ミディアムな口当たり。濃厚なレーズン、ベリー、シトラス、キャラメル、ダークチョコレート、ブラックコーヒー、ナッツ、トーストしたオーク、カルダモン、ペッパー"),
                   ("余韻", "ミディアムロング。レーズン、ドライフルーツ、シトラス、ダークチョコレート、ほのかなキャラメル、クルミ、オーク、レザー、カルダモン、ペッパー")]),
        "ko": dict(
            title="The Glenrothes 2000/2017 Single Cask #2364",
            lead="Berry Bros. & Rudd가 브랜드를 갖고 증류 연도로 이름을 붙이던 시절의 Glenrothes 싱글 캐스크.",
            desc="2000년 증류, 2017년 병입한 The Glenrothes 싱글 캐스크 #2364(Sherry Butt, 575병, 58.7%). UK Exclusive Single Cask Series Batch #1. BBR 시절 빈티지 라벨 보틀을 가오슝 Nova Whisky Bar에서 맛볼 수 있습니다.",
            summary="BBR 시절 빈티지 라벨. 2000년 증류, 2017년 병입, Sherry Butt #2364, 58.7%.",
            alt="금색 라벨의 The Glenrothes 2000 Single Cask #2364 보틀. 뒤로 Nova Whisky Bar의 술장이 보인다",
            fig="UK Exclusive Single Cask Series 첫 배치, Sherry Butt #2364.",
            info=[("증류소", "Glenrothes"), ("시리즈", "UK Exclusive Single Cask Series, Batch #1"), ("증류", "2000"), ("병입", "2017"),
                  ("캐스크", "Sherry Butt"), ("캐스크 번호", "#2364"), ("병 수", "575병"), ("도수", "58.7%")],
            body=["갑자기 선선해진 가오슝, 셰리 캐스크가 생각나는 밤입니다.",
                  "영국 주류상 BBR 시절의 증류 연도 라벨입니다. 2017년 5월 에드링턴이 브랜드를 되찾고, 이듬해 주력 라인은 숙성 연수 표기로 바뀌었죠.",
                  "반년만 가동하던 2000년에 증류해 브랜드가 돌아간 2017년에 병입했습니다. 58.7% 원액은 건포도와 베리 젤리 향 뒤로 중강배전 커피가 떠오릅니다. 오늘 밤 Nova에서 천천히 즐겨 보세요."],
            notes=[("향", "밝은 건포도, 베리 젤리, 검은 베리류, 시트러스, 말린 과일. 이어서 캐러멜, 견과류, 바닐라, 후반에는 오크, 감초, 시나몬, 후추"),
                   ("맛", "미디엄 바디. 풍부한 건포도, 베리, 시트러스, 캐러멜, 다크 초콜릿, 블랙 커피, 견과류, 토스트한 오크, 카다멈, 후추"),
                   ("피니시", "미디엄 롱. 건포도, 말린 과일, 시트러스, 다크 초콜릿, 은은한 캐러멜, 호두, 오크, 가죽, 카다멈, 후추")]),
    },
), dict(
    slug="laphroaig-10-friendship-cask", date="2026-11-11", img="laphroaig-friendship-cask",
    about="Laphroaig 10 Years Old The Friendship Cask (Bourbon Cask #7)",
    text={
        "zh": dict(
            title="Laphroaig 10 年 The Friendship Cask",
            lead="一支為台灣與韓國兩間酒吧的週年而選的 Laphroaig 單桶。",
            desc="Laphroaig 2016 蒸餾、2026 裝瓶的 10 年單桶，Bourbon Cask #7，265 瓶，59.5%。為紀念醉俠 The Drunken Master Whisky Bar 10 週年與韓國 Café Swing 6 週年而選，在高雄 Nova Whisky Bar 喝得到。",
            summary="紀念 The Drunken Master Whisky Bar 10 週年與韓國 Café Swing 6 週年的 Laphroaig 單桶，Bourbon Cask #7，59.5%。",
            alt="Laphroaig 10 年 The Friendship Cask 酒瓶，酒標為手繪的酒吧空間插畫，背景是 Nova Whisky Bar 的酒架",
            info=[("酒廠", "Laphroaig"), ("選桶", "The Drunken Master Whisky Bar 10 週年 × Café Swing 6 週年"),
                  ("蒸餾", "2016/06/09"), ("裝瓶", "2026/07"), ("酒齡", "10 年"), ("桶型", "Bourbon Cask"), ("桶號", "#7"),
                  ("瓶數", "265 瓶"), ("酒精度", "59.5%")],
            body=["微涼的天氣，總讓人想來一杯帶著煙燻香氣的泥煤威士忌。",
                  "今天這瓶 THE FRIENDSHIP CASK Laphroaig 10 年，是為了紀念台灣 The Drunken Master Whisky Bar 10 週年與韓國 Café Swing 6 週年而推出的特別紀念單桶。",
                  "Café Swing 的老闆喝到樣品時，說這是一款非常美味的 Laphroaig，波本桶帶來的多層次熱帶水果香氣，明亮而華麗地綻放，令人印象深刻。",
                  "酒標則由 The Drunken Master Whisky Bar 的店長 Elaine 親手繪製，將兩間酒吧的空間與回憶，留在這張特別的紀念酒標上。",
                  "今晚，這瓶象徵台韓友誼的 Laphroaig 10 年，已經可以在 Nova Whisky Bar 喝到單杯了，讓我們邊喝邊為這兩間酒吧慶祝一下吧！"],
            fig="The Drunken Master Whisky Bar 10 週年 × Café Swing 6 週年紀念單桶，酒標由 Elaine 手繪。",
            notes=[("品飲日期", "2026/11/11 20:05"), ("酒色", "淺琥珀色"),
                   ("香氣", "剛開始散發柔和的泥煤及煙燻氣息，鹹味、柑橘、鳳梨、蘋果、熱帶果香和些微碘味點綴著，接著是碳烤、黑巧克力、核桃和香草草本，後段是礦物感、薑、薄荷涼感與辛香料"),
                   ("口感", "中等口感。剛開始有些許鹹味、泥煤、煙燻、柑橘、烤鳳梨、熟果、麥芽、黑巧克力、薑與胡椒"),
                   ("尾韻", "中等尾韻。俐落的泥煤果香甜味、柑橘、檸檬、些微鹹香、麥芽、堅果、薑、草本、椰子、礦物感與胡椒")]),
        "en": dict(
            title="Laphroaig 2016/2026 10YO – The Friendship Cask",
            lead="A Laphroaig single cask chosen to mark the anniversaries of two bars — one in Taiwan, one in Korea.",
            desc="A 10-year-old Laphroaig single cask (distilled 2016, bottled 2026; Bourbon Cask #7, 265 bottles, 59.5% ABV) selected for The Drunken Master Whisky Bar's 10th and Café Swing's 6th anniversaries. Pouring at Nova Whisky Bar, Kaohsiung.",
            summary="A Laphroaig single cask for The Drunken Master Whisky Bar's 10th and Café Swing's 6th anniversaries. Bourbon Cask #7, 59.5% ABV.",
            alt="Bottle of Laphroaig 10 Years Old The Friendship Cask with a hand-drawn bar interior on the label, in front of the shelves at Nova Whisky Bar",
            info=[("Distillery", "Laphroaig"), ("Selected for", "The Drunken Master Whisky Bar 10th Anniversary × Café Swing 6th Anniversary"),
                  ("Distilled", "2016/06/09"), ("Bottled", "2026/07"), ("Age", "10 years"), ("Cask type", "Bourbon Cask"), ("Cask number", "#7"),
                  ("Bottles", "265"), ("ABV", "59.5%")],
            body=["A cool evening calls for something smoky.",
                  "THE FRIENDSHIP CASK is a 10-year-old Laphroaig single cask celebrating the 10th anniversary of The Drunken Master Whisky Bar in Taiwan and the 6th anniversary of Café Swing in Korea.",
                  "Café Swing's owner called it a truly delicious Laphroaig, praising its bright, layered tropical fruit aromas. The label was hand-drawn by Elaine, manager of The Drunken Master Whisky Bar, capturing both bars and the memories made in them.",
                  "Now pouring by the glass at Nova Whisky Bar. Come raise a glass to their friendship with us!"],
            fig="The anniversary cask for The Drunken Master Whisky Bar (10 years) and Café Swing (6 years), with a label hand-drawn by Elaine.",
            notes=[("Tasted", "2026/11/11 20:05"), ("Colour", "Pale amber"),
                   ("Nose", "Soft peat smoke, sea salt, citrus, pineapple and tropical fruit, with a touch of iodine. Then charred notes, dark chocolate, walnut, vanilla and herbs, followed by mineral notes, ginger, mint and spice."),
                   ("Palate", "Medium-bodied. Salt, peat smoke, citrus, grilled pineapple, ripe fruit, malt, dark chocolate, ginger and pepper."),
                   ("Finish", "Medium. Clean, with sweet, fruity peat smoke, citrus, lemon, light salinity, malt, nuts, ginger, coconut, minerals and pepper.")]),
        "ja": dict(
            title="Laphroaig 10年 The Friendship Cask",
            lead="台湾と韓国、ふたつのバーの周年を記念して選ばれた Laphroaig のシングルカスク。",
            desc="2016年蒸溜・2026年瓶詰めの Laphroaig 10年シングルカスク（Bourbon Cask #7、265本、59.5%）。The Drunken Master Whisky Bar 10周年と韓国 Café Swing 6周年の記念ボトル。高雄の Nova Whisky Bar で味わえます。",
            summary="The Drunken Master Whisky Bar 10周年と韓国 Café Swing 6周年を記念した Laphroaig のシングルカスク。Bourbon Cask #7、59.5%。",
            alt="Laphroaig 10年 The Friendship Cask のボトル。ラベルには手描きのバーのイラスト、背景は Nova Whisky Bar のボトル棚",
            info=[("蒸溜所", "Laphroaig"), ("セレクト", "The Drunken Master Whisky Bar 10周年 × Café Swing 6周年"),
                  ("蒸溜", "2016/06/09"), ("瓶詰め", "2026/07"), ("熟成年数", "10年"), ("樽", "Bourbon Cask"), ("樽番号", "#7"),
                  ("本数", "265本"), ("アルコール度数", "59.5%")],
            body=["肌寒い夜には、スモーキーなピートウイスキーを。",
                  "THE FRIENDSHIP CASK Laphroaig 10年は、台湾の The Drunken Master Whisky Bar 10周年と韓国の Café Swing 6周年を記念した特別なシングルカスクです。",
                  "Café Swingのオーナーも「とてもおいしいラフロイグ」と絶賛。幾重にも広がる、明るく華やかなトロピカルフルーツの香りが印象的です。",
                  "ラベルは The Drunken Master Whisky Bar の店長 Elaine が、両店の空間と思い出を手描きしました。",
                  "今夜から Nova Whisky Bar にてグラスでお楽しみいただけます。両店の記念日を一緒にお祝いしましょう！"],
            fig="The Drunken Master Whisky Bar 10周年 × Café Swing 6周年の記念シングルカスク。ラベルは Elaine の手描き。",
            notes=[("テイスティング日", "2026/11/11 20:05"), ("色", "淡いアンバー"),
                   ("香り", "はじめは穏やかなピートとスモーク。塩気、シトラス、パイナップル、リンゴ、トロピカルフルーツにほのかなヨード。続いて炭火のロースト香、ダークチョコレート、クルミ、バニラとハーブ。後半はミネラル、ジンジャー、ミントの清涼感とスパイス"),
                   ("味わい", "ミディアムボディ。はじめにほのかな塩気、ピート、スモーク、シトラス、焼きパイナップル、熟した果実、モルト、ダークチョコレート、ジンジャー、ペッパー"),
                   ("余韻", "ミディアム。すっきりとしたピーティーな果実の甘み、シトラス、レモン、ほのかな塩気、モルト、ナッツ、ジンジャー、ハーブ、ココナッツ、ミネラル、ペッパー")]),
        "ko": dict(
            title="Laphroaig 10년 The Friendship Cask",
            lead="대만과 한국, 두 바의 기념일을 위해 고른 Laphroaig 싱글 캐스크.",
            desc="2016년 증류, 2026년 병입한 Laphroaig 10년 싱글 캐스크(Bourbon Cask #7, 265병, 59.5%). The Drunken Master Whisky Bar 10주년과 한국 Café Swing 6주년 기념 보틀로, 가오슝 Nova Whisky Bar에서 맛볼 수 있습니다.",
            summary="The Drunken Master Whisky Bar 10주년과 한국 Café Swing 6주년을 기념한 Laphroaig 싱글 캐스크. Bourbon Cask #7, 59.5%.",
            alt="Laphroaig 10년 The Friendship Cask 보틀. 라벨에 손으로 그린 바 일러스트가 있고, 뒤로 Nova Whisky Bar의 술장이 보인다",
            info=[("증류소", "Laphroaig"), ("셀렉션", "The Drunken Master Whisky Bar 10주년 × Café Swing 6주년"),
                  ("증류", "2016/06/09"), ("병입", "2026/07"), ("숙성", "10년"), ("캐스크", "Bourbon Cask"), ("캐스크 번호", "#7"),
                  ("병 수", "265병"), ("도수", "59.5%")],
            body=["선선한 날씨에는 스모키한 피트 위스키 한 잔이 절로 생각납니다.",
                  "오늘 소개할 THE FRIENDSHIP CASK Laphroaig 10년은 대만 The Drunken Master Whisky Bar의 10주년과 한국 Café Swing의 6주년을 기념해 선보이는 특별한 싱글 캐스크입니다.",
                  "Café Swing 사장님은 샘플을 맛보고 정말 맛있는 Laphroaig라고 하셨습니다. 버번 캐스크에서 숙성된 이 위스키의 다채로운 열대과일 향이 밝고 화려하게 피어나 깊은 인상을 남겼다고 합니다.",
                  "라벨은 The Drunken Master Whisky Bar의 점장 Elaine이 직접 그렸습니다. 두 바의 공간과 추억을 이 특별한 기념 라벨에 담았습니다.",
                  "오늘 밤부터 대만과 한국의 우정을 담은 이 Laphroaig 10년을 Nova Whisky Bar에서 잔으로 즐기실 수 있습니다. 한 잔 기울이며 두 바의 기념일을 함께 축하해 주세요!"],
            fig="The Drunken Master Whisky Bar 10주년 × Café Swing 6주년 기념 싱글 캐스크. 라벨은 Elaine이 직접 그렸습니다.",
            notes=[("테이스팅 일시", "2026/11/11 20:05"), ("색", "옅은 앰버"),
                   ("향", "처음에는 부드러운 피트와 스모키함. 짭조름함, 시트러스, 파인애플, 사과, 열대과일에 은은한 요오드가 더해집니다. 이어서 숯불에 구운 향, 다크 초콜릿, 호두, 바닐라와 허브, 후반에는 미네랄, 생강, 민트의 청량감과 스파이스"),
                   ("맛", "미디엄 바디. 처음에는 약간의 짭조름함, 피트, 스모키함, 시트러스, 구운 파인애플, 잘 익은 과일, 몰트, 다크 초콜릿, 생강, 후추"),
                   ("피니시", "미디엄. 깔끔한 피트와 과일의 단맛, 시트러스, 레몬, 은은한 짭조름함, 몰트, 견과류, 생강, 허브, 코코넛, 미네랄, 후추")]),
    },
)]

def journal_url(lang):
    return BASE + L[lang]["path"] + "journal/"

def post_url(p, lang):
    return journal_url(lang) + p["slug"] + "/"

def date_tag(d):
    """頁面上顯示的日期：2026/11/22（datetime 保留 ISO 格式）。"""
    return f'<time datetime="{d}">{d.replace("-", "/")}</time>' if d else ""

def article_li(a):
    return f'<li><a href="{a["url"]}">{html.escape(a["title"])}</a>{date_tag(a.get("date"))}<span>{html.escape(a["summary"])}</span></li>'

def articles_for(lang):
    """文章列表：站內四語文章在前，舊的外部文章（只有繁中）在後。"""
    out = [dict(url=post_url(p, lang), title=p["text"][lang]["title"], summary=p["text"][lang]["summary"], date=p["date"]) for p in POSTS if lang in p["text"]]
    if lang == "zh":
        out += ARTICLES
    return out


# 品酒會：活動結束後把 "past" 改成 True，或整筆移到過往活動
LINEUP = [
    ("unpeated", "Bruichladdich 12 Aged Years", "46%", None),
    ("unpeated", "Bruichladdich 15 Aged Years", "46%", None),
    ("unpeated", "Bruichladdich 18 Aged Years", "50%", None),
    ("heavy", "Port Charlotte PC5 Redux", "63.5%", "40 PPM"),
    ("super", "Octomore 17.1", "59.7%", "81.0 PPM"),
    ("super", "Octomore 17.2", "59.5%", "81.0 PPM"),
    ("super", "Octomore 17.3", "60.9%", "132.1 PPM"),
    ("super", "Octomore OBA Redux", "54.2%", "undisclosed"),
]
EVENTS = [dict(
    id="bruichladdich-20261215", start="2026-12-15T19:30:00+08:00", end="2026-12-15T21:30:00+08:00", door="19:20",
    price=1000, seats=22, img="event-20261215",
    groups={
        "zh": {"unpeated": "無泥煤｜Bruichladdich", "heavy": "重泥煤｜Port Charlotte", "super": "超重泥煤｜Octomore", "undisclosed": "PPM 未公開"},
        "en": {"unpeated": "Unpeated | Bruichladdich", "heavy": "Heavily peated | Port Charlotte", "super": "Super-heavily peated | Octomore", "undisclosed": "PPM undisclosed"},
        "ja": {"unpeated": "ノンピート｜Bruichladdich", "heavy": "ヘビーピート｜Port Charlotte", "super": "スーパーヘビーピート｜Octomore", "undisclosed": "PPM非公開"},
        "ko": {"unpeated": "논피트｜Bruichladdich", "heavy": "헤비 피트｜Port Charlotte", "super": "슈퍼 헤비 피트｜Octomore", "undisclosed": "PPM 비공개"},
    },
    text={
        "zh": dict(title="零到一百三十二｜布萊迪的泥煤光譜",
            lede="一間酒廠、三種個性：清新帶麥芽與果香的無泥煤 Bruichladdich、煙燻與果香交織的重泥煤 Port Charlotte，以及以超重泥煤和實驗精神聞名的 Octomore。這次邀請人頭馬君度品牌大使 James，從布萊迪 12、15、18 年一路喝到 132.1 PPM 的 Octomore 17.3，八款酒走完布萊迪的泥煤光譜；其中包括酒廠復廠 25 週年在 Fèis Ìle 艾雷島節推出的 PC5 Redux，以及重新詮釋 Octomore Black Art 的 OBA Redux。",
            info=[("日期", "2026／12／15（二）"), ("時間", "19:30–21:30（19:20 開放進場）"), ("主講", "人頭馬君度品牌大使 James"), ("名額", "22 名"), ("費用", "NT$1,000／人"), ("報名", "私訊 Nova Whisky Bar（Instagram 或 Facebook）")],
            lineup_h="品飲酒款", alt="零到一百三十二：布萊迪的泥煤光譜品酒會主視覺，八支酒款由無泥煤排到 132.1 PPM", book="私訊報名"),
        "en": dict(title="From Zero to 132 | The Peat Spectrum of Bruichladdich",
            lede="One distillery, three personalities: the fresh, unpeated Bruichladdich, full of malt and fruit; the heavily peated Port Charlotte, where smoke and fruit intertwine; and Octomore, famed for super-heavy peat and experimental spirit. James, brand ambassador for Rémy Cointreau, guides us through eight whiskies, from Bruichladdich 12, 15 and 18 all the way to Octomore 17.3 at 132.1 PPM, including PC5 Redux, released at Fèis Ìle for the 25th anniversary of the distillery's reopening, and OBA Redux, a new take on Octomore Black Art.",
            info=[("Date", "Tue, 15 December 2026"), ("Time", "19:30–21:30 (doors 19:20)"), ("Host", "James, Rémy Cointreau brand ambassador"), ("Seats", "22"), ("Fee", "NT$1,000 per person"), ("Booking", "DM Nova Whisky Bar on Instagram or Facebook")],
            lineup_h="Line-up", alt="Key visual for From Zero to 132, a Bruichladdich tasting at Nova Whisky Bar, with eight bottles arranged from unpeated to 132.1 PPM", book="Book by DM"),
        "ja": dict(title="ゼロから132へ｜Bruichladdichのピート・スペクトラム",
            lede="ひとつの蒸溜所に三つの個性。モルトとフルーツが広がるノンピートのBruichladdich、スモーキーさと果実味が絡み合うヘビーピートのPort Charlotte、そしてスーパーヘビーピートと実験精神で知られるOctomore。Rémy CointreauブランドアンバサダーのJamesと一緒に、Bruichladdich 12年・15年・18年から132.1 PPMのOctomore 17.3まで、8種類を飲み進めます。再稼働25周年にFèis Ìleで発表されたPC5 Redux、Octomore Black Artを新たに解釈したOBA Reduxも登場します。",
            info=[("日時", "2026年12月15日（火）"), ("時間", "19:30–21:30（19:20開場）"), ("講師", "Rémy Cointreau ブランドアンバサダー James"), ("定員", "22名"), ("参加費", "NT$1,000／1名"), ("お申し込み", "Nova Whisky Bar の Instagram または Facebook へDM")],
            lineup_h="テイスティング・ラインナップ", alt="Nova Whisky Bar のBruichladdichテイスティング会「ゼロから132へ」のキービジュアル。ノンピートから132.1 PPMまで8本が並ぶ", book="DMで申し込む"),
        "ko": dict(title="0에서 132까지｜Bruichladdich 피트 스펙트럼",
            lede="한 증류소, 세 가지 개성. 몰트와 과일 향이 어우러진 산뜻한 논피트 Bruichladdich, 스모키함과 과실미가 얽힌 헤비 피트 Port Charlotte, 그리고 슈퍼 헤비 피트와 실험 정신으로 이름난 Octomore. Rémy Cointreau 브랜드 앰배서더 James와 함께 Bruichladdich 12년, 15년, 18년부터 132.1 PPM의 Octomore 17.3까지 여덟 가지를 맛봅니다. 재가동 25주년을 맞아 Fèis Ìle에서 공개된 PC5 Redux와 Octomore Black Art를 새롭게 해석한 OBA Redux도 포함됩니다.",
            info=[("일시", "2026년 12월 15일 (화)"), ("시간", "19:30–21:30 (19:20 입장)"), ("진행", "Rémy Cointreau 브랜드 앰배서더 James"), ("정원", "22명"), ("참가비", "NT$1,000 / 1인"), ("신청", "Nova Whisky Bar Instagram 또는 Facebook DM")],
            lineup_h="테이스팅 라인업", alt="Nova Whisky Bar Bruichladdich 테이스팅 「0에서 132까지」 키 비주얼. 논피트부터 132.1 PPM까지 여덟 병이 놓여 있다", book="DM으로 신청"),
    },
)]

def event_html(lang):
    out = ""
    for e in EVENTS:
        t = e["text"][lang]; g = e["groups"][lang]
        info = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in t["info"])
        rows, cur = "", None
        for grp, name, abv, ppm in LINEUP:
            if grp != cur:
                if cur: rows += "</ol>"
                rows += f'<p class="lg">{g[grp]}</p><ol>'
                cur = grp
            p = g["undisclosed"] if ppm == "undisclosed" else ppm
            sep = ("｜" + p) if p else ""
            rows += f'<li><span>{name}</span><span class="meta2">{abv}{sep}</span></li>'
        rows += "</ol>"
        img = e["img"]
        out += f"""<article class="event" id="{e['id']}"><picture><source type="image/webp" srcset="{BASE}assets/{img}-900.webp 900w, {BASE}assets/{img}-1600.webp 1600w" sizes="(max-width:900px) 92vw, 700px"><img src="{BASE}assets/{img}-1600.jpg" srcset="{BASE}assets/{img}-900.jpg 900w, {BASE}assets/{img}-1600.jpg 1600w" sizes="(max-width:900px) 92vw, 700px" width="1600" height="837" alt="{html.escape(t['alt'])}" loading="lazy"></picture>
<div class="ev-body"><h3>{t['title']}</h3><p>{t['lede']}</p><dl class="info">{info}</dl>
<p class="lineup-h">{t['lineup_h']}</p><div class="lineup">{rows}</div>
<p class="btns"><a class="btn" href="{IG}">{t['book']}・Instagram</a><a class="btn ghost" href="{FB}">Facebook</a></p></div></article>"""
    return out

def event_schema(lang, page_url):
    res = []
    for e in EVENTS:
        t = e["text"][lang]
        res.append({"@type": "Event", "@id": BASE + "#" + e["id"], "name": strip(t["title"]), "description": strip(t["lede"]),
            "startDate": e["start"], "endDate": e["end"], "doorTime": e["door"],
            "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "BarOrPub", "@id": BASE + "#bar", "name": "Nova Whisky Bar 新星威士忌酒館",
                         "address": {"@type": "PostalAddress", "streetAddress": "林森二路128巷14號2樓", "addressLocality": "苓雅區", "addressRegion": "高雄市", "postalCode": "802", "addressCountry": "TW"}},
            "image": [BASE + "assets/" + e["img"] + "-1600.jpg"],
            "organizer": {"@type": "Organization", "name": "Nova Whisky Bar 新星威士忌酒館", "url": BASE},
            "performer": {"@type": "Person", "name": "James"},
            "maximumAttendeeCapacity": e["seats"], "inLanguage": L[lang]["html_lang"],
            "offers": {"@type": "Offer", "price": e["price"], "priceCurrency": "TWD", "availability": "https://schema.org/InStock", "url": page_url + "#" + e["id"]}})
    return res

# ---------------------------------------------------------------
LANGS = ["zh", "en", "ja", "ko"]
HREFLANG = {"zh": "zh-TW", "en": "en", "ja": "ja", "ko": "ko"}

def url_of(lang):
    return BASE + L[lang]["path"]

def bar_schema(lang):
    d = L[lang]
    if lang == "zh":
        addr = {"@type": "PostalAddress", "streetAddress": "林森二路128巷14號2樓", "addressLocality": "苓雅區",
                "addressRegion": "高雄市", "postalCode": "802", "addressCountry": "TW"}
    else:
        addr = {"@type": "PostalAddress", "streetAddress": "2F., No. 14, Ln. 128, Linsen 2nd Rd.", "addressLocality": "Lingya Dist.",
                "addressRegion": "Kaohsiung City", "postalCode": "802", "addressCountry": "TW"}
    return {
        "@type": "BarOrPub", "@id": BASE + "#bar",
        "name": "Nova Whisky Bar",
        "alternateName": ["新星威士忌酒館", "Nova Whisky Bar 新星威士忌酒館", "高雄高地人小酒館", "Highlander Inn Takao"],
        "description": d["desc"], "url": url_of(lang), "image": [BASE + "assets/interior-2400.jpg", OG_IMG], "logo": BASE + "assets/logo-512.png",
        "telephone": TEL, "address": addr, "hasMap": MAP,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday", "Monday", "Wednesday", "Thursday", "Friday"], "opens": "20:00", "closes": "01:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "20:00", "closes": "02:00"},
        ],
        "acceptsReservations": True,
        "priceRange": "NT$500+ per person (minimum spend)",
        "currenciesAccepted": "TWD",
        "paymentAccepted": "Cash, Credit Card",
        "sameAs": [u for _, u in socials()],
        "knowsAbout": ["Scotch whisky", "Single malt whisky", "Independent bottlers", "Single cask whisky"],
        "parentOrganization": {"@type": "Organization", "name": "The Drunken Master 醉俠"},
    }

def faq_schema(lang, page_url):
    return {"@type": "FAQPage", "@id": page_url + "#faq", "mainEntity": [
        {"@type": "Question", "name": strip(html.unescape(q)),
         "acceptedAnswer": {"@type": "Answer", "text": strip(html.unescape(fill(a, lang)))}} for q, a in faq_items(lang)]}

def head(lang, title, desc, canonical, schema_graph, alternates=True, noindex=False, og=None):
    """alternates：True＝各語首頁；dict＝{lang: url} 這一頁的各語版本；False＝不加。
    og：文章頁用 dict(img=, w=, h=, type="article")。"""
    d = L[lang]
    alt = ""
    if alternates:
        urls = alternates if isinstance(alternates, dict) else {l: url_of(l) for l in LANGS}
        alt = "".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{u}">\n' for l, u in urls.items())
        alt += f'<link rel="alternate" hreflang="x-default" href="{urls.get("zh", BASE)}">\n'
    robots = '<meta name="robots" content="noindex">\n' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    ld = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, ensure_ascii=False, indent=1)
    og = og or dict(img=OG_IMG, w=1200, h=630, type="website")
    return f"""<!DOCTYPE html>
<html lang="{d['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}<meta name="google-site-verification" content="{GSC_VERIFY}">
<link rel="canonical" href="{canonical}">
{alt}<meta name="theme-color" content="#F6F4EF">
<meta property="og:type" content="{og['type']}">
<meta property="og:site_name" content="Nova Whisky Bar 新星威士忌酒館">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og['img']}">
<meta property="og:image:width" content="{og['w']}">
<meta property="og:image:height" content="{og['h']}">
<meta property="og:locale" content="{d['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og['img']}">
<link rel="icon" href="{BASE}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{BASE}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{BASE}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{d['fonts']}&display=swap">
<link rel="stylesheet" href="{BASE}assets/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
"""

def age_gate(lang):
    d = L[lang]
    return f"""<div id="agegate" hidden><div class="ag-box"><img class="ag-mark" src="{BASE}assets/logo-mark.svg" alt="" width="64" height="73"><img class="ag-word" src="{BASE}assets/logo-en.svg" alt="Nova Whisky Bar" width="160" height="45"><p>{d['age_q']}</p>
<button type="button" id="ag-yes">{d['age_yes']}</button><a href="https://www.google.com/" class="ag-no">{d['age_no']}</a></div></div>
<script>(function(){{var g=document.getElementById('agegate'),ok=false;try{{ok=localStorage.getItem('nova_age_ok')==='1'}}catch(e){{}}
if(!ok){{g.hidden=false}}document.getElementById('ag-yes').onclick=function(){{try{{localStorage.setItem('nova_age_ok','1')}}catch(e){{}}g.hidden=true}};}})();</script>
"""

def header(lang, is_home=False, alt_urls=None):
    d = L[lang]
    def href(h):
        if h.startswith("#"):
            return h if is_home else url_of(lang) + h
        if h.startswith(".."):
            return BASE + h[3:]
        return BASE + h
    nav = "".join(f'<a href="{href(h)}">{t}</a>' for h, t in d["nav"])
    alt_urls = alt_urls or {}
    langs = "".join(f'<a href="{alt_urls.get(l, url_of(l))}" hreflang="{HREFLANG[l]}"{" aria-current=\"true\"" if l == lang else ""}>{L[l]["lang_name"]}</a>' for l in LANGS)
    return f"""<header class="top"><div class="wrap bar"><a class="brand" href="{url_of(lang)}"><img class="bm" src="{BASE}assets/logo-mark.svg" alt="" width="30" height="34"><img class="be" src="{BASE}assets/logo-en.svg" alt="Nova Whisky Bar 新星威士忌酒館" width="132" height="37"><span class="badge">22.6°N · Kaohsiung</span></a>
<nav class="nav" aria-label="Main">{nav}</nav><nav class="langs" aria-label="Language">{langs}</nav></div></header>
"""

def footer(lang):
    d = L[lang]
    extra = f'<p class="warn-extra">{d["warn_extra"]}</p>' if d["warn_extra"] else ""
    soc = "｜".join(f'<a href="{u}">{n}</a>' for n, u in socials())
    return f"""<footer class="foot"><div class="wrap">
<p class="flogo"><img src="{BASE}assets/logo-mark.svg" alt="" width="44" height="50"><img src="{BASE}assets/logo-zh.svg" alt="新星威士忌酒館" width="194" height="32"></p>
<p class="warn">未成年請勿飲酒｜禁止酒駕｜飲酒過量有害健康｜短時間大量攝取酒精容易致命</p>{extra}
<p class="nap"><strong>Nova Whisky Bar 新星威士忌酒館</strong>（原 高雄高地人小酒館 Highlander Inn Takao）<br>
高雄市苓雅區林森二路128巷14號 2樓<br>2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City, Taiwan<br>
20:00–01:30 (Sun, Mon, Wed–Fri)｜20:00–02:00 (Sat)｜Closed Tue｜<a href="tel:{TEL}">{TEL_DISPLAY}</a></p>
<p class="nap">{soc}</p>
<p class="small">醉俠 The Drunken Master ・ 南曜蒸餾所 NOVA Distillery ・ 最後更新 {UPDATED}</p>
</div></footer>
"""

PLATE = """<svg viewBox="0 0 1200 540" role="img" aria-label="{label}" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="pw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0ECE3"/><stop offset="1" stop-color="#E2DACB"/></linearGradient>
<radialGradient id="glow" cx="50%" cy="55%" r="40%"><stop offset="0" stop-color="#8C5A2B" stop-opacity=".22"/><stop offset="1" stop-color="#8C5A2B" stop-opacity="0"/></radialGradient>
<linearGradient id="dram" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9803F" stop-opacity=".8"/><stop offset="1" stop-color="#6E401A"/></linearGradient>
<g id="bt"><path d="M0 0 V-62 L8 -74 V-96 H20 V-74 L28 -62 V0" fill="none" stroke="#6B665E" stroke-width="1.1"/></g>
<g id="bt2"><path d="M0 0 V-48 Q0 -58 10 -60 V-84 H20 V-60 Q30 -58 30 -48 V0" fill="none" stroke="#6B665E" stroke-width="1.1"/></g>
</defs>
<rect width="1200" height="540" fill="url(#pw)"/><rect width="1200" height="540" fill="url(#glow)"/>
<g stroke="#C8C0B2" stroke-width="1"><line x1="70" y1="210" x2="1130" y2="210"/><line x1="70" y1="370" x2="1130" y2="370"/></g>
<g opacity=".55"><use href="#bt" x="110" y="210"/><use href="#bt2" x="160" y="210"/><use href="#bt" x="212" y="210"/><use href="#bt2" x="262" y="210"/><use href="#bt" x="314" y="210"/>
<use href="#bt2" x="120" y="370"/><use href="#bt" x="172" y="370"/><use href="#bt" x="222" y="370"/><use href="#bt2" x="272" y="370"/>
<use href="#bt" x="850" y="210"/><use href="#bt2" x="900" y="210"/><use href="#bt" x="952" y="210"/><use href="#bt2" x="1002" y="210"/><use href="#bt" x="1054" y="210"/>
<use href="#bt2" x="868" y="370"/><use href="#bt" x="920" y="370"/><use href="#bt2" x="970" y="370"/><use href="#bt" x="1022" y="370"/></g>
<line x1="70" y1="270" x2="1130" y2="270" stroke="#8C5A2B" stroke-width=".9" stroke-dasharray="2 7"/>
<text x="1128" y="262" text-anchor="end" fill="#8C5A2B" font-family="Cormorant Garamond, serif" font-size="17" letter-spacing="3">22.6°N</text>
<circle cx="600" cy="285" r="150" fill="none" stroke="#1A1917" stroke-width=".8" opacity=".18"/>
<path d="M560 318 C560 352 576 372 600 372 C624 372 640 352 640 318 Z" fill="url(#dram)"/>
<ellipse cx="600" cy="318" rx="40" ry="6" fill="#C9935A" opacity=".7"/>
<path d="M575 200 H625 C623 240 642 276 642 316 C642 356 625 378 600 378 C575 378 558 356 558 316 C558 276 577 240 575 200 Z" fill="none" stroke="#1A1917" stroke-width="1.5"/>
<ellipse cx="600" cy="200" rx="25" ry="4.5" fill="none" stroke="#1A1917" stroke-width="1.2"/>
<path d="M586 378 L583 402 H617 L614 378" fill="none" stroke="#1A1917" stroke-width="1.3"/><ellipse cx="600" cy="402" rx="27" ry="5" fill="none" stroke="#1A1917" stroke-width="1.3"/>
<image href="{mark}" x="574" y="96" width="52" height="59"/>
<g stroke="#1A1917" stroke-width=".9" opacity=".5"><path d="M40 60V40H60M1140 40H1160V60M40 480V500H60M1140 500H1160V480" fill="none"/></g>
<text x="600" y="462" text-anchor="middle" fill="#6B665E" font-family="Cormorant Garamond, serif" font-size="14" letter-spacing="6">HIGHLANDER INN TAKAO → NOVA WHISKY BAR · 2026</text>
</svg>"""

def faq_items(lang):
    return [(q, a) for q, a in FAQ[lang] if strip(fill(a, lang))]

def faq_html(lang, n=None):
    items = faq_items(lang) if n is None else faq_items(lang)[:n]
    return "".join(f'<details><summary><span class="qn">{i+1:02d}</span><span class="qt">{q}</span></summary><p>{fill(a, lang)}</p></details>\n' for i, (q, a) in enumerate(items))

def sect(sid, k, h, inner, alt=False):
    return f'<section id="{sid}" class="band{" alt" if alt else ""}"><div class="wrap split"><div class="sh"><p class="k">{k}</p><h2>{h}</h2></div><div class="sb">{inner}</div></div></section>\n'

def home(lang):
    d = L[lang]
    page = url_of(lang)
    graph = [bar_schema(lang), {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "Nova Whisky Bar 新星威士忌酒館", "inLanguage": d["html_lang"]}]
    if lang != "zh":
        graph.append(faq_schema(lang, page))
    graph += event_schema(lang, page)
    about = "".join((f'<p class="beat">{p}</p>' if i == 1 else f"<p>{p}</p>") for i, p in enumerate(d["about"]))
    facts = "".join(f'<div><p class="k2">{a}</p><p class="fv">{b}</p></div>' for a, b in d["facts"])
    about_inner = f'<blockquote>「{d["quote"]}」</blockquote>{about}<div class="facts">{facts}</div>'
    drink = "".join(f'<article><h3>{t}</h3><p>{p}</p></article>' for t, p in d["drink"])
    visit = "".join(f"<div><dt>{k}</dt><dd>{fill(v, lang)}</dd></div>" for k, v in d["visit"] if strip(fill(v, lang)))
    soc = "".join(f'<a class="btn ghost" href="{u}">{n}</a>' for n, u in socials())
    family = "".join(f'<li><strong>{t}</strong><span>{p}</span></li>' for t, p in d["family"])
    side = "".join(f"<p>{s}</p>" for s in d["side"])
    arts = "".join(article_li(a) for a in articles_for(lang))
    journal_block = sect("journal", d["journal_k"], d["journal_h"], f'<ul class="list">{arts}</ul><p><a class="more" href="journal/">{d["journal_more"]} →</a></p>') if arts else ""
    if lang == "zh":
        faq_inner = faq_html(lang, 6) + f'<p><a class="more" href="faq/">{d["faq_more"]} →</a></p>'
        faq_href = "faq/"
    else:
        faq_inner = faq_html(lang)
        faq_href = "#faq"
    body = f"""<body>
{age_gate(lang)}{header(lang, True)}<main id="main">
<section class="hero"><div class="wrap">
<div class="strap"><span>{d['strap'][0]}</span><span>{d['strap'][1]}</span></div>
<div class="mast"><div class="mast-l"><h1><span class="h1en">Nova Whisky Bar</span><span class="h1zh">{d['h1_sub']}</span></h1>
<p class="lead">{d['lead']}</p><p class="formerly">{d['formerly']}</p></div>
<div class="mast-r"><img class="hero-mark" src="{BASE}assets/logo-mark.svg" alt="Nova Whisky Bar logo" width="120" height="137"><div class="side">{side}</div><p class="btns"><a class="btn" href="{MAP}">{d['btn_map']}</a><a class="btn ghost" href="{faq_href}">{d['btn_faq']}</a></p></div></div>
<figure class="plate photo"><picture><source type="image/webp" srcset="{BASE}assets/interior-900.webp 900w, {BASE}assets/interior-1600.webp 1600w, {BASE}assets/interior-2400.webp 2400w" sizes="(max-width:1160px) 92vw, 1040px"><img src="{BASE}assets/interior-1600.jpg" srcset="{BASE}assets/interior-900.jpg 900w, {BASE}assets/interior-1600.jpg 1600w, {BASE}assets/interior-2400.jpg 2400w" sizes="(max-width:1160px) 92vw, 1040px" width="2400" height="1351" alt="{html.escape(d['photo_alt'])}" fetchpriority="high"></picture><figcaption>{d['fig_caption']}</figcaption></figure>
</div></section>
{sect("about", d["about_k"], d["about_h"], about_inner)}
<section id="drink" class="band alt"><div class="wrap"><div class="sh row"><p class="k">{d['drink_k']}</p><h2>{d['drink_h']}</h2></div><div class="grid3">{drink}</div></div></section>
{sect("tastings", d["events_k"], d["events_h"], f'<p>{d["events"]}</p>' + event_html(lang))}
{sect("visit", d["visit_k"], d["visit_h"], f'<dl class="info">{visit}</dl><p class="note">{d["visit_note"]}</p><p class="btns"><a class="btn" href="{MAP}">{d["btn_map"]}</a>{soc}</p>', alt=True)}
{sect("faq", d["faq_k"], d["faq_h"], faq_inner)}
{sect("family", d["family_k"], d["family_h"], f'<ul class="list">{family}</ul>', alt=True)}
{journal_block}</main>
{footer(lang)}</body>
</html>
"""
    return head(lang, d["title"], d["desc"], page, graph) + body

def simple_page(lang, crumb, h1, lead, inner, alt_urls=None):
    return f"""<body>
{age_gate(lang)}{header(lang, alt_urls=alt_urls)}<main id="main"><section class="band"><div class="wrap narrow">
<p class="crumb"><a href="{url_of(lang)}">Nova Whisky Bar</a> / {crumb}</p>
<h1 class="page">{h1}</h1><p class="lead">{lead}</p>
{inner}
</div></section></main>
{footer(lang)}</body></html>
"""

def faq_page():
    lang = "zh"
    page = BASE + "faq/"
    title = "常見問題｜Nova Whisky Bar 新星威士忌酒館（高雄苓雅威士忌酒吧）"
    desc = "Nova Whisky Bar 新星威士忌酒館常見問題：新手與一個人來適不適合、半杯、Highball 與調酒、地址、營業時間、訂位、品酒會，以及和高雄高地人小酒館的關係。"
    graph = [faq_schema(lang, page), bar_schema(lang),
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Nova Whisky Bar", "item": BASE},
                 {"@type": "ListItem", "position": 2, "name": "常見問題", "item": page}]}]
    body = simple_page(lang, "常見問題", "常見問題", "關於 Nova Whisky Bar 新星威士忌酒館，第一次來的客人最常問的幾件事。", f'<div class="faq">{faq_html(lang)}</div>')
    return head(lang, title, desc, page, graph, alternates=False) + body

JOURNAL_UI = {
    "zh": dict(title="文章與品飲紀錄｜Nova Whisky Bar 新星威士忌酒館",
               desc="Nova Whisky Bar 新星威士忌酒館的威士忌文章與【座標 22.6°N｜新星亮這杯】品飲紀錄：酒廠故事、桶型知識與獨立裝瓶單桶。",
               h1="文章與品飲紀錄", lead="【座標 22.6°N｜新星亮這杯】與 Nova 的威士忌知識整理。新文章會陸續從社群搬過來。"),
    "en": dict(title="Journal & Tasting Notes | Nova Whisky Bar, Kaohsiung",
               desc="Whisky articles and 22.6°N | Nova in the Glass tasting notes from Nova Whisky Bar in Kaohsiung, Taiwan: distillery stories, casks and independent single casks.",
               h1="Journal", lead="22.6°N | Nova in the Glass — tasting notes and whisky stories from Nova, in English."),
    "ja": dict(title="記事・テイスティングノート｜Nova Whisky Bar 新星威士忌酒館（高雄）",
               desc="台湾・高雄の Nova Whisky Bar によるウイスキー記事とテイスティングノート「22.6°N | Nova in the Glass」。蒸溜所の物語、樽、独立瓶詰めのシングルカスク。",
               h1="記事", lead="テイスティングノート「22.6°N | Nova in the Glass」とウイスキーの話を、日本語でお届けします。"),
    "ko": dict(title="글・테이스팅 노트｜Nova Whisky Bar 新星威士忌酒館 (가오슝)",
               desc="대만 가오슝 Nova Whisky Bar의 위스키 글과 테이스팅 노트 「22.6°N | Nova in the Glass」. 증류소 이야기, 캐스크, 독립 병입 싱글 캐스크.",
               h1="글", lead="테이스팅 노트 「22.6°N | Nova in the Glass」와 위스키 이야기를 한국어로 전합니다."),
}

def journal_page(lang="zh"):
    page = journal_url(lang)
    j = JOURNAL_UI[lang]
    items = articles_for(lang)
    arts = "".join(article_li(a) for a in items)
    graph = [{"@type": "CollectionPage", "@id": page, "url": page, "name": j["title"], "inLanguage": L[lang]["html_lang"],
              "isPartOf": {"@id": BASE + "#site"}, "about": {"@id": BASE + "#bar"},
              "hasPart": [dict({"@type": "Article", "headline": a["title"], "url": a["url"]}, **({"datePublished": a["date"]} if a.get("date") else {})) for a in items]}]
    alts = {l: journal_url(l) for l in LANGS}
    body = simple_page(lang, POST_UI[lang]["crumb"], j["h1"], j["lead"], f'<ul class="list">{arts}</ul>', alt_urls=alts)
    return head(lang, j["title"], j["desc"], page, graph, alternates=alts) + body

def post_page(p, lang):
    t = p["text"][lang]; ui = POST_UI[lang]
    page = post_url(p, lang)
    title = f"【{SERIES[lang]}】{t['title']}｜Nova Whisky Bar" + (" 新星威士忌酒館" if lang == "zh" else "")
    img = p["img"]; big = f"{BASE}assets/{img}-1080.jpg"
    alts = {l: post_url(p, l) for l in LANGS if l in p["text"]}
    graph = [{"@type": "BlogPosting", "@id": page + "#post", "headline": t["title"], "description": t["desc"],
              "inLanguage": L[lang]["html_lang"], "url": page,
              "datePublished": p["date"], "dateModified": p["date"], "image": [big],
              "author": {"@type": "Person", "name": "醉郭", "alternateName": "Drunken Kuo", "url": "https://www.instagram.com/drunkenkuo/"},
              "publisher": {"@id": BASE + "#bar"}, "about": {"@type": "Thing", "name": p["about"]},
              "isPartOf": {"@id": journal_url(lang)}, "mainEntityOfPage": page},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Nova Whisky Bar", "item": url_of(lang)},
                 {"@type": "ListItem", "position": 2, "name": ui["crumb"], "item": journal_url(lang)},
                 {"@type": "ListItem", "position": 3, "name": t["title"], "item": page}]}]
    info = "".join(f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in t["info"])
    notes = "".join(f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in t["notes"])
    body_p = "".join(f"<p>{html.escape(x)}</p>" for x in t["body"])
    inner = f"""<p class="k">{SERIES[lang]}</p><p class="meta">{date_tag(p['date'])}</p>
<figure class="post-fig"><picture><source type="image/webp" srcset="{BASE}assets/{img}-720.webp 720w, {BASE}assets/{img}-1080.webp 1080w" sizes="(max-width:600px) 92vw, 460px"><img src="{big}" srcset="{BASE}assets/{img}-720.jpg 720w, {big} 1080w" sizes="(max-width:600px) 92vw, 460px" width="1080" height="1350" alt="{html.escape(t['alt'])}" fetchpriority="high"></picture>{('<figcaption>' + html.escape(t['fig']) + '</figcaption>') if t.get('fig') else ''}</figure>
<dl class="info">{info}</dl>
<div class="article">{body_p}</div>
<h2 class="post-h">{ui['notes_h']}</h2>
<dl class="info notes">{notes}</dl>
<p class="closing">{html.escape(ui['closing'])}</p>"""
    crumb = f'<a href="{journal_url(lang)}">{ui["crumb"]}</a> / {html.escape(t["title"])}'
    body = simple_page(lang, crumb, html.escape(t["title"]), html.escape(t["lead"]), inner, alt_urls=alts)
    og = dict(img=big, w=1080, h=1350, type="article")
    return head(lang, title, t["desc"], page, graph, alternates=alts, og=og) + body

def article_template():
    lang = "zh"
    page = BASE + "journal/SLUG/"
    title = "【座標 22.6°N｜新星亮這杯】酒款名稱｜Nova Whisky Bar 新星威士忌酒館"
    desc = "（一句話描述這支酒：酒廠、年份、桶型、裝瓶商，與 Nova 的品飲重點。120 字內。）"
    graph = [{"@type": "BlogPosting", "headline": "酒款名稱", "inLanguage": "zh-TW", "url": page,
              "datePublished": "YYYY-MM-DD", "dateModified": "YYYY-MM-DD", "image": OG_IMG,
              "author": {"@type": "Person", "name": "醉郭"},
              "publisher": {"@id": BASE + "#bar"}, "about": {"@type": "Thing", "name": "酒款名稱"},
              "mainEntityOfPage": page}]
    inner = """<p class="k">座標 22.6°N｜新星亮這杯</p><p class="meta"><time datetime="YYYY-MM-DD">YYYY/MM/DD</time></p>
<dl class="info"><div><dt>酒廠</dt><dd>—</dd></div><div><dt>裝瓶商</dt><dd>—</dd></div><div><dt>年份／酒齡</dt><dd>—</dd></div><div><dt>桶型／桶號</dt><dd>—</dd></div><div><dt>酒精度</dt><dd>—</dd></div><div><dt>瓶數</dt><dd>—</dd></div></dl>
<div class="article"><p>（貼上社群的繁中文案正文，段落照原樣分開即可。）</p><p class="beat">（關鍵轉折的單行短句）</p><p>（品飲描述）</p>
<p>這杯在高雄苓雅的 Nova Whisky Bar 新星威士忌酒館喝得到，數量有限，以現場為準。</p></div>"""
    body = simple_page(lang, '<a href="' + BASE + 'journal/">文章</a> / 酒款名稱', "酒款名稱", "（一句話導言）", inner)
    return head(lang, title, desc, page, graph, alternates=False, noindex=True) + body

def page_404():
    return f"""<!DOCTYPE html><html lang="zh-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>找不到頁面｜Nova Whisky Bar</title><meta name="robots" content="noindex"><link rel="stylesheet" href="{BASE}assets/style.css"></head>
<body><main class="wrap narrow" style="padding:18vh 0"><img src="{BASE}assets/logo-mark.svg" alt="" width="60" height="68"><h1 class="page">這杯好像倒空了</h1><p>找不到這個頁面。<a href="{BASE}">回到 Nova Whisky Bar 首頁</a></p></main></body></html>
"""

def sitemap():
    urls = []
    for l in LANGS:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[x]}" href="{url_of(x)}"/>' for x in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
        urls.append(f"<url><loc>{url_of(l)}</loc><lastmod>{UPDATED}</lastmod>{alts}</url>")
    urls.append(f"<url><loc>{BASE}faq/</loc><lastmod>{UPDATED}</lastmod></url>")
    def group(pages, lastmod):
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[x]}" href="{u}"/>' for x, u in pages.items())
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{pages.get("zh", next(iter(pages.values())))}"/>'
        for u in pages.values():
            urls.append(f"<url><loc>{u}</loc><lastmod>{lastmod}</lastmod>{alts}</url>")
    group({l: journal_url(l) for l in LANGS}, UPDATED)
    for p in POSTS:
        group({l: post_url(p, l) for l in LANGS if l in p["text"]}, p["date"])
    for a in ARTICLES:
        if a["url"].startswith(BASE):
            urls.append(f"<url><loc>{a['url']}</loc></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")

def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]
    s = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    return s + f"User-agent: *\nAllow: /\nDisallow: /journal/_template/\n\nSitemap: {BASE}sitemap.xml\n"

def llms():
    def plain(key):
        v = FACTS[key]["zh"]
        return v if v else "（尚未提供）"
    faq_lines = "\n".join(f"- {strip(html.unescape(q))}：{strip(html.unescape(fill(a, 'zh')))}" for q, a in faq_items("zh"))
    faq_lines = re.sub(r"【待填：[^】]+】", "（尚未提供）", faq_lines)
    arts = "\n".join(f"- [{a['title']}]({a['url']})：{a['summary']}" for a in articles_for("zh"))
    langname = {"en": "English", "ja": "日本語", "ko": "한국어"}
    for p in POSTS:
        others = "、".join(f"[{langname[l]}]({post_url(p, l)})" for l in ("en", "ja", "ko") if l in p["text"])
        if others:
            arts = arts.replace(f"({post_url(p, 'zh')})：{p['text']['zh']['summary']}", f"({post_url(p, 'zh')})：{p['text']['zh']['summary']}（{others}）")
    soc = "\n".join(f"- {n}：{u}" for n, u in socials())
    extra = "".join(f"- {lab}：{FACTS[k]['zh']}\n" for k, lab in [("price","消費方式"),("language","外語服務"),("payment","付款方式"),("bottles","酒款數量")] if FACTS[k]["zh"])
    return f"""# Nova Whisky Bar 新星威士忌酒館

> 高雄市苓雅區的威士忌酒吧，安靜、適合一個人獨飲。以蘇格蘭單一麥芽、獨立裝瓶與單桶威士忌為主，單杯超過 NT$500 的酒款可點半杯，也有 Highball、調酒與無酒精飲料。前身為高雄高地人小酒館（Highlander Inn Takao），2026 年 4 月更名。屬於醉俠 The Drunken Master 體系，與建置中的南曜蒸餾所 NOVA Distillery 同一團隊。
> A quiet, solo-friendly whisky bar in Lingya District, Kaohsiung, Taiwan (formerly Highlander Inn Takao), focused on Scotch single malts, independent bottlings and single casks. Half pours available for drams over NT$500.

## 基本資料
- 店名：Nova Whisky Bar 新星威士忌酒館（舊名：高雄高地人小酒館 Highlander Inn Takao）
- 類型：威士忌酒吧（Whisky Bar）
- 地址：高雄市苓雅區林森二路128巷14號 2樓／2F., No. 14, Ln. 128, Linsen 2nd Rd., Lingya Dist., Kaohsiung City, Taiwan
- 營業時間：週日、週一、週三至週五 20:00–01:30；週六 20:00–02:00；週二公休／Sun, Mon, Wed–Fri 20:00–01:30; Sat 20:00–02:00; closed Tue
- 電話：(07) 330-8050／+886-7-330-8050
{extra}
## 官方社群
{soc}

## 近期品酒會
- 2026/12/15（二）19:30–21:30「零到一百三十二｜布萊迪的泥煤光譜」：人頭馬君度品牌大使 James 主講，八款 Bruichladdich／Port Charlotte／Octomore（含 PC5 Redux、Octomore 17.1／17.2／17.3、OBA Redux），名額 22 名，NT$1,000／人，私訊 Nova Whisky Bar 報名。

## 適合誰
- 想喝蘇格蘭單一麥芽、獨立裝瓶、單桶威士忌的人
- 想一個人安靜喝酒，或兩三人輕聲聊天的人
- 威士忌新手：可依口味推薦，高價酒款可點半杯
- 同行有人不喝純飲：有 Highball、調酒與無酒精飲料
- 來高雄旅遊、想找威士忌酒吧的旅客（網站有英日韓語頁面）

## 頁面
- [繁體中文首頁]({BASE})
- [常見問題]({BASE}faq/)
- [English]({BASE}en/)
- [日本語]({BASE}ja/)
- [한국어]({BASE}ko/)
- [文章與品飲紀錄]({BASE}journal/)（[English]({BASE}en/journal/)、[日本語]({BASE}ja/journal/)、[한국어]({BASE}ko/journal/)）

## 常見問題
{faq_lines}

## 文章
{arts}
"""

CSS = r"""
/* VOICE 安靜、節制的威士忌酒吧刊物
   IDEA  一本酒吧的季刊：刊頭、版畫插圖、編排整齊的欄位
   PICTURE 刊頭下方的版畫：酒架、品飲杯與北緯 22.6 度線
   COLOUR 米白紙、墨黑、威士忌琥珀
   TYPE  Cormorant Garamond 搭配 Noto Serif／Sans（依語言） */
:root{--paper:#F6F4EF;--paper2:#EDE9E0;--ink:#1A1917;--stone:#6B665E;--line:#DBD6CC;--whisky:#8C5A2B;--soft:#EFE7DC;
--display:"Cormorant Garamond","Noto Serif TC",serif;--serif:"Noto Serif TC","Cormorant Garamond",serif;--sans:"Noto Sans TC",system-ui,sans-serif}
html[lang=ja]{--serif:"Noto Serif JP","Cormorant Garamond",serif;--sans:"Noto Sans JP",system-ui,sans-serif;--display:"Cormorant Garamond","Noto Serif JP",serif}
html[lang=ko]{--serif:"Noto Serif KR","Cormorant Garamond",serif;--sans:"Noto Sans KR",system-ui,sans-serif;--display:"Cormorant Garamond","Noto Serif KR",serif}
*{box-sizing:border-box;min-width:0}html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--paper);color:var(--ink);font:300 16px/1.9 var(--sans);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:var(--whisky);text-underline-offset:3px}a:hover{color:var(--ink)}
::selection{background:var(--whisky);color:var(--paper)}
.wrap{max-width:1120px;margin:0 auto;padding:0 max(5vw,18px)}.narrow{max-width:820px}
h1,h2,h3{font-weight:400;margin:0}
.top{position:sticky;top:0;z-index:10;background:rgba(246,244,239,.95);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 26px;min-height:68px;padding-top:10px;padding-bottom:10px}
.brand{color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:12px;flex-wrap:wrap}.brand .bm{height:34px;width:auto}.brand .be{height:37px;width:auto}
.badge{font-family:var(--sans);font-size:11px;letter-spacing:.12em;color:var(--stone);border:1px solid var(--line);padding:1px 8px;border-radius:2px}
.nav{display:flex;flex-wrap:wrap;gap:4px 22px;flex:1;justify-content:flex-end}.nav a{color:var(--stone);text-decoration:none;font-size:14px;padding:6px 0}.nav a:hover{color:var(--whisky)}
.langs{display:flex;gap:12px}.langs a{color:var(--stone);text-decoration:none;font-size:13px}.langs a[aria-current]{color:var(--ink);border-bottom:1px solid var(--ink)}
.hero{padding:34px 0 60px}
.strap{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:10px 0;display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 20px;font-size:12px;color:var(--stone);letter-spacing:.06em}
.mast{display:grid;grid-template-columns:minmax(0,8fr) minmax(0,4fr);gap:40px;align-items:end;padding:56px 0 44px}
.h1en{display:block;font-family:var(--display);font-size:clamp(46px,7vw,76px);line-height:1;letter-spacing:-.01em}
.h1zh{display:block;font-family:var(--serif);font-size:clamp(24px,3.4vw,36px);letter-spacing:.08em;margin-top:14px;color:rgba(26,25,23,.9)}
.lead{font-size:17px;line-height:1.95;max-width:44em;margin:26px 0 0}
.formerly{margin:18px 0 0;padding-left:14px;border-left:2px solid var(--whisky);font-size:13px;color:var(--stone)}
.mast-r{display:flex;flex-direction:column;align-items:flex-end;gap:20px;text-align:right}.hero-mark{width:120px;height:auto}
.side p{margin:0;font-size:13px;line-height:1.9;color:var(--stone)}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 20px;background:var(--ink);color:var(--paper);text-decoration:none;font-size:14px;border:1px solid var(--ink);border-radius:2px;transition:background .25s}
.btn:hover{background:var(--whisky);border-color:var(--whisky);color:var(--paper)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}.btn.ghost:hover{border-color:var(--whisky);color:var(--whisky);background:transparent}
.plate{margin:0;border-top:1px solid var(--line);padding-top:22px}
.plate svg{display:block;width:100%;aspect-ratio:1200/540;border:1px solid var(--line);border-radius:2px;background:var(--paper2)}
.plate.photo img{display:block;width:100%;height:auto;aspect-ratio:2400/1351;object-fit:cover;border-radius:2px;background:#2a241d}
.plate figcaption{margin-top:10px;font-size:12px;color:var(--stone);letter-spacing:.06em}
.band{padding:clamp(52px,7vw,96px) 0;border-top:1px solid var(--line)}.band.alt{background:rgba(237,233,224,.5)}
.split{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:48px}
.k{margin:0;font-size:13px;color:var(--whisky);letter-spacing:.08em;font-family:var(--display);font-style:italic;font-size:17px}
.sh h2{font-family:var(--serif);font-size:clamp(24px,3vw,32px);letter-spacing:.04em;margin-top:6px;line-height:1.35}
.sh.row{margin-bottom:34px}
.sb>p,.sb .article p{margin:0 0 1.1em}
blockquote{margin:0 0 28px;font-family:var(--serif);font-size:clamp(22px,2.6vw,30px);line-height:1.5;font-weight:400}
.beat{font-family:var(--serif);font-size:19px;color:var(--whisky);margin:26px 0!important}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;border-top:1px solid var(--line);margin-top:30px;padding-top:20px}
.k2{margin:0;font-size:12px;color:var(--stone);letter-spacing:.08em}.fv{margin:4px 0 0;font-family:var(--serif);font-size:15px;font-weight:400}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--line);background:var(--paper)}
.grid3 article{padding:30px 28px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);transition:background .3s}
.grid3 article:nth-child(3n){border-right:0}.grid3 article:nth-last-child(-n+3){border-bottom:0}.grid3 article:hover{background:rgba(239,231,220,.5)}
.grid3 h3{font-family:var(--serif);font-size:19px;font-weight:500;letter-spacing:.04em;margin-bottom:10px}.grid3 p{margin:0;font-size:15px;color:rgba(26,25,23,.8)}
.info{margin:0;border-top:1px solid var(--line)}.info>div{display:grid;grid-template-columns:8em minmax(0,1fr);gap:16px;padding:16px 0;border-bottom:1px solid var(--line)}
.info dt{font-size:13px;color:var(--stone)}.info dd{margin:0}.info small{color:var(--stone);font-size:13px}
.note,.crumb,.meta{font-size:14px;color:var(--stone)}.note{margin:16px 0 22px}
details{border-bottom:1px solid var(--line);padding:4px 0}details:first-child{border-top:1px solid var(--line)}
summary{display:flex;gap:16px;align-items:baseline;cursor:pointer;list-style:none;padding:18px 0;min-height:44px}summary::-webkit-details-marker{display:none}
summary::after{content:"＋";margin-left:auto;color:var(--stone);font-size:14px}details[open] summary::after{content:"－"}
.qn{font-family:var(--display);color:var(--whisky);font-size:15px;flex:none}.qt{font-family:var(--serif);font-size:17px;font-weight:400;line-height:1.6}
summary:hover .qt{color:var(--whisky)}details p{margin:0 0 20px;padding-left:34px;font-size:15px;color:rgba(26,25,23,.85)}
.list{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}.list li{padding:16px 0;border-bottom:1px solid var(--line)}
.list strong,.list a{display:block;font-family:var(--serif);font-weight:500}.list span{color:var(--stone);font-size:15px}.list time{display:block;color:var(--stone);font-size:13px;letter-spacing:.04em;margin:2px 0 4px}
.news{list-style:none;padding:0;margin:20px 0 0}.news li{display:flex;gap:16px;padding:12px 0;border-top:1px solid var(--line)}.news time{color:var(--whisky);font-size:13px;flex:none;padding-top:2px}
.more{display:inline-block;margin-top:18px}
.event{border:1px solid var(--line);background:var(--paper);margin-top:26px}.event img{display:block;width:100%;height:auto;aspect-ratio:1600/837;background:#1a1714}
.ev-body{padding:26px 28px 28px}.ev-body h3{font-family:var(--serif);font-size:22px;font-weight:500;letter-spacing:.03em;margin:0 0 12px;line-height:1.45}.ev-body>p{margin:0 0 18px}
.lineup-h{font-family:var(--display);font-style:italic;color:var(--whisky);font-size:17px;margin:24px 0 6px}.lg{margin:14px 0 4px;font-size:13px;color:var(--stone);letter-spacing:.04em}
.lineup ol{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}.lineup li{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:8px 0;border-bottom:1px solid var(--line);font-size:15px}
.meta2{color:var(--stone);white-space:nowrap}.ev-body .btns{margin-top:22px}
.post-fig{margin:30px 0 34px;text-align:center}.post-fig img{display:block;width:100%;max-width:460px;height:auto;aspect-ratio:1080/1350;margin:0 auto;border-radius:2px;background:#2a241d}
.post-fig figcaption{margin:10px auto 0;max-width:460px;font-size:12px;color:var(--stone);letter-spacing:.04em;line-height:1.7}
.article{margin-top:32px}.post-h{font-family:var(--serif);font-size:22px;letter-spacing:.04em;margin:44px 0 16px}
.notes>div{grid-template-columns:7em minmax(0,1fr)}.closing{margin:28px 0 0;padding-left:14px;border-left:2px solid var(--whisky);font-size:14px;color:var(--stone)}
h1.page{font-family:var(--serif);font-size:clamp(30px,4.6vw,44px);letter-spacing:.04em;margin:10px 0 6px}
.todo{background:#FBE3E0;color:#8A1F17;border:1px dashed #C8483D;padding:0 6px;border-radius:2px;font-size:.92em;font-weight:400}
.foot{border-top:1px solid var(--line);padding:40px 0 56px;font-size:13px;color:var(--stone)}
.flogo{display:flex;align-items:center;gap:14px;margin:0 0 22px}.flogo img{height:auto}.flogo img:first-child{width:44px}.flogo img:last-child{width:194px}
.warn{color:var(--ink);letter-spacing:.06em}.nap{line-height:1.9}.small{font-size:12px}
#agegate{position:fixed;inset:0;z-index:50;background:rgba(246,244,239,.97);display:flex;align-items:center;justify-content:center;padding:24px}
#agegate[hidden]{display:none}.ag-box{max-width:380px;text-align:center;border:1px solid var(--line);padding:36px 28px;background:var(--paper)}
.ag-mark{display:block;margin:0 auto 12px;width:64px;height:auto}.ag-word{display:block;margin:0 auto 18px;width:160px;height:auto}
#ag-yes{background:var(--ink);color:var(--paper);border:0;min-height:44px;padding:0 20px;font-size:15px;cursor:pointer;margin:8px;border-radius:2px}.ag-no{display:block;color:var(--stone);font-size:14px;margin-top:6px}
:focus-visible{outline:2px solid var(--whisky);outline-offset:2px}
@media (max-width:900px){.hero-mark{width:84px}.mast{grid-template-columns:1fr;gap:28px;padding:40px 0 34px}.mast-r{align-items:flex-start;text-align:left}
.split{grid-template-columns:1fr;gap:22px}.grid3{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid3 article:nth-child(3n){border-right:1px solid var(--line)}.grid3 article:nth-child(2n){border-right:0}.grid3 article:nth-last-child(-n+3){border-bottom:1px solid var(--line)}.grid3 article:nth-last-child(-n+2){border-bottom:0}}
@media (max-width:600px){.ev-body{padding:20px 18px 22px}.hero-mark{display:none}.nav{order:3;flex-basis:100%;justify-content:flex-start;gap:2px 18px}.langs{order:2}
.grid3{grid-template-columns:1fr}.grid3 article{border-right:0!important;border-bottom:1px solid var(--line)!important}.grid3 article:last-child{border-bottom:0!important}
.facts{grid-template-columns:1fr}.info>div{grid-template-columns:1fr;gap:2px}details p{padding-left:0}.plate svg{aspect-ratio:4/3}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#F6F4EF"/><path d="M32 8l5 19 19 5-19 5-5 19-5-19-19-5 19-5z" fill="#8C5A2B"/></svg>'

def build(out="site", base=None):
    global BASE, OG_IMG
    if base:
        BASE = base; OG_IMG = BASE + "assets/og.png"
    if os.path.exists(out):
        shutil.rmtree(out)
    def w(path, text):
        p = os.path.join(out, path); os.makedirs(os.path.dirname(p) or out, exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
    for l in LANGS:
        w(L[l]["path"] + "index.html", home(l))
    w("faq/index.html", faq_page())
    for l in LANGS:
        w(L[l]["path"] + "journal/index.html", journal_page(l))
        for p in POSTS:
            if l in p["text"]:
                w(L[l]["path"] + "journal/" + p["slug"] + "/index.html", post_page(p, l))
    w("journal/_template/index.html", article_template())
    w("404.html", page_404())
    w("sitemap.xml", sitemap())
    w("robots.txt", robots())
    w("llms.txt", llms())
    w("assets/style.css", CSS.strip() + "\n")
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    bdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand")
    for fn in os.listdir(bdir):
        shutil.copy(os.path.join(bdir, fn), os.path.join(out, "assets", fn))
    w(".nojekyll", "")
    todos = sorted({k for k in FACTS for l in LANGS if not FACTS[k][l]})
    if not FB: todos.append("FB")
    if not THREADS: todos.append("THREADS")
    print("built", out, "| 未填：", todos)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        HIDE_TODO = False
        build("preview", "/")
    else:
        build()
