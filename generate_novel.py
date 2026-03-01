# -*- coding: utf-8 -*-
"""
世界王 NovelForge テストモジュール
===================================
入力：都道府県名 + 世界線オプション
出力：5章構成の小説（マークダウン形式）

使い方：
  python generate_novel.py 京都 王印封
  python generate_novel.py 京都           # → 世界線一覧を表示
  python generate_novel.py                # → 都道府県一覧を表示
"""

import sys
import json
from world_kings_data import PREFECTURES, WORLD_SETTING, STORY_TEMPLATE, get_world_line_key


# ============================================================
# 各都道府県の実在スポット・歴史転換点データ
# （NovelForge用の「現実アンカー」素材）
# ============================================================

REAL_ANCHORS = {
    "京都": {
        "spots": ["清水寺", "伏見稲荷大社", "嵐山竹林", "金閣寺", "祇園花見小路"],
        "history": ["応仁の乱（1467）", "明治維新・東京遷都（1868）"],
        "seasons": ["春の桜と哲学の道", "夏の祇園祭", "秋の紅葉と東福寺", "冬の雪化粧の金閣"],
        "local_flavor": ["抹茶", "京町家", "舞妓", "石畳", "鴨川"]
    },
    "北海道": {
        "spots": ["函館山", "小樽運河", "富良野ラベンダー畑", "旭山動物園", "摩周湖"],
        "history": ["蝦夷地開拓（1869）", "五稜郭の戦い（1869）"],
        "seasons": ["春の芝桜", "夏のラベンダー", "秋の大雪山紅葉", "冬の流氷"],
        "local_flavor": ["海鮮", "ジンギスカン", "雪原", "白樺", "アイヌ文化"]
    },
    "東京": {
        "spots": ["浅草寺", "東京タワー", "渋谷スクランブル交差点", "明治神宮", "秋葉原"],
        "history": ["関東大震災（1923）", "東京大空襲（1945）"],
        "seasons": ["春の千鳥ヶ淵", "夏の隅田川花火", "秋の神宮外苑", "冬のイルミネーション"],
        "local_flavor": ["満員電車", "ネオン", "雑踏", "24時間", "加速する時間"]
    },
    "大阪": {
        "spots": ["道頓堀", "大阪城", "通天閣", "新世界", "中之島"],
        "history": ["大坂の陣（1615）", "大阪万博（1970）"],
        "seasons": ["春の造幣局桜通り", "夏の天神祭", "秋の御堂筋", "冬のイルミネーション"],
        "local_flavor": ["たこ焼き", "お笑い", "商人文化", "ド派手看板", "人情"]
    },
    "福島": {
        "spots": ["鶴ヶ城", "磐梯山", "五色沼", "大内宿", "花見山"],
        "history": ["戊辰戦争（1868）", "東日本大震災・原発事故（2011）"],
        "seasons": ["春の花見山", "夏の猪苗代湖", "秋の磐梯山紅葉", "冬の大内宿雪景色"],
        "local_flavor": ["桃", "喜多方ラーメン", "赤べこ", "会津魂", "再生への歩み"]
    },
    "沖縄": {
        "spots": ["首里城", "美ら海水族館", "国際通り", "斎場御嶽", "万座毛"],
        "history": ["琉球王国滅亡（1879）", "沖縄戦（1945）"],
        "seasons": ["春の海開き", "夏の碧い海", "秋の台風", "冬の穏やかな風"],
        "local_flavor": ["三線", "シーサー", "泡盛", "ちんすこう", "御嶽"]
    },
    "広島": {
        "spots": ["厳島神社", "原爆ドーム", "平和記念公園", "尾道", "しまなみ海道"],
        "history": ["原爆投下（1945）", "厳島の戦い（1555）"],
        "seasons": ["春の桜と平和公園", "夏の宮島水中花火", "秋の紅葉谷", "冬の牡蠣"],
        "local_flavor": ["お好み焼き", "もみじ饅頭", "路面電車", "川と橋", "平和の灯"]
    }
}

# デフォルトアンカー（個別データがない県用）
DEFAULT_ANCHORS = {
    "spots": ["県庁所在地の中心部", "地域の代表的神社", "主要な自然スポット"],
    "history": ["明治維新期の転換", "戦後復興"],
    "seasons": ["春", "夏", "秋", "冬"],
    "local_flavor": ["地域の風土", "人々の暮らし", "伝統文化"]
}


# ============================================================
# 世界線別の物語カラーリング
# ============================================================

