from __future__ import annotations

import argparse
import importlib
import os
from typing import List

import pandas as pd
from PyPDF2 import PdfWriter

from engine import SurveyConfig, fill_single_answer_to_writer, rebuild_pdf_from_files, _register_font_once


def main() -> None:
    parser = argparse.ArgumentParser(description="Survey PDF filler")
    parser.add_argument("year", help='configs の年度ファイル名（例: "52回"）')

    parser.add_argument("--csv", default=None, help="回答CSVのパス（省略時は ./input/<year>/回答.csv）")
    parser.add_argument("--out", default=None, help="出力PDFのパス（省略時は ./output/<year>/まとめたアンケート.pdf）")
    parser.add_argument("--tmpdir", default=None, help="一時PDF出力ディレクトリ（省略時は ./tmp/<year>）")
    parser.add_argument(
        "--template",
        default=None,
        help="テンプレPDFのパス（省略時は ./input/<year>/定期演奏会アンケート.pdf）",
    )

    args = parser.parse_args()

    # 年度設定（座標など）を読み込む: configs/<year>.py には FONT と FIELDS がある前提
    mod = importlib.import_module(f"configs.{args.year}")

    csv_path = args.csv or f"./input/{args.year}/回答.csv"
    out_path = args.out or f"./output/{args.year}/まとめたアンケート.pdf"
    tmpdir = args.tmpdir or f"./tmp/{args.year}"
    template_path = args.template or f"./input/{args.year}/定期演奏会アンケート.pdf"

    # 年度のテンプレPDFを自動で使う
    config = SurveyConfig(
        template_pdf_path=template_path,
        font=mod.FONT,
        fields=mod.FIELDS,
    )

    # 親切チェック（初心者が詰まりやすいので）
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"テンプレPDFが見つかりません: {template_path}")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"回答CSVが見つかりません: {csv_path}")
    if not os.path.exists(config.font.path):
        raise FileNotFoundError(f"フォントが見つかりません: {config.font.path}")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(tmpdir, exist_ok=True)

    _register_font_once(config.font)

    data = pd.read_csv(csv_path)

    tmp_files: List[str] = []
    for index, row in data.iterrows():
        answers = row.to_dict()

        writer = PdfWriter()
        fill_single_answer_to_writer(writer, answers, config)

        tmp_path = os.path.join(tmpdir, f"tmp_answer_{index}.pdf")
        with open(tmp_path, "wb") as f:
            writer.write(f)

        tmp_files.append(tmp_path)

    rebuild_pdf_from_files(tmp_files, out_path)
    print(f"{out_path} が作成されました。")


if __name__ == "__main__":
    main()
