#!/bin/bash

# Setup Verification Script for PPT Generator
# Run this after installation to verify everything is working

echo "🔍 Verifying PPT Generator Setup..."
echo ""

ERRORS=0

# Check if running from project directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project directory."
    exit 1
fi

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    ERRORS=$((ERRORS+1))
fi

# Check virtual environment
echo -n "Checking virtual environment... "
if [ -d "venv" ]; then
    echo "✅ Found"
else
    echo "❌ Not found"
    ERRORS=$((ERRORS+1))
fi

# Check dependencies
echo -n "Checking dependencies... "
if [ -f "requirements.txt" ]; then
    source venv/bin/activate 2>/dev/null
    if python -c "import flask; import pptx; import gunicorn" 2>/dev/null; then
        echo "✅ All installed"
    else
        echo "❌ Missing dependencies"
        ERRORS=$((ERRORS+1))
    fi
else
    echo "❌ requirements.txt not found"
    ERRORS=$((ERRORS+1))
fi

# Check main.py syntax
echo -n "Checking main.py syntax... "
if python -m py_compile main.py 2>/dev/null; then
    echo "✅ No syntax errors"
else
    echo "❌ Syntax errors found"
    ERRORS=$((ERRORS+1))
fi

# Check templates
echo -n "Checking templates... "
if [ -f "templates/index.html" ] && [ -f "templates/base.html" ]; then
    echo "✅ Found"
else
    echo "❌ Missing templates"
    ERRORS=$((ERRORS+1))
fi

# Check executable permissions
echo -n "Checking pptgen executable... "
if [ -x "pptgen" ]; then
    echo "✅ Executable"
else
    echo "⚠️  Not executable (run: chmod +x pptgen)"
    ERRORS=$((ERRORS+1))
fi

# Check install.sh
echo -n "Checking install.sh... "
if [ -f "install.sh" ] && [ -x "install.sh" ]; then
    echo "✅ Found and executable"
else
    echo "⚠️  Not executable (run: chmod +x install.sh)"
fi

# Check documentation
echo -n "Checking documentation... "
if [ -f "README.md" ] && [ -f "DEPLOYMENT.md" ]; then
    echo "✅ Found"
else
    echo "⚠️  Some documentation missing"
fi

# Try to start Flask (just import test)
echo -n "Testing Flask import... "
if python -c "from main import app" 2>/dev/null; then
    echo "✅ Success"
else
    echo "❌ Import failed"
    ERRORS=$((ERRORS+1))
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed! Setup is complete."
    echo ""
    echo "🚀 You can now run:"
    echo "   ./pptgen              # Development mode"
    echo "   ./pptgen -p           # Production mode"
    echo "   python main.py        # Direct Python"
    echo ""
    echo "📖 Visit http://localhost:5000 after starting"
else
    echo "❌ Found $ERRORS error(s). Please fix them before running."
    echo ""
    echo "💡 Common fixes:"
    echo "   - Run: pip install -r requirements.txt"
    echo "   - Run: chmod +x pptgen install.sh"
    echo "   - Make sure you're in the project directory"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

exit $ERRORS
