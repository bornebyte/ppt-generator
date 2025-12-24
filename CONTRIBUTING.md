# Contributing to PPT Generator

Thank you for your interest in contributing to PPT Generator! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When creating a bug report, include:

- **Description**: Clear and concise description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, browser (if applicable)
- **Screenshots**: If applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** and description
- **Use case**: Explain why this would be useful
- **Possible implementation**: If you have ideas on how to implement it

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit your changes**
   ```bash
   git commit -m "Add some amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/bornebyte/ppt-generator.git
cd ppt-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Code Example

```python
def style(run, size=18, bold=False):
    """
    Apply text styling to a PowerPoint text run.
    
    Args:
        run: The text run object to style
        size (int): Font size in points (default: 18)
        bold (bool): Whether to make text bold (default: False)
    """
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
```

### HTML/JavaScript

- Use consistent indentation (2 spaces)
- Add comments for complex logic
- Follow modern ES6+ syntax

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

Examples:
```
Add image grid layout support

- Implement grid layout for multiple images
- Add configuration options for grid columns
- Update documentation

Fixes #123
```

## Testing

Before submitting a PR, ensure:

1. **Functionality works**
   - Test with different JSON structures
   - Test error handling
   - Test with various browsers (if frontend changes)

2. **No breaking changes**
   - Existing functionality still works
   - Backward compatibility maintained

3. **Code quality**
   - No syntax errors
   - Follow coding standards
   - Add comments where necessary

## Project Structure

```
ppt-generator/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── content.json        # Example content
├── pptgen              # CLI executable
├── install.sh          # Installation script
├── templates/          # HTML templates
│   ├── base.html
│   └── index.html
├── static/             # Static files (CSS, JS)
│   └── css/
│       └── style.css
└── docs/               # Documentation
    ├── README.md
    ├── DEPLOYMENT.md
    └── CONTRIBUTING.md
```

## Adding New Features

### Adding a New Content Block Type

1. **Update JSON structure documentation**
2. **Add rendering function** in `main.py`
3. **Update `render_blocks` function**
4. **Add example to `content.json`**
5. **Update README.md**

Example:
```python
def render_custom_block(slide, block):
    """
    Render a custom block type.
    
    Args:
        slide: PowerPoint slide object
        block: Block configuration dict
    """
    # Implementation here
    pass
```

### Adding UI Features

1. **Update HTML** in `templates/`
2. **Add styling** in `static/css/`
3. **Add JavaScript** for interactivity
4. **Test across browsers**

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment-related changes
- Add inline comments for complex code
- Include examples in documentation

## Release Process

Maintainers will:

1. Review and merge PRs
2. Update version number
3. Create release notes
4. Tag release in Git
5. Deploy to production

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues (see SECURITY.md)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to PPT Generator! 🎉
