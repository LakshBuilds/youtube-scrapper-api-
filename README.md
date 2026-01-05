# YouTube Scraper API

A FastAPI-based internal API to scrape YouTube video and shorts metadata.

## Features

- Scrape metadata from YouTube videos and Shorts
- Returns comprehensive data including:
  - Video snippet (title, description, thumbnails, channel info)
  - Statistics (views, likes, comments)
  - Content details (duration, definition, captions)
  - Channel information with URL
  - Player embed HTML

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LakshBuilds/youtube-scrapper-api-.git
cd youtube-scrapper-api-
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/video?url=<youtube_url>` | Get video data via query param |
| POST | `/video` | Get video data via JSON body |

### Example Requests:

**GET Request:**
```bash
curl "http://localhost:8000/video?url=https://www.youtube.com/watch?v=VIDEO_ID"
```

**POST Request:**
```bash
curl -X POST "http://localhost:8000/video" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/shorts/VIDEO_ID"}'
```

### Example Response:
```json
{
  "success": true,
  "data": {
    "videoId": "VIDEO_ID",
    "isShort": false,
    "snippet": {
      "publishedAt": "2024-11-05T00:00:00Z",
      "channelId": "CHANNEL_ID",
      "channelUrl": "https://www.youtube.com/channel/CHANNEL_ID",
      "title": "Video Title",
      "description": "Video description...",
      "thumbnails": {...},
      "channelTitle": "Channel Name",
      "tags": [...]
    },
    "statistics": {
      "viewCount": "12345",
      "likeCount": "678",
      "commentCount": "90"
    },
    "contentDetails": {
      "duration": "PT10M30S",
      "durationSeconds": 630,
      "definition": "hd"
    },
    "channel": {
      "id": "CHANNEL_ID",
      "title": "Channel Name",
      "subscriberCount": "1000"
    }
  }
}
```

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Tech Stack

- **FastAPI** - Web framework
- **yt-dlp** - YouTube data extraction
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## License

MIT
