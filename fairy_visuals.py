# -*- coding: utf-8 -*-
"""
世界王 妖精ビジュアルデータベース
==================================
各妖精の SD prompt base（外見固定用タグ）

設計思想：
- 妖精は「人型だが人ではない」 → 半透明・発光・浮遊感
- 主席妖精：ドラマ担当、個性的な外見
- 地域特化妖精：土地の象徴を纏う、やや抽象的
- 共通ルール：
  - 身長は人間より小さめ（140-155cm相当の描写）
  - 瞳に属性色の発光
  - 衣装に紋章モチーフを組み込む
  - 半透明の羽 or 光のオーラ
"""

# ============================================================
# 妖精の共通SDタグ（全妖精に付与）
# ============================================================

FAIRY_COMMON_TAGS = (
    "ethereal being, translucent skin, glowing eyes, "
    "floating particles, soft magical aura, "
    "delicate features, otherworldly beauty, "
    "fantasy illustration, detailed"
)

FAIRY_NEGATIVE_EXTRA = (
    "realistic human, masculine, muscular, "
    "wings like bird, mechanical, robot"
)

# ============================================================
# 全47都道府県 妖精ビジュアル
# ============================================================

FAIRY_VISUALS = {
    "北海道": {
        "chief": {
            "name": "フロストリン",
            "sd_prompt": (
                "1girl, ice fairy, short silver-white hair, ice blue glowing eyes, "
                "pale translucent skin with frost patterns, "
                "white and silver flowing robe with ice crystal ornaments, "
                "snowflake halo above head, bare feet hovering above snow, "
                "cold breath visible, northern lights reflecting on body, "
                "small stature 145cm, serene stoic expression"
            )
        },
        "special": {
            "name": "オーロリア",
            "sd_prompt": (
                "1girl, aurora fairy, long flowing hair shifting green-purple-blue like aurora, "
                "eyes glowing soft green, translucent body with aurora patterns, "
                "gossamer dress made of light ribbons in aurora colors, "
                "floating in dark sky, star particles around her, "
                "vast and lonely expression, ethereal and immense presence"
            )
        }
    },
    "青森": {
        "chief": {
            "name": "ネブラ",
            "sd_prompt": (
                "1girl, mist fairy, wavy silver-lavender hair fading into mist, "
                "pale violet glowing eyes, translucent misty skin, "
                "layered white and pale pink kimono-inspired dress dissolving into fog, "
                "apple blossom petals floating around her, "
                "warm motherly expression despite ghostly appearance, "
                "small stature 148cm, gentle aura"
            )
        },
        "special": {
            "name": "ネブリナ",
            "sd_prompt": (
                "1girl, rebirth fairy, deep red hair like autumn apple, "
                "golden-red glowing eyes, skin with faint ring-shaped patterns, "
                "dress of woven red and white threads cycling in spiral patterns, "
                "holding translucent apple with light core, "
                "peaceful cyclical expression, surrounded by falling petals"
            )
        }
    },
    "岩手": {
        "chief": {
            "name": "ルーンティア",
            "sd_prompt": (
                "1girl, stone rune fairy, dark grey-blue hair in neat braid, "
                "eyes glowing with ancient script characters, grey-blue irises, "
                "robes of dark stone-textured fabric with carved rune patterns, "
                "carrying small glowing stone tablet, "
                "quiet scholarly expression, "
                "small stature 142cm, surrounded by floating ancient letters"
            )
        },
        "special": {
            "name": "イハトヴァ",
            "sd_prompt": (
                "1girl, folklore fairy, brown-green hair with leaf accessories, "
                "warm brown glowing eyes, earthy skin tone, "
                "layered folk dress in forest green and brown with embroidered stories, "
                "small storybook floating beside her, "
                "gentle nostalgic smile, woodland atmosphere"
            )
        }
    },
    "宮城": {
        "chief": {
            "name": "ルミエラ",
            "sd_prompt": (
                "1girl, light fairy, warm golden hair flowing upward like flame, "
                "amber-gold glowing eyes, sun-kissed translucent skin, "
                "white and gold dress with lantern motifs, "
                "holding small eternal flame in cupped hands, "
                "strong yet gentle expression, warm golden aura, "
                "small stature 150cm, light particles rising from feet"
            )
        },
        "special": {
            "name": "ツキヒカリ",
            "sd_prompt": (
                "1girl, reconstruction light fairy, silver-gold gradient hair, "
                "white-gold glowing eyes with determination, "
                "armor-like white dress with wave and light motifs, "
                "beam of light rising behind her, "
                "resolute hopeful expression, standing on water surface"
            )
        }
    },
    "秋田": {
        "chief": {
            "name": "ネージュリィ",
            "sd_prompt": (
                "1girl, snow fairy, pure white short hair, "
                "pale ice-blue glowing eyes, porcelain white skin, "
                "simple white dress with subtle snowflake lace patterns, "
                "minimal accessories, barefoot on snow, "
                "quiet reserved expression, barely visible, "
                "small stature 140cm, almost camouflaged in snow"
            )
        },
        "special": {
            "name": "ナマハル",
            "sd_prompt": (
                "1girl, mask fairy, dark hair partially hidden under ceremonial hood, "
                "red glowing eyes visible through ornate demon-like half mask, "
                "traditional dark robe with straw rope accents, "
                "stern disciplinary aura, fearsome yet protective presence, "
                "ritual atmosphere"
            )
        }
    },
    "山形": {
        "chief": {
            "name": "フルッタ",
            "sd_prompt": (
                "1girl, harvest fairy, warm auburn hair adorned with small fruits, "
                "green-gold glowing eyes, healthy warm skin, "
                "earthy dress in harvest gold and green with fruit embroidery, "
                "gentle motherly smile, cradling glowing seedling, "
                "small stature 148cm, surrounded by floating cherry blossoms and fruits"
            )
        },
        "special": {
            "name": "サクラン",
            "sd_prompt": (
                "1girl, cherry fruit fairy, pink-red gradient hair in twin tails, "
                "ruby red glowing eyes, rosy cheeks, "
                "cute dress decorated with cherry motifs in red and pink, "
                "patient nurturing expression, cherry branch accessory"
            )
        }
    },
    "福島": {
        "chief": {
            "name": "リヴィア",
            "sd_prompt": (
                "1girl, rebirth fairy, dark teal hair with streaks of gold, "
                "teal-gold glowing eyes with intense focus, "
                "structured dress in blue and gold with crack-repair patterns like kintsugi, "
                "golden light seeping through fabric cracks, "
                "serious responsible expression, strong posture, "
                "small stature 152cm, determination aura"
            )
        },
        "special": {
            "name": "ヒバリナ",
            "sd_prompt": (
                "1girl, hope bird fairy, light brown feathered hair swept upward, "
                "sky blue glowing eyes, light airy presence, "
                "wind-swept white and blue dress with feather accents, "
                "small bird perched on shoulder, "
                "quiet brave smile, dawn light behind her"
            )
        }
    },
    "茨城": {
        "chief": {
            "name": "フロンティ",
            "sd_prompt": (
                "1girl, wind frontier fairy, tousled teal-green hair, "
                "bright green glowing eyes full of curiosity, "
                "adventurer-style outfit in green and silver with wind motifs, "
                "goggles pushed up on forehead, "
                "excited adventurous expression, wind swirling around her, "
                "small stature 145cm, dynamic pose"
            )
        },
        "special": {
            "name": "トネリア",
            "sd_prompt": (
                "1girl, great river fairy, long straight blue hair flowing like water, "
                "deep blue glowing eyes, water-like translucent skin, "
                "simple flowing blue dress, river water particles around her, "
                "direct focused expression"
            )
        }
    },
    "栃木": {
        "chief": {
            "name": "セラフィナ",
            "sd_prompt": (
                "1girl, sacred peak fairy, platinum blonde hair in strict updo, "
                "white-gold glowing eyes, porcelain dignified features, "
                "ceremonial white and purple armor-dress with guardian wing motifs, "
                "small shield-like ornament at hip, "
                "stern loyal expression, holy light behind, "
                "small stature 155cm, military bearing"
            )
        },
        "special": {
            "name": "ニッコラ",
            "sd_prompt": (
                "1girl, sacred light fairy, bright gold hair with ornate hairpin, "
                "golden glowing eyes, radiant skin, "
                "shrine maiden inspired white and red outfit with light patterns, "
                "sincere devoted expression, mountain light"
            )
        }
    },
    "群馬": {
        "chief": {
            "name": "ヴェントラ",
            "sd_prompt": (
                "1girl, wind steam fairy, wild orange-red hair blowing in all directions, "
                "orange glowing eyes, lightly flushed warm skin, "
                "loose wild outfit in orange and grey with steam and wind motifs, "
                "steam wisps rising from body, "
                "free spirited grin, dynamic windswept pose, "
                "small stature 143cm, untamed energy"
            )
        },
        "special": {
            "name": "オンセンナ",
            "sd_prompt": (
                "1girl, hot spring fairy, warm pink misty hair, "
                "warm pink glowing eyes, rosy steaming skin, "
                "towel-inspired white wrap dress with steam patterns, "
                "relaxed free expression, steam clouds around her"
            )
        }
    },
    "埼玉": {
        "chief": {
            "name": "アンブラル",
            "sd_prompt": (
                "1girl, shadow fairy, dark navy-black hair blending into shadows, "
                "silver glowing eyes barely visible, pale skin, "
                "dark navy cloak and simple dress almost invisible in dim light, "
                "observing from corner, sharp watchful eyes, "
                "small stature 144cm, easily overlooked but always present"
            )
        },
        "special": {
            "name": "カゲミナ",
            "sd_prompt": (
                "1girl, daily shadow fairy, plain dark brown hair in ponytail, "
                "silver-grey glowing eyes, ordinary appearance, "
                "inconspicuous dark casual outfit, "
                "sharp perceptive expression despite plain looks"
            )
        }
    },
    "千葉": {
        "chief": {
            "name": "ゲイリア",
            "sd_prompt": (
                "1girl, gate fairy, wavy sea-blue hair with shell accessories, "
                "aqua blue glowing eyes, tanned healthy skin, "
                "breezy white and sky blue dress with gate arch motifs, "
                "welcoming open arms gesture, sea breeze around her, "
                "small stature 150cm, warm welcoming smile"
            )
        },
        "special": {
            "name": "ウミナリア",
            "sd_prompt": (
                "1girl, tide gate fairy, flowing ocean blue-green hair, "
                "bright aqua glowing eyes, sea-spray skin, "
                "flowing dress of ocean waves pattern, "
                "diplomatic welcoming expression, ocean horizon behind"
            )
        }
    },
    "東京": {
        "chief": {
            "name": "アークレア",
            "sd_prompt": (
                "1girl, electric acceleration fairy, sharp black hair with neon blue streaks, "
                "electric blue glowing eyes rapidly shifting, "
                "sleek modern black and electric blue outfit with circuit patterns, "
                "data streams flowing around her body, "
                "intense impatient intellectual expression, "
                "small stature 147cm, crackling with electric energy"
            )
        },
        "special": {
            "name": "クロノアーク",
            "sd_prompt": (
                "1girl, time acceleration fairy, silver hair with clock-hand accessories, "
                "white-blue glowing eyes, calm pale features, "
                "structured dark outfit with clock and gear motifs, "
                "cool composed expression, time distortion effect around her"
            )
        }
    },
    "神奈川": {
        "chief": {
            "name": "ノクシア",
            "sd_prompt": (
                "1girl, harbor blend fairy, mixed-texture brown and blonde hair, "
                "warm amber glowing eyes, olive toned skin, "
                "eclectic dress mixing Japanese and Western elements in navy and gold, "
                "port anchor necklace, flexible diplomatic posture, "
                "small stature 149cm, culturally fluid appearance"
            )
        },
        "special": {
            "name": "ミナトラ",
            "sd_prompt": (
                "1girl, port fairy, navy blue hair in neat style, "
                "golden glowing eyes, "
                "naval-inspired blue and white uniform dress with port motifs, "
                "flexible adaptable expression, harbor lights behind"
            )
        }
    },
    "新潟": {
        "chief": {
            "name": "アルバナ",
            "sd_prompt": (
                "1girl, white space fairy, long pure white hair spread wide, "
                "pale blue-white glowing eyes, snow-white translucent skin, "
                "expansive white dress fading into empty space at edges, "
                "patient enduring expression, vast white background, "
                "small stature 146cm, barely distinguishable from white void"
            )
        },
        "special": {
            "name": "コシヒカリス",
            "sd_prompt": (
                "1girl, golden rice fairy, golden blonde hair like rice stalks, "
                "warm gold glowing eyes, sun-warmed skin, "
                "simple dress of golden grain patterns, "
                "gentle peaceful expression, golden light, rice paddies"
            )
        }
    },
    "富山": {
        "chief": {
            "name": "アクエリス",
            "sd_prompt": (
                "1girl, water vein fairy, crystal clear blue hair like pure water, "
                "transparent blue glowing eyes, glass-clear translucent skin, "
                "flowing dress of pure water fabric completely transparent, "
                "water droplet crown, pristine sincere expression, "
                "small stature 144cm, almost invisible like pure water"
            )
        },
        "special": {
            "name": "タテヤミア",
            "sd_prompt": (
                "1girl, snow wall fairy, white-blue frosted hair, "
                "ice-crystal blue glowing eyes, frost-covered skin, "
                "heavy winter white robes like snow walls, "
                "silent guarding expression, mountain snow backdrop"
            )
        }
    },
    "石川": {
        "chief": {
            "name": "アルティナ",
            "sd_prompt": (
                "1girl, craft beauty fairy, elegant black hair with gold leaf flakes, "
                "gold glowing eyes with artistic depth, refined porcelain skin, "
                "exquisite kimono-inspired dress with gold leaf and lacquer patterns, "
                "carrying delicate golden craft tool, "
                "perfectionist discerning expression, "
                "small stature 148cm, impeccable grooming"
            )
        },
        "special": {
            "name": "カナザリア",
            "sd_prompt": (
                "1girl, gold leaf fairy, shimmering gold hair, "
                "rich gold glowing eyes, golden-dusted skin, "
                "dress layered with actual gold leaf textures, "
                "delicate precise expression, gold particles floating"
            )
        }
    },
    "福井": {
        "chief": {
            "name": "ストラリス",
            "sd_prompt": (
                "1girl, geological layer fairy, layered brown-grey gradient hair, "
                "earthy amber glowing eyes, stone-textured skin, "
                "dress with visible geological strata layers in earth tones, "
                "fossil imprints on fabric, calm composed expression, "
                "small stature 150cm, ancient grounded presence"
            )
        },
        "special": {
            "name": "ジュラミア",
            "sd_prompt": (
                "1girl, ancient layer fairy, dark earth-toned hair with fossil ornaments, "
                "deep amber glowing eyes, weathered stone-like skin, "
                "heavy robes with dinosaur fossil patterns, "
                "patient ancient expression, surrounded by stone particles"
            )
        }
    },
    "山梨": {
        "chief": {
            "name": "ルミナラ",
            "sd_prompt": (
                "1girl, peak fruit fairy, bright purple-red hair adorned with grape and peach, "
                "vivid purple glowing eyes looking upward, radiant skin, "
                "elegant dress in purple and gold with mountain and fruit motifs, "
                "always looking toward summit, optimistic expression, "
                "small stature 147cm, Mt Fuji silhouette behind"
            )
        },
        "special": {
            "name": "フジルミナ",
            "sd_prompt": (
                "1girl, sacred peak fairy, white-violet gradient hair rising like mountain, "
                "violet glowing eyes, noble dignified features, "
                "ceremonial white and purple robes with Fuji motifs, "
                "noble proud expression, volcanic energy aura"
            )
        }
    },
    "長野": {
        "chief": {
            "name": "セルフィア",
            "sd_prompt": (
                "1girl, highland introspection fairy, silver-blue hair in contemplative style, "
                "deep blue glowing eyes turned inward, pale thoughtful features, "
                "simple blue and white mountain dress with wind motifs, "
                "sitting in meditation pose, philosophical expression, "
                "small stature 143cm, mountain breeze effect"
            )
        },
        "special": {
            "name": "アルペナ",
            "sd_prompt": (
                "1girl, alpine wind fairy, windswept light blue hair, "
                "clear sky-blue glowing eyes, fresh highland complexion, "
                "airy white dress with mountain wind patterns, "
                "deep contemplative expression, high altitude atmosphere"
            )
        }
    },
    "岐阜": {
        "chief": {
            "name": "バラント",
            "sd_prompt": (
                "1girl, balance boundary fairy, half dark half light split hair, "
                "one eye gold one eye silver glowing, balanced symmetrical face, "
                "dress split in contrasting colors with boundary line pattern, "
                "mediator pose with open palms, calm neutral expression, "
                "small stature 150cm, perfectly balanced stance"
            )
        },
        "special": {
            "name": "ギフリス",
            "sd_prompt": (
                "1girl, mountain boundary fairy, dark green and brown split hair, "
                "earth-gold glowing eyes, weathered but balanced features, "
                "mountain-pattern robes in mixed earth tones, "
                "diplomatic calm expression, mountain pass backdrop"
            )
        }
    },
    "静岡": {
        "chief": {
            "name": "エクイナ",
            "sd_prompt": (
                "1girl, equilibrium fairy, perfectly balanced teal hair at shoulder length, "
                "serene teal glowing eyes, harmonious features, "
                "balanced blue-white-gold dress with wave and mountain motifs, "
                "peaceful centered expression, Mt Fuji and ocean horizon, "
                "small stature 148cm, absolute calm aura"
            )
        },
        "special": {
            "name": "スルガミア",
            "sd_prompt": (
                "1girl, sea-mountain fairy, blue-white gradient hair, "
                "blue-green glowing eyes, "
                "dress combining ocean wave bottom and mountain peak top, "
                "balanced harmonious expression, sea and mountain landscape"
            )
        }
    },
    "愛知": {
        "chief": {
            "name": "メカリス",
            "sd_prompt": (
                "1girl, mechanism fairy, sharp geometric black hair with silver accents, "
                "analytical silver glowing eyes, precise features, "
                "structured dark outfit with visible gear and mechanism patterns, "
                "small holographic display near hand, "
                "calculating efficient expression, "
                "small stature 149cm, precise controlled movements"
            )
        },
        "special": {
            "name": "テクノリア",
            "sd_prompt": (
                "1girl, tech mechanism fairy, metallic silver-black hair, "
                "red-silver glowing eyes, mechanical precision features, "
                "industrial-design outfit with gear motifs, "
                "analytical cold expression, factory-light backdrop"
            )
        }
    },
    "三重": {
        "chief": {
            "name": "サンクティア",
            "sd_prompt": (
                "1girl, sacred domain fairy, long straight white hair with gold tips, "
                "pure white-gold glowing eyes, immaculate pale skin, "
                "pristine white shrine maiden inspired dress with golden rope accents, "
                "prayer beads at wrist, solemn reverent expression, "
                "small stature 146cm, sacred light aura, torii gate silhouette"
            )
        },
        "special": {
            "name": "イセリア",
            "sd_prompt": (
                "1girl, sacred precinct fairy, pure white hair with golden sheen, "
                "divine gold glowing eyes, luminous sacred skin, "
                "elaborate white ceremonial robes with shrine motifs, "
                "holy dignified expression, divine light pillar"
            )
        }
    },
    "滋賀": {
        "chief": {
            "name": "メモリアル",
            "sd_prompt": (
                "1girl, lake memory fairy, long flowing blue-green hair like lake water, "
                "deep blue glowing eyes holding old memories, gentle aged wisdom face, "
                "flowing dress in lake blue-green with ripple patterns, "
                "holding translucent memory orb, nostalgic gentle expression, "
                "small stature 145cm, lake surface reflection"
            )
        },
        "special": {
            "name": "ビワリア",
            "sd_prompt": (
                "1girl, great lake fairy, deep blue-green long hair, "
                "deep lake-blue glowing eyes, water-clear gentle features, "
                "flowing layered dress in lake water colors with sediment patterns, "
                "kind gentle expression, vast lake behind"
            )
        }
    },
    "京都": {
        "chief": {
            "name": "シレア",
            "sd_prompt": (
                "1girl, seal barrier fairy, long straight midnight purple hair with gold hairpin, "
                "deep violet glowing eyes with ancient wisdom, pale elegant features, "
                "layered dark purple and gold kimono-dress with seal circle patterns, "
                "glowing seal mark on forehead, barrier hexagon particles floating, "
                "quiet intelligent expression, composed posture, "
                "small stature 150cm, purple-gold magical aura"
            )
        },
        "special": {
            "name": "カグラリス",
            "sd_prompt": (
                "1girl, sacred dance fairy, elegant black hair in traditional updo with ornate kanzashi, "
                "deep gold glowing eyes, refined porcelain skin, "
                "ornate layered kimono in deep red and gold with wave-circle patterns, "
                "fan in hand, graceful dance pose, "
                "dignified elegant expression, cherry blossom petals, shrine backdrop"
            )
        }
    },
    "大阪": {
        "chief": {
            "name": "リベルタ",
            "sd_prompt": (
                "1girl, laughter fairy, wild spiky orange-red hair, "
                "bright amber-gold glowing eyes sparkling with mischief, warm tanned skin, "
                "bold red and gold street-style outfit with tiger and merchant motifs, "
                "wide confident grin, arms spread dramatically, "
                "small stature 148cm, infectious golden energy radiating"
            )
        },
        "special": {
            "name": "ナニワラ",
            "sd_prompt": (
                "1girl, naniwa laughing fairy, bold red spiky hair, "
                "fiery gold glowing eyes, energetic tanned skin, "
                "flashy red and gold outfit with comedy mask motifs, "
                "boisterous laughing expression, neon lights backdrop"
            )
        }
    },
    "兵庫": {
        "chief": {
            "name": "クロッサ",
            "sd_prompt": (
                "1girl, crossroads fairy, asymmetric half-red half-blue hair, "
                "one eye red one eye blue glowing, contrasting dual features, "
                "dress split between eastern and western styles in red and blue, "
                "standing at crossroads, conflicted but resolute expression, "
                "small stature 151cm, two-toned aura"
            )
        },
        "special": {
            "name": "コウベリア",
            "sd_prompt": (
                "1girl, foreign wave fairy, wavy brown hair with exotic accessories, "
                "warm dual-tone glowing eyes, multicultural features, "
                "fusion dress mixing Japanese and Western port town elements, "
                "adaptable knowing expression, port city lights"
            )
        }
    },
    "奈良": {
        "chief": {
            "name": "オリジェラ",
            "sd_prompt": (
                "1girl, origin layer fairy, long straight dark brown hair to waist, "
                "deep amber glowing eyes ancient beyond time, serene ageless face, "
                "ancient-style simple earth-toned robes with spiral origin patterns, "
                "sitting motionless under ancient tree, unmoved peaceful expression, "
                "small stature 142cm, deer nearby, oldest most patient presence"
            )
        },
        "special": {
            "name": "ヤマトナ",
            "sd_prompt": (
                "1girl, ancient deer fairy, warm brown hair with antler-like ornaments, "
                "deep ancient amber glowing eyes, timeless serene features, "
                "earth-toned ancient robes with deer and temple patterns, "
                "absolute stillness expression, ancient temple backdrop, deer"
            )
        }
    },
    "和歌山": {
        "chief": {
            "name": "パセラ",
            "sd_prompt": (
                "1girl, pilgrimage path fairy, long white-green hair flowing like path, "
                "gentle green glowing eyes full of compassion, warm kind features, "
                "pilgrim-style white and green robes with path and forest motifs, "
                "carrying walking staff with light, guiding gentle expression, "
                "small stature 146cm, forest path light, ancient cedar trees"
            )
        },
        "special": {
            "name": "クマノア",
            "sd_prompt": (
                "1girl, pilgrimage road fairy, deep green long hair with vine-like strands, "
                "forest green glowing eyes, nature-blended features, "
                "flowing green robes with mountain path patterns, "
                "compassionate guiding expression, ancient forest road"
            )
        }
    },
    "鳥取": {
        "chief": {
            "name": "デザリア",
            "sd_prompt": (
                "1girl, sand desert fairy, short sandy blonde hair wind-dried, "
                "amber glowing eyes squinting against sand, weathered tan skin, "
                "minimal sand-colored wrap with dune wave patterns, "
                "standing alone in vast emptiness, self-reliant expression, "
                "small stature 140cm, sand particles around, lone figure"
            )
        },
        "special": {
            "name": "サキュリア",
            "sd_prompt": (
                "1girl, sand dune fairy, wind-swept sand-gold hair, "
                "golden-amber glowing eyes, sandy weathered skin, "
                "minimal desert wraps in sand colors, "
                "stoic independent expression, vast sand dunes"
            )
        }
    },
    "島根": {
        "chief": {
            "name": "ミスティラ",
            "sd_prompt": (
                "1girl, mythical destiny fairy, long dark purple hair with magatama ornaments, "
                "mystic purple glowing eyes seeing fate threads, mysterious pale features, "
                "elaborate dark purple shrine-style dress with red cord patterns, "
                "red fate strings visible between fingers, "
                "enigmatic knowing expression, "
                "small stature 147cm, destiny threads and magatama floating"
            )
        },
        "special": {
            "name": "イズモナ",
            "sd_prompt": (
                "1girl, bond destiny fairy, deep purple-red hair with shimenawa rope, "
                "mystic red-purple glowing eyes, otherworldly features, "
                "shrine maiden style dark dress with bond/thread patterns, "
                "mysterious connection expression, shrine twilight"
            )
        }
    },
    "岡山": {
        "chief": {
            "name": "クリアナ",
            "sd_prompt": (
                "1girl, clear sky fairy, bright sunny yellow hair, "
                "clear sky-blue glowing eyes, healthy sun-bright skin, "
                "cheerful yellow and blue dress with sun and peach motifs, "
                "reassuring warm smile, blue sky background, "
                "small stature 148cm, perpetually sunny aura"
            )
        },
        "special": {
            "name": "ハレリア",
            "sd_prompt": (
                "1girl, fair weather fairy, golden-yellow hair, "
                "bright clear blue glowing eyes, healthy sunny features, "
                "simple sunny yellow dress with clear sky patterns, "
                "stable reassuring expression, endless blue sky"
            )
        }
    },
    "広島": {
        "chief": {
            "name": "フェニア",
            "sd_prompt": (
                "1girl, phoenix memorial fairy, deep red gradient to black hair, "
                "solemn red-gold glowing eyes, strong but gentle features, "
                "dark red and gold dress with phoenix and flame renewal patterns, "
                "eternal flame hovering in palm, "
                "quietly powerful expression bearing weight of memory, "
                "small stature 152cm, memorial light, peace"
            )
        },
        "special": {
            "name": "ミヤジマナ",
            "sd_prompt": (
                "1girl, island shrine fairy, deep crimson hair, "
                "solemn golden glowing eyes, strong sacred features, "
                "red shrine maiden robes with torii and wave patterns, "
                "quiet strength expression, floating torii gate, sea"
            )
        }
    },
    "山口": {
        "chief": {
            "name": "リヴァナ",
            "sd_prompt": (
                "1girl, tide change fairy, wild dark blue-black hair flowing like current, "
                "fierce teal glowing eyes, strong determined features, "
                "bold dark outfit with tide current and revolution motifs, "
                "standing against strong wind, daring fearless expression, "
                "small stature 153cm, ocean current energy swirling"
            )
        },
        "special": {
            "name": "チョウリュウナ",
            "sd_prompt": (
                "1girl, tidal current fairy, flowing dark blue hair like ocean stream, "
                "intense teal glowing eyes, bold strong features, "
                "dynamic dark outfit with current and change motifs, "
                "bold revolutionary expression, powerful waves"
            )
        }
    },
    "徳島": {
        "chief": {
            "name": "ヴォルテラ",
            "sd_prompt": (
                "1girl, vortex dance fairy, spiraling indigo-blue hair in motion, "
                "bright indigo glowing eyes spinning with energy, vivid animated features, "
                "dynamic dance outfit in indigo and white with whirlpool patterns, "
                "caught mid-dance spin, exhilarated expression, "
                "small stature 146cm, whirlpool energy around feet"
            )
        },
        "special": {
            "name": "アワナミ",
            "sd_prompt": (
                "1girl, dance wave fairy, flowing blue-white hair in spiral, "
                "bright blue glowing eyes, energetic features, "
                "festival dance outfit in indigo and white, "
                "joyful dancing expression, whirlpool waves"
            )
        }
    },
    "香川": {
        "chief": {
            "name": "ミニエル",
            "sd_prompt": (
                "1girl, minimal island fairy, short neat white-grey hair, "
                "quiet grey-blue glowing eyes, clean simple features, "
                "minimalist white dress with single blue accent line, "
                "no unnecessary accessories, still quiet expression, "
                "small stature 138cm, smallest fairy, island in background"
            )
        },
        "special": {
            "name": "ウドニア",
            "sd_prompt": (
                "1girl, simplicity fairy, plain straight light grey hair, "
                "soft grey glowing eyes, clean minimal features, "
                "extremely simple white dress one piece, "
                "quietly content expression, zen minimalism"
            )
        }
    },
    "愛媛": {
        "chief": {
            "name": "リリシア",
            "sd_prompt": (
                "1girl, lyric poetry fairy, soft wavy orange-blonde hair with flower, "
                "warm amber glowing eyes with poetic depth, soft gentle features, "
                "flowing orange and cream dress with literary patterns and citrus motifs, "
                "holding small glowing book of poetry, wistful lyrical expression, "
                "small stature 145cm, floating letters and orange blossoms"
            )
        },
        "special": {
            "name": "ミカナリア",
            "sd_prompt": (
                "1girl, citrus light fairy, bright orange hair, "
                "warm orange glowing eyes, sunny warm features, "
                "bright orange dress with mandarin orange patterns, "
                "gentle warm expression, citrus grove light"
            )
        }
    },
    "高知": {
        "chief": {
            "name": "フリダ",
            "sd_prompt": (
                "1girl, freedom ocean fairy, wild untamed dark blue-green hair, "
                "fierce ocean-blue glowing eyes, strong tanned features, "
                "rugged ocean-style outfit in blue and red torn edges, "
                "standing on wave crest, bold fearless grin, "
                "small stature 152cm, ocean spray and wild wind"
            )
        },
        "special": {
            "name": "カツオラ",
            "sd_prompt": (
                "1girl, ocean bold fairy, short wild dark blue hair, "
                "intense blue glowing eyes, deeply tanned strong features, "
                "bold seafaring outfit in blue and red, "
                "fearless wild grin, massive ocean waves"
            )
        }
    },
    "福岡": {
        "chief": {
            "name": "ゲートリア",
            "sd_prompt": (
                "1girl, gateway ambition fairy, sharp styled black-gold hair, "
                "ambitious gold glowing eyes, confident sharp features, "
                "sleek black and gold outfit with gate and challenge motifs, "
                "bold confident stance looking outward, "
                "small stature 151cm, gateway light, city skyline"
            )
        },
        "special": {
            "name": "ハカタリア",
            "sd_prompt": (
                "1girl, hakata gate fairy, slicked back black hair with gold accent, "
                "blazing gold glowing eyes, confident sharp features, "
                "bold black and gold outfit with gate motifs, "
                "ambitious forward expression, city lights"
            )
        }
    },
    "佐賀": {
        "chief": {
            "name": "アンベラ",
            "sd_prompt": (
                "1girl, clay quiet fire fairy, earthy red-brown hair in simple style, "
                "deep amber glowing eyes with hidden heat, quiet warm features, "
                "pottery-textured earthy dress in amber and dark brown with kiln patterns, "
                "hands with clay-like texture, quiet burning patience expression, "
                "small stature 144cm, kiln ember glow"
            )
        },
        "special": {
            "name": "アリタナ",
            "sd_prompt": (
                "1girl, porcelain fire fairy, white-blue porcelain-like hair, "
                "deep kiln-orange glowing eyes, porcelain smooth skin, "
                "outfit decorated with blue-and-white Arita pottery patterns, "
                "patient intense expression, kiln fire glow"
            )
        }
    },
    "長崎": {
        "chief": {
            "name": "クロナ",
            "sd_prompt": (
                "1girl, prayer crossing fairy, long wavy brown hair with cross hairpin, "
                "gentle blue-gold glowing eyes, soft compassionate features, "
                "blend of Japanese and European style dress in blue and white with stained glass patterns, "
                "hands clasped in prayer, merciful gentle expression, "
                "small stature 147cm, stained glass light, church and temple blend"
            )
        },
        "special": {
            "name": "デジマリア",
            "sd_prompt": (
                "1girl, cultural bridge fairy, mixed brown-blonde wavy hair, "
                "warm blue-amber glowing eyes, mixed heritage features, "
                "Dutch-Japanese fusion dress with trade route patterns, "
                "compassionate bridging expression, harbor exotic lights"
            )
        }
    },
    "熊本": {
        "chief": {
            "name": "ヴァルニア",
            "sd_prompt": (
                "1girl, volcanic passion fairy, wild spiked red-black hair like lava, "
                "blazing red-orange glowing eyes, fierce warm skin with magma vein patterns, "
                "bold red and black armor-dress with volcanic crack patterns, "
                "fist clenched, passionate determined expression, "
                "small stature 154cm, volcanic heat haze, ash particles"
            )
        },
        "special": {
            "name": "アソリア",
            "sd_prompt": (
                "1girl, Aso volcanic fairy, dark red-black wild hair, "
                "intense red glowing eyes, powerful fierce features, "
                "volcanic rock-textured outfit in red and black, "
                "powerful roaring expression, volcanic smoke and fire"
            )
        }
    },
    "大分": {
        "chief": {
            "name": "ミスティア",
            "sd_prompt": (
                "1girl, hot spring mist fairy, soft white-pink misty hair, "
                "warm pink glowing eyes, dewy soft skin, "
                "soft white and light blue flowing robe like steam, "
                "surrounded by warm mist, nurturing peaceful expression, "
                "small stature 145cm, hot spring steam everywhere"
            )
        },
        "special": {
            "name": "ユフリア",
            "sd_prompt": (
                "1girl, Yufuin spring fairy, soft white misty hair, "
                "warm rose glowing eyes, dewy gentle features, "
                "light flowing dress dissolving into steam, "
                "healing peaceful expression, hot spring mist, mountain"
            )
        }
    },
    "宮崎": {
        "chief": {
            "name": "ソリア",
            "sd_prompt": (
                "1girl, solar mythology fairy, bright golden-orange hair like sunbeams, "
                "blazing golden glowing eyes, radiant sun-bright skin, "
                "brilliant white and gold dress with sun disc and mythical patterns, "
                "arms spread receiving sunlight, bright hopeful expression, "
                "small stature 149cm, brilliant sunlight, divine rays"
            )
        },
        "special": {
            "name": "タカチホナ",
            "sd_prompt": (
                "1girl, mythical light fairy, radiant gold hair, "
                "divine golden glowing eyes, luminous sacred features, "
                "white ceremonial robes with heavenly descent motifs, "
                "radiant joyful expression, divine light from above, sacred gorge"
            )
        }
    },
    "鹿児島": {
        "chief": {
            "name": "リボルナ",
            "sd_prompt": (
                "1girl, revolution fairy, fierce short black hair with red streaks, "
                "burning red glowing eyes, strong defiant features, "
                "dark revolutionary outfit in black and red with volcanic ash patterns, "
                "standing against wind, rebellious determined expression, "
                "small stature 153cm, volcanic ash and fire behind"
            )
        },
        "special": {
            "name": "サクラジマナ",
            "sd_prompt": (
                "1girl, Sakurajima fire fairy, ash-grey hair with glowing red tips, "
                "volcanic red glowing eyes, ash-dusted fierce features, "
                "dark volcanic outfit with eruption patterns, "
                "defiant rebel expression, erupting volcano silhouette"
            )
        }
    },
    "沖縄": {
        "chief": {
            "name": "エコラ",
            "sd_prompt": (
                "1girl, boundary echo fairy, long flowing turquoise-blue hair with coral ornaments, "
                "deep sea-blue glowing eyes holding ancient memories, elegant strong features, "
                "flowing turquoise and purple dress with ocean wave and star map patterns, "
                "shell and coral accessories, dignified melancholic grace, "
                "small stature 148cm, ocean horizon, starry sky, coral reef"
            )
        },
        "special": {
            "name": "ウタキナ",
            "sd_prompt": (
                "1girl, sacred grove fairy, deep green-black hair with white flower, "
                "deep emerald glowing eyes with spiritual depth, solemn sacred features, "
                "traditional white robes with Ryukyu patterns and sacred tree motifs, "
                "hands together in prayer at sacred site, "
                "deeply spiritual expression, sacred grove, spiritual light"
            )
        }
    },
}


def get_fairy_prompt(pref_name: str, fairy_type: str = "chief") -> str:
    """
    妖精のSDプロンプトを取得
    
    Args:
        pref_name: 都道府県名
        fairy_type: "chief"（主席妖精）or "special"（地域特化妖精）
    
    Returns:
        SD prompt string with common tags appended
    """
    visuals = FAIRY_VISUALS.get(pref_name, {})
    fairy = visuals.get(fairy_type, {})
    base = fairy.get("sd_prompt", "")
    
    if not base:
        return ""
    
    return f"{base}, {FAIRY_COMMON_TAGS}"


def get_fairy_negative_extra() -> str:
    """妖精用の追加ネガティブプロンプト"""
    return FAIRY_NEGATIVE_EXTRA
