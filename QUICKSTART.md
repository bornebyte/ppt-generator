# PPT Generator - Quick Reference

## 🚀 Installation

### One-Line Install
```bash
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

### Manual Install
```bash
git clone https://github.com/bornebyte/ppt-generator.git
cd ppt-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🏃 Running the App

```bash
# Development mode (auto-reload)
./pptgen
# or
python main.py

# Production mode with Gunicorn
./pptgen -p
# or
gunicorn -w 4 -b 0.0.0.0:5000 main:app

# Custom port
./pptgen -p 8000
```

## 📡 Endpoints

- **Home**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Generate PPT**: POST to /generate_ppt

## 🧩 JSON Structure

```json
{
  "meta": {
    "title": "Presentation Title",
    "subtitle": "Subtitle"
  },
  "slides": [
    {"type": "title"},
    {
      "type": "content",
      "title": "Slide Title",
      "blocks": [
        {"kind": "paragraph", "text": "Text here"},
        {
          "kind": "bullets",
          "items": ["Item 1", "Item 2"]
        },
        {
          "kind": "images",
          "layout": "row",
          "items": [{"path": "image.png"}]
        }
      ]
    }
  ]
}
```

## 🔧 Environment Variables

```bash
FLASK_ENV=production
PORT=5000
SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=16777216
```

## 📦 Dependencies

- Flask (web framework)
- python-pptx (PowerPoint generation)
- Gunicorn (production server)
- Pillow (image handling)

## 🛠️ Troubleshooting

### Port in use
```bash
lsof -ti:5000 | xargs kill -9
```

### Reinstall python-pptx
```bash
pip uninstall python-pptx
pip install python-pptx
```

### Permission denied
```bash
chmod +x pptgen install.sh
```

## 📚 Documentation

- **README.md** - Full user guide
- **DEPLOYMENT.md** - Deployment instructions
- **CONTRIBUTING.md** - How to contribute
- **PROJECT_SUMMARY.md** - Complete project overview

## 🔗 Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version

# Test Flask app
python -m py_compile main.py

# View logs (if using systemd)
journalctl -u pptgen -f

# Check if server is running
curl http://localhost:5000/health
```

## 📝 Content Block Types

| Type | Description |
|------|-------------|
| `paragraph` | Text paragraph |
| `bullets` | Bullet points with optional sub-points |
| `images` | Images with layouts: row, column, grid |

## 🎨 Image Layouts

- **row**: Images side by side
- **column**: Images stacked vertically  
- **grid**: Images in 2-column grid

## ⚙️ Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Change `SECRET_KEY`
- [ ] Use Gunicorn (not Flask dev server)
- [ ] Set up reverse proxy (Nginx/Apache)
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up logging
- [ ] Monitor resources

---

**Quick Help**: `./pptgen -h`
