# -*- coding: utf-8 -*-
"""
世界王 - 47 Guardians of Japan
完全データベース（構想蓄積データ ver.10）
"""

# ============================================================
# 共通設定
# ============================================================

WORLD_SETTING = {
    "title": "世界王 – 47 Guardians of Japan",
    "tagline": "この国は、見えない王たちに守られている。",
    "mother_star": "Regis Astra（レギス・アストラ）",
    "term_years": 7,
    "emotion_levels": {
        1: "違和感",
        2: "共感",
        3: "愛着（警告）",
        4: "執着（交代準備）",
        5: "帰還拒否（強制帰還）"
    },
    "fairy_types_common": ["地妖精", "水妖精", "風妖精", "火妖精", "記憶妖精"],
    "world_lines": {
        "封印線": "歪み・禁忌・封じられた力・結界・守護・封印崩壊",
        "商都線": "商い・経済・人流・欲望・市場・交換・活力",
        "静律線": "精神・祈り・沈黙・内面・神社仏閣・鎮魂",
        "変革線": "革命・転換・噴火・挑戦・時代転換点",
        "境界線": "海・山・国境・文化交差・出会いと別れ"
    }
}

# ============================================================
# 物語テンプレート（5章構成）
# ============================================================

STORY_TEMPLATE = {
    "opening": "あなたはまだ気づいていない。この土地にも、王がいることを。",
    "closing": "あなたの町にも、王がいる。",
    "chapters": {
        1: {
            "title": "現実アンカー",
            "description": "実在地名・スポット・季節・時刻で始まる。リアリティ確保。",
            "elements": ["実在スポット描写", "季節感", "時刻", "日常の空気"]
        },
        2: {
            "title": "歪みの兆候",
            "description": "小さな違和感、妖精のざわめき、王の感知。静かに始まる。",
            "elements": ["違和感", "妖精の反応", "王の感知", "不穏な気配"]
        },
        3: {
            "title": "王の葛藤",
            "description": "王は迷う。守れるか、間に合うか、帰還命令は近いか。",
            "elements": ["内面描写", "感情進化", "使命と感情の対立", "決断"]
        },
        4: {
            "title": "主席妖精との対話",
            "description": "哲学パート。読者が刺さる台詞を入れる。",
            "elements": ["妖精の言葉", "王への問いかけ", "感情の交差", "核心台詞"]
        },
        5: {
            "title": "微調整と余韻",
            "description": "派手にしない。0.5秒遅らせる、風を変える。静かに終わる。",
            "elements": ["微調整アクション", "人間は気づかない", "王の独白", "余韻"]
        }
    }
}

# ============================================================
# 47都道府県 完全データ
# ============================================================

