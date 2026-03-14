import httpx
import json
import time
from typing import List, Dict, Any

# New batch of YouTube shorts URLs
urls = [
    "https://youtube.com/shorts/FxShM1Tvkw0",
    "https://youtube.com/shorts/I1vtKzpiU90",
    "https://youtube.com/shorts/-g9103sFiME",
    "https://youtube.com/shorts/Pm1parjnS-0",
    "https://youtube.com/shorts/UkKXzIYy-1o",
    "https://youtube.com/shorts/vr-ejDhrfHw",
    "https://youtube.com/shorts/TlNAbH8Buw8",
    "https://youtube.com/shorts/XF6OKFHYNow",
    "https://youtube.com/shorts/DjX9GQy0shs",
    "https://youtube.com/shorts/keJh0gZWxBs",
    "https://youtube.com/shorts/VKUHFtCOG54",
    "https://youtube.com/shorts/3Tej1MFanF4",
    "https://youtube.com/shorts/HI2Yg1u1pgg",
    "https://youtube.com/shorts/OR2bPGkAQxE",
    "https://youtube.com/shorts/-_81PRDUOeI",
    "https://youtube.com/shorts/VCbGoBE0chM",
    "https://youtube.com/shorts/OxTDb6V9hPY",
    "https://youtube.com/shorts/mwUJ47nbK7w",
    "https://youtube.com/shorts/ltYFAlA2Ncc",
    "https://youtube.com/shorts/xwgfeLX4EHs",
    "https://youtube.com/shorts/PCSEh6uhdls",
    "https://youtube.com/shorts/wLyHYMmRbNM",
    "https://youtube.com/shorts/2keFs0aJiSU",
    "https://youtube.com/shorts/W5RwaJiM9hI",
    "https://youtube.com/shorts/KJKN0pTPeow",
    "https://youtube.com/shorts/jJutxhN_pP4",
    "https://youtube.com/shorts/IeDFf7TJHbM",
    "https://youtube.com/shorts/xwGu7LdpPkI",
    "https://youtube.com/shorts/854HG-J1JBY",
    "https://youtube.com/shorts/hWskm7S_bl8",
    "https://youtube.com/shorts/p8pxHgUE5mA",
    "https://youtube.com/shorts/ExjtwpyBRlk",
    "https://youtube.com/shorts/0wFWYIIzudo",
    "https://youtube.com/shorts/ds4qOVc1rgo",
    "https://youtube.com/shorts/vzGk6P95Vfo",
    "https://youtube.com/shorts/hmqwI7Uu-PM",
    "https://youtube.com/shorts/idyC7QenOD4",
    "https://youtube.com/shorts/yivYzdkrkC0",
    "https://youtube.com/shorts/CakwI591FLk",
    "https://youtube.com/shorts/XkKC0WFvcvM",
    "https://youtube.com/shorts/MdRmMcT_JBg",
    "https://youtube.com/shorts/hHDoakCUREQ",
    "https://youtube.com/shorts/apADcRErzNk",
    "https://youtube.com/shorts/Idok52dlQ_A",
    "https://youtube.com/shorts/0a_IpYHkaTg",
]

# API endpoint
API_BASE_URL = "http://localhost:8001"
DELAY_SECONDS = 3

def fetch_video_data(client: httpx.Client, url: str, index: int) -> Dict[str, Any]:
    """Fetch data for a single video"""
    try:
        print(f"[{index + 1}/{len(urls)}] Fetching: {url}")
        response = client.get(
            f"{API_BASE_URL}/video",
            params={"url": url},
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            video_data = data.get('data', {})
            stats = video_data.get('statistics', {})
            snippet = video_data.get('snippet', {})
            
            title = snippet.get('title', 'N/A')[:70]
            views = stats.get('viewCount', '0')
            likes = stats.get('likeCount', '0')
            
            print(f"[{index + 1}/{len(urls)}] ✓ {title}")
            print(f"              👁️ {int(views):,} views | ❤️ {int(likes):,} likes")
            
            return {
                "url": url,
                "status": "success",
                "data": data
            }
        else:
            print(f"[{index + 1}/{len(urls)}] ✗ Error {response.status_code}")
            return {
                "url": url,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        print(f"[{index + 1}/{len(urls)}] ✗ Exception: {str(e)}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }

def main():
    print("="*80)
    print(f"FETCHING DATA FOR {len(urls)} NEW YOUTUBE SHORTS")
    print("="*80)
    print(f"API: {API_BASE_URL}")
    print(f"Delay: {DELAY_SECONDS} seconds between requests\n")
    
    results = []
    
    with httpx.Client() as client:
        for i, url in enumerate(urls):
            result = fetch_video_data(client, url, i)
            results.append(result)
            
            if i < len(urls) - 1:
                time.sleep(DELAY_SECONDS)
    
    # Calculate totals
    total_views = 0
    total_likes = 0
    total_comments = 0
    successful = 0
    
    for result in results:
        if result['status'] == 'success':
            successful += 1
            video_data = result['data']['data']
            stats = video_data.get('statistics', {})
            
            total_views += int(stats.get('viewCount', 0))
            total_likes += int(stats.get('likeCount', 0))
            total_comments += int(stats.get('commentCount', 0))
    
    # Save results
    with open("new_batch_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create CSV
    with open("new_batch_summary.csv", "w", encoding="utf-8") as f:
        f.write("URL,Video ID,Title,Channel,Views,Likes,Comments,Duration (seconds),Status\n")
        for result in results:
            if result['status'] == 'success':
                video_data = result['data']['data']
                video_id = video_data.get('videoId', 'N/A')
                snippet = video_data.get('snippet', {})
                stats = video_data.get('statistics', {})
                content = video_data.get('contentDetails', {})
                
                title = snippet.get('title', 'N/A').replace('"', '""')
                channel = snippet.get('channelTitle', 'N/A').replace('"', '""')
                views = stats.get('viewCount', '0')
                likes = stats.get('likeCount', '0')
                comments = stats.get('commentCount', '0')
                duration = content.get('durationSeconds', '0')
                
                f.write(f'"{result["url"]}",{video_id},"{title}","{channel}",{views},{likes},{comments},{duration},success\n')
    
    # Print summary
    print("\n" + "="*80)
    print("📊 SUMMARY FOR NEW BATCH")
    print("="*80)
    print(f"Total URLs:              {len(urls)}")
    print(f"Successful:              {successful}")
    print(f"Failed:                  {len(urls) - successful}")
    print()
    print(f"👁️  TOTAL VIEWS:          {total_views:,}")
    print(f"❤️  TOTAL LIKES:          {total_likes:,}")
    print(f"💬 TOTAL COMMENTS:       {total_comments:,}")
    print()
    if successful > 0:
        print(f"📈 AVERAGES:")
        print(f"Average Views:           {total_views // successful:,}")
        print(f"Average Likes:           {total_likes // successful:,}")
        print(f"Average Comments:        {total_comments // successful:,}")
    print()
    print(f"Files saved:")
    print(f"  • new_batch_data.json")
    print(f"  • new_batch_summary.csv")
    print("="*80)

if __name__ == "__main__":
    main()
