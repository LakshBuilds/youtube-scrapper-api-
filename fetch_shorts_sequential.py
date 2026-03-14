import httpx
import json
import time
from typing import List, Dict, Any

# List of YouTube shorts URLs
urls = [
    "https://www.youtube.com/shorts/oXGX-UX9T1k",
    "https://youtube.com/shorts/H1E-b2lgbGA?si=jIVo2Sd3APbIcNE5",
    "https://youtube.com/shorts/SSYhsp0srgg?feature=share",
    "https://youtube.com/shorts/f9K8vbrqFSU?si=eTcqVtE3kiKk5d6f",
    "https://youtube.com/shorts/4yZ50Q5NHYA?si=r5mpOn65TfTLPEBY",
    "https://youtube.com/shorts/YjzEMWsUOAE?si=4hdS90g8wi6VP57O",
    "https://youtube.com/shorts/Xgae-sM4NS0?si=qJbEbE0HTXoSpIQ9",
    "https://youtube.com/shorts/6ph0A8pGle0?si=ud2JT1b_ksI2QylB",
    "https://youtube.com/shorts/1Cyy6-69Eyc?si=9Kkva6UJQB5foGDt",
    "https://youtube.com/shorts/sAFIFaJSfGQ?si=FnnA0ZXDBZPmvsjz",
    "https://youtube.com/shorts/YaBhPjChGRQ?si=MN_2hRqTCTofGgiU",
    "https://youtube.com/shorts/ZnJ7P1gqf6w?feature=share",
    "https://youtube.com/shorts/Msps2x2vfVM?si=qLw2v9qeVBRNCt9W",
    "https://youtube.com/shorts/dsVutiaddBI?si=zrjgToXAxspVSbqt",
    "https://youtube.com/shorts/dQek1OdXS9c?feature=share",
    "https://youtube.com/shorts/4QYqcmieix0?si=PQreij9bO8jNAgJV",
    "https://youtube.com/shorts/hIOl0REo2ug?si=f3kHCFeT4UVGG90F",
    "https://youtube.com/shorts/JJQv1WwwjeU?si=h1TOMlfyJ9jGA_fn",
    "https://youtube.com/shorts/Fdf_mEPswRU?si=3H3kCFRrxqiWFNM7",
    "https://youtube.com/shorts/fZ_z_t68BVk?si=1OHnI8ULDTCAaVAG",
    "https://youtube.com/shorts/e0R9ZdX59lI?si=hPD4Yvu7V-HNxI2q",
    "https://youtube.com/shorts/0SB0njXNz4A?si=MQme8-ORwEecJd_D",
    "https://youtube.com/shorts/m8ayG9PC7is?si=etnB0zoBSXCNuFAs",
    "https://youtube.com/shorts/TOoG9eoNzq4?si=xJcqFcwOmkSpht0w",
    "https://youtube.com/shorts/U_0TGnBVnT0?si=5lEiiUTcjDIhniH5",
    "https://youtube.com/shorts/Dt0ZEMyEj-Q?si=Rl21NQgmkSi76Zvl",
    "https://youtube.com/shorts/qzl6zbZ_heE?si=mJMqHXe2QXi60QuL",
    "https://youtube.com/shorts/cwneTIbotXY?si=1YGTD-qRstbbeFcx",
    "https://youtube.com/shorts/cwneTIbotXY?si=ONw-1cQwTeyJ9uHn",
    "https://youtube.com/shorts/o77fJzaODYo?si=M5amf0Lijw8kewS3",
    "https://youtube.com/shorts/-36ta3k3Mms?si=x_A3R2td-ZM5oN1x",
    "https://youtube.com/shorts/axlTYjjcMXg?si=6HPA_W27F9OrjWe3",
    "https://youtube.com/shorts/OAuIrZeUohg?si=spTY994ZLHPYJZnl",
    "https://youtube.com/shorts/RHupQkR6wvw?si=c28IUp8qTj4fZzvn",
    "https://youtube.com/shorts/wY7SZE6BQas?si=uw00w8r7bfklPVHh",
    "https://youtube.com/shorts/m0m9ipNnZ2g?si=XOF6aNXiIxicLqAE",
    "https://youtube.com/shorts/v-UlgJsZ-A4?si=KVrsA4kOpBqEoWsd",
    "https://youtube.com/shorts/iYa-ZYEviZA?si=pwVNrB1ZULQtF17h",
    "https://youtube.com/shorts/17rMlTafCkg?si=frZmBGpJroQ8cEsz",
    "https://youtube.com/shorts/zTNsphy7tFs?si=YYl65yUIq59bZkEn",
    "https://youtube.com/shorts/5p-Ble5Zzjc?si=U0WHeH9mhDKrKdPk",
    "https://youtube.com/shorts/LMb8to4jE_w?si=0Q1mtLZNGFBVq5h9",
    "https://youtube.com/shorts/ceLKSStcq1Q?si=Ow6LW9V65j9S1NQo",
    "https://youtube.com/shorts/HFFWZuLIPBM?si=JzkFLh7O2BnskZSx",
    "https://youtube.com/shorts/rZUR_ArFwOw?si=snvTDjPgHAEFsuu9",
    "https://youtube.com/shorts/zOedim4wXKs?si=051rffCW32NXyRP7",
    "https://youtube.com/shorts/AyKkDkEemrQ?si=FoItq_IpP-umdaNr",
    "https://youtube.com/shorts/ULPOjTCMG9E?si=oXyvdEuY9LDW2iSE",
    "https://youtube.com/shorts/hrQOT2uPU0o?si=dI4puvzLKkr1lPi-",
    "https://youtube.com/shorts/A7HllcBoAKA?si=Di85ggHhgYOoric3",
    "https://youtube.com/shorts/xgvE7AIhIb4?si=DJMKLVPeAGepl5JW",
    "https://youtube.com/shorts/QgpAM6Rz9D0?si=926jXkqC95qmoJ_V",
    "https://youtube.com/shorts/sd-PM0aaScQ?si=0eOdRY5X_ZhXO2DN",
    "https://youtube.com/shorts/YXEJEdwgug0?si=5EFFi3H7j50Ag2Kj",
    "https://youtube.com/shorts/F59hKB6NYfg?si=0oAkbjLO0DlkhfFM",
    "https://youtube.com/shorts/zNfLUb5-doc?si=UGnPO4__lGEKEzqn",
    "https://youtube.com/shorts/z3uLtkD55mY?si=BY51r0ua0e2rYRMP",
    "https://youtube.com/shorts/fDQIFIlQd_4?si=XHL4spW7mWjlI4iV",
    "https://youtube.com/shorts/p49yVN-ZXJ8?si=g33nODLlC-d7QGjB",
    "https://youtube.com/shorts/10t2x3BTW7I?si=3QOSTK6tihjXUSRt",
    "https://youtube.com/shorts/kHjmqbOD4LI?si=TqyYOt4YnKi80kG_",
    "https://youtube.com/shorts/rQAEwT1Am-4?si=ps8S--xRLyf-gMJ8",
    "https://youtube.com/shorts/vEyN7yqFZLI?si=jqOI1ywQy2ywYkga",
    "https://youtube.com/shorts/WWm7Kvf37sk?si=bJ_YfmACFXUAM7u-",
    "https://youtube.com/shorts/djdr6CgauUM?si=bZuocacvPmbDFGs_",
    "https://youtube.com/shorts/on0SDpc41Jc?si=8CtnNjBZrNiQtxJG",
    "https://youtube.com/shorts/5_lJsHdvAdM?si=2pQbip4vBvE06bSj",
    "https://youtube.com/shorts/E6XLzYbq-rE?si=ob-t6nV5ALAwC_MX",
    "https://youtube.com/shorts/NvBhOYBfiBQ?si=9wnwQkutfhpqa_ij",
    "https://youtube.com/shorts/oDnNOAihmx0?si=uaWFqxcdfUs6lhQ0",
    "https://youtube.com/shorts/2ZL55q0ugBs?si=Kd2i9FFud7FLB9fn",
    "https://www.youtube.com/shorts/_GTB9QU1JFo",
    "https://youtube.com/shorts/8VvfBMauVIY?si=YR4-jDNXCnI93GSQ",
    "https://youtube.com/shorts/ef3Nhv3PxTk?si=kJYkKcb03hN4_neS",
    "https://youtube.com/shorts/2RoQn-WbcBA?si=oW1Is00zJdlBHBrQ",
    "https://youtube.com/shorts/ky2WBd5c88M?si=DpmpfPtRbqgaZfxq",
    "https://youtube.com/shorts/qscPMza-Rk0?si=QgOtQPEw1ubg3X2I",
    "https://youtube.com/shorts/d-_PMGQ79HI?si=6IqQpxAuksIF2mch",
    "https://youtube.com/shorts/gskhrTJ-pzU?si=XjIJan7Dq3oHHXez",
    "https://youtube.com/shorts/DPJGSvtuWQY?feature=shared",
    "https://youtube.com/shorts/uS4E6XRdVI8?si=C1nfE5jCzncz1cLJ",
    "https://youtube.com/shorts/3A1-QEeizrY?si=qe9VRFPBFyjIa-bi",
    "https://youtube.com/shorts/FxShM1Tvkw0?si=N1m01WodF-sNeRZT",
    "https://youtube.com/shorts/I1vtKzpiU90?si=-8PrbANQZdFD-CU8",
    "https://youtube.com/shorts/-g9103sFiME?si=qdGp33Mp0H0iyzOY",
    "https://youtube.com/shorts/Pm1parjnS-0?si=XiQrcsfcyX11k6Nl",
    "https://youtube.com/shorts/UkKXzIYy-1o?si=PsLmyVK7yQRJN06L",
    "https://youtube.com/shorts/vr-ejDhrfHw?si=15gwo0s79lHvrHee",
    "https://youtube.com/shorts/TlNAbH8Buw8?si=ZWKxipRUl6rmYriY",
]

