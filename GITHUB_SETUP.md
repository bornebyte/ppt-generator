# Setup Instructions for GitHub

Before pushing to GitHub, update the following placeholders:

## Files to Update

### 1. README.md
Replace `bornebyte` with your GitHub username (if different):
- Line with installation command
- Manual installation git clone command

### 2. install.sh
Replace `bornebyte` in:
- `REPO_URL="https://github.com/bornebyte/ppt-generator.git"`

### 3. After Pushing to GitHub

The installation command will be:
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/ppt-generator/main/install.sh | bash
```

## Quick Setup Commands

```bash
# Set your GitHub username
GITHUB_USER="your-github-username"

# Update README.md
sed -i "s/YOUR_USERNAME/$GITHUB_USER/g" README.md

# Update install.sh
sed -i "s/YOUR_USERNAME/$GITHUB_USER/g" install.sh

# Update CONTRIBUTING.md
sed -i "s/YOUR_USERNAME/$GITHUB_USER/g" CONTRIBUTING.md
```

## Initial Git Setup

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: PPT Generator application"

# Add remote
git remote add origin https://github.com/bornebyte/ppt-generator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## After Pushing

Test the installation script:
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/ppt-generator/main/install.sh | bash
```