WORLD_LINE_COLORS = {
    "封印線": {
        "tone": "静謐で不穏。封じられた力が目覚めかける緊張感。",
        "chapter_focus": {
            1: "封印されたものが眠る場所の描写",
            2: "結界の揺らぎ、封印の劣化兆候",
            3: "封印を維持するか解放するかの葛藤",
            4: "妖精が封印の歴史と意味を語る",
            5: "封印を修復する微調整。代償の予感。"
        }
    },
    "商都線": {
        "tone": "活気と欲望。人の流れと金の流れの中に隠れた歪み。",
        "chapter_focus": {
            1: "賑わう商いの場、市場や通りの描写",
            2: "経済や人流の中の微妙な異変",
            3: "人間の欲望と守護のバランスへの葛藤",
            4: "妖精が商いの本質と人の営みを語る",
            5: "人流や偶然を微調整。誰も気づかない。"
        }
    },
    "静律線": {
        "tone": "深い静寂。祈りと内面の世界。最も精神性が高い。",
        "chapter_focus": {
            1: "神社仏閣や聖地の静かな空気",
            2: "祈りのエネルギーの揺らぎ",
            3: "沈黙の中で王が自分自身と対峙",
            4: "妖精が祈りの意味と魂の安定を語る",
            5: "目に見えない精神波の調整。最も静かな結末。"
        }
    },
    "変革線": {
        "tone": "激動。歴史が動く瞬間の裏側。最もドラマチック。",
        "chapter_focus": {
            1: "歴史転換点に関わる場所の現在",
            2: "時代の歪みが現代に影響する兆候",
            3: "変革を促すか止めるかの決断",
            4: "妖精が変革のリスクと必要性を語る",
            5: "歴史の流れを1度だけ曲げる。最も大きな代償。"
        }
    },
    "境界線": {
        "tone": "異文化と出会い。内と外の狭間。哀愁と希望が交差。",
        "chapter_focus": {
            1: "境界に位置する場所——海、山、港、国境",
            2: "外部からの影響による歪み",
            3: "受け入れるか拒むかの選択",
            4: "妖精が出会いと別れの本質を語る",
            5: "文化や人の流れを微調整。静かな邂逅。"
        }
    }
}


# ============================================================
# 小説生成エンジン
# ============================================================

