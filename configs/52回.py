from engine import FontConfig, TextDraw, CheckboxDraw, BoxTextDraw

FONT = FontConfig(
    name="IPAexGothic",
    path="./fonts/ipaexg.ttf",
    subfont_index=0,
)

SIDE_WIDTH = 70
BOX_SIDE_X = 68

BOX_WIDTH = 346
BOX_HEIGHT = 80

MAX_SIZE = 12
MIN_SIZE = 3
SPACE_RATIO = 1.2

FIELDS = [
    # 1ページ目：名前
    TextDraw(page_index=0, csv_key="name", x=260, y=205, font_size=12),

    # 1ページ目：どのように知ったか（チェック）
    CheckboxDraw(
        page_index=0,
        csv_key="how",
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
        page_index=1, csv_key="all",
        x=BOX_SIDE_X, y=515, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：バンド
    BoxTextDraw(
        page_index=1, csv_key="band",
        x=BOX_SIDE_X, y=399, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：ミュージカル
    BoxTextDraw(
        page_index=1, csv_key="musical",
        x=BOX_SIDE_X, y=279, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),

    # 2ページ目：合唱
    BoxTextDraw(
        page_index=1, csv_key="chorus",
        x=BOX_SIDE_X, y=162, box_width=BOX_WIDTH, box_height=BOX_HEIGHT,
        max_font_size=MAX_SIZE, min_font_size=MIN_SIZE, line_spacing_ratio=SPACE_RATIO,
    ),
]
