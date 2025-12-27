# アンケート.py
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


# ----------------------------
# 可変文字サイズ & 折り返し（ここは今後いじらない想定）
# ----------------------------
def draw_text_in_box(
    can: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    box_width: float,
    box_height: float,
    font_name: str,
    max_font_size: int,
    min_font_size: int,
    line_spacing_ratio: float,
) -> None:
    original_lines = text.splitlines()

    def _wrap_single_line(line: str, font_size: int) -> List[str]:
        wrapped = []
        current_line = ""
        for ch in line:
            test_line = current_line + ch
            if can.stringWidth(test_line, font_name, font_size) <= box_width:
                current_line = test_line
            else:
                if current_line:
                    wrapped.append(current_line)
                current_line = ch
        if current_line:
            wrapped.append(current_line)
        return wrapped

    def wrap_text_lines(lines: List[str], font_size: int) -> List[str]:
        wrapped_lines: List[str] = []
        for line in lines:
            wrapped_lines.extend(_wrap_single_line(line, font_size))
        return wrapped_lines

    for fs in range(max_font_size, min_font_size - 1, -1):
        wrapped_lines = wrap_text_lines(original_lines, fs)
        line_height = fs * line_spacing_ratio
        total_height = len(wrapped_lines) * line_height
        if total_height <= box_height:
            can.setFont(font_name, fs)
            current_y = y
            for line in wrapped_lines:
                can.drawString(x, current_y, line)
                current_y -= line_height
            return

    wrapped_lines = wrap_text_lines(original_lines, min_font_size)
    can.setFont(font_name, min_font_size)
    line_height = min_font_size * line_spacing_ratio
    current_y = y
    for line in wrapped_lines:
        if current_y < (y - box_height):
            break
        can.drawString(x, current_y, line)
        current_y -= line_height


# ----------------------------
# 年度設定が渡してくる「描画指示」データ構造
# ----------------------------
@dataclass(frozen=True)
class FontConfig:
    name: str
    path: str
    subfont_index: int = 0


@dataclass(frozen=True)
class TextDraw:
    page_index: int
    csv_key: str
    x: float
    y: float
    font_size: int = 12


@dataclass(frozen=True)
class CheckboxDraw:
    page_index: int
    csv_key: str
    check_positions: Dict[str, Tuple[float, float]]
    other_check_key: str
    other_text_position: Tuple[float, float]
    separator: str = ","


@dataclass(frozen=True)
class BoxTextDraw:
    page_index: int
    csv_key: str
    x: float
    y: float
    box_width: float
    box_height: float
    max_font_size: int = 12
    min_font_size: int = 3
    line_spacing_ratio: float = 1.2


DrawItem = Union[TextDraw, CheckboxDraw, BoxTextDraw]


@dataclass(frozen=True)
class SurveyConfig:
    template_pdf_path: str
    font: FontConfig
    fields: List[DrawItem]


# ----------------------------
# PDF生成（年度設定に従って描画するだけ）
# ----------------------------
def _is_valid_value(v: object) -> bool:
    if v is None:
        return False
    try:
        return pd.notna(v)
    except Exception:
        return True


def _to_str(v: object) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    return str(v)


def _register_font_once(font: FontConfig) -> None:
    pdfmetrics.registerFont(TTFont(font.name, font.path, subfontIndex=font.subfont_index))


def fill_single_answer_to_writer(writer: PdfWriter, answers: Dict[str, object], config: SurveyConfig) -> None:
    existing_pdf = PdfReader(config.template_pdf_path)
    page_count = len(existing_pdf.pages)

    for page_index in range(page_count):
        base_page = existing_pdf.pages[page_index]

        packet = BytesIO()
        can = canvas.Canvas(packet)
        can.setFont(config.font.name, 12)

        for item in config.fields:
            if item.page_index != page_index:
                continue

            if isinstance(item, TextDraw):
                v = answers.get(item.csv_key, "")
                if _is_valid_value(v):
                    can.setFont(config.font.name, item.font_size)
                    can.drawString(item.x, item.y, _to_str(v))

            elif isinstance(item, CheckboxDraw):
                v = answers.get(item.csv_key, "")
                if _is_valid_value(v):
                    raw = _to_str(v)
                    for choice in [c.strip() for c in raw.split(item.separator) if c.strip()]:
                        if choice in item.check_positions:
                            x, y = item.check_positions[choice]
                            can.drawString(x, y, "✓")
                        else:
                            x, y = item.check_positions[item.other_check_key]
                            can.drawString(x, y, "✓")
                            can.drawString(item.other_text_position[0], item.other_text_position[1], choice)

            elif isinstance(item, BoxTextDraw):
                v = answers.get(item.csv_key, "")
                if _is_valid_value(v):
                    draw_text_in_box(
                        can=can,
                        text=_to_str(v),
                        x=item.x,
                        y=item.y,
                        box_width=item.box_width,
                        box_height=item.box_height,
                        font_name=config.font.name,
                        max_font_size=item.max_font_size,
                        min_font_size=item.min_font_size,
                        line_spacing_ratio=item.line_spacing_ratio,
                    )

        can.drawString(0, 0, "")
        can.save()
        packet.seek(0)

        overlay_pdf = PdfReader(packet)
        base_page.merge_page(overlay_pdf.pages[0])
        writer.add_page(base_page)


def rebuild_pdf_from_files(input_files: List[str], output_file: str) -> None:
    writer = PdfWriter()
    for file in input_files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