def generate_novel(pref_name, world_line_option=None):
    """
    5章構成の小説を生成する
    
    Args:
        pref_name: 都道府県名（例：京都）
        world_line_option: 世界線オプション（例：王印封）
    
    Returns:
        str: マークダウン形式の5章構成小説
    """
    
    # データ取得
    pref = PREFECTURES.get(pref_name)
    if not pref:
        return f"エラー: '{pref_name}' は登録されていません。"
    
    # 世界線の解決
    if world_line_option:
        wl_key = get_world_line_key(pref_name, world_line_option)
        if not wl_key:
            # 直接キー指定の場合
            if world_line_option in WORLD_LINE_COLORS:
                wl_key = world_line_option
            else:
                available = pref["world_lines"]
                return f"エラー: '{world_line_option}' は無効です。\n利用可能: {json.dumps(available, ensure_ascii=False, indent=2)}"
    else:
        wl_key = "封印線"  # デフォルト
    
    wl_color = WORLD_LINE_COLORS.get(wl_key, WORLD_LINE_COLORS["封印線"])
    wl_value = pref["world_lines"].get(wl_key, "")
    
    # 実在スポットデータ
    anchors = REAL_ANCHORS.get(pref_name, DEFAULT_ANCHORS)
    
    # 王・妖精データ
    king = pref["king"]
    fairy = pref["chief_fairy"]
    special = pref["special_fairy"]
    
    # ============================================================
    # 小説本文の組み立て
    # ============================================================
    
    novel = []
    
    # ヘッダー
    novel.append(f"# 世界王 ── {pref['kingdom']}")
    novel.append(f"## 〈{wl_key}〉{wl_value}")
    novel.append("")
    novel.append(f"**王国テーマ：** {pref['theme']}")
    novel.append(f"**核となる問い：** {pref['question']}")
    novel.append(f"**物語のトーン：** {wl_color['tone']}")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 導入
    novel.append(f"> {STORY_TEMPLATE['opening']}")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 第1章
    ch1 = wl_color["chapter_focus"][1]
    novel.append(f"## 第一章　現実の{pref_name}")
    novel.append("")
    novel.append(f"【場面設定】{ch1}")
    novel.append("")
    novel.append(f"実在スポット候補：{', '.join(anchors['spots'])}")
    novel.append(f"季節素材：{', '.join(anchors['seasons'])}")
    novel.append(f"土地の質感：{', '.join(anchors['local_flavor'])}")
    novel.append("")
    novel.append(f"ここに{pref_name}の現実がある。")
    novel.append(f"観光客の喧噪が遠ざかり、日常が戻る時刻。")
    novel.append(f"しかし{king['title']}・{king['name']}は知っている。")
    novel.append(f"この静けさの下に、地脈の歪みが潜んでいることを。")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 第2章
    ch2 = wl_color["chapter_focus"][2]
    novel.append("## 第二章　歪みの兆候")
    novel.append("")
    novel.append(f"【展開】{ch2}")
    novel.append("")
    novel.append(f"主席妖精・{fairy['name']}（{fairy['attribute']}）が最初に異変を感知した。")
    novel.append(f"「……揺れている」")
    novel.append(f"それは地震ではない。もっと深い層——感情の地脈が軋んでいる。")
    novel.append("")
    novel.append(f"地域特化妖精・{special['name']}（{special['attribute']}）も報告する。")
    novel.append(f"「{special['role']}に異常あり」")
    novel.append("")
    novel.append(f"{king['title']}は静かに目を閉じた。")
    novel.append(f"歪みの正体を、見極めなければならない。")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 第3章
    ch3 = wl_color["chapter_focus"][3]
    novel.append("## 第三章　王の葛藤")
    novel.append("")
    novel.append(f"【内面】{ch3}")
    novel.append("")
    novel.append(f"{king['name']}——{king['personality']}")
    novel.append(f"今、その心に{king['emotion']}が渦巻いている。")
    novel.append("")
    novel.append(f"王の星・レギス・アストラでは感情は「未成熟」とされる。")
    novel.append(f"だがこの国——{pref_name}の{pref['theme']}に触れるたび、")
    novel.append(f"王は自分の中に、名前のつけられない振動を感じている。")
    novel.append("")
    novel.append(f"感情進化レベル：現在推定 2〜3")
    novel.append(f"記録官の監視ログに、小さな警告が灯った。")
    novel.append("")
    novel.append(f"任期残り：あと数年。")
    novel.append(f"その前に——この歪みを、どうする。")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 第4章
    ch4 = wl_color["chapter_focus"][4]
    novel.append("## 第四章　妖精との対話")
    novel.append("")
    novel.append(f"【哲学パート】{ch4}")
    novel.append("")
    novel.append(f"{fairy['name']}は{fairy['personality']}。")
    novel.append(f"王に向かって、静かに言った。")
    novel.append("")
    novel.append(f"「守るって、計算じゃないよ」")
    novel.append("")
    novel.append(f"{king['title']}は答えない。")
    novel.append(f"だが、その沈黙の中に——")
    novel.append(f"レギス・アストラでは決して生まれないはずの、")
    novel.append(f"わずかな震えがあった。")
    novel.append("")
    novel.append(f"ペアダイナミクス：{pref['pair_dynamic']}")
    novel.append("")
    novel.append(f"問いが響く。")
    novel.append(f"「{pref['question']}」")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # 第5章
    ch5 = wl_color["chapter_focus"][5]
    novel.append("## 第五章　微調整と余韻")
    novel.append("")
    novel.append(f"【結末】{ch5}")
    novel.append("")
    novel.append(f"{king['title']}は動いた。")
    novel.append(f"ほんの少し——0.5秒だけ、何かをずらした。")
    novel.append(f"風の向きか。光の角度か。人の足取りか。")
    novel.append("")
    novel.append(f"誰も気づかない。")
    novel.append(f"その「ほんの少し」が、明日の{pref_name}を変えたことに。")
    novel.append("")
    novel.append(f"{king['title']}は独白する。")
    novel.append(f"「また一つ、見えない歪みが消えた」")
    novel.append("")
    novel.append("---")
    novel.append("")
    novel.append(f"> {STORY_TEMPLATE['closing']}")
    novel.append("")
    novel.append("---")
    novel.append("")
    
    # メタデータ
    novel.append("## 📊 生成メタデータ")
    novel.append("")
    novel.append(f"- **都道府県：** {pref_name}")
    novel.append(f"- **王国名：** {pref['kingdom']}")
    novel.append(f"- **世界線：** {wl_key}（{wl_value}）")
    novel.append(f"- **王：** {king['name']}（{king['title']}）")
    novel.append(f"- **主席妖精：** {fairy['name']}（{fairy['attribute']}）")
    novel.append(f"- **地域特化妖精：** {special['name']}（{special['attribute']}）")
    novel.append(f"- **紋章：** {pref['emblem']['motif']}　色：{pref['emblem']['colors']}")
    novel.append(f"- **歴史素材：** {', '.join(anchors.get('history', ['未設定']))}")
    
    return "\n".join(novel)