PREFECTURES = {
    "北海道": {
        "theme": "孤独と広さの王国",
        "kingdom": "ノルディア・エルム",
        "question": "あなたは、広さに耐えられるか？",
        "king": {
            "name": "ノルディア・エルム",
            "title": "孤広王",
            "personality": "寡黙で観察者。広さを愛する。",
            "emotion": "静かな孤独と優しさ"
        },
        "chief_fairy": {
            "name": "フロストリン",
            "attribute": "氷・大地",
            "personality": "無口で忠実",
            "role": "地脈圧の分散"
        },
        "special_fairy": {
            "name": "オーロリア",
            "attribute": "極光",
            "personality": "静かで広大",
            "role": "寒冷波と孤独感の緩和"
        },
        "pair_dynamic": "無言同士。会話は少ないが最も信頼が厚い。",
        "emblem": {
            "motif": "氷結した大地に北斗七星",
            "colors": "アイスブルー＋銀",
            "symbol": "広さ・孤高"
        },
        "world_lines": {
            "封印線": "氷結界",
            "商都線": "開拓商圏",
            "静律線": "北静域",
            "変革線": "独立志",
            "境界線": "大陸境界"
        }
    },
    "青森": {
        "theme": "終着と再生の王国",
        "kingdom": "アオモリア・レヴナント",
        "question": "終わりは、本当に終わりか？",
        "king": {
            "name": "アオモリア・レヴナント",
            "title": "再生王",
            "personality": "終わりを恐れない。忍耐強い。",
            "emotion": "静かな希望"
        },
        "chief_fairy": {
            "name": "ネブラ",
            "attribute": "霧・記憶",
            "personality": "静かで包容力",
            "role": "終わりの感情を再生へ導く"
        },
        "special_fairy": {
            "name": "ネブリナ",
            "attribute": "林檎輪廻",
            "personality": "穏やか",
            "role": "終焉と再生の感情循環"
        },
        "pair_dynamic": "王が前を向き、妖精が後ろを抱きしめる。",
        "emblem": {
            "motif": "輪廻する林檎と霧環",
            "colors": "深紅＋白",
            "symbol": "再生"
        },
        "world_lines": {
            "封印線": "終焉封",
            "商都線": "港市線",
            "静律線": "霊山静",
            "変革線": "再生変革",
            "境界線": "北海境"
        }
    },
    "岩手": {
        "theme": "静謐と民話の王国",
        "kingdom": "イワティア・ルーン",
        "question": "語られない物語は、消えるのか？",
        "king": {
            "name": "イワティア・ルーン",
            "title": "語守王",
            "personality": "古い物語を重んじる。内省的。",
            "emotion": "深い共感"
        },
        "chief_fairy": {
            "name": "ルーンティア",
            "attribute": "古語・石",
            "personality": "物静かで聡明",
            "role": "土地の物語保存"
        },
        "special_fairy": {
            "name": "イハトヴァ",
            "attribute": "民話",
            "personality": "物静か",
            "role": "土地神話の保存"
        },
        "pair_dynamic": "言葉を共有する静かな同志関係。",
        "emblem": {
            "motif": "石碑と古文様の刻印",
            "colors": "墨黒＋青",
            "symbol": "語り継ぎ"
        },
        "world_lines": {
            "封印線": "古碑封",
            "商都線": "農商圏",
            "静律線": "民話静",
            "変革線": "復興転",
            "境界線": "山境界"
        }
    },
    "宮城": {
        "theme": "灯と復興の王国",
        "kingdom": "ミヤグリア・ルクス",
        "question": "失ったあと、何を灯す？",
        "king": {
            "name": "ミヤグリア・ルクス",
            "title": "灯王",
            "personality": "責任感が強い。自責傾向あり。",
            "emotion": "喪失と再起"
        },
        "chief_fairy": {
            "name": "ルミエラ",
            "attribute": "灯火",
            "personality": "優しくも芯が強い",
            "role": "希望の感情を増幅"
        },
        "special_fairy": {
            "name": "ツキヒカリ",
            "attribute": "復興灯",
            "personality": "芯が強い",
            "role": "再生意志の増幅"
        },
        "pair_dynamic": "王が重さを抱え、妖精が光を差し込む。",
        "emblem": {
            "motif": "灯火と波紋円",
            "colors": "金＋群青",
            "symbol": "復興の光"
        },
        "world_lines": {
            "封印線": "津波封",
            "商都線": "港商都",
            "静律線": "鎮魂静",
            "変革線": "復興革",
            "境界線": "海境"
        }
    },
    "秋田": {
        "theme": "雪と沈黙の王国",
        "kingdom": "アキタリア・ネージュ",
        "question": "沈黙は、逃避か力か？",
        "king": {
            "name": "アキタリア・ネージュ",
            "title": "雪王",
            "personality": "沈黙を尊ぶ。控えめ。",
            "emotion": "孤高"
        },
        "chief_fairy": {
            "name": "ネージュリィ",
            "attribute": "雪",
            "personality": "控えめで誠実",
            "role": "感情の沈静化"
        },
        "special_fairy": {
            "name": "ナマハル",
            "attribute": "仮面",
            "personality": "厳粛",
            "role": "恐れの制御"
        },
        "pair_dynamic": "感情をほぼ表に出さない静寂ペア。",
        "emblem": {
            "motif": "雪結晶と静円",
            "colors": "純白＋淡青",
            "symbol": "沈黙"
        },
        "world_lines": {
            "封印線": "雪封印",
            "商都線": "地方商圏",
            "静律線": "沈黙静",
            "変革線": "農革",
            "境界線": "寒境"
        }
    },
    "山形": {
        "theme": "実りと忍耐の王国",
        "kingdom": "ヤマガリア・フルクト",
        "question": "待つことは、敗北か？",
        "king": {
            "name": "ヤマガリア・フルクト",
            "title": "実王",
            "personality": "努力家。結果より過程重視。",
            "emotion": "穏やかな誇り"
        },
        "chief_fairy": {
            "name": "フルッタ",
            "attribute": "実り",
            "personality": "穏やかで母性的",
            "role": "忍耐の波を保つ"
        },
        "special_fairy": {
            "name": "サクラン",
            "attribute": "花実",
            "personality": "母性的",
            "role": "忍耐の補強"
        },
        "pair_dynamic": "妖精が王を励ます役割。",
        "emblem": {
            "motif": "実りの枝と山影",
            "colors": "朱＋緑",
            "symbol": "忍耐"
        },
        "world_lines": {
            "封印線": "実封印",
            "商都線": "果商圏",
            "静律線": "山静域",
            "変革線": "産革",
            "境界線": "内陸境"
        }
    },
    "福島": {
        "theme": "分断と再起の王国",
        "kingdom": "フクシマル・リボーン",
        "question": "壊れた世界を、再設計できるか？",
        "king": {
            "name": "フクシマル・リボーン",
            "title": "再構王",
            "personality": "葛藤を抱える。強い責任感。",
            "emotion": "悔恨と決意"
        },
        "chief_fairy": {
            "name": "リヴィア",
            "attribute": "再生",
            "personality": "責任感が強い",
            "role": "崩壊後の均衡回復"
        },
        "special_fairy": {
            "name": "ヒバリナ",
            "attribute": "希望鳥",
            "personality": "静かな勇気",
            "role": "再起の兆し拡散"
        },
        "pair_dynamic": "王が自責、妖精が支える。",
        "emblem": {
            "motif": "裂け目を縫う光線",
            "colors": "蒼＋金",
            "symbol": "再構築"
        },
        "world_lines": {
            "封印線": "核封印",
            "商都線": "再生商",
            "静律線": "鎮魂静",
            "変革線": "再構革",
            "境界線": "断層境"
        }
    },
    "茨城": {
        "theme": "境界と実験の王国",
        "kingdom": "イバラキア・フロンティア",
        "question": "境界を越えたとき、何が変わる？",
        "king": {
            "name": "イバラキア・フロンティア",
            "title": "境界王",
            "personality": "挑戦的。未来志向。",
            "emotion": "好奇心"
        },
        "chief_fairy": {
            "name": "フロンティ",
            "attribute": "風",
            "personality": "活発で好奇心旺盛",
            "role": "未来への直感補正"
        },
        "special_fairy": {
            "name": "トネリア",
            "attribute": "大河",
            "personality": "直線的",
            "role": "流れの方向微調整"
        },
        "pair_dynamic": "一緒に未来へ突っ込むコンビ。",
        "emblem": {
            "motif": "境界線を越える矢印円",
            "colors": "深緑＋銀",
            "symbol": "実験"
        },
        "world_lines": {
            "封印線": "実験封",
            "商都線": "流通商",
            "静律線": "筑波静",
            "変革線": "技革",
            "境界線": "川境"
        }
    },
    "栃木": {
        "theme": "霊峰と守護の王国",
        "kingdom": "トチギア・セラフィム",
        "question": "守るべきものは何か？",
        "king": {
            "name": "トチギア・セラフィム",
            "title": "守護王",
            "personality": "規律重視。義務感が強い。",
            "emotion": "忠誠"
        },
        "chief_fairy": {
            "name": "セラフィナ",
            "attribute": "霊峰",
            "personality": "厳格で忠誠心高い",
            "role": "守護結界維持"
        },
        "special_fairy": {
            "name": "ニッコラ",
            "attribute": "霊峰光",
            "personality": "誠実",
            "role": "聖域波動安定"
        },
        "pair_dynamic": "規律重視の軍師的ペア。",
        "emblem": {
            "motif": "霊峰と守護翼",
            "colors": "深紫＋白",
            "symbol": "守護"
        },
        "world_lines": {
            "封印線": "霊峰封",
            "商都線": "観光商",
            "静律線": "神域静",
            "変革線": "幕革",
            "境界線": "山境"
        }
    },
    "群馬": {
        "theme": "風と湯煙の王国",
        "kingdom": "グンマリア・ヴェント",
        "question": "あなたを動かす風は何か？",
        "king": {
            "name": "グンマリア・ヴェント",
            "title": "風王",
            "personality": "自由奔放。即断型。",
            "emotion": "解放感"
        },
        "chief_fairy": {
            "name": "ヴェントラ",
            "attribute": "風・湯気",
            "personality": "自由奔放",
            "role": "気流調整"
        },
        "special_fairy": {
            "name": "オンセンナ",
            "attribute": "湯気精",
            "personality": "自由",
            "role": "地熱圧の緩和"
        },
        "pair_dynamic": "暴走気味だが息は合う。",
        "emblem": {
            "motif": "渦巻く風と湯煙紋",
            "colors": "橙＋灰",
            "symbol": "風"
        },
        "world_lines": {
            "封印線": "地熱封",
            "商都線": "湯商圏",
            "静律線": "高原静",
            "変革線": "維新革",
            "境界線": "山境"
        }
    },
    "埼玉": {
        "theme": "日常と影の王国",
        "kingdom": "サイタマル・アンブラ",
        "question": "平凡の裏に何を見る？",
        "king": {
            "name": "サイタマル・アンブラ",
            "title": "影王",
            "personality": "地味だが芯が強い。",
            "emotion": "隠れた誇り"
        },
        "chief_fairy": {
            "name": "アンブラル",
            "attribute": "影",
            "personality": "控えめだが観察力高い",
            "role": "日常の偶然補正"
        },
        "special_fairy": {
            "name": "カゲミナ",
            "attribute": "日常影",
            "personality": "地味だが鋭い",
            "role": "都市圧の緩衝"
        },
        "pair_dynamic": "目立たないが実務最強。",
        "emblem": {
            "motif": "影円と細光線",
            "colors": "濃紺＋銀",
            "symbol": "影"
        },
        "world_lines": {
            "封印線": "都市封",
            "商都線": "首都商",
            "静律線": "日常静",
            "変革線": "通革",
            "境界線": "平野境"
        }
    },
    "千葉": {
        "theme": "海風と入口の王国",
        "kingdom": "チバリア・ゲート",
        "question": "あなたの入口はどこか？",
        "king": {
            "name": "チバリア・ゲート",
            "title": "門王",
            "personality": "社交的。受容的。",
            "emotion": "歓迎"
        },
        "chief_fairy": {
            "name": "ゲイリア",
            "attribute": "門・潮風",
            "personality": "社交的",
            "role": "出会いの導線微調整"
        },
        "special_fairy": {
            "name": "ウミナリア",
            "attribute": "潮門",
            "personality": "外交的",
            "role": "来訪者エネルギー調整"
        },
        "pair_dynamic": "出会いを作る外交ペア。",
        "emblem": {
            "motif": "開いた門と潮線",
            "colors": "水色＋白",
            "symbol": "入口"
        },
        "world_lines": {
            "封印線": "海門封",
            "商都線": "成田商",
            "静律線": "浜静域",
            "変革線": "物流革",
            "境界線": "海境"
        }
    },
    "東京": {
        "theme": "欲望と加速の王国",
        "kingdom": "トキオニア・アークス",
        "question": "速さは、進化か消耗か？",
        "king": {
            "name": "トキオニア・アークス",
            "title": "加速王",
            "personality": "野心家。効率重視。",
            "emotion": "焦燥"
        },
        "chief_fairy": {
            "name": "アークレア",
            "attribute": "電気・加速",
            "personality": "せっかちで知的",
            "role": "過密感情の分散"
        },
        "special_fairy": {
            "name": "クロノアーク",
            "attribute": "時間加速",
            "personality": "冷静",
            "role": "都市時間歪み補正"
        },
        "pair_dynamic": "王が焦り、妖精がブレーキ役。",
        "emblem": {
            "motif": "加速する三重円",
            "colors": "黒＋金＋赤",
            "symbol": "加速"
        },
        "world_lines": {
            "封印線": "時間封",
            "商都線": "超商都",
            "静律線": "都会静",
            "変革線": "革命革",
            "境界線": "首都境"
        }
    },
    "神奈川": {
        "theme": "港と混交の王国",
        "kingdom": "カナガリア・ノクス",
        "question": "混ざることで何を得る？",
        "king": {
            "name": "カナガリア・ノクス",
            "title": "混交王",
            "personality": "寛容。異文化に強い。",
            "emotion": "柔軟さ"
        },
        "chief_fairy": {
            "name": "ノクシア",
            "attribute": "港・混交",
            "personality": "柔軟で外交的",
            "role": "文化衝突緩和"
        },
        "special_fairy": {
            "name": "ミナトラ",
            "attribute": "港精",
            "personality": "柔軟",
            "role": "文化混合調整"
        },
        "pair_dynamic": "調整力に長けた外交型ペア。",
        "emblem": {
            "motif": "港錨と交差波",
            "colors": "群青＋金",
            "symbol": "混交"
        },
        "world_lines": {
            "封印線": "港封印",
            "商都線": "国際商",
            "静律線": "横静域",
            "変革線": "開港革",
            "境界線": "文化境"
        }
    },
    "新潟": {
        "theme": "余白と豪雪の王国",
        "kingdom": "ニイガリア・アルバ",
        "question": "余白に何を書く？",
        "king": {
            "name": "ニイガリア・アルバ",
            "title": "余白王",
            "personality": "思慮深い。静観型。",
            "emotion": "忍耐"
        },
        "chief_fairy": {
            "name": "アルバナ",
            "attribute": "雪・余白",
            "personality": "忍耐強い",
            "role": "過剰圧の緩和"
        },
        "special_fairy": {
            "name": "コシヒカリス",
            "attribute": "稲穂光",
            "personality": "穏やか",
            "role": "豊穣波安定"
        },
        "pair_dynamic": "沈黙のバランサー。",
        "emblem": {
            "motif": "雪原と余白円",
            "colors": "白＋藍",
            "symbol": "余白"
        },
        "world_lines": {
            "封印線": "雪封印",
            "商都線": "米商圏",
            "静律線": "豪雪静",
            "変革線": "農革",
            "境界線": "海境"
        }
    },
    "富山": {
        "theme": "水脈と透明の王国",
        "kingdom": "トヤマリア・アクア",
        "question": "透明であることは強さか？",
        "king": {
            "name": "トヤマリア・アクア",
            "title": "透明王",
            "personality": "純粋。真実を好む。",
            "emotion": "誠実"
        },
        "chief_fairy": {
            "name": "アクエリス",
            "attribute": "水脈",
            "personality": "透明で純粋",
            "role": "水流均衡"
        },
        "special_fairy": {
            "name": "タテヤミア",
            "attribute": "雪壁",
            "personality": "静寂",
            "role": "水源保護"
        },
        "pair_dynamic": "透明で安定。",
        "emblem": {
            "motif": "水滴と山線",
            "colors": "透明青＋銀",
            "symbol": "透明"
        },
        "world_lines": {
            "封印線": "水源封",
            "商都線": "湾商圏",
            "静律線": "透明静",
            "変革線": "工革",
            "境界線": "山海境"
        }
    },
    "石川": {
        "theme": "美と職人の王国",
        "kingdom": "イシカリア・アルテ",
        "question": "美は、守るものか創るものか？",
        "king": {
            "name": "イシカリア・アルテ",
            "title": "美王",
            "personality": "美意識が高い。職人気質。",
            "emotion": "静かな情熱"
        },
        "chief_fairy": {
            "name": "アルティナ",
            "attribute": "工芸・光",
            "personality": "美意識高い",
            "role": "文化的記憶保全"
        },
        "special_fairy": {
            "name": "カナザリア",
            "attribute": "金箔光",
            "personality": "繊細",
            "role": "美意識振動維持"
        },
        "pair_dynamic": "完璧主義コンビ。",
        "emblem": {
            "motif": "金箔円と職人紋様",
            "colors": "金＋黒",
            "symbol": "美"
        },
        "world_lines": {
            "封印線": "金箔封",
            "商都線": "工芸商",
            "静律線": "雅静域",
            "変革線": "維革",
            "境界線": "北陸境"
        }
    },
    "福井": {
        "theme": "古層と静観の王国",
        "kingdom": "フクイア・ストラタ",
        "question": "古さは、停滞か土台か？",
        "king": {
            "name": "フクイア・ストラタ",
            "title": "層王",
            "personality": "歴史を重視。慎重派。",
            "emotion": "安定志向"
        },
        "chief_fairy": {
            "name": "ストラリス",
            "attribute": "地層",
            "personality": "冷静沈着",
            "role": "地盤安定"
        },
        "special_fairy": {
            "name": "ジュラミア",
            "attribute": "古層",
            "personality": "落ち着き",
            "role": "地質記憶保存"
        },
        "pair_dynamic": "保守的安定ペア。",
        "emblem": {
            "motif": "地層断面と恐竜影",
            "colors": "茶＋緑",
            "symbol": "古層"
        },
        "world_lines": {
            "封印線": "地層封",
            "商都線": "恐商圏",
            "静律線": "古静域",
            "変革線": "地革",
            "境界線": "海山境"
        }
    },
    "山梨": {
        "theme": "霊峰と果実の王国",
        "kingdom": "ヤマナリア・ルミナ",
        "question": "高みを目指す理由は何か？",
        "king": {
            "name": "ヤマナリア・ルミナ",
            "title": "峰王",
            "personality": "理想主義。高み志向。",
            "emotion": "向上心"
        },
        "chief_fairy": {
            "name": "ルミナラ",
            "attribute": "峰・果実",
            "personality": "前向き",
            "role": "火山圧調整"
        },
        "special_fairy": {
            "name": "フジルミナ",
            "attribute": "霊峰精",
            "personality": "気高い",
            "role": "火山波安定"
        },
        "pair_dynamic": "妖精が王を現実に戻す。",
        "emblem": {
            "motif": "霊峰と果実輪",
            "colors": "紫＋金",
            "symbol": "霊峰"
        },
        "world_lines": {
            "封印線": "霊峰封",
            "商都線": "果商圏",
            "静律線": "山静域",
            "変革線": "信革",
            "境界線": "山境"
        }
    },
    "長野": {
        "theme": "高地と内省の王国",
        "kingdom": "ナガノリア・セルフ",
        "question": "あなたは自分と向き合えるか？",
        "king": {
            "name": "ナガノリア・セルフ",
            "title": "内省王",
            "personality": "哲学的。自己探求型。",
            "emotion": "静かな迷い"
        },
        "chief_fairy": {
            "name": "セルフィア",
            "attribute": "高地・風",
            "personality": "内省的",
            "role": "精神波安定"
        },
        "special_fairy": {
            "name": "アルペナ",
            "attribute": "高原風",
            "personality": "哲学的",
            "role": "静寂増幅"
        },
        "pair_dynamic": "深い対話型ペア。",
        "emblem": {
            "motif": "高地風紋と静円",
            "colors": "青＋白",
            "symbol": "内省"
        },
        "world_lines": {
            "封印線": "高地封",
            "商都線": "観商圏",
            "静律線": "内静域",
            "変革線": "思想革",
            "境界線": "山境"
        }
    },
    "岐阜": {
        "theme": "境と調和の王国",
        "kingdom": "ギフリア・バランス",
        "question": "境目でどう立つ？",
        "king": {
            "name": "ギフリア・バランス",
            "title": "均衡王",
            "personality": "調停者。中立的。",
            "emotion": "冷静"
        },
        "chief_fairy": {
            "name": "バラント",
            "attribute": "境界",
            "personality": "調停型",
            "role": "断層緩衝"
        },
        "special_fairy": {
            "name": "ギフリス",
            "attribute": "境界山",
            "personality": "調停型",
            "role": "断層波緩衝"
        },
        "pair_dynamic": "冷静な戦略家ペア。",
        "emblem": {
            "motif": "境界山と均衡線",
            "colors": "深緑＋金",
            "symbol": "均衡"
        },
        "world_lines": {
            "封印線": "境封印",
            "商都線": "山商圏",
            "静律線": "合掌静",
            "変革線": "内革",
            "境界線": "境界山"
        }
    },
    "静岡": {
        "theme": "均衡と富士の王国",
        "kingdom": "スルガリア・エクイノクス",
        "question": "均衡は止まることか？",
        "king": {
            "name": "スルガリア・エクイノクス",
            "title": "均整王",
            "personality": "整合性重視。穏やか。",
            "emotion": "平衡"
        },
        "chief_fairy": {
            "name": "エクイナ",
            "attribute": "均衡",
            "personality": "穏やか",
            "role": "山海エネルギー調整"
        },
        "special_fairy": {
            "name": "スルガミア",
            "attribute": "海富士",
            "personality": "均衡型",
            "role": "山海均整"
        },
        "pair_dynamic": "理想的な安定コンビ。",
        "emblem": {
            "motif": "富士と水平円",
            "colors": "青＋白＋金",
            "symbol": "均衡"
        },
        "world_lines": {
            "封印線": "富士封",
            "商都線": "茶商圏",
            "静律線": "均静域",
            "変革線": "産革",
            "境界線": "海山境"
        }
    },
    "愛知": {
        "theme": "技と実利の王国",
        "kingdom": "アイチア・メカニカ",
        "question": "合理は、心を救うか？",
        "king": {
            "name": "アイチア・メカニカ",
            "title": "機構王",
            "personality": "合理主義。感情抑制型。",
            "emotion": "計算"
        },
        "chief_fairy": {
            "name": "メカリス",
            "attribute": "機構",
            "personality": "合理的",
            "role": "都市振動調整"
        },
        "special_fairy": {
            "name": "テクノリア",
            "attribute": "機構精",
            "personality": "合理的",
            "role": "産業振動安定"
        },
        "pair_dynamic": "感情を最も抑えたペア。",
        "emblem": {
            "motif": "歯車と均整線",
            "colors": "赤＋銀",
            "symbol": "機構"
        },
        "world_lines": {
            "封印線": "機構封",
            "商都線": "製商都",
            "静律線": "合理静",
            "変革線": "工革",
            "境界線": "中部境"
        }
    },
    "三重": {
        "theme": "神域と巡礼の王国",
        "kingdom": "ミエリア・サンクトゥム",
        "question": "祈りは、誰のため？",
        "king": {
            "name": "ミエリア・サンクトゥム",
            "title": "神域王",
            "personality": "厳粛。祈りを尊重。",
            "emotion": "敬意"
        },
        "chief_fairy": {
            "name": "サンクティア",
            "attribute": "祈り",
            "personality": "厳粛",
            "role": "聖域波安定"
        },
        "special_fairy": {
            "name": "イセリア",
            "attribute": "神域",
            "personality": "神聖",
            "role": "巡礼波保護"
        },
        "pair_dynamic": "神域管理ペア。",
        "emblem": {
            "motif": "鳥居と光環",
            "colors": "白＋金",
            "symbol": "神域"
        },
        "world_lines": {
            "封印線": "神域封",
            "商都線": "巡商圏",
            "静律線": "祈静域",
            "変革線": "参革",
            "境界線": "伊勢境"
        }
    },
    "滋賀": {
        "theme": "湖と記憶の王国",
        "kingdom": "オウミリア・メモリア",
        "question": "記憶は流れるか、留まるか？",
        "king": {
            "name": "オウミリア・メモリア",
            "title": "湖王",
            "personality": "記憶重視。懐古的。",
            "emotion": "郷愁"
        },
        "chief_fairy": {
            "name": "メモリアル",
            "attribute": "湖",
            "personality": "優しい",
            "role": "感情沈殿処理"
        },
        "special_fairy": {
            "name": "ビワリア",
            "attribute": "湖精",
            "personality": "優しい",
            "role": "感情沈殿浄化"
        },
        "pair_dynamic": "過去を大切にする。",
        "emblem": {
            "motif": "湖円と波紋層",
            "colors": "青＋水色",
            "symbol": "記憶"
        },
        "world_lines": {
            "封印線": "湖封印",
            "商都線": "湖商圏",
            "静律線": "記静域",
            "変革線": "内革",
            "境界線": "湖境"
        }
    },
    "京都": {
        "theme": "継承と封印の王国",
        "kingdom": "キョウトリア・シール",
        "question": "守ることで、何を閉ざす？",
        "king": {
            "name": "キョウトリア・シール",
            "title": "封印王",
            "personality": "静かで深い。感情を隠す。",
            "emotion": "秘めた愛着"
        },
        "chief_fairy": {
            "name": "シレア",
            "attribute": "封印",
            "personality": "静かで賢い",
            "role": "歴史結界維持"
        },
        "special_fairy": {
            "name": "カグラリス",
            "attribute": "雅",
            "personality": "優雅",
            "role": "歴史波動制御"
        },
        "pair_dynamic": "最も強い結界連携。",
        "emblem": {
            "motif": "封印印章と重円結界",
            "colors": "紫＋金",
            "symbol": "封印"
        },
        "world_lines": {
            "封印線": "王印封",
            "商都線": "雅商圏",
            "静律線": "禅静域",
            "変革線": "維革",
            "境界線": "都境"
        }
    },
    "大阪": {
        "theme": "商魂と笑いの王国",
        "kingdom": "オオサカリア・リベル",
        "question": "笑いは武器か盾か？",
        "king": {
            "name": "オオサカリア・リベル",
            "title": "笑王",
            "personality": "陽気。機転が利く。",
            "emotion": "情熱"
        },
        "chief_fairy": {
            "name": "リベルタ",
            "attribute": "笑い",
            "personality": "明るく大胆",
            "role": "怒気分散"
        },
        "special_fairy": {
            "name": "ナニワラ",
            "attribute": "笑気",
            "personality": "豪快",
            "role": "怒気分散"
        },
        "pair_dynamic": "王が豪快、妖精がさらに煽る。",
        "emblem": {
            "motif": "笑面と商輪",
            "colors": "赤＋金",
            "symbol": "笑い"
        },
        "world_lines": {
            "封印線": "商魂封",
            "商都線": "大商都",
            "静律線": "笑静域",
            "変革線": "経革",
            "境界線": "商境"
        }
    },
    "兵庫": {
        "theme": "港湾と交差の王国",
        "kingdom": "ヒョウゴリア・クロス",
        "question": "交差点で何を選ぶ？",
        "king": {
            "name": "ヒョウゴリア・クロス",
            "title": "交差王",
            "personality": "多面的。二面性あり。",
            "emotion": "葛藤"
        },
        "chief_fairy": {
            "name": "クロッサ",
            "attribute": "交差",
            "personality": "二面性",
            "role": "多層衝突緩和"
        },
        "special_fairy": {
            "name": "コウベリア",
            "attribute": "異国波",
            "personality": "多面的",
            "role": "港湾衝突緩和"
        },
        "pair_dynamic": "常に葛藤しながら最適解を出す。",
        "emblem": {
            "motif": "交差剣と港円",
            "colors": "青＋赤",
            "symbol": "交差"
        },
        "world_lines": {
            "封印線": "港封印",
            "商都線": "湾商圏",
            "静律線": "異静域",
            "変革線": "震革",
            "境界線": "交境"
        }
    },
    "奈良": {
        "theme": "古層と静寂の王国",
        "kingdom": "ナラティア・オリジン",
        "question": "始まりはどこにある？",
        "king": {
            "name": "ナラティア・オリジン",
            "title": "始原王",
            "personality": "古層的。動じない。",
            "emotion": "静寂"
        },
        "chief_fairy": {
            "name": "オリジェラ",
            "attribute": "古層",
            "personality": "穏やか",
            "role": "古代波保存"
        },
        "special_fairy": {
            "name": "ヤマトナ",
            "attribute": "古層鹿",
            "personality": "静寂",
            "role": "古代波保存"
        },
        "pair_dynamic": "静寂の最古ペア。",
        "emblem": {
            "motif": "古木と始原円",
            "colors": "深緑＋金",
            "symbol": "始原"
        },
        "world_lines": {
            "封印線": "古封印",
            "商都線": "鹿商圏",
            "静律線": "始静域",
            "変革線": "律革",
            "境界線": "古境"
        }
    },
    "和歌山": {
        "theme": "聖地と巡礼路の王国",
        "kingdom": "キイリア・パスウェイ",
        "question": "あなたの道は続いているか？",
        "king": {
            "name": "キイリア・パスウェイ",
            "title": "巡礼王",
            "personality": "導く性格。優しい。",
            "emotion": "慈悲"
        },
        "chief_fairy": {
            "name": "パセラ",
            "attribute": "巡礼",
            "personality": "慈悲深い",
            "role": "信仰波安定"
        },
        "special_fairy": {
            "name": "クマノア",
            "attribute": "巡礼道",
            "personality": "慈悲深い",
            "role": "信仰流安定"
        },
        "pair_dynamic": "優しさで支える。",
        "emblem": {
            "motif": "巡礼路と光道",
            "colors": "白＋緑",
            "symbol": "巡礼"
        },
        "world_lines": {
            "封印線": "巡封印",
            "商都線": "梅商圏",
            "静律線": "聖静域",
            "変革線": "修革",
            "境界線": "海山境"
        }
    },
    "鳥取": {
        "theme": "砂丘と孤高の王国",
        "kingdom": "トットリア・デザート",
        "question": "孤独は敵か味方か？",
        "king": {
            "name": "トットリア・デザート",
            "title": "孤砂王",
            "personality": "孤独耐性高い。直線的。",
            "emotion": "自立"
        },
        "chief_fairy": {
            "name": "デザリア",
            "attribute": "砂",
            "personality": "孤高",
            "role": "乾燥波緩和"
        },
        "special_fairy": {
            "name": "サキュリア",
            "attribute": "砂丘",
            "personality": "孤高",
            "role": "乾燥波制御"
        },
        "pair_dynamic": "無駄を削ぎ落とす。",
        "emblem": {
            "motif": "砂丘波と孤円",
            "colors": "砂色＋黒",
            "symbol": "孤高"
        },
        "world_lines": {
            "封印線": "砂封印",
            "商都線": "砂商圏",
            "静律線": "孤静域",
            "変革線": "過革",
            "境界線": "砂境"
        }
    },
    "島根": {
        "theme": "神話と縁の王国",
        "kingdom": "イズモリア・ミスティカ",
        "question": "縁は偶然か必然か？",
        "king": {
            "name": "イズモリア・ミスティカ",
            "title": "縁王",
            "personality": "神秘的。運命思考。",
            "emotion": "深縁"
        },
        "chief_fairy": {
            "name": "ミスティラ",
            "attribute": "神話",
            "personality": "神秘的",
            "role": "縁結び波調整"
        },
        "special_fairy": {
            "name": "イズモナ",
            "attribute": "縁精",
            "personality": "神秘",
            "role": "縁波操作"
        },
        "pair_dynamic": "運命を微調整。",
        "emblem": {
            "motif": "神話勾玉と結環",
            "colors": "紫＋金",
            "symbol": "縁"
        },
        "world_lines": {
            "封印線": "神封印",
            "商都線": "縁商圏",
            "静律線": "神静域",
            "変革線": "古革",
            "境界線": "縁境"
        }
    },
    "岡山": {
        "theme": "晴天と均整の王国",
        "kingdom": "オカヤマリア・クリア",
        "question": "整うことは幸福か？",
        "king": {
            "name": "オカヤマリア・クリア",
            "title": "晴王",
            "personality": "安定志向。安心感。",
            "emotion": "温和"
        },
        "chief_fairy": {
            "name": "クリアナ",
            "attribute": "晴天",
            "personality": "安定型",
            "role": "天候均衡"
        },
        "special_fairy": {
            "name": "ハレリア",
            "attribute": "晴天精",
            "personality": "安定",
            "role": "天候均衡"
        },
        "pair_dynamic": "平和主義コンビ。",
        "emblem": {
            "motif": "晴天光線と安定円",
            "colors": "黄＋青",
            "symbol": "晴天"
        },
        "world_lines": {
            "封印線": "晴封印",
            "商都線": "果商圏",
            "静律線": "安静域",
            "変革線": "桃革",
            "境界線": "山陽境"
        }
    },
    "広島": {
        "theme": "記憶と平和の王国",
        "kingdom": "ヒロシマリア・フェニクス",
        "question": "記憶は未来を救えるか？",
        "king": {
            "name": "ヒロシマリア・フェニクス",
            "title": "記憶王",
            "personality": "重みを背負う。静かな強さ。",
            "emotion": "鎮魂"
        },
        "chief_fairy": {
            "name": "フェニア",
            "attribute": "鎮魂",
            "personality": "静かな強さ",
            "role": "悲哀吸収"
        },
        "special_fairy": {
            "name": "ミヤジマナ",
            "attribute": "厳島波",
            "personality": "静かな強さ",
            "role": "鎮魂増幅"
        },
        "pair_dynamic": "深い理解と再生。",
        "emblem": {
            "motif": "鳳凰と再生火",
            "colors": "赤＋金",
            "symbol": "再生"
        },
        "world_lines": {
            "封印線": "鎮封印",
            "商都線": "湾商圏",
            "静律線": "祈静域",
            "変革線": "平革",
            "境界線": "島境"
        }
    },
    "山口": {
        "theme": "潮流と変革の王国",
        "kingdom": "ヤマグチア・リバース",
        "question": "流れを変える勇気はあるか？",
        "king": {
            "name": "ヤマグチア・リバース",
            "title": "潮流王",
            "personality": "変革志向。大胆。",
            "emotion": "革命性"
        },
        "chief_fairy": {
            "name": "リヴァナ",
            "attribute": "潮流",
            "personality": "大胆",
            "role": "歴史転換波補正"
        },
        "special_fairy": {
            "name": "チョウリュウナ",
            "attribute": "潮流精",
            "personality": "大胆",
            "role": "変革波補正"
        },
        "pair_dynamic": "変化を恐れない。",
        "emblem": {
            "motif": "潮流曲線と変革紋",
            "colors": "藍＋白",
            "symbol": "変革"
        },
        "world_lines": {
            "封印線": "潮封印",
            "商都線": "港商圏",
            "静律線": "静域",
            "変革線": "維革",
            "境界線": "西境"
        }
    },
    "徳島": {
        "theme": "渦と舞の王国",
        "kingdom": "トクシマリア・ヴォルテクス",
        "question": "巻き込まれても立てるか？",
        "king": {
            "name": "トクシマリア・ヴォルテクス",
            "title": "渦王",
            "personality": "躍動型。エネルギッシュ。",
            "emotion": "昂揚"
        },
        "chief_fairy": {
            "name": "ヴォルテラ",
            "attribute": "渦",
            "personality": "躍動的",
            "role": "エネルギー循環制御"
        },
        "special_fairy": {
            "name": "アワナミ",
            "attribute": "舞波",
            "personality": "活発",
            "role": "渦波安定"
        },
        "pair_dynamic": "エネルギー最大級。",
        "emblem": {
            "motif": "渦潮と舞輪",
            "colors": "藍＋白",
            "symbol": "渦"
        },
        "world_lines": {
            "封印線": "渦封印",
            "商都線": "舞商圏",
            "静律線": "踊静域",
            "変革線": "波革",
            "境界線": "海境"
        }
    },
    "香川": {
        "theme": "小島と簡素の王国",
        "kingdom": "カガワリア・ミニマ",
        "question": "少なさは豊かさか？",
        "king": {
            "name": "カガワリア・ミニマ",
            "title": "簡素王",
            "personality": "無駄を嫌う。質素。",
            "emotion": "淡々"
        },
        "chief_fairy": {
            "name": "ミニエル",
            "attribute": "簡素",
            "personality": "静か",
            "role": "無駄波排除"
        },
        "special_fairy": {
            "name": "ウドニア",
            "attribute": "簡素精",
            "personality": "質素",
            "role": "無駄波削減"
        },
        "pair_dynamic": "ミニマルペア。",
        "emblem": {
            "motif": "小島円と簡素線",
            "colors": "白＋青",
            "symbol": "簡素"
        },
        "world_lines": {
            "封印線": "簡封印",
            "商都線": "麺商圏",
            "静律線": "淡静域",
            "変革線": "小革",
            "境界線": "島境"
        }
    },
    "愛媛": {
        "theme": "柑橘と文学の王国",
        "kingdom": "エヒメリア・リリック",
        "question": "言葉は救いになるか？",
        "king": {
            "name": "エヒメリア・リリック",
            "title": "詩王",
            "personality": "言葉を愛する。柔らかい。",
            "emotion": "叙情"
        },
        "chief_fairy": {
            "name": "リリシア",
            "attribute": "詩",
            "personality": "柔らかい",
            "role": "言霊波調整"
        },
        "special_fairy": {
            "name": "ミカナリア",
            "attribute": "柑橘光",
            "personality": "優しい",
            "role": "温暖波維持"
        },
        "pair_dynamic": "言葉を通じて動く。",
        "emblem": {
            "motif": "柑橘輪と詩紋",
            "colors": "橙＋金",
            "symbol": "詩"
        },
        "world_lines": {
            "封印線": "柑封印",
            "商都線": "柑商圏",
            "静律線": "詩静域",
            "変革線": "内革",
            "境界線": "海境"
        }
    },
    "高知": {
        "theme": "奔放と海原の王国",
        "kingdom": "コウチリア・フリーダム",
        "question": "自由とは孤独か？",
        "king": {
            "name": "コウチリア・フリーダム",
            "title": "奔王",
            "personality": "豪胆。自由奔放。",
            "emotion": "直情"
        },
        "chief_fairy": {
            "name": "フリダ",
            "attribute": "奔放",
            "personality": "豪快",
            "role": "海流補正"
        },
        "special_fairy": {
            "name": "カツオラ",
            "attribute": "海豪",
            "personality": "豪胆",
            "role": "海流補正"
        },
        "pair_dynamic": "豪快ペア。",
        "emblem": {
            "motif": "海原線と自由翼",
            "colors": "青＋赤",
            "symbol": "自由"
        },
        "world_lines": {
            "封印線": "海封印",
            "商都線": "鰹商圏",
            "静律線": "奔静域",
            "変革線": "自由革",
            "境界線": "南境"
        }
    },
    "福岡": {
        "theme": "玄関と野心の王国",
        "kingdom": "フクオカリア・ゲートウェイ",
        "question": "外へ出る覚悟はあるか？",
        "king": {
            "name": "フクオカリア・ゲートウェイ",
            "title": "玄関王",
            "personality": "野心的。社交性高い。",
            "emotion": "挑戦心"
        },
        "chief_fairy": {
            "name": "ゲートリア",
            "attribute": "玄関",
            "personality": "野心的",
            "role": "人流バランス"
        },
        "special_fairy": {
            "name": "ハカタリア",
            "attribute": "玄関精",
            "personality": "野心",
            "role": "人流安定"
        },
        "pair_dynamic": "外へ拡張。",
        "emblem": {
            "motif": "門扉と挑戦輪",
            "colors": "黒＋金",
            "symbol": "玄関"
        },
        "world_lines": {
            "封印線": "門封印",
            "商都線": "玄商都",
            "静律線": "都静域",
            "変革線": "拡革",
            "境界線": "九州境"
        }
    },
    "佐賀": {
        "theme": "陶土と静火の王国",
        "kingdom": "サガリア・アンバー",
        "question": "静かな情熱は続くか？",
        "king": {
            "name": "サガリア・アンバー",
            "title": "静火王",
            "personality": "寡黙。内に熱を持つ。",
            "emotion": "持続"
        },
        "chief_fairy": {
            "name": "アンベラ",
            "attribute": "陶土",
            "personality": "寡黙",
            "role": "火圧制御"
        },
        "special_fairy": {
            "name": "アリタナ",
            "attribute": "陶土",
            "personality": "静火",
            "role": "焼成波調整"
        },
        "pair_dynamic": "静かな情熱。",
        "emblem": {
            "motif": "陶紋と火芯円",
            "colors": "琥珀＋黒",
            "symbol": "静火"
        },
        "world_lines": {
            "封印線": "陶封印",
            "商都線": "陶商圏",
            "静律線": "静火域",
            "変革線": "内革",
            "境界線": "筑境"
        }
    },
    "長崎": {
        "theme": "交差と祈りの王国",
        "kingdom": "ナガサキア・クロニクル",
        "question": "痛みは祈りに変わるか？",
        "king": {
            "name": "ナガサキア・クロニクル",
            "title": "祈王",
            "personality": "祈り深い。静かな強さ。",
            "emotion": "赦し"
        },
        "chief_fairy": {
            "name": "クロナ",
            "attribute": "祈り",
            "personality": "優しい",
            "role": "交差波緩衝"
        },
        "special_fairy": {
            "name": "デジマリア",
            "attribute": "交差波",
            "personality": "慈悲",
            "role": "文化緩衝"
        },
        "pair_dynamic": "深い慈悲。",
        "emblem": {
            "motif": "十字光と祈円",
            "colors": "青＋白",
            "symbol": "祈り"
        },
        "world_lines": {
            "封印線": "交封印",
            "商都線": "港商圏",
            "静律線": "祈静域",
            "変革線": "開革",
            "境界線": "国境"
        }
    },
    "熊本": {
        "theme": "城郭と火山の王国",
        "kingdom": "クマモトリア・ヴァルカン",
        "question": "崩れても立てるか？",
        "king": {
            "name": "クマモトリア・ヴァルカン",
            "title": "火山王",
            "personality": "激情型だが理性あり。",
            "emotion": "闘志"
        },
        "chief_fairy": {
            "name": "ヴァルニア",
            "attribute": "火山",
            "personality": "情熱型",
            "role": "噴気圧分散"
        },
        "special_fairy": {
            "name": "アソリア",
            "attribute": "火山精",
            "personality": "力強い",
            "role": "噴気圧分散"
        },
        "pair_dynamic": "熱量最大。",
        "emblem": {
            "motif": "火山と城影",
            "colors": "赤＋黒",
            "symbol": "火山"
        },
        "world_lines": {
            "封印線": "火封印",
            "商都線": "城商圏",
            "静律線": "震静域",
            "変革線": "再革",
            "境界線": "火山境"
        }
    },
    "大分": {
        "theme": "湯煙と癒しの王国",
        "kingdom": "オオイタリア・ミスト",
        "question": "癒しは逃避か再生か？",
        "king": {
            "name": "オオイタリア・ミスト",
            "title": "湯王",
            "personality": "癒し型。包容力。",
            "emotion": "安堵"
        },
        "chief_fairy": {
            "name": "ミスティア",
            "attribute": "湯煙",
            "personality": "癒し型",
            "role": "熱量調整"
        },
        "special_fairy": {
            "name": "ユフリア",
            "attribute": "湯精",
            "personality": "癒し",
            "role": "温泉波安定"
        },
        "pair_dynamic": "包容力。",
        "emblem": {
            "motif": "湯煙と癒光輪",
            "colors": "白＋薄青",
            "symbol": "癒し"
        },
        "world_lines": {
            "封印線": "湯封印",
            "商都線": "湯商圏",
            "静律線": "癒静域",
            "変革線": "温革",
            "境界線": "山海境"
        }
    },
    "宮崎": {
        "theme": "神話と太陽の王国",
        "kingdom": "ヒュウガリア・ソル",
        "question": "光を直視できるか？",
        "king": {
            "name": "ヒュウガリア・ソル",
            "title": "太陽王",
            "personality": "明朗。希望を重視。",
            "emotion": "光"
        },
        "chief_fairy": {
            "name": "ソリア",
            "attribute": "太陽",
            "personality": "明朗",
            "role": "光波増幅"
        },
        "special_fairy": {
            "name": "タカチホナ",
            "attribute": "神話光",
            "personality": "明朗",
            "role": "太陽波増幅"
        },
        "pair_dynamic": "明るさ最大。",
        "emblem": {
            "motif": "太陽円と神話紋",
            "colors": "橙＋金",
            "symbol": "太陽"
        },
        "world_lines": {
            "封印線": "神封印",
            "商都線": "陽商圏",
            "静律線": "光静域",
            "変革線": "日革",
            "境界線": "南境"
        }
    },
    "鹿児島": {
        "theme": "南端と革命の王国",
        "kingdom": "サツマリア・リボルト",
        "question": "変革は破壊か創造か？",
        "king": {
            "name": "サツマリア・リボルト",
            "title": "革命王",
            "personality": "反骨精神。独立志向。",
            "emotion": "覚悟"
        },
        "chief_fairy": {
            "name": "リボルナ",
            "attribute": "革命",
            "personality": "強気",
            "role": "地熱均衡"
        },
        "special_fairy": {
            "name": "サクラジマナ",
            "attribute": "火精",
            "personality": "反骨",
            "role": "地熱均衡"
        },
        "pair_dynamic": "反骨コンビ。",
        "emblem": {
            "motif": "噴火影と革命線",
            "colors": "黒＋赤",
            "symbol": "革命"
        },
        "world_lines": {
            "封印線": "噴封印",
            "商都線": "黒商圏",
            "静律線": "烈静域",
            "変革線": "薩革",
            "境界線": "南端境"
        }
    },
    "沖縄": {
        "theme": "境界と記憶の王国",
        "kingdom": "リュウキュリア・エコー",
        "question": "あなたは何を受け継ぐ？",
        "king": {
            "name": "リュウキュリア・エコー",
            "title": "境界王",
            "personality": "深い記憶を抱える。優雅で強い。",
            "emotion": "継承と哀愁"
        },
        "chief_fairy": {
            "name": "エコラ",
            "attribute": "境界",
            "personality": "優雅で深い",
            "role": "台風波分散"
        },
        "special_fairy": {
            "name": "ウタキナ",
            "attribute": "聖域波",
            "personality": "深い優雅さ",
            "role": "境界波保護"
        },
        "pair_dynamic": "最も感情が深いペア。",
        "emblem": {
            "motif": "境界波と星環",
            "colors": "碧＋紫",
            "symbol": "境界"
        },
        "world_lines": {
            "封印線": "境封印",
            "商都線": "観商圏",
            "静律線": "鎮静域",
            "変革線": "返革",
            "境界線": "海境"
        }
    }
}


def get_prefecture(name):
    """都道府県データを取得"""
    if name in PREFECTURES:
        return PREFECTURES[name]
    return None


def get_world_line_key(pref_name, world_line_value):
    """世界線の値からキーを逆引き"""
    pref = get_prefecture(pref_name)
    if not pref:
        return None
    for key, val in pref["world_lines"].items():
        if val == world_line_value:
            return key
    return None


def list_prefectures():
    """全都道府県名を一覧"""
    return list(PREFECTURES.keys())


if __name__ == "__main__":
    print(f"世界王データベース: {len(PREFECTURES)}都道府県")
    for name in PREFECTURES:
        p = PREFECTURES[name]
        print(f"  {name}: {p['kingdom']} ({p['king']['title']})")
