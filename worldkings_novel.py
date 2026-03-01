#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  世界王 NovelForge パイプライン v3                                ║
║  World Kings × NovelForge Integrated Pipeline                    ║
║                                                                  ║
║  テキスト生成: Claude API / DeepSeek API (選択可能)               ║
║  画像生成:     Stable Diffusion WebUI (ローカル)                  ║
║  世界観:       世界王47都道府県データベース自動注入                  ║
║                                                                  ║
║  使い方:                                                          ║
║    python worldkings_novel.py 京都 王印封                         ║
║    python worldkings_novel.py 京都 王印封 --llm deepseek          ║
║    python worldkings_novel.py 京都 王印封 --llm claude            ║
║    python worldkings_novel.py 京都 王印封 --skip-images           ║
║    python worldkings_novel.py 京都 --all   # 5世界線一括          ║
║                                                                  ║
║  環境変数:                                                        ║
║    ANTHROPIC_API_KEY  = sk-ant-...                                ║
║    DEEPSEEK_API_KEY   = sk-...                                   ║
║    SD_WEBUI_URL       = http://localhost:7860 (default)           ║
║    GITHUB_USERNAME    = your-username                             ║
║    GITHUB_TOKEN       = ghp_...                                  ║
╚══════════════════════════════════════════════════════════════════╝

Requirements:
  pip install requests rich pyyaml jinja2 --break-system-packages
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import requests

# ─── Rich fallback ────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (
        BarColumn, Progress, SpinnerColumn, TaskProgressColumn,
        TextColumn, TimeElapsedColumn,
    )
    from rich.table import Table
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# ─── World Kings Data ─────────────────────────────────────────
from world_kings_data import PREFECTURES, WORLD_SETTING, get_world_line_key
from fairy_visuals import get_fairy_prompt, get_fairy_negative_extra, FAIRY_VISUALS


# ─── Simple Console fallback ──────────────────────────────────
class SimpleConsole:
    def print(self, msg="", **kwargs):
        # Strip rich markup
        import re
        clean = re.sub(r'\[.*?\]', '', str(msg))
        print(clean)

console = Console() if HAS_RICH else SimpleConsole()

# ─── Config ───────────────────────────────────────────────────
SD_URL = os.getenv("SD_WEBUI_URL", "http://localhost:7860")
OUTPUT_BASE = Path("./worldkings_output").resolve()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA CLASSES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class LLMConfig:
    provider: str = "claude"          # "claude" or "deepseek"
    claude_model: str = "claude-sonnet-4-20250514"
    deepseek_model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4096

    @property
    def api_key(self) -> str:
        if self.provider == "claude":
            key = os.getenv("ANTHROPIC_API_KEY", "")
        else:
            key = os.getenv("DEEPSEEK_API_KEY", "")
        if not key:
            console.print(f"[red]❌ {self.provider.upper()} API キーが未設定[/]")
            console.print(f"  export {'ANTHROPIC_API_KEY' if self.provider == 'claude' else 'DEEPSEEK_API_KEY'}=your-key")
            sys.exit(1)
        return key