def generate_novelforge_prompt(pref_name, world_line_option):
    """
    NovelForge用のLLMプロンプトを生成する
    （ローカルAIに投げるための最適化済みプロンプト）
    """
    pref = PREFECTURES.get(pref_name)
    if not pref:
        return f"エラー: '{pref_name}' は登録されていません。"
    
    wl_key = get_world_line_key(pref_name, world_line_option)
    if not wl_key and world_line_option in WORLD_LINE_COLORS:
        wl_key = world_line_option
    
    wl_color = WORLD_LINE_COLORS.get(wl_key, WORLD_LINE_COLORS["封印線"])
    wl_value = pref["world_lines"].get(wl_key, world_line_option)
    
    king = pref["king"]
    fairy = pref["chief_fairy"]
    special = pref["special_fairy"]
    anchors = REAL_ANCHORS.get(pref_name, DEFAULT_ANCHORS)
    
    prompt = f"""あなたは「世界王」プロジェクトの物語作家です。
以下の設定に基づき、5章構成の短編小説（1200〜1500字）を日本語で執筆してください。

# 世界観
{WORLD_SETTING['tagline']}
日本は地震帯という"歪みの列島"。王の星（レギス・アストラ）から47人の王が派遣され、姿を変えて日常に溶け込み、歪みを微調整している。王は災害を消せないが、揺れを1段階緩和し、津波を数秒遅延させ、偶然を微調整できる。王は本来感情を持たないが、日本の感情密度の高さにより感情進化を起こし始める。

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

# 実在素材
- スポット：{', '.join(anchors['spots'])}
- 歴史転換点：{', '.join(anchors.get('history', ['未設定']))}
- 季節：{', '.join(anchors['seasons'])}
- 土地の質感：{', '.join(anchors['local_flavor'])}

# 5章構成（必須）
第一章「現実の{pref_name}」：{wl_color['chapter_focus'][1]}
  実在スポットで始める。季節と時刻を明記。日常の空気感を描写。
第二章「歪みの兆候」：{wl_color['chapter_focus'][2]}
  静かに始まる。妖精が最初に感知する。
第三章「王の葛藤」：{wl_color['chapter_focus'][3]}
  王の内面を深く描く。感情進化の兆候を含める。
第四章「妖精との対話」：{wl_color['chapter_focus'][4]}
  哲学的な会話。核となる問いを自然に組み込む。
第五章「微調整と余韻」：{wl_color['chapter_focus'][5]}
  派手にしない。0.5秒ずらす程度。誰も気づかない。王の独白で締める。

# 文体ルール
- 静か、切ない、誇張しない
- 現実を否定しない、災害を消費しない
- 王はヒーローではなく調整者
- 最初の一文は実在スポットの描写で始める
- 最後は「あなたの町にも、王がいる。」で締める
- 各章は300字前後

# 紋章情報（挿絵プロンプト参考）
紋章：{pref['emblem']['motif']}
色：{pref['emblem']['colors']}
象徴：{pref['emblem']['symbol']}
"""
    return prompt


# ============================================================
# メイン実行
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("世界王 NovelForge テストモジュール")
        print("=" * 60)
        print()
        print("使い方:")
        print("  python generate_novel.py <都道府県名> <世界線オプション>")
        print("  python generate_novel.py 京都 王印封")
        print("  python generate_novel.py 京都        # → 世界線一覧表示")
        print()
        print("登録済み都道府県:")
        for name in PREFECTURES:
            p = PREFECTURES[name]
            print(f"  {name}: {p['kingdom']} ({p['king']['title']})")
        return
    
    pref_name = sys.argv[1]
    
    if pref_name not in PREFECTURES:
        print(f"エラー: '{pref_name}' は登録されていません。")
        return
    
    pref = PREFECTURES[pref_name]
    
    if len(sys.argv) < 3:
        print(f"\n{pref_name}の世界線オプション:")
        print("-" * 40)
        for key, val in pref["world_lines"].items():
            print(f"  {key}: {val}")
        print()
        print(f"例: python generate_novel.py {pref_name} {list(pref['world_lines'].values())[0]}")
        return
    
    world_line_option = sys.argv[2]
    
    # 小説構造を生成
    novel = generate_novel(pref_name, world_line_option)
    
    # ファイル出力
    wl_key = get_world_line_key(pref_name, world_line_option) or world_line_option
    filename = f"novel_{pref_name}_{wl_key}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(novel)
    
    print(f"✅ 小説構造を生成: {filename}")
    print()
    print(novel)
    
    # NovelForge用プロンプトも出力
    prompt = generate_novelforge_prompt(pref_name, world_line_option)
    prompt_filename = f"prompt_{pref_name}_{wl_key}.txt"
    
    with open(prompt_filename, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print()
    print(f"✅ NovelForge用プロンプト: {prompt_filename}")


if __name__ == "__main__":
    main()
