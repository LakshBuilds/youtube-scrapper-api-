#!/bin/bash
# Monitor Render deployment and test statistics

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🔍 RENDER DEPLOYMENT STATUS CHECKER                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

API_URL="https://youtube-scrapper-api.onrender.com"
TEST_VIDEO="https://youtube.com/shorts/oXGX-UX9T1k"

echo "⏰ Waiting for Render auto-deploy (typically 3-5 minutes)..."
echo ""

for i in {1..10}; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔄 Check #$i at $(date '+%H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Test health endpoint
    echo "1️⃣ Health Check..."
    HEALTH=$(curl -s "$API_URL/health" --max-time 10 2>&1)
    if echo "$HEALTH" | grep -q "status"; then
        echo "   ✅ API is online"
        VERSION=$(echo "$HEALTH" | python3 -c "import sys, json; print(json.load(sys.stdin).get('version', 'unknown'))" 2>/dev/null || echo "unknown")
        echo "   📦 Version: $VERSION"
    else
        echo "   ❌ API not responding"
        echo ""
        echo "⏳ Waiting 30 seconds before next check..."
        sleep 30
        continue
    fi
    
    # Test video endpoint
    echo ""
    echo "2️⃣ Testing Video Extraction..."
    RESULT=$(curl -s "$API_URL/video?url=$TEST_VIDEO" --max-time 15 2>&1)
    
    if echo "$RESULT" | grep -q "videoId"; then
        echo "   ✅ Video endpoint working"
        
        # Extract statistics
        VIEWS=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['statistics']['viewCount'])" 2>/dev/null || echo "0")
        LIKES=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['statistics']['likeCount'])" 2>/dev/null || echo "0")
        COMMENTS=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['statistics']['commentCount'])" 2>/dev/null || echo "0")
        METHOD=$(echo "$RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data'].get('additionalInfo',{}).get('extractionMethod', 'unknown'))" 2>/dev/null || echo "unknown")
        
        echo ""
        echo "   📊 STATISTICS:"
        echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "   📈 Views:    $VIEWS"
        echo "   👍 Likes:    $LIKES"
        echo "   💬 Comments: $COMMENTS"
        echo "   🔧 Method:   $METHOD"
        
        if [ "$VIEWS" != "0" ] && [ "$VIEWS" != "" ]; then
            echo ""
            echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "   🎉 SUCCESS! Statistics working!"
            echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "╔════════════════════════════════════════════════════════════════╗"
            echo "║              ✅ DEPLOYMENT SUCCESSFUL                          ║"
            echo "║         InnerTube API is working on Render!                    ║"
            echo "╚════════════════════════════════════════════════════════════════╝"
            exit 0
        else
            echo ""
            echo "   ⚠️  Still getting 0 views - old version may be cached"
        fi
    else
        echo "   ❌ Video endpoint failed"
    fi
    
    echo ""
    echo "⏳ Waiting 30 seconds before next check..."
    echo ""
    sleep 30
done

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ⏱️ TIMEOUT - Manual check required                ║"
echo "║  Deployment may take longer. Check Render dashboard logs.      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
