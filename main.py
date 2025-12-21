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

def render_images(slide, block, top=2.5):
    items = block["items"]
    count = len(items)

    if block["layout"] == "row":
        width = 8 / count
        for i, img in enumerate(items):
            slide.shapes.add_picture(
                img["path"],
                Inches(0.5 + i * width),
                Inches(top),
                width=Inches(width - 0.2)
            )

    elif block["layout"] == "column":
        height = 4 / count
        for i, img in enumerate(items):
            slide.shapes.add_picture(
                img["path"],
                Inches(2),
                Inches(top + i * height),
                height=Inches(height - 0.2)
            )

    elif block["layout"] == "grid":
        cols = 2
        rows = (count + 1) // 2
        w, h = 4, 2
        for idx, img in enumerate(items):
            r, c = divmod(idx, cols)
            slide.shapes.add_picture(
                img["path"],
                Inches(0.5 + c * w),
                Inches(top + r * h),
                width=Inches(w - 0.3)
            )

def render_blocks(slide, blocks):
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()

    for block in blocks:
        if block["kind"] == "paragraph":
            add_text(tf, block["text"])

        elif block["kind"] == "bullets":
            for item in block["items"]:
                if isinstance(item, str):
                    add_text(tf, item)
                else:
                    add_text(tf, item["text"], bold=True)
                    for sub in item.get("subpoints", []):
                        add_text(tf, sub, level=1)

        elif block["kind"] == "images":
            render_images(slide, block)

# ----------------------------
# Load JSON
# ----------------------------
with open("content.json", "r", encoding="utf-8") as f:
    data = json.load(f)

prs = Presentation()

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = data["meta"]["title"]
slide.placeholders[1].text = data["meta"]["subtitle"]

# Content slides
for s in data["slides"]:
    if s["type"] == "title":
        continue

    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = s["title"]

    if "subtitle" in s:
        p = slide.shapes.title.text_frame.add_paragraph()
        p.text = s["subtitle"]
        p.level = 1

    render_blocks(slide, s.get("blocks", []))

    if "notes" in s:
        slide.notes_slide.notes_text_frame.text = s["notes"]

prs.save("GNU_GNOME_Final.pptx")
print("✅ Fully automated PPT generated")
