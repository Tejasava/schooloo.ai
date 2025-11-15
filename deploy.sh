#!/bin/bash

# 🚀 Schooloo AI Agent - Vercel Deployment Script
# This script guides you through deploying to Vercel

set -e

echo "════════════════════════════════════════════════════════"
echo "🚀 Schooloo AI Agent - Vercel Deployment Script"
echo "════════════════════════════════════════════════════════"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"
echo ""

# Check Git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git is installed${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}📝 Please edit .env and add your Google API key:${NC}"
        echo "   nano .env"
        exit 1
    fi
fi
echo -e "${GREEN}✓ .env file exists${NC}"

# Check if API_KEY is set
if ! grep -q "API_KEY=" .env || grep "^API_KEY=$" .env > /dev/null; then
    echo -e "${YELLOW}❌ API_KEY is not set in .env file${NC}"
    echo "   Add your Google Gemini API key to .env file"
    exit 1
fi
echo -e "${GREEN}✓ API_KEY is configured${NC}"

# Check git status
if [ -z "$(git config user.email)" ]; then
    echo -e "${YELLOW}⚠️  Git user not configured. Setting up...${NC}"
    git config user.email "developer@schooloo.ai"
    git config user.name "Schooloo Developer"
fi

# Check if git repo is initialized
if [ ! -d .git ]; then
    echo -e "${BLUE}📦 Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: Schooloo AI Agent"
fi

echo ""
echo -e "${BLUE}📋 Pre-deployment Checklist${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. ✓ Git is initialized and ready"
echo "2. ✓ .env file is configured with API_KEY"
echo "3. ✓ All files are committed to Git"
echo ""
echo "4. □ GitHub repository is created (next step)"
echo "5. □ Vercel project is created (final step)"
echo ""

echo -e "${BLUE}📍 Next Steps:${NC}"
echo ""
echo "1️⃣  Create a new GitHub repository:"
echo "   https://github.com/new"
echo ""
echo "2️⃣  Push your code to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/schooloo-agent.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Deploy to Vercel:"
echo "   a) Sign in to https://vercel.com/dashboard"
echo "   b) Click 'New Project'"
echo "   c) Click 'Import Git Repository'"
echo "   d) Paste your GitHub repo URL"
echo "   e) Click 'Import'"
echo ""
echo "4️⃣  Add Environment Variables in Vercel:"
echo "   a) Go to Settings → Environment Variables"
echo "   b) Add API_KEY from your .env file"
echo "   c) Click 'Save'"
echo ""
echo "5️⃣  Deploy!"
echo "   Vercel will automatically build and deploy"
echo ""

echo -e "${GREEN}✓ Deployment preparation complete!${NC}"
echo ""
echo "For detailed instructions, see: VERCEL_DEPLOYMENT_GUIDE.md"
echo ""
