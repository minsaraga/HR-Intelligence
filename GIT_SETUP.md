# Git Setup Instructions

## Step 1: Create Repository on GitHub/GitLab

1. Go to GitHub.com or GitLab.com
2. Click "New Repository" or "New Project"
3. Name it: `ai-hr-talent-intelligence`
4. Keep it **Public** or **Private** (your choice)
5. **DO NOT** initialize with README, .gitignore, or license
6. Copy the repository URL (e.g., `https://github.com/yourusername/ai-hr-talent-intelligence.git`)

## Step 2: Initialize Local Repository

Open WSL terminal and run:

```bash
# Navigate to project
cd ~/.openclaw/workspace/ai-hr-talent-intelligence

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AI HR Talent Intelligence MVP"

# Add remote (replace with your URL)
git remote add origin https://github.com/yourusername/ai-hr-talent-intelligence.git

# Push to main branch
git branch -M main
git push -u origin main
```

## Step 3: Verify

Visit your repository URL to see all files pushed successfully.

## Common Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push

# Pull latest
git pull

# View remote
git remote -v
```

## Troubleshooting

**Authentication Error:**
- Use Personal Access Token instead of password
- GitHub: Settings → Developer settings → Personal access tokens → Generate new token
- Use token as password when prompted

**Permission Denied:**
```bash
# Configure git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Already exists error:**
```bash
# Force push (only for initial setup)
git push -u origin main --force
```
