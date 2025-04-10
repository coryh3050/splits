# User Guide: YouTube Automation for AI-Generated Music

This guide provides detailed instructions on how to use the YouTube Automation system for managing a channel featuring AI-generated music.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Preparing Your Music](#preparing-your-music)
3. [System Configuration](#system-configuration)
4. [Running the System](#running-the-system)
5. [Monitoring Your Channel](#monitoring-your-channel)
6. [Understanding Analytics](#understanding-analytics)
7. [Optimizing Performance](#optimizing-performance)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

Before using the system, ensure you have:

- A YouTube channel with good standing
- Google account with access to YouTube API
- AI-generated music files ready for upload
- A computer or server that meets the [system requirements](README.md#system-requirements)

### First-Time Setup

1. **Install the system** following the [installation instructions](README.md#installation)

2. **Set up YouTube API access**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download the client secrets file and save as `client_secret.json` in the project root

3. **Initial configuration**:
   - Run the system once to generate the default configuration:
     ```
     python src/main.py
     ```
   - This will create a `config.json` file that you can customize

4. **Authentication**:
   - The first time you run the system, it will prompt for YouTube authentication
   - Follow the instructions to authorize the application
   - The system will save the credentials for future use

## Preparing Your Music

### Audio File Requirements

- **Supported formats**: MP3, WAV, FLAC, OGG
- **Recommended quality**: 320kbps for MP3, 16-bit/44.1kHz for WAV
- **File naming**: Use descriptive names with underscores instead of spaces
  - Example: `Dark_Thoughts_Instrumental.mp3`

### File Organization

1. Place all your AI-generated music files in the `input` directory
2. The system will automatically process files in this directory
3. After processing, files are moved to `input/processed` to avoid duplication

### Metadata Preparation

While the system automatically generates metadata, you can influence it by:

- Using descriptive file names that will be converted to video titles
- Creating a metadata.json file alongside your audio file with the same base name
  - Example: For `Dark_Thoughts_Instrumental.mp3`, create `Dark_Thoughts_Instrumental.json`

Example metadata.json:
```json
{
  "title_prefix": "LEAKED",
  "artist": "Kendrick Lamar",
  "year": "2025",
  "custom_tags": ["unreleased", "rare", "exclusive"]
}
```

## System Configuration

### Configuration File Structure

The `config.json` file controls all aspects of the system. Key sections include:

#### General Settings

```json
"general": {
  "working_dir": "/path/to/working/directory",
  "input_dir": "input",
  "output_dir": "output",
  "temp_dir": "temp",
  "data_dir": "data"
}
```

- `working_dir`: Base directory for all operations
- `input_dir`: Directory for audio files (relative to working_dir)
- `output_dir`: Directory for generated videos and thumbnails
- `temp_dir`: Directory for temporary processing files
- `data_dir`: Directory for system state and analytics data

#### Video Generator Settings

```json
"video_generator": {
  "resolution": "1080p",
  "fps": 30,
  "transition_style": "beat_sync",
  "visual_effects": ["zoom", "pulse", "glitch"],
  "color_scheme": "high_contrast"
}
```

- `resolution`: Video resolution (720p, 1080p, 1440p, 2160p)
- `fps`: Frames per second (24, 30, 60)
- `transition_style`: Visual transition style (beat_sync, smooth, cut, fade)
- `visual_effects`: List of effects to apply
- `color_scheme`: Color palette for visualizations

#### Uploader Settings

```json
"uploader": {
  "schedule_strategy": "optimal_time",
  "upload_frequency": "daily",
  "max_daily_uploads": 1,
  "client_secrets_file": "client_secret.json",
  "credentials_file": "youtube_credentials.json"
}
```

- `schedule_strategy`: How to schedule uploads (optimal_time, fixed_time, immediate)
- `upload_frequency`: How often to upload (daily, alternate_days, weekly)
- `max_daily_uploads`: Maximum uploads per day
- `client_secrets_file`: Path to YouTube API credentials
- `credentials_file`: Path to save authentication tokens

#### Promotion Settings

```json
"promotion": {
  "platforms": ["twitter", "reddit", "tiktok"],
  "comment_response_rate": 0.7,
  "auto_engagement": true,
  "notification_frequency": "daily"
}
```

- `platforms`: Social media platforms for promotion
- `comment_response_rate`: Percentage of comments to respond to (0.0-1.0)
- `auto_engagement`: Whether to automatically engage with comments
- `notification_frequency`: How often to send performance notifications

#### Analytics Settings

```json
"analytics": {
  "data_window_days": 30,
  "update_frequency": 24,
  "viral_threshold": 10000,
  "dashboard_types": ["channel", "videos", "trends", "audience"]
}
```

- `data_window_days`: Number of days to include in analysis
- `update_frequency`: How often to update analytics (hours)
- `viral_threshold`: View count to consider a video viral
- `dashboard_types`: Types of dashboards to generate

#### Automation Settings

```json
"automation": {
  "process_frequency": 1,
  "upload_time_slots": ["15:00", "18:00", "21:00"],
  "promotion_delay": 15,
  "analysis_frequency": 24
}
```

- `process_frequency`: How often to check for new files (hours)
- `upload_time_slots`: Preferred upload times (24-hour format)
- `promotion_delay`: Minutes to wait after upload before promoting
- `analysis_frequency`: How often to run analytics (hours)

### Recommended Configurations

#### For Maximum Virality

```json
{
  "video_generator": {
    "resolution": "1080p",
    "transition_style": "beat_sync",
    "visual_effects": ["zoom", "pulse", "glitch", "text_overlay"],
    "color_scheme": "high_contrast"
  },
  "uploader": {
    "schedule_strategy": "optimal_time",
    "upload_frequency": "daily"
  },
  "promotion": {
    "platforms": ["twitter", "reddit", "tiktok", "instagram"],
    "comment_response_rate": 0.9,
    "auto_engagement": true
  },
  "automation": {
    "upload_time_slots": ["15:00", "18:00", "21:00"]
  }
}
```

#### For Resource Efficiency

```json
{
  "video_generator": {
    "resolution": "720p",
    "fps": 24,
    "visual_effects": ["pulse"],
    "color_scheme": "simple"
  },
  "uploader": {
    "schedule_strategy": "fixed_time",
    "upload_frequency": "alternate_days"
  },
  "promotion": {
    "platforms": ["twitter"],
    "comment_response_rate": 0.5
  },
  "automation": {
    "process_frequency": 6,
    "analysis_frequency": 48
  }
}
```

## Running the System

### Starting the System

To start the automation system:

```
python src/main.py
```

This will:
1. Process any new audio files in the input directory
2. Schedule uploads according to your configuration
3. Start the promotion and analytics processes
4. Run continuously until stopped

### Running in Background

#### On Linux/macOS:

Using nohup:
```
nohup python src/main.py > automation.log 2>&1 &
```

Using screen:
```
screen -S youtube-automation
python src/main.py
# Press Ctrl+A, then D to detach
```

To reattach:
```
screen -r youtube-automation
```

#### On Windows:

Create a batch file (run.bat):
```
@echo off
start /B pythonw src/main.py > automation.log 2>&1
```

### Command Line Options

```
python src/main.py --help
```

Available options:
- `--config PATH`: Specify a custom configuration file
- `--status`: Print current system status and exit
- `--detailed`: Print detailed system status and exit

### Stopping the System

To stop the system:
- If running in the foreground: Press Ctrl+C
- If running in the background:
  - Find the process ID: `ps aux | grep main.py`
  - Stop the process: `kill [PID]`

## Monitoring Your Channel

### System Status

Check the current status:

```
python src/main.py --status
```

This shows:
- Current system state
- Number of videos processed
- Pending uploads
- Active promotions
- Last upload/promotion/analysis times
- Error count

For more detailed information:

```
python src/main.py --detailed
```

### Log Files

The system generates several log files:

- `youtube_automation.log`: Main system log
- `video_generator.log`: Video creation logs
- `youtube_uploader.log`: Upload process logs
- `social_media.log`: Promotion activity logs
- `comment_engagement.log`: Comment interaction logs
- `youtube_analytics.log`: Analytics processing logs

### Performance Dashboards

The system generates visual dashboards in the `dashboards` directory:

- `channel_dashboard.png`: Overall channel performance
- `videos_dashboard.png`: Individual video performance
- `trends_dashboard.png`: Content trend analysis
- `audience_dashboard.png`: Audience demographics

These are updated according to the `update_frequency` setting.

## Understanding Analytics

### Key Metrics

The system tracks several key metrics:

1. **View Performance**:
   - Total views
   - View growth rate
   - Views per video

2. **Engagement Metrics**:
   - Like-to-view ratio
   - Comment-to-view ratio
   - Average watch time
   - Audience retention

3. **Growth Metrics**:
   - Subscriber growth
   - Returning viewers percentage
   - Channel reach

4. **Content Performance**:
   - Best performing video types
   - Optimal video length
   - Most engaging thumbnails
   - Title pattern effectiveness

### Interpreting Dashboards

#### Channel Dashboard

The channel dashboard shows:
- Views over time with trend line
- Subscriber growth/loss
- Engagement metrics comparison
- Watch time distribution

Look for:
- Upward trends in views and subscribers
- High engagement rates (>5%)
- Consistent watch time growth

#### Videos Dashboard

The videos dashboard shows:
- Top videos by views
- Engagement comparison across videos
- Performance by video type
- View velocity (views per hour after publishing)

Look for:
- Videos with high engagement but low views (potential for promotion)
- Videos with high initial velocity (viral potential)
- Common elements in top-performing videos

#### Trends Dashboard

The trends dashboard shows:
- Content trend analysis
- Trending topics in your niche
- Optimal video characteristics
- Performance prediction for future content

Use this to:
- Identify emerging trends
- Optimize future content
- Adjust promotion strategies

#### Audience Dashboard

The audience dashboard shows:
- Age and gender distribution
- Geographic distribution
- Traffic sources
- Viewing patterns

Use this to:
- Target content to your audience
- Schedule uploads for peak viewing times
- Optimize for specific demographics

## Optimizing Performance

### Content Optimization

Based on analytics, you can optimize your content by:

1. **Title Optimization**:
   - Use patterns identified in trend analysis
   - Include viral keywords ("LEAKED", "UNRELEASED", etc.)
   - Keep titles under 60 characters

2. **Thumbnail Optimization**:
   - Use high contrast colors
   - Include text overlays with viral keywords
   - Feature attention-grabbing elements

3. **Video Optimization**:
   - Adjust video length to match optimal duration
   - Use visual effects that drive engagement
   - Sync transitions to beat drops

4. **Description Optimization**:
   - Include timestamps for key moments
   - Add calls to action
   - Use trending keywords and hashtags

### Promotion Optimization

Improve your promotion strategy by:

1. **Platform Focus**:
   - Concentrate on platforms with highest conversion
   - Adjust posting times based on platform analytics
   - Customize content for each platform

2. **Comment Engagement**:
   - Increase response rate for high-potential videos
   - Pin controversial comments to drive discussion
   - Ask engaging questions in comments

3. **Cross-Promotion**:
   - Link to related videos in descriptions
   - Create playlists for similar content
   - Mention previous popular videos in new uploads

### System Optimization

For better system performance:

1. **Resource Allocation**:
   - Adjust process_frequency based on server capacity
   - Lower video resolution if processing is too slow
   - Reduce effects complexity for faster rendering

2. **Upload Scheduling**:
   - Fine-tune upload time slots based on audience activity
   - Adjust upload frequency based on content pipeline
   - Balance consistency with quality

3. **Analytics Focus**:
   - Prioritize dashboard types that provide actionable insights
   - Adjust data_window_days based on channel age
   - Focus on metrics that correlate with growth

## Troubleshooting

### Common Issues

#### Authentication Problems

**Symptoms**: Upload failures, "Authentication required" errors

**Solutions**:
1. Delete the `youtube_credentials.json` file to force re-authentication
2. Verify your `client_secret.json` file is valid
3. Check that your Google project has the YouTube Data API enabled
4. Ensure your account has proper permissions

#### Video Generation Failures

**Symptoms**: Missing output files, error messages about FFmpeg

**Solutions**:
1. Verify FFmpeg is installed correctly: `ffmpeg -version`
2. Check audio file format compatibility
3. Ensure sufficient disk space
4. Look for specific error messages in `video_generator.log`

#### Upload Failures

**Symptoms**: Videos processed but not appearing on YouTube

**Solutions**:
1. Check YouTube API quota limits in Google Cloud Console
2. Verify network connectivity
3. Ensure video meets YouTube's requirements (no copyright issues)
4. Check for specific error messages in `youtube_uploader.log`

#### Analytics Errors

**Symptoms**: Missing dashboards, analytics not updating

**Solutions**:
1. Verify YouTube Analytics API is enabled
2. Check authentication for analytics scope
3. Ensure the channel has sufficient data for analysis
4. Look for specific error messages in `youtube_analytics.log`

### Error Logs

When troubleshooting, check the system state for errors:

```
python src/main.py --detailed
```

This will show recent errors with:
- Timestamp
- Component that generated the error
- Error message

### Getting Support

If you encounter persistent issues:

1. Check the full logs in the log files
2. Search for similar issues in the project repository
3. Contact support with:
   - Detailed error description
   - Relevant log excerpts
   - System configuration
   - Steps to reproduce the issue

---

## Quick Reference

### Key Commands

- Start system: `python src/main.py`
- Check status: `python src/main.py --status`
- Detailed status: `python src/main.py --detailed`
- Custom config: `python src/main.py --config custom_config.json`

### File Locations

- Configuration: `config.json`
- Input audio: `input/`
- Generated videos: `output/`
- System state: `data/system_state.json`
- Dashboards: `dashboards/`
- Logs: `./*.log`

### Optimal Settings for Virality

- Upload time: 18:00-21:00 local time
- Video length: 2-4 minutes
- Title format: "LEAKED: [Artist] - [Track Name] [Unreleased YYYY]"
- Thumbnail: High contrast with text overlay
- Description: Include timestamps and calls to action
- Promotion: All platforms with 15-minute delay after upload
