#!/bin/bash

echo "=================================================="
echo "🔑 GitHub SSH Key Setup Script"
echo "=================================================="
echo ""

# Get email
read -p "Enter your GitHub email: " email

if [ -z "$email" ]; then
    echo "❌ Email is required!"
    exit 1
fi

echo ""
echo "📝 Step 1: Generating SSH Key..."
echo "Press Enter 3 times (or set a passphrase if you want)"
echo ""

# Generate SSH key
ssh-keygen -t ed25519 -C "$email"

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate SSH key"
    exit 1
fi

echo ""
echo "✅ SSH Key generated successfully!"
echo ""

# Check if key exists
if [ ! -f ~/.ssh/id_ed25519.pub ]; then
    echo "❌ SSH public key not found at ~/.ssh/id_ed25519.pub"
    exit 1
fi

echo "=================================================="
echo "📋 Step 2: Your SSH Public Key"
echo "=================================================="
echo ""
echo "Copy the following key (including ssh-ed25519 and email):"
echo ""
echo "---START---"
cat ~/.ssh/id_ed25519.pub
echo ""
echo "---END---"
echo ""

# Copy to clipboard if pbcopy is available
if command -v pbcopy &> /dev/null; then
    cat ~/.ssh/id_ed25519.pub | pbcopy
    echo "✅ Key copied to clipboard!"
    echo ""
fi

echo "=================================================="
echo "📝 Step 3: Add to GitHub"
echo "=================================================="
echo ""
echo "1. Open this URL in browser:"
echo "   https://github.com/settings/keys"
echo ""
echo "2. Click 'New SSH key'"
echo ""
echo "3. Enter:"
echo "   Title: MacBook Air - YouTube Scraper"
echo "   Key: Paste the key (already in clipboard)"
echo ""
echo "4. Click 'Add SSH key'"
echo ""

read -p "Press Enter after adding key to GitHub..."

echo ""
echo "=================================================="
echo "🔍 Step 4: Testing Connection"
echo "=================================================="
echo ""

# Test SSH connection
echo "Testing connection to GitHub..."
ssh -T git@github.com

if [ $? -eq 1 ]; then
    echo ""
    echo "✅ SSH connection successful!"
    echo ""
    
    echo "=================================================="
    echo "🔧 Step 5: Updating Git Remote"
    echo "=================================================="
    echo ""
    
    cd /Users/buyhatke/Desktop/youtube_project
    
    if [ -d .git ]; then
        echo "Updating remote URL to use SSH..."
        git remote set-url origin git@github.com:LakshBuilds/youtube-scrapper-api-.git
        
        echo ""
        echo "Current remote:"
        git remote -v
        echo ""
        
        echo "=================================================="
        echo "✅ Setup Complete!"
        echo "=================================================="
        echo ""
        echo "You can now push to GitHub:"
        echo "  cd /Users/buyhatke/Desktop/youtube_project"
        echo "  git push origin main"
        echo ""
    else
        echo "⚠️  Not a git repository"
    fi
else
    echo ""
    echo "❌ SSH connection failed"
    echo ""
    echo "Try these troubleshooting steps:"
    echo "1. Make sure you added the key to GitHub"
    echo "2. Run: ssh-add ~/.ssh/id_ed25519"
    echo "3. Try again: ssh -T git@github.com"
    echo ""
fi

echo "=================================================="
echo "📖 For more help, see: SSH_KEY_SETUP_GUIDE.md"
echo "=================================================="
