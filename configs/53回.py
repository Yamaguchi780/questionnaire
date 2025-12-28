from engine import FontConfig, TextDraw, CheckboxDraw, BoxTextDraw

FONT = FontConfig(
    name="IPAexGothic",
    path="./fonts/ipaexg.ttf",
    subfont_index=0,
)

SIDE_WIDTH = 70
BOX_SIDE_X = 68

BOX_WIDTH = 306
BOX_HEIGHT = 74

MAX_SIZE = 12
MIN_SIZE = 3
SPACE_RATIO = 1.2

FIELDS = [
    # 1ページ目：名前
    TextDraw(page_index=0, csv_key="お名前を教えてください", x=260, y=205, font_size=12),

    # 1ページ目：どのように知ったか（チェック）
    CheckboxDraw(
        page_index=0,
        csv_key="本日の演奏会をどのようにしてお知りになりましたか？",
        check_positions={
            "Instagram": (SIDE_WIDTH, 157),
            "X(旧Twitter)": (SIDE_WIDTH, 144),
            "現役生の家族や友人": (SIDE_WIDTH, 131),
            "家族や友人から": (SIDE_WIDTH, 118),
            "メーリングリスト(OBの方)": (SIDE_WIDTH, 105),
            "過去のSlack(OBの方)": (SIDE_WIDTH, 92),
            "その他": (SIDE_WIDTH, 79),
        },
        other_check_key="その他",
        other_text_position=(120, 80),
        separator=",",
    ),

    # 2ページ目：全体
    BoxTextDraw(
        page_index=1,
        csv_key="定期演奏会全体を通して、ご感想やお気づきの点がございましたらご自由にお書きください",
        x=BOX_SIDE_X, y=535, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：第一部
    BoxTextDraw(
        page_index=1,
        csv_key="「第一部 BMC横断プログラム」 について、ご感想やお気づきの点がございましたらご自由にお書きください",
        x=BOX_SIDE_X, y=430, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：第二部
    BoxTextDraw(
        page_index=1,
        csv_key="「第二部 バンド」 について、ご感想やお気づきの点がございましたらご自由にお書きください",
        x=BOX_SIDE_X, y=325, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：
    BoxTextDraw(
        page_index=1,
        csv_key="「第三部 ミュージカル」 について、ご感想やお気づきの点がございましたらご自由にお書きください",
        x=BOX_SIDE_X, y=220, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：第四部
    BoxTextDraw(
        page_index=1,
        csv_key="「第四部 合唱 」について、ご感想やお気づきの点がございましたらご自由にお書きください",
        x=BOX_SIDE_X, y=115, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),
]
