# YouTube Automation Web Application Architecture

## Overview

This document outlines the architecture for the YouTube Automation web application, which provides a user-friendly interface to manage AI-generated music videos on YouTube.

## Technology Stack

- **Frontend**: Next.js with Tailwind CSS
- **Backend**: Next.js API routes + Cloudflare Workers
- **Database**: Cloudflare D1 (SQLite-compatible)
- **Storage**: Cloudflare R2 (S3-compatible)
- **Authentication**: Clerk.js
- **Deployment**: Cloudflare Pages

## System Components

### 1. User Interface Layer

- **Dashboard**: Main control panel for monitoring channel performance
- **Upload Interface**: For uploading AI-generated music files
- **Video Manager**: For managing generated videos and uploads
- **Analytics Dashboard**: For viewing performance metrics
- **Settings Panel**: For configuring automation parameters

### 2. API Layer

- **Authentication API**: User authentication and session management
- **Upload API**: Handling file uploads and processing
- **YouTube API Integration**: Managing YouTube channel operations
- **Analytics API**: Retrieving and processing performance data
- **Settings API**: Managing user preferences and system configuration

### 3. Service Layer

- **Video Generation Service**: Creates videos from audio files
- **Upload Scheduler Service**: Manages optimal upload timing
- **Promotion Service**: Handles cross-platform promotion
- **Analytics Service**: Processes performance data
- **Notification Service**: Manages user notifications

### 4. Data Layer

- **User Database**: Stores user accounts and preferences
- **Media Database**: Tracks uploaded audio and generated videos
- **Analytics Database**: Stores performance metrics and trends
- **Configuration Database**: Stores system and user settings

### 5. Storage Layer

- **Audio Storage**: For uploaded audio files
- **Video Storage**: For generated video files
- **Thumbnail Storage**: For generated thumbnails
- **Dashboard Storage**: For analytics dashboards and reports

## Data Flow

1. **User Authentication Flow**:
   - User logs in → Authentication API → User Database → Dashboard

2. **Upload Flow**:
   - User uploads audio → Upload API → Audio Storage → Video Generation Service → Video Storage → Upload Scheduler Service → YouTube API

3. **Analytics Flow**:
   - YouTube API → Analytics Service → Analytics Database → Analytics Dashboard

4. **Notification Flow**:
   - System events → Notification Service → User Interface

## Integration with Existing YouTube Automation System

The existing YouTube automation system will be integrated as follows:

1. **Video Generator**: Integrated as a service accessible via API
2. **Upload Manager**: Integrated as a service with database persistence
3. **Promotion System**: Integrated as a background service
4. **Analytics System**: Integrated as a service with dashboard generation

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  youtube_credentials TEXT,
  settings TEXT
);
```

### Audio Files Table
```sql
CREATE TABLE audio_files (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  status TEXT NOT NULL,
  metadata TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Videos Table
```sql
CREATE TABLE videos (
  id TEXT PRIMARY KEY,
  audio_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  youtube_id TEXT,
  title TEXT NOT NULL,
  description TEXT,
  thumbnail_path TEXT,
  video_path TEXT NOT NULL,
  status TEXT NOT NULL,
  upload_time TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (audio_id) REFERENCES audio_files(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Analytics Table
```sql
CREATE TABLE analytics (
  id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL,
  views INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  watch_time INTEGER DEFAULT 0,
  data TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (video_id) REFERENCES videos(id)
);
```

### Promotions Table
```sql
CREATE TABLE promotions (
  id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  status TEXT NOT NULL,
  post_id TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (video_id) REFERENCES videos(id)
);
```

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user

### Upload Endpoints
- `POST /api/upload/audio` - Upload audio file
- `GET /api/upload/status/:id` - Get upload status
- `GET /api/upload/list` - List uploaded files

### Video Endpoints
- `GET /api/videos` - List all videos
- `GET /api/videos/:id` - Get video details
- `POST /api/videos/generate` - Generate video from audio
- `POST /api/videos/upload/:id` - Upload video to YouTube
- `DELETE /api/videos/:id` - Delete video

### Analytics Endpoints
- `GET /api/analytics/channel` - Get channel analytics
- `GET /api/analytics/videos` - Get videos analytics
- `GET /api/analytics/video/:id` - Get specific video analytics
- `GET /api/analytics/trends` - Get trend analysis

### Settings Endpoints
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update user settings
- `POST /api/settings/youtube` - Connect YouTube account

## Security Considerations

1. **Authentication**: JWT-based authentication with Clerk.js
2. **Authorization**: Role-based access control
3. **Data Protection**: Encryption of sensitive data
4. **API Security**: Rate limiting and CORS protection
5. **YouTube Credentials**: Secure storage of OAuth tokens

## Deployment Architecture

1. **Frontend**: Deployed on Cloudflare Pages
2. **Backend**: Deployed as Cloudflare Workers
3. **Database**: Cloudflare D1
4. **Storage**: Cloudflare R2
5. **CI/CD**: GitHub Actions for automated deployment

## Scalability Considerations

1. **Horizontal Scaling**: Multiple worker instances
2. **Queue System**: For processing large numbers of videos
3. **Caching**: For frequently accessed data
4. **Rate Limiting**: To prevent API abuse
5. **Background Processing**: For time-consuming tasks

## Monitoring and Logging

1. **Application Logs**: Stored in Cloudflare
2. **Error Tracking**: Integrated with error reporting service
3. **Performance Monitoring**: Dashboard for system performance
4. **User Activity Tracking**: For usage analytics
5. **Audit Logs**: For security monitoring
