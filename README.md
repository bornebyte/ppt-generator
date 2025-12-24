# PowerPoint Generator 📊

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

A Flask-based web application that generates PowerPoint presentations from JSON data. Create professional presentations programmatically with customizable slides, content blocks, images, and formatting.

## 📚 Documentation

- **[Platform Guide](PLATFORM_GUIDE.md)** - Detailed Windows/macOS/Linux installation
- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Project Summary](PROJECT_SUMMARY.md)** - Complete overview of the project

## ✨ Features

- 🎨 **Web Interface**: User-friendly web UI for generating presentations
- 📝 **JSON-Driven**: Define your entire presentation structure in JSON
- 🤖 **AI Helper**: Built-in prompt template to get JSON from ChatGPT/Claude
- 🎓 **Jain University Support**: Custom title slides for academic presentations
  - Single student presentations with details
  - Group projects with student tables
  - Professional university branding
- 🖼️ **Image Support**: Add images with flexible layouts (row, column, grid)
- 📋 **Rich Content**: Support for paragraphs, bullet points, and nested sub-points
- 🎯 **Customizable**: Configure titles, subtitles, and notes for each slide
- 🚀 **Production Ready**: Includes Gunicorn for production deployment
- 🔧 **Easy Setup**: One-command installation script

## 🚀 Quick Install

### One-Line Installation

**Linux / macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

**Windows (Command Prompt):**
```cmd
curl -o install.bat https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.bat && install.bat
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.ps1" -OutFile "install.ps1"; powershell -ExecutionPolicy Bypass -File install.ps1
```

This will:
- Clone the repository
- Set up a virtual environment
- Install all dependencies
- Create a launcher command for easy access

### After Installation

**Linux / macOS:**
```bash
pptgen        # Start the development server
pptgen -p     # Start with production server (Gunicorn)
```

**Windows:**
```cmd
pptgen.bat        # Start the development server
pptgen.bat -p     # Start with production server
```

Or use the universal Python launcher (all platforms):
```bash
python pptgen-launcher.py
python pptgen-launcher.py -p
```

## 📦 Manual Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bornebyte/ppt-generator.git
   cd ppt-generator
   ```

2. **Create a virtual environment**
   
   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   
   **Development mode:**
   
   *Linux / macOS:*
   ```bash
   ./pptgen
   # or
   python main.py
   ```
   
   *Windows:*
   ```cmd
   pptgen.bat
   REM or
   python main.py
   ```
   
   **Production mode:**
   
   *Linux / macOS:*
   ```bash
   ./pptgen -p
   # or
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```
   
   *Windows:*
   ```cmd
   pptgen.bat -p
   REM or
   python -m gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🎯 Usage

### Using the Web Interface

1. Open the application in your browser
2. **(Optional) Enable Jain University mode** for academic presentations
   - Toggle "Create for JAIN University"
   - Enter presentation title
   - Choose single student or group project
   - Fill in student details (name, USN, course, semester)
   - Enter professor name (submitted to)
3. **Get JSON from AI** (if needed):
   - Click "Copy Prompt" in the AI Helper section
   - Paste into ChatGPT, Claude, or any AI assistant
   - Replace "[YOUR TOPIC]" with your actual topic
   - Copy the generated JSON
4. Enter a filename for your presentation
5. Paste your JSON content
6. Click "Generate PPT"
7. Download your generated PowerPoint file

### JSON Format

Here's a basic structure for your presentation:

```json
{
    "meta": {
        "title": "Your Presentation Title",
        "subtitle": "Your Subtitle",
        "author": "Your Name",
        "institution": "Your Institution"
    },
    "slides": [
        {
            "type": "title"
        },
        {
            "type": "content",
            "title": "Slide Title",
            "subtitle": "Optional Subtitle",
            "blocks": [
                {
                    "kind": "paragraph",
                    "text": "Your paragraph text here."
                },
                {
                    "kind": "bullets",
                    "items": [
                        "Bullet point 1",
                        "Bullet point 2",
                        {
                            "text": "Bullet with sub-points",
                            "subpoints": [
                                "Sub-point 1",
                                "Sub-point 2"
                            ]
                        }
                    ]
                }
            ],
            "notes": "Speaker notes for this slide"
        }
    ]
}
```

### Content Block Types

#### 1. Paragraph Block
```json
{
    "kind": "paragraph",
    "text": "Your paragraph text here."
}
```

#### 2. Bullets Block
```json
{
    "kind": "bullets",
    "items": [
        "Simple bullet point",
        {
            "text": "Bullet with sub-points",
            "subpoints": ["Sub 1", "Sub 2"]
        }
    ]
}
```

#### 3. Images Block
```json
{
    "kind": "images",
    "layout": "row",
    "items": [
        {
            "path": "path/to/image.png",
            "caption": "Image caption"
        }
    ]
}
```

Available layouts: `row`, `column`, `grid`

## 📁 Project Structure

```
ppt-generator/
├── main.py              # Flask application
├── requirements.txt     # Python dependencies
├── content.json        # Example JSON content
├── install.sh          # Installation script
├── pptgen              # CLI executable
├── templates/
│   ├── base.html       # Base template
│   └── index.html      # Main page
├── static/
│   └── css/
│       └── style.css   # Custom styles
└── README.md           # Documentation
```

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
export FLASK_APP=main.py
export FLASK_ENV=development  # or production
export PORT=5000              # Default port
```

### Production Deployment

For production deployment, use Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

Options:
- `-w 4`: Number of worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `--timeout 120`: Request timeout in seconds

## 🛠️ API Endpoints

### `GET /`
Home page with the web interface.

### `POST /generate_ppt`
Generate a PowerPoint presentation.

**Request Body:**
```json
{
    "file_name": "my_presentation",
    "json_data": "{...JSON content...}"
}
```

**Response:**
- Success: PowerPoint file download
- Error: JSON with error message and status code

## 🧪 Example

See [`content.json`](content.json) for a complete example presentation about "Metals in Mobile Phones".

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Platform-Specific Issues

See the [Platform Guide](PLATFORM_GUIDE.md) for detailed platform-specific troubleshooting.

### Installation Timeout/Network Issues

If installation fails with timeout errors:

```bash
# Manual installation with increased timeout
cd ~/.ppt-generator  # or your install directory
source venv/bin/activate
pip install --timeout 300 -r requirements.txt

# Or try with retry
pip install --timeout 300 --retries 5 -r requirements.txt
```

### "Package not found" Error

If you encounter `Package not found at '.../pptx/templates/default.pptx'`:

```bash
pip uninstall python-pptx
pip install python-pptx
```

### Port Already in Use

If port 5000 is already in use:

```bash
# Change port
export PORT=8000
python main.py
```

Or kill the existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

### Virtual Environment Issues

If you have issues with the virtual environment:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📧 Support

If you have any questions or run into issues, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [python-pptx](https://python-pptx.readthedocs.io/)
- Flask web framework
- Bootstrap for UI components

---

Made with ❤️ by the PPT Generator team
