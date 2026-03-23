#!/bin/bash

# Git Setup Script for AI HR Talent Intelligence

echo "🚀 Git Repository Setup"
echo "======================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if already initialized
if [ -d .git ]; then
    echo "⚠️  Git repository already initialized."
    read -p "Do you want to reinitialize? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    rm -rf .git
fi

# Get repository URL
echo "📝 Enter your Git repository URL:"
echo "   Example: https://github.com/yourusername/ai-hr-talent-intelligence.git"
read -p "URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Repository URL is required."
    exit 1
fi

# Configure git user if not set
if [ -z "$(git config --global user.name)" ]; then
    read -p "Enter your name: " GIT_NAME
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$(git config --global user.email)" ]; then
    read -p "Enter your email: " GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
fi

# Initialize repository
echo ""
echo "🔧 Initializing Git repository..."
git init

echo "📦 Adding files..."
git add .

echo "💾 Creating initial commit..."
git commit -m "Initial commit: AI HR Talent Intelligence MVP with React frontend and FastAPI backend"

echo "🔗 Adding remote origin..."
git remote add origin "$REPO_URL"

echo "🌿 Setting main branch..."
git branch -M main

echo "⬆️  Pushing to remote..."
git push -u origin main

echo ""
echo "✅ Repository setup complete!"
echo "🌐 View your repository at: $REPO_URL"
echo ""
echo "📚 Common commands:"
echo "   git status          - Check status"
echo "   git add .           - Stage all changes"
echo "   git commit -m 'msg' - Commit changes"
echo "   git push            - Push to remote"
echo ""