@dataclass
class SDConfig:
    url: str = SD_URL
    steps: int = 28
    cfg_scale: float = 7.0
    width: int = 768
    height: int = 512
    sampler: str = "DPM++ 2M Karras"
    style_suffix: str = (
        "masterpiece, best quality, detailed background, "
        "anime style, soft lighting, atmospheric, "
        "fantasy illustration, mythical japan"
    )
    negative: str = (
        "lowres, bad anatomy, bad hands, text, error, "
        "missing fingers, extra digit, fewer digits, cropped, "
        "worst quality, low quality, normal quality, "
        "jpeg artifacts, signature, watermark, username, blurry, "
        "nsfw, nude"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  REAL ANCHORS (実在スポット・歴史)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL_ANCHORS = {
    "北海道": {
        "spots": ["函館山", "小樽運河", "富良野ラベンダー畑", "摩周湖", "旭山動物園"],
        "history": ["蝦夷地開拓（1869）", "五稜郭の戦い（1869）"],
        "local": ["海鮮", "ジンギスカン", "雪原", "白樺", "アイヌ文化"]
    },
    "青森": {
        "spots": ["弘前城", "奥入瀬渓流", "恐山", "十和田湖", "ねぶた会館"],
        "history": ["津軽藩の歴史", "青函トンネル開通（1988）"],
        "local": ["りんご", "ねぶた", "津軽三味線", "地吹雪", "イタコ"]
    },
    "岩手": {
        "spots": ["中尊寺金色堂", "龍泉洞", "浄土ヶ浜", "花巻温泉", "遠野"],
        "history": ["奥州藤原氏の栄華", "宮沢賢治のイーハトーブ"],
        "local": ["わんこそば", "南部鉄器", "座敷わらし", "遠野物語", "三陸海岸"]
    },
    "宮城": {
        "spots": ["松島", "瑞鳳殿", "仙台城跡", "蔵王", "石巻"],
        "history": ["伊達政宗の城下町", "東日本大震災（2011）"],
        "local": ["牛タン", "笹かまぼこ", "七夕飾り", "ずんだ", "樹氷"]
    },
    "秋田": {
        "spots": ["角館武家屋敷", "田沢湖", "男鹿半島", "乳頭温泉", "大曲"],
        "history": ["なまはげ伝統", "佐竹藩の歴史"],
        "local": ["きりたんぽ", "なまはげ", "枝垂れ桜", "竿燈", "横手かまくら"]
    },
    "山形": {
        "spots": ["山寺（立石寺）", "蔵王温泉", "銀山温泉", "最上川", "出羽三山"],
        "history": ["松尾芭蕉の奥の細道", "出羽三山の修験道"],
        "local": ["さくらんぼ", "芋煮", "将棋の駒", "花笠", "蔵王樹氷"]
    },
    "福島": {
        "spots": ["鶴ヶ城", "磐梯山", "五色沼", "大内宿", "花見山"],
        "history": ["戊辰戦争・白虎隊（1868）", "東日本大震災・原発事故（2011）"],
        "local": ["桃", "喜多方ラーメン", "赤べこ", "会津魂", "再生への歩み"]
    },
    "茨城": {
        "spots": ["偕楽園", "筑波山", "袋田の滝", "大洗磯前神社", "霞ヶ浦"],
        "history": ["水戸黄門（徳川光圀）", "つくば研究学園都市"],
        "local": ["納豆", "干し芋", "あんこう鍋", "メロン", "筑波研究"]
    },
    "栃木": {
        "spots": ["日光東照宮", "華厳の滝", "中禅寺湖", "那須高原", "足利学校"],
        "history": ["徳川家康の霊廟", "足利学校の学問"],
        "local": ["餃子", "いちご", "日光彫り", "湯葉", "那須温泉"]
    },
    "群馬": {
        "spots": ["草津温泉", "伊香保温泉", "富岡製糸場", "榛名山", "尾瀬"],
        "history": ["富岡製糸場と近代化", "上州の風と気質"],
        "local": ["水沢うどん", "焼きまんじゅう", "だるま", "温泉", "からっ風"]
    },
    "埼玉": {
        "spots": ["川越小江戸", "秩父神社", "長瀞", "氷川神社", "鉄道博物館"],
        "history": ["武蔵国の中心地", "秩父事件（1884）"],
        "local": ["草加煎餅", "十万石饅頭", "狭山茶", "小江戸の蔵造り", "祭り囃子"]
    },
    "千葉": {
        "spots": ["成田山新勝寺", "九十九里浜", "鋸山", "銚子", "養老渓谷"],
        "history": ["成田山の信仰", "房総半島の漁業文化"],
        "local": ["落花生", "海苔", "びわ", "醤油", "潮風"]
    },
    "東京": {
        "spots": ["浅草寺", "東京タワー", "渋谷スクランブル交差点", "明治神宮", "秋葉原"],
        "history": ["関東大震災（1923）", "東京大空襲（1945）"],
        "local": ["満員電車", "ネオン", "雑踏", "24時間", "もんじゃ"]
    },
    "神奈川": {
        "spots": ["鎌倉大仏", "箱根", "横浜中華街", "江ノ島", "三渓園"],
        "history": ["鎌倉幕府", "ペリー来航・開港（1853）"],
        "local": ["しらす", "崎陽軒シウマイ", "鳩サブレー", "湘南", "港町"]
    },
    "新潟": {
        "spots": ["佐渡島", "越後湯沢", "弥彦神社", "星峠の棚田", "清津峡"],
        "history": ["上杉謙信の居城", "佐渡金山"],
        "local": ["コシヒカリ", "日本酒", "へぎそば", "笹団子", "豪雪"]
    },
    "富山": {
        "spots": ["黒部ダム", "立山連峰", "五箇山合掌造り", "富山湾", "雨晴海岸"],
        "history": ["立山信仰", "北前船の交易"],
        "local": ["ます寿司", "ホタルイカ", "氷見ブリ", "薬売り", "黒部の水"]
    },
    "石川": {
        "spots": ["兼六園", "金沢城", "ひがし茶屋街", "21世紀美術館", "輪島"],
        "history": ["加賀百万石の文化", "輪島塗の伝統"],
        "local": ["金箔", "加賀友禅", "治部煮", "能登の海", "茶屋街"]
    },
    "福井": {
        "spots": ["永平寺", "東尋坊", "恐竜博物館", "一乗谷朝倉氏遺跡", "三方五湖"],
        "history": ["曹洞宗の大本山永平寺", "恐竜化石の宝庫"],
        "local": ["越前がに", "焼き鯖寿司", "恐竜", "永平寺の禅", "水仙"]
    },
    "山梨": {
        "spots": ["富士五湖", "昇仙峡", "甲府城", "忍野八海", "清里高原"],
        "history": ["武田信玄の甲斐国", "富士山信仰"],
        "local": ["ぶどう", "桃", "ほうとう", "ワイン", "富士山"]
    },
    "長野": {
        "spots": ["上高地", "善光寺", "松本城", "軽井沢", "諏訪大社"],
        "history": ["川中島の戦い", "善光寺の信仰"],
        "local": ["そば", "おやき", "野沢菜", "信州味噌", "高原の風"]
    },
    "岐阜": {
        "spots": ["白川郷", "高山古い町並み", "下呂温泉", "岐阜城", "郡上八幡"],
        "history": ["関ケ原の戦い（1600）", "白川郷の合掌造り集落"],
        "local": ["飛騨牛", "朴葉味噌", "鮎", "和紙", "郡上踊り"]
    },
    "静岡": {
        "spots": ["三保の松原", "久能山東照宮", "修善寺", "浜名湖", "富士宮"],
        "history": ["駿府城と家康の隠居", "東海道五十三次"],
        "local": ["茶", "うなぎ", "桜エビ", "みかん", "富士山の絶景"]
    },
    "愛知": {
        "spots": ["名古屋城", "熱田神宮", "犬山城", "トヨタ産業技術記念館", "覚王山"],
        "history": ["三英傑（信長・秀吉・家康）", "名古屋の産業革命"],
        "local": ["味噌煮込みうどん", "手羽先", "きしめん", "ういろう", "モーニング"]
    },
    "三重": {
        "spots": ["伊勢神宮", "鳥羽水族館", "熊野古道（伊勢路）", "志摩", "赤目四十八滝"],
        "history": ["伊勢神宮の式年遷宮", "お伊勢参りの文化"],
        "local": ["伊勢うどん", "赤福", "松阪牛", "真珠", "お伊勢参り"]
    },
    "滋賀": {
        "spots": ["琵琶湖", "彦根城", "比叡山延暦寺", "近江八幡", "竹生島"],
        "history": ["比叡山の仏教文化", "近江商人の精神"],
        "local": ["近江牛", "鮒寿司", "信楽焼", "琵琶湖", "近江商人"]
    },
    "京都": {
        "spots": ["清水寺", "伏見稲荷大社", "嵐山竹林", "金閣寺", "祇園花見小路"],
        "history": ["応仁の乱（1467）", "明治維新・東京遷都（1868）"],
        "local": ["抹茶", "京町家", "舞妓", "石畳", "鴨川"]
    },
    "大阪": {
        "spots": ["道頓堀", "大阪城", "通天閣", "新世界", "中之島"],
        "history": ["大坂の陣（1615）", "大阪万博（1970）"],
        "local": ["たこ焼き", "お好み焼き", "お笑い", "商人文化", "人情"]
    },
    "兵庫": {
        "spots": ["姫路城", "神戸港", "有馬温泉", "城崎温泉", "淡路島"],
        "history": ["源平合戦（1184）", "阪神・淡路大震災（1995）"],
        "local": ["神戸ビーフ", "明石焼き", "そばめし", "灘の酒", "異人館"]
    },
    "奈良": {
        "spots": ["東大寺", "春日大社", "法隆寺", "奈良公園", "吉野山"],
        "history": ["平城京（710）", "聖武天皇と大仏建立"],
        "local": ["鹿せんべい", "柿の葉寿司", "奈良漬け", "鹿", "古都の静寂"]
    },
    "和歌山": {
        "spots": ["高野山", "那智の滝", "熊野古道", "白浜", "友ヶ島"],
        "history": ["空海と高野山開創", "熊野三山の巡礼"],
        "local": ["梅干し", "みかん", "熊野の杉", "紀州備長炭", "巡礼道"]
    },
    "鳥取": {
        "spots": ["鳥取砂丘", "砂の美術館", "浦富海岸", "大山", "三朝温泉"],
        "history": ["因幡の白兎伝説", "鳥取城の歴史"],
        "local": ["松葉がに", "二十世紀梨", "砂丘", "とうふちくわ", "大山の水"]
    },
    "島根": {
        "spots": ["出雲大社", "石見銀山", "松江城", "足立美術館", "隠岐の島"],
        "history": ["出雲神話", "石見銀山（世界遺産）"],
        "local": ["出雲そば", "しじみ", "勾玉", "神在月", "縁結び"]
    },
    "岡山": {
        "spots": ["倉敷美観地区", "岡山後楽園", "備中松山城", "吉備津神社", "瀬戸大橋"],
        "history": ["桃太郎伝説", "備前焼の歴史"],
        "local": ["桃", "マスカット", "きびだんご", "備前焼", "晴れの国"]
    },
    "広島": {
        "spots": ["厳島神社", "原爆ドーム", "平和記念公園", "尾道", "しまなみ海道"],
        "history": ["原爆投下（1945）", "厳島の戦い（1555）"],
        "local": ["お好み焼き", "もみじ饅頭", "牡蠣", "路面電車", "平和の灯"]
    },
    "山口": {
        "spots": ["角島大橋", "秋芳洞", "錦帯橋", "松下村塾", "元乃隅神社"],
        "history": ["吉田松陰と明治維新", "下関海峡の戦い"],
        "local": ["ふぐ", "瓦そば", "夏みかん", "萩焼", "維新の志士"]
    },
    "徳島": {
        "spots": ["鳴門の渦潮", "祖谷のかずら橋", "眉山", "大歩危小歩危", "阿波おどり会館"],
        "history": ["阿波おどりの歴史", "藍染め文化"],
        "local": ["すだち", "鳴門金時", "阿波おどり", "藍染め", "渦潮"]
    },
    "香川": {
        "spots": ["栗林公園", "金刀比羅宮", "小豆島", "直島", "父母ヶ浜"],
        "history": ["空海の生誕地", "瀬戸内国際芸術祭"],
        "local": ["讃岐うどん", "オリーブ", "醤油", "和三盆", "盆栽"]
    },
    "愛媛": {
        "spots": ["道後温泉", "松山城", "しまなみ海道", "下灘駅", "内子の町並み"],
        "history": ["夏目漱石「坊っちゃん」", "正岡子規の俳句革新"],
        "local": ["みかん", "じゃこ天", "坊っちゃん団子", "今治タオル", "道後の湯"]
    },
    "高知": {
        "spots": ["桂浜", "四万十川", "高知城", "室戸岬", "仁淀川"],
        "history": ["坂本龍馬", "自由民権運動の発祥"],
        "local": ["かつおのたたき", "四万十の清流", "よさこい", "文旦", "土佐の酒"]
    },
    "福岡": {
        "spots": ["太宰府天満宮", "福岡タワー", "中洲屋台", "門司港レトロ", "志賀島"],
        "history": ["元寇（1274, 1281）", "太宰府の古代政庁"],
        "local": ["博多ラーメン", "もつ鍋", "明太子", "屋台文化", "博多祇園山笠"]
    },
    "佐賀": {
        "spots": ["有田陶磁の里", "唐津城", "吉野ヶ里遺跡", "嬉野温泉", "虹の松原"],
        "history": ["有田焼400年の歴史", "吉野ヶ里の弥生時代"],
        "local": ["有田焼", "伊万里焼", "嬉野茶", "佐賀牛", "バルーンフェスタ"]
    },
    "長崎": {
        "spots": ["グラバー園", "大浦天主堂", "軍艦島", "平和公園", "出島"],
        "history": ["出島とオランダ交易", "原爆投下（1945）"],
        "local": ["ちゃんぽん", "カステラ", "皿うどん", "キリシタン文化", "異国情緒"]
    },
    "熊本": {
        "spots": ["熊本城", "阿蘇山", "水前寺成趣園", "黒川温泉", "通潤橋"],
        "history": ["加藤清正の築城", "熊本地震（2016）"],
        "local": ["馬刺し", "太平燕", "からし蓮根", "くまモン", "阿蘇の草原"]
    },
    "大分": {
        "spots": ["別府地獄めぐり", "由布院温泉", "臼杵石仏", "国東半島", "くじゅう連山"],
        "history": ["宇佐神宮（全国八幡の総本宮）", "南蛮文化の受容"],
        "local": ["とり天", "だんご汁", "かぼす", "温泉", "湯けむり"]
    },
    "宮崎": {
        "spots": ["高千穂峡", "青島神社", "鵜戸神宮", "都井岬", "えびの高原"],
        "history": ["天孫降臨の神話", "日向国の古代文化"],
        "local": ["チキン南蛮", "マンゴー", "地鶏", "日向夏", "神楽"]
    },
    "鹿児島": {
        "spots": ["桜島", "屋久島", "知覧特攻平和会館", "霧島神宮", "仙巌園"],
        "history": ["薩摩藩と明治維新", "西南戦争（1877）"],
        "local": ["黒豚", "焼酎", "さつまあげ", "桜島大根", "西郷どん"]
    },
    "沖縄": {
        "spots": ["首里城", "美ら海水族館", "国際通り", "斎場御嶽", "万座毛"],
        "history": ["琉球王国滅亡（1879）", "沖縄戦（1945）"],
        "local": ["三線", "シーサー", "泡盛", "ちんすこう", "御嶽"]
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  WORLD LINE COLORS (物語カラーリング)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WORLD_LINE_COLORS = {
    "封印線": {
        "tone": "静謐で不穏。封じられた力が目覚めかける緊張感。",
        "focus": {
            1: "封印されたものが眠る場所の描写",
            2: "結界の揺らぎ、封印の劣化兆候",
            3: "封印を維持するか解放するかの葛藤",
            4: "妖精が封印の歴史と意味を語る",
            5: "封印を修復する微調整。代償の予感。"
        },
        "sd_mood": "dark atmosphere, ancient seal, glowing runes, mystical barrier"
    },
    "商都線": {
        "tone": "活気と欲望。人の流れと金の流れの中に隠れた歪み。",
        "focus": {
            1: "賑わう商いの場、市場や通りの描写",
            2: "経済や人流の中の微妙な異変",
            3: "人間の欲望と守護のバランスへの葛藤",
            4: "妖精が商いの本質と人の営みを語る",
            5: "人流や偶然を微調整。誰も気づかない。"
        },
        "sd_mood": "bustling market, warm lanterns, flowing crowd, hidden magic"
    },
    "静律線": {
        "tone": "深い静寂。祈りと内面の世界。最も精神性が高い。",
        "focus": {
            1: "神社仏閣や聖地の静かな空気",
            2: "祈りのエネルギーの揺らぎ",
            3: "沈黙の中で王が自分自身と対峙",
            4: "妖精が祈りの意味と魂の安定を語る",
            5: "目に見えない精神波の調整。最も静かな結末。"
        },
        "sd_mood": "serene temple, morning mist, zen garden, spiritual light"
    },
    "変革線": {
        "tone": "激動。歴史が動く瞬間の裏側。最もドラマチック。",
        "focus": {
            1: "歴史転換点に関わる場所の現在",
            2: "時代の歪みが現代に影響する兆候",
            3: "変革を促すか止めるかの決断",
            4: "妖精が変革のリスクと必要性を語る",
            5: "歴史の流れを1度だけ曲げる。最も大きな代償。"
        },
        "sd_mood": "dramatic sky, turning point, dynamic energy, historical echoes"
    },
    "境界線": {
        "tone": "異文化と出会い。内と外の狭間。哀愁と希望が交差。",
        "focus": {
            1: "境界に位置する場所——海、山、港、国境",
            2: "外部からの影響による歪み",
            3: "受け入れるか拒むかの選択",
            4: "妖精が出会いと別れの本質を語る",
            5: "文化や人の流れを微調整。静かな邂逅。"
        },
        "sd_mood": "borderland, sea horizon, cultural crossing, melancholic beauty"
    }
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LLM TEXT GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def call_llm(system_prompt: str, user_prompt: str, config: LLMConfig) -> str:
    """Unified LLM call — Claude API or DeepSeek API"""

    if config.provider == "claude":
        return _call_claude(system_prompt, user_prompt, config)
    elif config.provider == "deepseek":
        return _call_deepseek(system_prompt, user_prompt, config)
    else:
        raise ValueError(f"Unknown provider: {config.provider}")


def _call_claude(system_prompt: str, user_prompt: str, config: LLMConfig) -> str:
    """Call Anthropic Claude API"""
    headers = {
        "x-api-key": config.api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": config.claude_model,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()

    # Extract text from response
    return "".join(
        block["text"] for block in data["content"] if block["type"] == "text"
    )


def _call_deepseek(system_prompt: str, user_prompt: str, config: LLMConfig) -> str:
    """Call DeepSeek API (OpenAI-compatible)"""
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.deepseek_model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SYSTEM PROMPT BUILDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_system_prompt(pref_name: str, wl_key: str) -> str:
    """Build the story-writing system prompt from World Kings data"""
    pref = PREFECTURES[pref_name]
    wl_color = WORLD_LINE_COLORS[wl_key]
    wl_value = pref["world_lines"][wl_key]
    king = pref["king"]
    fairy = pref["chief_fairy"]
    special = pref["special_fairy"]
    anchors = REAL_ANCHORS.get(pref_name, {"spots": [], "history": [], "local": []})

    return f"""あなたは「世界王」プロジェクトの物語作家です。
5章構成の短編小説（各章300〜400字、合計1500〜2000字）を日本語で執筆してください。

# 世界観
この国は、見えない王たちに守られている。
日本は地震帯という"歪みの列島"。王の星（レギス・アストラ）から47人の王が派遣され、
姿を変えて日常に溶け込み、歪みを微調整している。
王は災害を消せないが、揺れを1段階緩和し、津波を数秒遅延させ、偶然を微調整できる。
王は本来感情を持たないが、日本の感情密度の高さにより感情進化を起こし始める。

# 今回の設定
- 都道府県：{pref_name}
- 王国名：{pref['kingdom']}
- 王国テーマ：{pref['theme']}
- 核となる問い：{pref['question']}
- 世界線：{wl_key}（{wl_value}）
- トーン：{wl_color['tone']}

# キャラクター
- 王：{king['name']}（{king['title']}）
  性格：{king['personality']}
  感情傾向：{king['emotion']}
- 主席妖精：{fairy['name']}（{fairy['attribute']}）
  性格：{fairy['personality']}
  役割：{fairy['role']}
- 地域特化妖精：{special['name']}（{special['attribute']}）
  役割：{special['role']}
- ペアダイナミクス：{pref['pair_dynamic']}

# 実在素材（必ず使用）
- スポット：{', '.join(anchors.get('spots', []))}
- 歴史転換点：{', '.join(anchors.get('history', []))}
- 土地の質感：{', '.join(anchors.get('local', []))}

# 紋章情報
- 紋章：{pref['emblem']['motif']}
- 色：{pref['emblem']['colors']}

# 文体ルール
- 静か、切ない、誇張しない
- 現実を否定しない、災害を消費しない
- 王はヒーローではなく調整者
- 最初の一文は実在スポットの描写で始める
- 最後は「あなたの町にも、王がいる。」で締める
- 各章タイトルを「第一章　〇〇」形式で付ける
- 出力は小説本文のみ。メタ説明は不要
"""


def build_chapter_prompt(chapter_num: int, wl_key: str, pref_name: str, prev_text: str = "") -> str:
    """Build chapter-specific prompt"""
    wl = WORLD_LINE_COLORS[wl_key]
    pref = PREFECTURES[pref_name]
    focus = wl["focus"][chapter_num]

    ch_names = {1: "第一章", 2: "第二章", 3: "第三章", 4: "第四章", 5: "第五章"}
    ch_titles = {
        1: f"現実の{pref_name}",
        2: "歪みの兆候",
        3: "王の葛藤",
        4: "妖精との対話",
        5: "微調整と余韻"
    }

    prev_section = ""
    if prev_text:
        # 前章の最後200文字を文脈として渡す
        prev_section = f"\n【前章末尾（接続用）】\n{prev_text[-200:]}\n"

    opening = ""
    if chapter_num == 1:
        opening = "\n※冒頭に以下を含めてください：\n「あなたはまだ気づいていない。この土地にも、王がいることを。」\n"

    closing = ""
    if chapter_num == 5:
        closing = "\n※末尾に以下を含めてください：\n「あなたの町にも、王がいる。」\n"

    return f"""{prev_section}
{ch_names[chapter_num]}「{ch_titles[chapter_num]}」を執筆してください。

【この章のフォーカス】{focus}

【核となる問い】{pref['question']}
{opening}{closing}
300〜400字程度で。章タイトルを冒頭に。"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SD IMAGE GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_sd_prompt(
    pref_name: str, chapter_num: int, wl_key: str,
    chapter_text: str, llm_config: LLMConfig
) -> tuple[str, str]:
    """Build SD positive/negative prompts using LLM for scene analysis + fairy character"""
    pref = PREFECTURES[pref_name]
    wl = WORLD_LINE_COLORS[wl_key]
    sd_cfg = SDConfig()

    # ── Fairy character selection per chapter ──
    # Ch1: scenery only (no fairy)
    # Ch2: chief fairy appears (sensing distortion)
    # Ch3: no fairy (king's inner struggle)
    # Ch4: chief fairy + special fairy (dialogue scene)
    # Ch5: chief fairy (quiet ending)
    fairy_prompt = ""
    if chapter_num == 2:
        fairy_prompt = get_fairy_prompt(pref_name, "chief")
    elif chapter_num == 4:
        # Both fairies in dialogue scene — use chief as main
        chief = get_fairy_prompt(pref_name, "chief")
        special = get_fairy_prompt(pref_name, "special")
        if chief and special:
            fairy_prompt = f"{chief}, another fairy in background"
        else:
            fairy_prompt = chief or special
    elif chapter_num == 5:
        fairy_prompt = get_fairy_prompt(pref_name, "chief")

    # ── Scene analysis via LLM ──
    scene_prompt = f"""以下の小説テキストから、挿絵の背景情景を英語のStable Diffusionタグに変換してください。
出力はカンマ区切りのタグのみ。文章は不要。40タグ以内。
品質タグ(masterpiece等)は含めないでください。
人物の描写は含めないでください（別途指定します）。
背景・風景・雰囲気・光・天候に集中してください。

小説テキスト:
{chapter_text[:500]}

紋章イメージ: {pref['emblem']['motif']}、色: {pref['emblem']['colors']}
"""
    try:
        scene_tags = call_llm(
            "You are a Stable Diffusion prompt expert. Output ONLY comma-separated English background/scene tags. NO character descriptions.",
            scene_prompt,
            LLMConfig(
                provider=llm_config.provider,
                claude_model=llm_config.claude_model,
                deepseek_model=llm_config.deepseek_model,
                temperature=0.3,
                max_tokens=256,
            )
        )
        scene_tags = scene_tags.replace("```", "").replace("`", "").strip()
        if scene_tags.startswith('"'):
            scene_tags = scene_tags.strip('"')
    except Exception as e:
        console.print(f"  [yellow]⚠ シーン翻訳失敗: {e}[/]")
        scene_tags = "japanese landscape, mystical atmosphere"

    # ── Compose final prompt ──
    parts = []
    if fairy_prompt:
        parts.append(fairy_prompt)
        console.print(f"    [dim]🧚 妖精キャラ注入[/]")
    parts.append(scene_tags)
    parts.append(wl["sd_mood"])
    parts.append(sd_cfg.style_suffix)

    positive = ", ".join(p for p in parts if p)
    negative = sd_cfg.negative
    if fairy_prompt:
        negative = f"{negative}, {get_fairy_negative_extra()}"

    return positive, negative


def generate_image(
    positive: str, negative: str, output_path: Path,
    sd_config: SDConfig, has_fairy: bool = False
) -> bool:
    """Call SD WebUI API to generate image.
    If has_fairy=True: portrait orientation + ADetailer for face quality."""

    # Fairy chapters: portrait (512x768), landscape otherwise (768x512)
    w = 512 if has_fairy else sd_config.width
    h = 768 if has_fairy else sd_config.height

    payload = {
        "prompt": positive,
        "negative_prompt": negative,
        "steps": sd_config.steps,
        "cfg_scale": sd_config.cfg_scale,
        "width": w,
        "height": h,
        "sampler_name": sd_config.sampler,
        "seed": -1,
    }

    # Add ADetailer if available (auto-detect)
    if has_fairy and _has_adetailer(sd_config):
        payload["alwayson_scripts"] = {
            "ADetailer": {
                "args": [
                    True,   # enabled
                    False,  # skip img2img
                    {
                        "ad_model": "face_yolov8n.pt",
                        "ad_prompt": positive,
                        "ad_negative_prompt": negative,
                        "ad_denoising_strength": 0.35,
                        "ad_inpaint_only_masked": True,
                        "ad_inpaint_only_masked_padding": 64,
                    }
                ]
            }
        }
        console.print(f"    [dim]🔍 ADetailer ON（顔修復）[/]")

    try:
        r = requests.post(f"{sd_config.url}/sdapi/v1/txt2img", json=payload, timeout=300)
        r.raise_for_status()
        data = r.json()
        img_data = base64.b64decode(data["images"][0])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(img_data)
        return True
    except Exception as e:
        console.print(f"  [red]❌ 画像生成失敗: {e}[/]")
        return False


def _has_adetailer(sd_config: SDConfig) -> bool:
    """Check if ADetailer extension is available"""
    try:
        r = requests.get(f"{sd_config.url}/sdapi/v1/scripts", timeout=5)
        if r.status_code == 200:
            scripts = r.json()
            all_scripts = scripts.get("txt2img", [])
            return any("adetailer" in s.lower() for s in all_scripts)
    except Exception:
        pass
    return False


def check_sd(sd_config: SDConfig) -> bool:
    """Check if SD WebUI is running"""
    try:
        r = requests.get(f"{sd_config.url}/sdapi/v1/options", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HTML READER BUILDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_html_reader(
    pref_name: str, wl_key: str, chapters: list[str],
    image_files: list[str], output_dir: Path
) -> Path:
    """Generate a beautiful HTML reader for the novel"""
    pref = PREFECTURES[pref_name]
    wl_value = pref["world_lines"][wl_key]
    emblem = pref["emblem"]

    # Color mapping
    color_map = {
        "封印線": ("#1a0a2e", "#7b2ff7", "#c084fc"),
        "商都線": ("#2a1a0a", "#f7a02f", "#fcd084"),
        "静律線": ("#0a1a2e", "#2f7bf7", "#84c0fc"),
        "変革線": ("#2e0a0a", "#f72f2f", "#fc8484"),
        "境界線": ("#0a2e1a", "#2ff77b", "#84fcc0"),
    }
    bg, accent, accent_light = color_map.get(wl_key, ("#1a1a2e", "#7b7bf7", "#c0c0fc"))

    # Build chapters HTML
    chapters_html = ""
    for i, text in enumerate(chapters):
        img_tag = ""
        if i < len(image_files) and image_files[i]:
            img_tag = f'<img src="images/{image_files[i]}" alt="第{i+1}章" class="chapter-img">'

        # Convert newlines to paragraphs
        paragraphs = "\n".join(
            f"<p>{line}</p>" for line in text.split("\n") if line.strip()
        )
        chapters_html += f"""
    <section class="chapter" id="ch{i+1}">
      {img_tag}
      <div class="chapter-text">{paragraphs}</div>
    </section>
"""

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>世界王 ── {pref['kingdom']}〈{wl_key}〉{wl_value}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: {bg};
    color: #e0e0e0;
    font-family: 'Noto Serif JP', serif;
    line-height: 2;
    min-height: 100vh;
  }}

  .hero {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
    background: radial-gradient(ellipse at center, {accent}22, transparent 70%);
  }}

  .hero h1 {{
    font-size: clamp(1.8rem, 5vw, 3.5rem);
    color: {accent_light};
    margin-bottom: 0.5rem;
    letter-spacing: 0.1em;
  }}

  .hero .subtitle {{
    font-size: 1.1rem;
    color: {accent};
    margin-bottom: 1rem;
  }}

  .hero .question {{
    font-size: 1.3rem;
    color: #fff;
    font-style: italic;
    margin: 1.5rem 0;
    opacity: 0.8;
  }}

  .hero .tagline {{
    font-size: 0.9rem;
    color: #888;
    margin-top: 2rem;
  }}

  .meta {{
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 0.85rem;
  }}

  .meta span {{
    display: inline-block;
    margin: 0 0.8rem;
  }}

  .chapter {{
    max-width: 720px;
    margin: 0 auto;
    padding: 3rem 1.5rem;
    border-bottom: 1px solid {accent}33;
  }}

  .chapter-img {{
    max-width: 100%;
    max-height: 500px;
    object-fit: contain;
    display: block;
    margin: 0 auto 2rem auto;
    border-radius: 8px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
  }}

  .chapter-text p {{
    margin-bottom: 1em;
    text-indent: 1em;
  }}

  .footer {{
    text-align: center;
    padding: 4rem 2rem;
    color: {accent};
    font-size: 1.2rem;
  }}

  .emblem-info {{
    text-align: center;
    padding: 2rem;
    color: #555;
    font-size: 0.8rem;
  }}
</style>
</head>
<body>

<div class="hero">
  <h1>世界王 ── {pref['kingdom']}</h1>
  <div class="subtitle">〈{wl_key}〉{wl_value}</div>
  <div class="question">「{pref['question']}」</div>
  <div class="tagline">この国は、見えない王たちに守られている。</div>
</div>

<div class="meta">
  <span>👑 {pref['king']['name']}（{pref['king']['title']}）</span>
  <span>🧚 {pref['chief_fairy']['name']}</span>
  <span>✨ {pref['special_fairy']['name']}</span>
</div>

{chapters_html}

<div class="footer">
  あなたの町にも、王がいる。
</div>

<div class="emblem-info">
  紋章：{emblem['motif']}　｜　色：{emblem['colors']}　｜　象徴：{emblem['symbol']}
</div>

</body>
</html>"""

    # Inject i18n support
    i18n_block = _get_detail_i18n_block()
    html = html.replace('</body>', i18n_block + '\n</body>')

    output_path = output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _get_detail_i18n_block():
    """Return i18n HTML/CSS/JS block for detail pages (v2 - Google Translate)"""
    return '''
<!-- i18n patch v2 -->
<style>
.back-link{position:fixed;top:12px;left:12px;z-index:9999;color:#888;text-decoration:none;font-size:.85rem;padding:4px 10px;background:rgba(255,255,255,.06);border-radius:4px;border:1px solid rgba(255,255,255,.1);transition:.2s}
.back-link:hover{color:#fff;background:rgba(255,255,255,.12)}
.translated-ltr .back-link,.translated-rtl .back-link{top:50px}
.gtranslate-wrap{position:fixed;top:10px;right:12px;z-index:9999}
.translated-ltr .gtranslate-wrap,.translated-rtl .gtranslate-wrap{top:50px}
.goog-te-gadget{font-size:0!important}
.goog-te-gadget .goog-te-combo{
  background:rgba(20,20,30,.9)!important;
  border:1px solid rgba(255,255,255,.2)!important;
  color:#ccc!important;
  padding:5px 8px;border-radius:4px;font-size:.8rem;
  cursor:pointer;outline:none;
}
.goog-te-gadget .goog-te-combo option{background:#1a1a2e;color:#ccc}
.goog-te-banner-frame{display:none!important}
body{top:0!important}
</style>
<a class="back-link" href="../../index.html">← 戻る</a>
<div class="gtranslate-wrap">
<div id="google_translate_element"></div>
</div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({
    pageLanguage:'ja',
    includedLanguages:'ja,en,zh-CN,ko',
    layout:google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay:false
  },'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<script>
(function(){
  var p=new URLSearchParams(location.search);
  var lang=p.get('lang');
  if(lang&&lang!=='ja'){
    var map={en:'en',zh:'zh-CN',ko:'ko'};
    var target=map[lang]||lang;
    var attempts=0;
    var iv=setInterval(function(){
      attempts++;
      var sel=document.querySelector('.goog-te-combo');
      if(sel){sel.value=target;sel.dispatchEvent(new Event('change'));clearInterval(iv);}
      if(attempts>50)clearInterval(iv);
    },200);
  }
})();
</script>
'''


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EMAIL NOTIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def send_gmail(
    output_dir: Path, pref_name: str, wl_key: str,
    chapters: list[str], image_files: list[str]
) -> bool:
    """Send generated novel via Gmail with HTML + images attached."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    gmail_user = os.getenv("GMAIL_ADDRESS", "")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "")
    gmail_to = os.getenv("GMAIL_TO", gmail_user)  # default: send to self

    if not gmail_user or not gmail_pass:
        console.print("[yellow]⚠ Gmail未設定、メール送信をスキップ[/]")
        console.print("  $env:GMAIL_ADDRESS = \"your@gmail.com\"")
        console.print("  $env:GMAIL_APP_PASSWORD = \"xxxx xxxx xxxx xxxx\"")
        console.print("  （Googleアカウント → セキュリティ → アプリパスワードで発行）")
        return False

    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = f"世界王 {pref_name}〈{wl_key}〉生成完了"
        msg["From"] = gmail_user
        msg["To"] = gmail_to

        # Build email body — chapters + inline images
        body_parts = []
        body_parts.append(f"<h1>世界王 ── {pref_name}〈{wl_key}〉</h1>")
        body_parts.append(f"<p>全{len(chapters)}章 生成完了</p><hr>")

        for i, text in enumerate(chapters):
            # Inline image
            if i < len(image_files) and image_files[i]:
                body_parts.append(f'<img src="cid:chapter_{i+1}" style="max-width:100%;height:auto;border-radius:8px;margin:16px 0;">')

            # Chapter text
            paragraphs = "".join(
                f"<p style='text-indent:1em;line-height:1.8;'>{line}</p>"
                for line in text.split("\n") if line.strip()
            )
            body_parts.append(paragraphs)
            body_parts.append("<hr>")

        body_parts.append("<p style='color:#888;'>世界王 NovelForge パイプラインより自動送信</p>")

        html_body = MIMEText(
            f"<html><body style='font-family:serif;max-width:600px;margin:0 auto;padding:16px;background:#1a1a2e;color:#e0e0e0;'>{''.join(body_parts)}</body></html>",
            "html", "utf-8"
        )
        msg.attach(html_body)

        # Attach images inline
        for i, img_name in enumerate(image_files):
            if img_name:
                img_path = output_dir / "images" / img_name
                if img_path.exists():
                    with open(img_path, "rb") as f:
                        img = MIMEImage(f.read(), name=img_name)
                        img.add_header("Content-ID", f"<chapter_{i+1}>")
                        img.add_header("Content-Disposition", "inline", filename=img_name)
                        msg.attach(img)

        # Send
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)

        console.print(f"  [green]✅ Gmail送信完了 → {gmail_to}[/]")
        return True

    except Exception as e:
        console.print(f"  [red]❌ Gmail送信失敗: {e}[/]")
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GIT PUSH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def git_push(output_dir: Path, pref_name: str, wl_key: str) -> bool:
    """Add generated files to PARENT repo and push.
    Does NOT create nested git repos — works with the parent worldkingjapan repo."""
    
    # Find parent repo root (walk up from output_dir until we find .git)
    parent = output_dir.resolve()
    repo_root = None
    for _ in range(10):
        parent = parent.parent
        if (parent / ".git").exists():
            repo_root = parent
            break
    
    if not repo_root:
        console.print("[yellow]⚠ 親Gitリポジトリが見つかりません。git initしてください。[/]")
        console.print(f"  cd {OUTPUT_BASE.resolve().parent}")
        console.print(f"  git init && git remote add origin https://github.com/yourname/worldkingjapan.git")
        return False

    try:
        original_cwd = os.getcwd()
        os.chdir(repo_root)

        # Stage the output directory
        rel_path = output_dir.resolve().relative_to(repo_root)
        subprocess.run(["git", "add", str(rel_path)], capture_output=True, check=True)

        # Commit (use ASCII message to avoid cp932 issues on Windows)
        pref_ascii = rel_path.parts[-1] if rel_path.parts else pref_name
        msg = f"worldkings: {pref_ascii}"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            console.print(f"  [green]✅ コミット完了[/]")
        else:
            if "nothing to commit" in (result.stdout or ""):
                console.print(f"  [yellow]⚠ 変更なし（既にコミット済み）[/]")
            else:
                console.print(f"  [yellow]⚠ コミット: {(result.stderr or '').strip()}[/]")

        # Detect current branch
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        branch = (branch_result.stdout or "").strip() or "main"

        # Push (use default remote)
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            console.print(f"  [green]✅ プッシュ完了[/]")
            return True
        else:
            console.print(f"  [red]❌ プッシュ失敗: {(result.stderr or '').strip()}[/]")
            return False

    except Exception as e:
        console.print(f"  [red]❌ Git操作失敗: {e}[/]")
        return False
    finally:
        os.chdir(original_cwd)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MAIN PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_pipeline(
    pref_name: str,
    world_line_option: str,
    llm_config: LLMConfig,
    sd_config: SDConfig,
    skip_images: bool = False,
    skip_push: bool = False,
    send_email: bool = False,
):
    """Run the full pipeline for one prefecture + world line"""

    pref = PREFECTURES.get(pref_name)
    if not pref:
        console.print(f"[red]❌ '{pref_name}' は未登録[/]")
        return

    # Resolve world line
    wl_key = get_world_line_key(pref_name, world_line_option)
    if not wl_key:
        if world_line_option in WORLD_LINE_COLORS:
            wl_key = world_line_option
        else:
            console.print(f"[red]❌ 世界線 '{world_line_option}' は無効[/]")
            console.print(f"利用可能: {json.dumps(pref['world_lines'], ensure_ascii=False)}")
            return

    wl_value = pref["world_lines"][wl_key]

    # Output directory
    output_dir = OUTPUT_BASE / f"{pref_name}_{wl_key}"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "images").mkdir(exist_ok=True)

    # Header
    console.print()
    if HAS_RICH:
        console.print(Panel(
            f"[bold]世界王 ── {pref['kingdom']}[/bold]\n"
            f"〈{wl_key}〉{wl_value}\n"
            f"👑 {pref['king']['name']}（{pref['king']['title']}）\n"
            f"🧚 {pref['chief_fairy']['name']}  ✨ {pref['special_fairy']['name']}\n"
            f"LLM: {llm_config.provider.upper()}  |  SD: {'ON' if not skip_images else 'SKIP'}",
            title="🌏 世界王 NovelForge Pipeline",
            border_style="cyan",
        ))
    else:
        console.print(f"{'='*60}")
        console.print(f"🌏 世界王 NovelForge Pipeline")
        console.print(f"  世界王 ── {pref['kingdom']}")
        console.print(f"  〈{wl_key}〉{wl_value}")
        console.print(f"  👑 {pref['king']['name']}（{pref['king']['title']}）")
        console.print(f"  🧚 {pref['chief_fairy']['name']}  ✨ {pref['special_fairy']['name']}")
        console.print(f"  LLM: {llm_config.provider.upper()}  |  SD: {'ON' if not skip_images else 'SKIP'}")
        console.print(f"{'='*60}")

    # System prompt
    system_prompt = build_system_prompt(pref_name, wl_key)

    chapters = []
    image_files = []
    prev_text = ""

    if HAS_RICH:
        progress_ctx = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        )
    else:
        from contextlib import contextmanager

        class FakeTask:
            def add_task(self, desc, total=0):
                return 0
            def update(self, task_id, **kw):
                desc = kw.get("description", "")
                if desc:
                    print(f"  {desc}")
            def advance(self, task_id):
                pass

        @contextmanager
        def _fake_progress():
            yield FakeTask()

        progress_ctx = _fake_progress()

    with progress_ctx as progress:

        task = progress.add_task("📖 物語生成中...", total=5)

        for ch_num in range(1, 6):
            progress.update(task, description=f"📖 第{ch_num}章 生成中...")

            # Generate text
            user_prompt = build_chapter_prompt(ch_num, wl_key, pref_name, prev_text)

            try:
                chapter_text = call_llm(system_prompt, user_prompt, llm_config)
                chapters.append(chapter_text)
                prev_text = chapter_text
                console.print(f"  [green]✅ 第{ch_num}章 テキスト完了[/] ({len(chapter_text)}字)")

                # Save text
                (output_dir / f"chapter_{ch_num:02d}.txt").write_text(
                    chapter_text, encoding="utf-8"
                )
            except Exception as e:
                console.print(f"  [red]❌ 第{ch_num}章 生成失敗: {e}[/]")
                chapters.append(f"（第{ch_num}章：生成エラー）")
                image_files.append("")
                progress.advance(task)
                continue

            # Generate image
            if not skip_images and check_sd(sd_config):
                progress.update(task, description=f"🎨 第{ch_num}章 挿絵生成中...")
                # Ch2, Ch4, Ch5 have fairy characters
                fairy_in_chapter = ch_num in (2, 4, 5)
                try:
                    positive, negative = build_sd_prompt(
                        pref_name, ch_num, wl_key, chapter_text, llm_config
                    )
                    img_path = output_dir / "images" / f"chapter_{ch_num:02d}.png"
                    if generate_image(positive, negative, img_path, sd_config, has_fairy=fairy_in_chapter):
                        orient = "縦" if fairy_in_chapter else "横"
                        console.print(f"  [green]✅ 第{ch_num}章 挿絵完了[/] ({orient})")
                        image_files.append(f"chapter_{ch_num:02d}.png")
                    else:
                        image_files.append("")
                except Exception as e:
                    console.print(f"  [yellow]⚠ 第{ch_num}章 挿絵失敗: {e}[/]")
                    image_files.append("")
            else:
                image_files.append("")

            progress.advance(task)

    # Build HTML
    console.print("\n[cyan]📄 HTMLリーダー構築中...[/]")
    html_path = build_html_reader(pref_name, wl_key, chapters, image_files, output_dir)
    console.print(f"  [green]✅ {html_path}[/]")

    # Save metadata
    meta = {
        "prefecture": pref_name,
        "kingdom": pref["kingdom"],
        "world_line": wl_key,
        "world_line_value": wl_value,
        "king": pref["king"],
        "fairy": pref["chief_fairy"],
        "special_fairy": pref["special_fairy"],
        "llm_provider": llm_config.provider,
        "chapters_count": len(chapters),
        "images_count": len([f for f in image_files if f]),
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Git push
    if not skip_push:
        console.print("\n[cyan]🚀 GitHub Pages へデプロイ中...[/]")
        git_push(output_dir, pref_name, wl_key)

    # Email notification
    if send_email:
        console.print("\n[cyan]📧 Gmail送信中...[/]")
        send_gmail(output_dir, pref_name, wl_key, chapters, image_files)

    # Summary
    console.print()
    if HAS_RICH:
        table = Table(title="📊 生成サマリー", box=box.ROUNDED)
        table.add_column("項目", style="cyan")
        table.add_column("値")
        table.add_row("都道府県", pref_name)
        table.add_row("王国", pref["kingdom"])
        table.add_row("世界線", f"{wl_key}（{wl_value}）")
        table.add_row("王", f"{pref['king']['name']}（{pref['king']['title']}）")
        table.add_row("LLM", llm_config.provider.upper())
        table.add_row("テキスト", f"{len(chapters)}章")
        table.add_row("挿絵", f"{len([f for f in image_files if f])}枚")
        table.add_row("出力", str(output_dir))
        console.print(table)
    else:
        console.print(f"📊 生成サマリー")
        console.print(f"  都道府県: {pref_name}")
        console.print(f"  王国: {pref['kingdom']}")
        console.print(f"  世界線: {wl_key}（{wl_value}）")
        console.print(f"  王: {pref['king']['name']}（{pref['king']['title']}）")
        console.print(f"  LLM: {llm_config.provider.upper()}")
        console.print(f"  テキスト: {len(chapters)}章")
        console.print(f"  挿絵: {len([f for f in image_files if f])}枚")
        console.print(f"  出力: {output_dir}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CLI ENTRY POINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="世界王 NovelForge パイプライン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python worldkings_novel.py 京都 王印封
  python worldkings_novel.py 京都 王印封 --llm deepseek
  python worldkings_novel.py 京都 王印封 --llm claude --skip-images
  python worldkings_novel.py 京都 --all
  python worldkings_novel.py --list
        """,
    )
    parser.add_argument("prefecture", nargs="?", help="都道府県名（例: 京都）")
    parser.add_argument("worldline", nargs="?", help="世界線オプション（例: 王印封）")
    parser.add_argument("--llm", default="claude", choices=["claude", "deepseek"],
                        help="テキスト生成LLM (default: claude)")
    parser.add_argument("--claude-model", default="claude-sonnet-4-20250514",
                        help="Claude model (default: claude-sonnet-4-20250514)")
    parser.add_argument("--deepseek-model", default="deepseek-chat",
                        help="DeepSeek model (default: deepseek-chat)")
    parser.add_argument("--skip-images", action="store_true", help="画像生成をスキップ")
    parser.add_argument("--skip-push", action="store_true", help="GitHub pushをスキップ")
    parser.add_argument("--email", action="store_true", help="生成完了後にGmailで送信")
    parser.add_argument("--all", action="store_true", help="5世界線すべてを一括生成")
    parser.add_argument("--list", action="store_true", help="全都道府県一覧を表示")
    parser.add_argument("--sd-url", default=None, help="SD WebUI URL")

    args = parser.parse_args()

    # List mode
    if args.list:
        console.print("\n[bold cyan]🗾 世界王 47都道府県一覧[/]\n")
        for name, p in PREFECTURES.items():
            wl = " | ".join(p["world_lines"].values())
            console.print(f"  [bold]{name}[/] : {p['kingdom']}（{p['king']['title']}）")
            console.print(f"    世界線: {wl}")
        return

    if not args.prefecture:
        parser.print_help()
        return

    if args.prefecture not in PREFECTURES:
        console.print(f"[red]❌ '{args.prefecture}' は未登録[/]")
        console.print("使用可能: " + ", ".join(PREFECTURES.keys()))
        return

    # Config
    llm_config = LLMConfig(
        provider=args.llm,
        claude_model=args.claude_model,
        deepseek_model=args.deepseek_model,
    )

    sd_config = SDConfig()
    if args.sd_url:
        sd_config.url = args.sd_url

    pref = PREFECTURES[args.prefecture]

    if args.all:
        # Run all 5 world lines
        for wl_key in pref["world_lines"]:
            wl_value = pref["world_lines"][wl_key]
            console.print(f"\n{'='*60}")
            console.print(f"[bold]📌 {args.prefecture} × {wl_key}（{wl_value}）[/]")
            console.print(f"{'='*60}")
            run_pipeline(
                args.prefecture, wl_key, llm_config, sd_config,
                skip_images=args.skip_images,
                skip_push=args.skip_push,
                send_email=args.email,
            )
    else:
        if not args.worldline:
            console.print(f"\n[bold]{args.prefecture}の世界線オプション:[/]")
            for key, val in pref["world_lines"].items():
                console.print(f"  {key}: {val}")
            console.print(f"\n例: python worldkings_novel.py {args.prefecture} {list(pref['world_lines'].values())[0]}")
            return

        run_pipeline(
            args.prefecture, args.worldline, llm_config, sd_config,
            skip_images=args.skip_images,
            skip_push=args.skip_push,
            send_email=args.email,
        )


if __name__ == "__main__":
    main()
