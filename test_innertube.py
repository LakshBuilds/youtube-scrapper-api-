#!/usr/bin/env python3
"""
Test InnerTube API directly (YouTube's internal API)
This is the most reliable method for deployed environments
"""

import httpx
import json
import asyncio
import random

async def test_innertube():
    video_id = "oXGX-UX9T1k"
    
    api_keys = [
        'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w',
    ]
    
    clients = [
        {
            "clientName": "ANDROID",
            "clientVersion": "19.09.37",
            "androidSdkVersion": 30,
            "userAgent": "com.google.android.youtube/19.09.37 (Linux; U; Android 11) gzip",
            "hl": "en",
            "gl": "US"
        },
        {
            "clientName": "IOS",
            "clientVersion": "19.09.3",
            "deviceMake": "Apple",
            "deviceModel": "iPhone14,3",
            "userAgent": "com.google.ios.youtube/19.09.3 (iPhone14,3; U; CPU iOS 15_6 like Mac OS X)",
            "hl": "en",
            "gl": "US"
        }
    ]
    
    print("🔬 Testing InnerTube API Methods...\n")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, client_config in enumerate(clients, 1):
            try:
                print(f"{'='*60}")
                print(f"Test {idx}: {client_config['clientName']} Client")
                print(f"{'='*60}")
                
                api_key = random.choice(api_keys)
                api_url = f"https://www.youtube.com/youtubei/v1/player?key={api_key}"
                
                payload = {
                    "videoId": video_id,
                    "context": {
                        "client": client_config
                    }
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': client_config['userAgent'],
                    'X-YouTube-Client-Name': '3' if client_config['clientName'] == 'ANDROID' else '5',
                    'X-YouTube-Client-Version': client_config['clientVersion'],
                    'Origin': 'https://www.youtube.com',
                    'Referer': f'https://www.youtube.com/watch?v={video_id}'
                }
                
                print(f"\n📤 Sending request to InnerTube API...")
                response = await client.post(api_url, json=payload, headers=headers)
                
                print(f"📥 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    video_details = data.get('videoDetails', {})
                    
                    title = video_details.get('title', 'N/A')
                    view_count = video_details.get('viewCount', '0')
                    author = video_details.get('author', 'N/A')
                    length = video_details.get('lengthSeconds', '0')
                    
                    print(f"\n✅ SUCCESS!")
                    print(f"   Title: {title}")
                    print(f"   Channel: {author}")
                    print(f"   Views: {view_count}")
                    print(f"   Duration: {length}s")
                    
                    if int(view_count) > 0:
                        print(f"\n🎉 JACKPOT! Got real statistics!")
                        print(f"\n📝 Full Response Preview:")
                        print(json.dumps({
                            'videoDetails': video_details,
                            'microformat': data.get('microformat', {})
                        }, indent=2)[:500] + "...")
                        return True
                    else:
                        print(f"\n⚠️ Views are 0 - trying next client...")
                else:
                    print(f"❌ Failed with status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print()
    
    print(f"\n{'='*60}")
    print("❌ All InnerTube methods failed")
    print(f"{'='*60}")
    return False

if __name__ == "__main__":
    result = asyncio.run(test_innertube())
    exit(0 if result else 1)
