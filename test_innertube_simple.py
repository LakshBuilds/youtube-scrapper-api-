#!/usr/bin/env python3
"""Test YouTube InnerTube API - Direct method"""

import requests
import json

video_id = "oXGX-UX9T1k"

# Method 1: Android TV (works best on servers)
payload = {
    "videoId": video_id,
    "context": {
        "client": {
            "clientName": "ANDROID_TESTSUITE",
            "clientVersion": "1.9",
            "androidSdkVersion": 30,
            "hl": "en",
            "gl": "US"
        }
    }
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'com.google.android.youtube/1.9 (Linux; U; Android 11)',
}

url = "https://www.youtube.com/youtubei/v1/player"

print("🔬 Testing InnerTube API (ANDROID_TESTSUITE)...\n")
response = requests.post(url, json=payload, headers=headers, timeout=20)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    vd = data.get('videoDetails', {})
    
    print(f"\n✅ SUCCESS!\n")
    print(f"Title: {vd.get('title')}")
    print(f"Channel: {vd.get('author')}")
    print(f"📊 Views: {vd.get('viewCount', '0')}")
    print(f"⏱️ Duration: {vd.get('lengthSeconds')}s")
    print(f"🆔 Channel ID: {vd.get('channelId')}")
else:
    print(f"\n❌ Failed")
    print(response.text[:200])
