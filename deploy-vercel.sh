#!/bin/bash
# Quick Vercel Deployment Script for Schooloo AI

set -e

echo "🚀 Schooloo AI - Vercel Deployment Script"
echo "==========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run: git init"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "📝 Committing changes..."
git add -A
git commit -m "Prepare for Vercel deployment" || echo "No changes to commit"

echo "🔄 Pushing to GitHub..."
git push origin main || git push origin master || echo "Push skipped"

echo ""
echo "✅ Repository updated!"
echo ""
echo "Next steps:"
echo "1. Go to https://vercel.com/dashboard"
echo "2. Click 'Add New' → 'Project'"
echo "3. Import your GitHub repository"
echo "4. Set environment variables:"
echo "   - API_KEY: Your Google Gemini API Key"
echo "   - FLASK_ENV: production"
echo "5. Click 'Deploy'"
echo ""
echo "Or use Vercel CLI:"
echo "  vercel login"
echo "  vercel --prod"
echo ""
