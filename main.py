import json
import os
from flask import Flask, render_template, request, send_file, jsonify
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
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


def create_jain_title_slide(prs, jain_data):
    """Create custom Jain University title slide"""
    # Use blank layout for custom design
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Add Jain logo at top center
    logo_path = 'static/jain.png'
    if os.path.exists(logo_path):
        left = Inches(3.5)  # Center position
        top = Inches(0.5)
        height = Inches(1.2)
        slide.shapes.add_picture(logo_path, left, top, height=height)
    
    # Add university name
    uni_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(0.5))
    uni_tf = uni_box.text_frame
    uni_tf.text = "JAIN (Deemed-to-be University)"
    uni_p = uni_tf.paragraphs[0]
    uni_p.alignment = PP_ALIGN.CENTER
    uni_p.font.size = Pt(24)
    uni_p.font.bold = True
    uni_p.font.color.rgb = RGBColor(0, 0, 128)
    
    # Add presentation title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.7), Inches(8), Inches(0.8))
    title_tf = title_box.text_frame
    title_tf.text = jain_data.get('title', 'Presentation Title')
    title_tf.word_wrap = True
    title_p = title_tf.paragraphs[0]
    title_p.alignment = PP_ALIGN.CENTER
    title_p.font.size = Pt(32)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(0, 0, 0)
    
    # Check if single or group
    if jain_data.get('type') == 'single':
        # Single student details
        details_top = 3.8
        details_box = slide.shapes.add_textbox(Inches(2), Inches(details_top), Inches(6), Inches(2.5))
        details_tf = details_box.text_frame
        details_tf.word_wrap = True
        
        # Submitted by
        p = details_tf.paragraphs[0]
        p.text = "Submitted By:"
        p.font.size = Pt(16)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        
        # Student details
        student_info = [
            f"Name: {jain_data.get('student_name', '')}",
            f"USN: {jain_data.get('usn', '')}",
            f"Course: {jain_data.get('course', '')}",
            f"Semester: {jain_data.get('semester', '')}"
        ]
        
        for info in student_info:
            p = details_tf.add_paragraph()
            p.text = info
            p.font.size = Pt(14)
            p.alignment = PP_ALIGN.CENTER
            p.space_before = Pt(6)
        
        # Submitted to
        p = details_tf.add_paragraph()
        p.text = f"\nSubmitted To: {jain_data.get('professor', '')}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(12)
        
    elif jain_data.get('type') == 'group':
        # Group - create table for students
        students = jain_data.get('students', [])
        
        # Add "Submitted By:" text
        sub_box = slide.shapes.add_textbox(Inches(2), Inches(3.7), Inches(6), Inches(0.4))
        sub_tf = sub_box.text_frame
        sub_p = sub_tf.paragraphs[0]
        sub_p.text = "Submitted By:"
        sub_p.font.size = Pt(16)
        sub_p.font.bold = True
        sub_p.alignment = PP_ALIGN.CENTER
        
        # Create table
        if students:
            rows = len(students) + 1  # +1 for header
            cols = 2
            left = Inches(2.5)
            top = Inches(4.2)
            width = Inches(5)
            height = Inches(0.4 * rows)
            
            table = slide.shapes.add_table(rows, cols, left, top, width, height).table
            
            # Set column widths
            table.columns[0].width = Inches(2.5)
            table.columns[1].width = Inches(2.5)
            
            # Header row
            table.cell(0, 0).text = "Name"
            table.cell(0, 1).text = "USN"
            
            for i, cell in enumerate([table.cell(0, 0), table.cell(0, 1)]):
                cell.text_frame.paragraphs[0].font.bold = True
                cell.text_frame.paragraphs[0].font.size = Pt(12)
                cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(200, 200, 200)
            
            # Data rows
            for idx, student in enumerate(students):
                table.cell(idx + 1, 0).text = student.get('name', '')
                table.cell(idx + 1, 1).text = student.get('usn', '')
                
                for col in range(2):
                    cell = table.cell(idx + 1, col)
                    cell.text_frame.paragraphs[0].font.size = Pt(11)
                    cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Submitted to
        prof_box = slide.shapes.add_textbox(Inches(2), Inches(6.5), Inches(6), Inches(0.4))
        prof_tf = prof_box.text_frame
        prof_p = prof_tf.paragraphs[0]
        prof_p.text = f"Submitted To: {jain_data.get('professor', '')}"
        prof_p.font.size = Pt(14)
        prof_p.font.bold = True
        prof_p.alignment = PP_ALIGN.CENTER


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
                jain_data = data.get('jain_data')  # Get Jain university data if provided
            else:
                content = data
                file_name = 'presentation'
                jain_data = None
        else:
            # Fallback to content.json file
            with open('content.json', 'r', encoding='utf-8') as f:
                content = json.load(f)
            file_name = 'Generated'
            jain_data = None
        
        # Validate required fields
        if 'meta' not in content or 'slides' not in content:
            return jsonify({'error': 'Invalid JSON structure. Required: meta and slides'}), 400
        
        # Create presentation
        prs = Presentation()

        # Add Jain title slide if requested
        if jain_data and jain_data.get('enabled'):
            create_jain_title_slide(prs, jain_data)
        else:
            # Standard title slide
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
