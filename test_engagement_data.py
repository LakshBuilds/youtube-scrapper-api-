#!/usr/bin/env python3
"""Test different methods to get likes and comments"""

import requests
import json
import re

video_id = "oXGX-UX9T1k"

print("🔬 Testing Engagement Data Extraction Methods\n")
print("="*70)

# Method 1: InnerTube "next" API
print("\n1️⃣ Testing InnerTube 'next' API for engagement...")
print("-"*70)

next_payload = {
    "videoId": video_id,
    "context": {
        "client": {
            "clientName": "WEB",
            "clientVersion": "2.20240304.00.00"
        }
    }
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.post(
        "https://www.youtube.com/youtubei/v1/next",
        json=next_payload,
        headers=headers,
        timeout=15
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Look for engagement in videoPrimaryInfoRenderer
        contents = data.get('contents', {}).get('twoColumnWatchNextResults', {}).get('results', {}).get('results', {}).get('contents', [])
        
        for content in contents:
            if 'videoPrimaryInfoRenderer' in content:
                renderer = content['videoPrimaryInfoRenderer']
                
                # Try to find like button
                menu = renderer.get('videoActions', {}).get('menuRenderer', {}).get('topLevelButtons', [])
                for button in menu:
                    if 'segmentedLikeDislikeButtonRenderer' in button:
                        like_btn = button['segmentedLikeDislikeButtonRenderer'].get('likeButton', {})
                        toggle_btn = like_btn.get('toggleButtonRenderer', {})
                        
                        # Look for text in different places
                        if 'defaultText' in toggle_btn:
                            like_text = toggle_btn['defaultText'].get('accessibility', {}).get('accessibilityData', {}).get('label', '')
                            print(f"✅ Found likes: {like_text}")
                        
                        if 'accessibilityData' in toggle_btn:
                            like_text = toggle_btn['accessibilityData'].get('accessibilityData', {}).get('label', '')
                            print(f"✅ Accessibility label: {like_text}")
        
        # Look for comments
        for content in contents:
            if 'itemSectionRenderer' in content:
                section = content['itemSectionRenderer'].get('contents', [])
                for item in section:
                    if 'commentsEntryPointHeaderRenderer' in item:
                        comment_renderer = item['commentsEntryPointHeaderRenderer']
                        comment_count = comment_renderer.get('commentCount', {}).get('simpleText', '0')
                        print(f"✅ Found comments: {comment_count}")
        
        # Save response for analysis
        with open('next_api_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Full response saved to: next_api_response.json")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Method 2: Scrape from webpage
print("\n" + "="*70)
print("\n2️⃣ Testing Webpage Scraping...")
print("-"*70)

try:
    response = requests.get(
        f"https://www.youtube.com/watch?v={video_id}",
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout=15
    )
    
    if response.status_code == 200:
        html = response.text
        
        # Method 2a: ytInitialData
        match = re.search(r'var ytInitialData = ({.+?});', html)
        if match:
            try:
                yt_data = json.loads(match.group(1))
                
                # Navigate to engagement data
                contents = yt_data.get('contents', {}).get('twoColumnWatchNextResults', {}).get('results', {}).get('results', {}).get('contents', [])
                
                for content in contents:
                    if 'videoPrimaryInfoRenderer' in content:
                        renderer = content['videoPrimaryInfoRenderer']
                        
                        # Get view count
                        view_count = renderer.get('viewCount', {}).get('videoViewCountRenderer', {}).get('viewCount', {}).get('simpleText', '0')
                        print(f"✅ Views from webpage: {view_count}")
                        
                        # Get likes from menu
                        menu = renderer.get('videoActions', {}).get('menuRenderer', {}).get('topLevelButtons', [])
                        for button in menu:
                            if 'segmentedLikeDislikeButtonRenderer' in button:
                                like_data = button['segmentedLikeDislikeButtonRenderer']
                                like_button = like_data.get('likeButton', {}).get('toggleButtonRenderer', {})
                                
                                # Try different text locations
                                default_text = like_button.get('defaultText', {})
                                if 'simpleText' in default_text:
                                    print(f"✅ Likes: {default_text['simpleText']}")
                                elif 'accessibility' in default_text:
                                    acc_label = default_text['accessibility'].get('accessibilityData', {}).get('label', '')
                                    # Extract number from "like this video along with 16 other people"
                                    nums = re.findall(r'\d+', acc_label)
                                    if nums:
                                        print(f"✅ Likes (parsed): {nums[0]}")
                
                # Get comments
                for content in contents:
                    if 'itemSectionRenderer' in content:
                        items = content['itemSectionRenderer'].get('contents', [])
                        for item in items:
                            if 'commentsEntryPointHeaderRenderer' in item:
                                comment_header = item['commentsEntryPointHeaderRenderer']
                                comment_count = comment_header.get('commentCount', {}).get('simpleText', '0')
                                print(f"✅ Comments: {comment_count}")
                
                # Save for analysis
                with open('ytInitialData.json', 'w') as f:
                    json.dump(yt_data, f, indent=2)
                print(f"\n💾 ytInitialData saved to: ytInitialData.json")
                
            except Exception as e:
                print(f"⚠️ Parse error: {str(e)}")
        else:
            print("❌ ytInitialData not found")
            
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE - Check JSON files for full data structure")
print("="*70)
