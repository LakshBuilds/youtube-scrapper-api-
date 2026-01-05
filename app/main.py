from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import yt_dlp
import re
from datetime import datetime

app = FastAPI(
    title="YouTube Video Scraper API",
    description="Internal API to scrape YouTube video/shorts metadata",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str


class VideoResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_duration(seconds: int) -> str:
    """Convert seconds to ISO 8601 duration format (PT#H#M#S)"""
    if not seconds:
        return "PT0S"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    duration = "PT"
    if hours:
        duration += f"{hours}H"
    if minutes:
        duration += f"{minutes}M"
    if secs or (not hours and not minutes):
        duration += f"{secs}S"
    
    return duration


def get_thumbnail_urls(video_id: str) -> Dict[str, Dict[str, Any]]:
    """Generate thumbnail URLs for all sizes"""
    return {
        "default": {
            "url": f"https://i.ytimg.com/vi/{video_id}/default.jpg",
            "width": 120,
            "height": 90
        },
        "medium": {
            "url": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
            "width": 320,
            "height": 180
        },
        "high": {
            "url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            "width": 480,
            "height": 360
        },
        "standard": {
            "url": f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg",
            "width": 640,
            "height": 480
        },
        "maxres": {
            "url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
            "width": 1280,
            "height": 720
        }
    }


def scrape_youtube_video(url: str) -> Dict[str, Any]:
    """Scrape YouTube video data using yt-dlp"""
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    # Determine if it's a short
    is_short = '/shorts/' in url or (info.get('duration', 0) and info.get('duration', 0) <= 60)
    
    # Format upload date
    upload_date = info.get('upload_date', '')
    if upload_date:
        try:
            formatted_date = datetime.strptime(upload_date, '%Y%m%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            formatted_date = upload_date
    else:
        formatted_date = None
    
    # Build channel URL
    channel_id = info.get('channel_id', '')
    channel_url = info.get('channel_url', '') or (f"https://www.youtube.com/channel/{channel_id}" if channel_id else '')
    
    # Build response structure matching YouTube Data API format
    response = {
        "videoId": video_id,
        "isShort": is_short,
        "snippet": {
            "publishedAt": formatted_date,
            "channelId": channel_id,
            "channelUrl": channel_url,
            "title": info.get('title', ''),
            "description": info.get('description', ''),
            "thumbnails": get_thumbnail_urls(video_id),
            "channelTitle": info.get('channel', '') or info.get('uploader', ''),
            "categoryId": str(info.get('categories', [''])[0]) if info.get('categories') else None,
            "liveBroadcastContent": "live" if info.get('is_live') else "none",
            "defaultLanguage": info.get('language', None),
            "localized": {
                "title": info.get('title', ''),
                "description": info.get('description', '')
            },
            "defaultAudioLanguage": info.get('language', None),
            "tags": info.get('tags', [])
        },
        "statistics": {
            "viewCount": str(info.get('view_count', 0) or 0),
            "likeCount": str(info.get('like_count', 0) or 0),
            "favoriteCount": "0",
            "commentCount": str(info.get('comment_count', 0) or 0)
        },
        "status": {
            "uploadStatus": "processed",
            "privacyStatus": "public" if info.get('availability') == 'public' else info.get('availability', 'public'),
            "license": "youtube",
            "embeddable": True,
            "publicStatsViewable": True,
            "madeForKids": info.get('is_age_restricted', False) == False
        },
        "contentDetails": {
            "duration": format_duration(info.get('duration', 0)),
            "durationSeconds": info.get('duration', 0),
            "dimension": "2d",
            "definition": "hd" if info.get('height', 0) >= 720 else "sd",
            "caption": str(bool(info.get('subtitles') or info.get('automatic_captions'))).lower(),
            "licensedContent": True,
            "contentRating": {},
            "projection": "rectangular"
        },
        "player": {
            "embedHtml": f'<iframe width="480" height="270" src="//www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
        },
        "channel": {
            "id": info.get('channel_id', ''),
            "title": info.get('channel', '') or info.get('uploader', ''),
            "customUrl": info.get('uploader_url', ''),
            "subscriberCount": str(info.get('channel_follower_count', 0) or 0),
            "thumbnails": {
                "default": {
                    "url": info.get('channel_thumbnail', '') or '',
                    "width": 88,
                    "height": 88
                }
            }
        },
        "additionalInfo": {
            "ageRestricted": info.get('age_limit', 0) > 0,
            "availableCountries": info.get('availability', None),
            "webpage_url": info.get('webpage_url', ''),
            "originalUrl": url
        }
    }
    
    return response


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "YouTube Video Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "GET /video": "Get video data by URL query parameter",
            "POST /video": "Get video data by URL in request body",
            "GET /health": "Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/video", response_model=VideoResponse)
async def get_video_by_query(url: str = Query(..., description="YouTube video or shorts URL")):
    """
    Get YouTube video metadata by URL query parameter
    
    Example: /video?url=https://www.youtube.com/watch?v=VIDEO_ID
    """
    try:
        data = scrape_youtube_video(url)
        return VideoResponse(success=True, data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape video: {str(e)}")


@app.post("/video", response_model=VideoResponse)
async def get_video_by_body(request: VideoRequest):
    """
    Get YouTube video metadata by URL in request body
    
    Request body: {"url": "https://www.youtube.com/watch?v=VIDEO_ID"}
    """
    try:
        data = scrape_youtube_video(request.url)
        return VideoResponse(success=True, data=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape video: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
