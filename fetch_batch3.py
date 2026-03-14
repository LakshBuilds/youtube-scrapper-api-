import httpx
import json
import time
from typing import List, Dict, Any

# Batch 3 of YouTube shorts URLs
urls = [
    "https://youtube.com/shorts/tDADgC9ROyM?si=rFq9L9RMaisfkPMD",
    "https://youtube.com/shorts/p-tPhiviEGQ?si=wXHBvy62y4b1HrYJ",
    "https://youtube.com/shorts/IeDFf7TJHbM?si=J2t26cAV_pk1Yyiz",
    "https://youtube.com/shorts/xwGu7LdpPkI?si=WEy7UBFKqTpAqNi8",
    "https://youtube.com/shorts/p8pxHgUE5mA?si=LN8hr3iOtXNN4J_P",
    "https://youtube.com/shorts/apADcRErzNk?si=ql3tq_pyKSowwQ9I",
    "https://youtube.com/shorts/0a_IpYHkaTg?si=dEfI1kaK9qpDLNpG",
    "https://youtube.com/shorts/OiYSpWI6GTg?si=3rYvrRRRR2-kEh7Q",
    "https://youtube.com/shorts/nU2fhaTsYKw?si=n2-OnnG1v3EfnNvp",
    "https://youtube.com/shorts/sPdMhpV9of4?si=ptcWU8l74P1Dby8Z",
    "https://youtube.com/shorts/854HG-J1JBY?si=MPiqrPo0U04R-dTN",
    "https://youtube.com/shorts/hWskm7S_bl8?si=mLQgWKlKRsRHLSNA",
    "https://youtube.com/shorts/ExjtwpyBRlk?si=tISoDQvibU_YHU8s",
    "https://youtube.com/shorts/0wFWYIIzudo?si=2INmCqLTXSpA9RcZ",
    "https://youtube.com/shorts/ds4qOVc1rgo?si=xYNUEKFi3bplYPtM",
    "https://youtube.com/shorts/vzGk6P95Vfo?si=hBxbDHwYx5t0wuqr",
    "https://youtube.com/shorts/hmqwI7Uu-PM?si=t9Esdt7xMLJN5zPs",
    "https://youtube.com/shorts/idyC7QenOD4?si=eVMeqbd9pmO_T2Ao",
    "https://youtube.com/shorts/yivYzdkrkC0?si=fWEbtuotDPnvmr3Q",
    "https://youtube.com/shorts/CakwI591FLk?si=q8sThADLSNE21-7s",
    "https://youtube.com/shorts/Idok52dlQ_A?si=ovoWxcW7qhTRbd3g",
    "https://youtube.com/shorts/r3BwIh7XDqY?si=aHdAACGSildutidZ",
    "https://youtube.com/shorts/Be64fjoRbU0?si=yPTmZ64hS6WVGRon",
    "https://youtube.com/shorts/ZQ7gfMfXzhU?si=cN7gXDMwpuY0Lxqm",
    "https://youtube.com/shorts/uZCUNertG24?si=X5Bto84J1xJS_IOz",
    "https://youtube.com/shorts/UVd0-CTgzKg?si=DjHFLr-Cx6MZJ8O_",
    "https://youtube.com/shorts/sFfiOTMS-Ic?si=2_Tl4ld5GsSauzSR",
    "https://youtube.com/shorts/KmWu0kq0UdI?si=7dtyuetQYtwIGegj",
    "https://youtube.com/shorts/ITsAcFz9bPQ?si=kVjIbYjI6IK2b0Y7",
    "https://youtube.com/shorts/3XKgMErMZ20?si=Y8HNq-3FkUe9WoC2",
    "https://youtube.com/shorts/1K75bhQPLY4?si=_r21jQU0oY5SomE9",
    "https://youtube.com/shorts/tsP-Le7Ucng?si=MBRC4QhZ2Y64Q2cK",
    "https://youtube.com/shorts/bnl1VXioa54?si=1QMm7gZL6eGMZrNe",
    "https://youtube.com/shorts/IKVxqu5PAec?si=1B7u8HS2jGe1qgiJ",
    "https://youtube.com/shorts/VhfAD7H2An0?si=YtrYhJvl6KJJ33oC",
    "https://youtube.com/shorts/w4wb00RHN9U?si=TpDVrjJWKBW1wMD0",
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
            comments = stats.get('commentCount', '0')
            
            print(f"[{index + 1}/{len(urls)}] ✓ {title}")
            print(f"              👁️ {int(views):,} views | ❤️ {int(likes):,} likes | 💬 {int(comments):,} comments")
            
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
    print(f"FETCHING DATA FOR BATCH 3: {len(urls)} YOUTUBE SHORTS")
    print("="*80)
    print(f"API: {API_BASE_URL}\n")
    
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
    with open("batch3_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create CSV
    with open("batch3_summary.csv", "w", encoding="utf-8") as f:
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
    print("📊 BATCH 3 SUMMARY")
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
    print(f"  • batch3_data.json")
    print(f"  • batch3_summary.csv")
    print("="*80)

if __name__ == "__main__":
    main()
