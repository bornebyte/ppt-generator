import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

FONT = "Calibri"

def style(run, size=18, bold=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)

def add_text(tf, text, level=0, size=18, bold=False):
    p = tf.add_paragraph() if tf.text else tf.paragraphs[0]
    p.text = text
    p.level = level
    for r in p.runs:
        style(r, size, bold)

def render_blocks(slide, blocks):
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()

    for block in blocks:
        if block["kind"] == "paragraph":
            add_text(tf, block["text"], size=18)

        elif block["kind"] == "bullets":
            for item in block["items"]:
                if isinstance(item, str):
                    add_text(tf, item, level=0)
                else:
                    add_text(tf, item["text"], level=0, bold=True)
                    for sub in item.get("subpoints", []):
                        add_text(tf, sub, level=1)

        elif block["kind"] == "table":
            rows = len(block["rows"]) + 1
            cols = len(block["columns"])
            table = slide.shapes.add_table(
                rows, cols,
                Inches(0.5), Inches(2.3),
                Inches(9), Inches(3.5)
            ).table

            for c, col in enumerate(block["columns"]):
                table.cell(0, c).text = col

            for r, row in enumerate(block["rows"], start=1):
                for c, val in enumerate(row):
                    table.cell(r, c).text = val

        elif block["kind"] == "image":
            slide.shapes.add_picture(
                block["path"],
                Inches(1), Inches(2.5),
                width=Inches(6)
            )

# ----------------------------
# Load JSON
# ----------------------------
with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

prs = Presentation()

# Title slide
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = data["meta"]["title"]
title_slide.placeholders[1].text = data["meta"]["subtitle"]

# Content slides
for slide_data in data["slides"]:
    if slide_data["type"] == "title":
        continue

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = slide_data["title"]

    if "subtitle" in slide_data:
        subtitle = slide.shapes.title.text_frame.add_paragraph()
        subtitle.text = slide_data["subtitle"]
        subtitle.level = 1

    render_blocks(slide, slide_data.get("blocks", []))

    if "notes" in slide_data:
        slide.notes_slide.notes_text_frame.text = slide_data["notes"]

prs.save("GNU_GNOME_Presentation.pptx")
print("✅ PPT generated successfully")
