# このパッケージがバージョンによって上手くいかないっぽい
# 2024/12/23の時点で「pip install "PyPDF2==2.9.7"」で正常に動くことを確認
# 上手くいかない場合はターミナルで「pip install "PyPDF2==2.9.7"」を実行してみるとよい
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd

# スプレッドシートからCSVファイルをダウンロードし、「回答.csv」としてこのディレクトリに保存して下さい
# csvファイルの1行目には質問のラベルが入っています。これがkeyとなるので「timeStamp,mailAddress,name,how,all,band,musical,chorus」のように適宜修正して下さい
# 白紙のアンケート用紙をこのディレクトリに「定期演奏会アンケート.pdf」として保存して下さい
# can1.drawString(x, y, "✓")など、書き込む箇所について座標を適宜修正して下さい。（単位はポイント、原点は左下です）
# あまりにも文字数や改行箇所がおいと上手くいかないので、改行を無視する処理や高さや幅のの制限を取り払うなどの実装を適宜して下さい
# 回答がまとめられたpdfがこのディレクトリに「まとめたアンケート.pdf」として保存されます
# 特殊文字には対応していません
# 普段 Pythonを使ってないと環境構築などが難しいと思うので 66期 capか周りの詳しい人までお問い合わせを


# 日本語フォントの登録
pdfmetrics.registerFont(TTFont("IPAexGothic", "./fonts/ipaexg.ttf", subfontIndex=0))

sideWidth = 70
max_size = 12
min_size = 3
space_ratio = 1.2
boxWidth = 346
boxHeight = 80
box_side_width = 68

def draw_text_in_box(can, text, x, y, box_width, box_height, 
                     font_name="IPAexGothic",
                     max_font_size=12, min_font_size=6,
                     line_spacing_ratio=1.2):
    """
    テキストを与えられたボックス内 (x, y, box_width, box_height) に収まるよう
    自動的に折り返しを行い、必要に応じてフォントサイズを縮小して描画する。

    Parameters:
    -----------
    can : reportlab.pdfgen.canvas.Canvas
        描画先のキャンバス
    text : str
        描画する文字列
    x, y : float
        描画開始位置 (左下)
    box_width : float
        テキストを収めたい領域の幅
    box_height : float
        テキストを収めたい領域の高さ
    font_name : str, optional
        使用するフォント名
    max_font_size : int, optional
        試行する最大フォントサイズ
    min_font_size : int, optional
        試行する最小フォントサイズ
    line_spacing_ratio : float, optional
        フォントサイズに対する行間の倍率 (例: 1.2)
    """
    original_lines = text.splitlines()

    def wrap_text_lines(can, lines, font_name, font_size, box_width):
        """複数行を行ごとに wrap して返す。"""
        wrapped_lines = []
        for line in lines:
            result = _wrap_single_line(can, line, font_name, font_size, box_width)
            wrapped_lines.extend(result)
        return wrapped_lines

    def _wrap_single_line(can, line, font_name, font_size, box_width):
      """
      1つの行を文字単位で横幅を超えないよう折り返す。
      """
      wrapped = []
      current_line = ""

      # ★ここで1文字ずつループする
      for ch in line:
          test_line = current_line + ch
          test_line_width = can.stringWidth(test_line, font_name, font_size)

          if test_line_width <= box_width:
              current_line = test_line
          else:
              # 収まらない場合
              wrapped.append(current_line)
              current_line = ch

      if current_line:
          wrapped.append(current_line)

      return wrapped

    # 最大フォントサイズから順に試し、収まるか判定
    for fs in range(max_font_size, min_font_size - 1, -1):
        wrapped_lines = wrap_text_lines(can, original_lines, font_name, fs, box_width)
        line_height = fs * line_spacing_ratio
        total_height = len(wrapped_lines) * line_height

        if total_height <= box_height:
            # 描画
            can.setFont(font_name, fs)
            current_y = y
            for line in wrapped_lines:
                can.drawString(x, current_y, line)
                current_y -= line_height
            return

    # 最小フォントサイズでも収まらなかった場合
    wrapped_lines = wrap_text_lines(can, original_lines, font_name, min_font_size, box_width)
    can.setFont(font_name, min_font_size)
    line_height = min_font_size * line_spacing_ratio
    current_y = y
    for line in wrapped_lines:
        # これ以上はみ出す場合は描画を打ち切る
        if current_y < (y - box_height):
            break
        can.drawString(x, current_y, line)
        current_y -= line_height