# API endpoint - using local API for accurate statistics
API_BASE_URL = "http://localhost:8001"
DELAY_SECONDS = 3  # Delay between requests (longer delay for accuracy)

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
            title = data.get('data', {}).get('snippet', {}).get('title', 'N/A')[:70]
            print(f"[{index + 1}/{len(urls)}] ✓ Success - {title}")
            return {
                "url": url,
                "status": "success",
                "data": data
            }
        else:
            print(f"[{index + 1}/{len(urls)}] ✗ Error {response.status_code}: {response.text[:100]}")
            return {
                "url": url,
                "status": "error",
                "error": f"HTTP {response.status_code}",
                "response": response.text[:500]
            }
    except Exception as e:
        print(f"[{index + 1}/{len(urls)}] ✗ Exception: {str(e)}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }

def main():
    print(f"Starting to fetch data for {len(urls)} YouTube shorts...")
    print(f"Using API: {API_BASE_URL}")
    print(f"Delay between requests: {DELAY_SECONDS} seconds\n")
    
    results = []
    
    with httpx.Client() as client:
        for i, url in enumerate(urls):
            result = fetch_video_data(client, url, i)
            results.append(result)
            
            # Add delay between requests (except for the last one)
            if i < len(urls) - 1:
                time.sleep(DELAY_SECONDS)
    
    # Save results to JSON file
    output_file = "shorts_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful
    
    print("\n" + "="*60)
    print(f"SUMMARY:")
    print(f"Total URLs: {len(urls)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nResults saved to: {output_file}")
    print("="*60)
    
    # Create a simplified CSV report
    csv_file = "shorts_summary.csv"
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write("URL,Video ID,Title,Channel,Views,Likes,Duration (seconds),Status\n")
        for result in results:
            if result["status"] == "success":
                data = result.get("data", {}).get("data", {})
                video_id = data.get("videoId", "N/A")
                snippet = data.get("snippet", {})
                stats = data.get("statistics", {})
                content = data.get("contentDetails", {})
                
                title = snippet.get("title", "N/A").replace('"', '""')
                channel = snippet.get("channelTitle", "N/A").replace('"', '""')
                views = stats.get("viewCount", "0")
                likes = stats.get("likeCount", "0")
                duration = content.get("durationSeconds", "0")
                
                f.write(f'"{result["url"]}",{video_id},"{title}","{channel}",{views},{likes},{duration},success\n')
            else:
                error_msg = result.get("error", "error").replace('"', '""')
                f.write(f'"{result["url"]}",N/A,N/A,N/A,0,0,0,"{error_msg}"\n')
    
    print(f"CSV summary saved to: {csv_file}\n")

if __name__ == "__main__":
    main()
