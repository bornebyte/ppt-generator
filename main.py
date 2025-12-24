import json
import os
from flask import Flask, render_template, request, send_file, jsonify
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
FONT = "Calibri"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'ppt-generator',
        'version': '1.0.0'
    })



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
            try:
                slide.shapes.add_picture(
                    img["path"],
                    Inches(0.5 + i * width),
                    Inches(top),
                    width=Inches(width - 0.2)
                )
            except FileNotFoundError:
                print(f"Warning: Image file not found at {img['path']}")

    elif block["layout"] == "column":
        height = 4 / count
        for i, img in enumerate(items):
            try:
                slide.shapes.add_picture(
                    img["path"],
                    Inches(2),
                    Inches(top + i * height),
                    height=Inches(height - 0.2)
                )
            except FileNotFoundError:
                print(f"Warning: Image file not found at {img['path']}")

    elif block["layout"] == "grid":
        cols = 2
        rows = (count + 1) // 2
        w, h = 4, 2
        for idx, img in enumerate(items):
            try:
                r, c = divmod(idx, cols)
                slide.shapes.add_picture(
                    img["path"],
                    Inches(0.5 + c * w),
                    Inches(top + r * h),
                    width=Inches(w - 0.3)
                )
            except FileNotFoundError:
                print(f"Warning: Image file not found at {img['path']}")

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


@app.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    try:
        # Get JSON data from request or use default content.json
        if request.is_json:
            data = request.get_json()
            if 'json_data' in data:
                # Parse JSON string from frontend
                content = json.loads(data['json_data'])
                file_name = data.get('file_name', 'presentation')
            else:
                content = data
                file_name = 'presentation'
        else:
            # Fallback to content.json file
            with open('content.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
            file_name = 'Generated'
        
        # Validate required fields
        if 'meta' not in content or 'slides' not in content:
            return jsonify({'error': 'Invalid JSON structure. Required: meta and slides'}), 400
        
        # Create presentation
        prs = Presentation()

        # Title slide
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = content["meta"].get("title", "Presentation")
        if len(slide.placeholders) > 1:
            slide.placeholders[1].text = content["meta"].get("subtitle", "")

        # Content slides
        for s in content["slides"]:
            if s.get("type") == "title":
                continue

            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = s.get("title", "Slide")

            if "subtitle" in s:
                p = slide.shapes.title.text_frame.add_paragraph()
                p.text = s["subtitle"]
                p.level = 1

            render_blocks(slide, s.get("blocks", []))

            if "notes" in s:
                slide.notes_slide.notes_text_frame.text = s["notes"]

        # Save with secure filename
        output_filename = f"{secure_filename(file_name)}.pptx"
        prs.save(output_filename)
        print(f"✅ PPT generated: {output_filename}")
        
        return send_file(output_filename, 
                        as_attachment=True, 
                        download_name=output_filename,
                        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        print(f"Error generating PPT: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Development server only
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