def add_answers_to_pdf(writer, template_path, answers):
    # テンプレートを読み込む
    existing_pdf = PdfReader(template_path)
    page1 = existing_pdf.pages[0]  # 1ページ目
    page2 = existing_pdf.pages[1]  # 2ページ目

    # ページ1に回答を記入
    packet1 = BytesIO()
    can1 = canvas.Canvas(packet1)
    can1.setFont("IPAexGothic", 12)

    # 質問1: name
    if pd.notna(answers.get("name", "")):
        can1.drawString(260, 205, f"{answers['name']}")

    # 質問2: how (チェックボックス)
    check_positions = {
        "Instagram": (sideWidth, 157),
        "X(旧Twitter)": (sideWidth, 144),
        "現役生の家族や友人": (sideWidth, 131),
        "家族や友人から": (sideWidth, 118),
        "メーリングリスト(OBの方)": (sideWidth, 105),
        "過去のSlack(OBの方)": (sideWidth, 92),
        "その他": (sideWidth, 79),
    }
    # その他の内容を記入する位置
    other_text_position = (120, 80)

    how_value = answers.get("how", "")
    if pd.notna(how_value):
        for choice in how_value.split(","):
            choice = choice.strip()
            if choice in check_positions:
                # 定義済みの選択肢に該当する場合、チェックをつける
                x, y = check_positions[choice]
                can1.drawString(x, y, "✓")
            else:
                # 「その他」にチェックをつけ、その内容を記入
                x, y = check_positions["その他"]
                can1.drawString(x, y, "✓")
                # 「その他」の内容を記入
                can1.drawString(*other_text_position, f"{choice}")

    can1.save()
    packet1.seek(0)
    new_pdf1 = PdfReader(packet1)
    page1.merge_page(new_pdf1.pages[0])

    # ページ2に質問3以降を記入
    packet2 = BytesIO()
    can2 = canvas.Canvas(packet2)
    can2.setFont("IPAexGothic", 12)

    # 質問3: all
    if pd.notna(answers.get("all", "")):
        # 例: 幅 350pt, 高さ 80pt の領域に収める（座標は適宜修正）
        draw_text_in_box(
            can=can2,
            text=answers["all"],
            x=box_side_width, y=515,
            box_width=boxWidth, box_height=boxHeight,
            font_name="IPAexGothic",
            max_font_size=max_size,
            min_font_size=min_size,
            line_spacing_ratio=space_ratio
        )
    # 質問4: band
    if pd.notna(answers.get("band", "")):
        draw_text_in_box(
            can = can2,
            text = answers["band"],
            x = box_side_width, y = 399,
            box_width = boxWidth, box_height = boxHeight,
            font_name = "IPAexGothic",
            max_font_size = max_size,
            min_font_size = min_size,
            line_spacing_ratio=space_ratio
        )


    # 質問5: musical
    if pd.notna(answers.get("musical", "")):
        draw_text_in_box(
            can = can2,
            text = answers["musical"],
            x = box_side_width, y = 279,
            box_width = boxWidth, box_height = boxHeight,
            font_name = "IPAexGothic",
            max_font_size = max_size,
            min_font_size = min_size,
            line_spacing_ratio=space_ratio
        )

    # 質問6: chorus
    if pd.notna(answers.get("chorus", "")):
        draw_text_in_box(
            can = can2,
            text = answers["chorus"],
            x = box_side_width, y = 162,
            box_width = boxWidth, box_height = boxHeight,
            font_name = "IPAexGothic",
            max_font_size = max_size,
            min_font_size = min_size,
            line_spacing_ratio=space_ratio
        )

    # 空文字を入れておいてページの編集内容を確定
    can2.drawString(0, 0, "")
    can2.save()
    packet2.seek(0)
    new_pdf2 = PdfReader(packet2)
    page2.merge_page(new_pdf2.pages[0])

    # ページをPDFに追加
    writer.add_page(page1)
    writer.add_page(page2)


# CSVを読み込む
csv_path = "回答.csv"
pdf_template_path = "定期演奏会アンケート.pdf"
output_pdf_path = "まとめたアンケート.pdf"

# CSVデータを処理
writer = PdfWriter()
data = pd.read_csv(csv_path)

# 個別PDF生成
for index, row in data.iterrows():
    answers = row.to_dict()
    writer = PdfWriter()
    # 1回答分のPDFを生成
    add_answers_to_pdf(writer, pdf_template_path, answers)

    filename = f"tmp_answer_{index}.pdf"
    with open(filename, "wb") as f:
        writer.write(f)

# まとめPDF作成
def rebuild_pdf_from_readers(input_files, output_file):
    """
    複数の PDF ファイルを読み込み、それらのページを PdfReader で取得して
    PdfWriter で一つにまとめ、output_file へ出力する。
    """
    writer = PdfWriter()

    for file in input_files:
        # PdfReaderを使って既存PDFを読み込む
        reader = PdfReader(file)
        # ページを順に追加
        for page in reader.pages:
            writer.add_page(page)

    # まとめたPDFを書き込む
    with open(output_file, "wb") as f:
        writer.write(f)

filenames = [f"tmp_answer_{i}.pdf" for i in range(len(data))]
rebuild_pdf_from_readers(filenames, output_pdf_path)


# 不要な個別PDFを削除するなど後処理
# 不要なものを作る前に結合すれば良いと思うかもしれないがPyPDF2 で報告されている結合処理の失敗に遭遇したので回避するためにこのような処理を行っている
# 個別のPDFが入らない場合はここのコメントを外すと良い
# for index in range(len(data)):
#     filename = f"tmp_answer_{index}.pdf"
#     os.remove(filename)

print(f"{output_pdf_path} が作成されました。")
