# YouTube Automation for AI-Generated Music

A comprehensive system for automating the creation, upload, promotion, and optimization of AI-generated music videos on YouTube.

## Overview

This system automates the entire workflow for running a YouTube channel featuring AI-generated music. It handles:

1. **Video Generation** - Creates visually appealing videos from audio files with beat-synchronized visualizations
2. **Upload Management** - Schedules and uploads videos at optimal times for maximum engagement
3. **Viral Marketing** - Automatically promotes videos across social media platforms and engages with comments
4. **Analytics & Optimization** - Analyzes performance trends and optimizes content for maximum viral potential

The system is designed to be fully automated, requiring minimal human intervention once set up.

## System Requirements

- Python 3.8 or higher
- FFmpeg (for video processing)
- YouTube API credentials
- Social media API credentials (optional, for promotion features)
- Sufficient disk space for video processing

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/youtube-automation.git
   cd youtube-automation
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. Set up YouTube API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download the client secrets file and save as `client_secret.json` in the project root

## Directory Structure

```
youtube_automation/
├── src/
│   ├── video_generator/     # Video creation components
│   ├── uploader/            # YouTube upload components
│   ├── promotion/           # Social media promotion components
│   ├── analytics/           # Performance analysis components
│   ├── config/              # Configuration files
│   └── main.py              # Main controller
├── input/                   # Place audio files here
├── output/                  # Generated videos and thumbnails
├── temp/                    # Temporary processing files
├── data/                    # System state and analytics data
├── docs/                    # Documentation
└── config.json              # Main configuration file
```

## Configuration

The system is configured through the `config.json` file. A default configuration is created on first run, which you can then customize.

Key configuration sections:

### General Settings

```json
"general": {
  "working_dir": "/path/to/working/directory",
  "input_dir": "input",
  "output_dir": "output",
  "temp_dir": "temp",
  "data_dir": "data"
}
```

### Video Generator Settings

```json
"video_generator": {
  "resolution": "1080p",
  "fps": 30,
  "transition_style": "beat_sync",
  "visual_effects": ["zoom", "pulse", "glitch"],
  "color_scheme": "high_contrast"
}
```

### Uploader Settings

```json
"uploader": {
  "schedule_strategy": "optimal_time",
  "upload_frequency": "daily",
  "max_daily_uploads": 1,
  "client_secrets_file": "client_secret.json",
  "credentials_file": "youtube_credentials.json"
}
```

### Promotion Settings

```json
"promotion": {
  "platforms": ["twitter", "reddit", "tiktok"],
  "comment_response_rate": 0.7,
  "auto_engagement": true,
  "notification_frequency": "daily"
}
```

### Analytics Settings

```json
"analytics": {
  "data_window_days": 30,
  "update_frequency": 24,
  "viral_threshold": 10000,
  "dashboard_types": ["channel", "videos", "trends", "audience"]
}
```

### Automation Settings

```json
"automation": {
  "process_frequency": 1,
  "upload_time_slots": ["15:00", "18:00", "21:00"],
  "promotion_delay": 15,
  "analysis_frequency": 24
}
```

## Usage

### Basic Usage

1. Place your AI-generated music files in the `input` directory
2. Run the main controller:
   ```
   python src/main.py
   ```
3. The system will automatically:
   - Process audio files into videos
   - Schedule uploads at optimal times
   - Promote videos across configured platforms
   - Analyze performance and optimize future content

### Command Line Options

```
python src/main.py --help
```

Available options:
- `--config PATH`: Specify a custom configuration file
- `--status`: Print current system status and exit
- `--detailed`: Print detailed system status and exit

### Monitoring

The system creates log files and maintains a system state file in the data directory. You can check the status at any time:

```
python src/main.py --status
```

For more detailed information:

```
python src/main.py --detailed
```

## Workflow

1. **Input Processing**:
   - System scans the input directory for new audio files
   - Each audio file is processed to create a video with visualizations
   - Thumbnails are generated with viral-optimized designs
   - Metadata (title, description, tags) is created based on trend analysis

2. **Upload Management**:
   - System determines optimal upload times based on audience analytics
   - Videos are uploaded to YouTube with optimized metadata
   - Videos are scheduled according to the configured frequency

3. **Promotion**:
   - After upload, videos are automatically promoted across social media
   - System engages with comments using AI-driven responses
   - Strategic comments are posted to drive engagement

4. **Analytics & Optimization**:
   - Performance data is collected and analyzed
   - Trends are identified to optimize future content
   - Performance dashboards are generated
   - Recommendations are provided for content optimization

## Viral Optimization Features

The system includes several features designed to maximize viral potential:

1. **Metadata Optimization**:
   - Titles are crafted with viral elements ("LEAKED", "UNRELEASED", etc.)
   - Descriptions include engagement prompts and strategic keywords
   - Tags are optimized based on trending topics

2. **Strategic Commenting**:
   - System posts first comments to drive engagement
   - Controversial comments are posted to spark discussion
   - Engagement questions are posted to increase comment count

3. **Thumbnail Optimization**:
   - High-contrast designs with attention-grabbing elements
   - Strategic text placement with viral keywords
   - Optimized for maximum click-through rate

4. **Trend Analysis**:
   - System analyzes top-performing videos to identify patterns
   - Content is optimized based on identified trends
   - Upload timing is adjusted for maximum initial velocity

## Customization

### Custom Video Templates

You can create custom video templates by modifying the visualizer settings in `src/video_generator/visualizer.py`. The system supports various visualization styles that can be configured in the `config.json` file.

### Custom Promotion Strategies

Promotion strategies can be customized in `src/promotion/social_media.py` and `src/promotion/comment_engagement.py`. You can adjust the templates, posting frequency, and engagement patterns.

### Custom Analytics

The analytics system can be extended by modifying `src/analytics/trend_analyzer.py`. You can add custom metrics and optimization strategies based on your specific needs.

## Troubleshooting

### Authentication Issues

If you encounter authentication issues:

1. Check that your `client_secret.json` file is valid and properly located
2. Delete the `youtube_credentials.json` file to force re-authentication
3. Ensure your API project has the YouTube Data API v3 enabled
4. Check API quota limits in the Google Cloud Console

### Video Generation Issues

If videos aren't generating properly:

1. Verify FFmpeg is installed and accessible in your PATH
2. Check the input audio file format (supported formats: MP3, WAV, FLAC, OGG)
3. Ensure sufficient disk space for video processing
4. Check the logs for specific error messages

### Upload Issues

If uploads are failing:

1. Verify your YouTube account is in good standing
2. Check API quota limits
3. Ensure video files meet YouTube's requirements
4. Check network connectivity

## Advanced Configuration

### Custom Upload Scheduling

You can implement custom upload scheduling by modifying `src/uploader/scheduler.py`. The system supports various scheduling strategies that can be configured in the `config.json` file.

### Social Media Integration

To enable social media promotion:

1. Create API credentials for each platform
2. Add the credentials to the appropriate configuration files
3. Enable the platforms in the `promotion.platforms` configuration

### Performance Optimization

For large-scale operations:

1. Adjust the `process_frequency` setting to control resource usage
2. Use a dedicated server with sufficient CPU and memory
3. Consider using cloud storage for video files
4. Implement a distributed processing system for video generation

## Security Considerations

1. Store API credentials securely
2. Do not expose the `client_secret.json` file
3. Use environment variables for sensitive information
4. Implement proper access controls for the system

## Deployment Guide

### Local Deployment

For running the system on your local machine:

1. Complete the installation steps above
2. Configure the system as needed
3. Run the main controller:
   ```
   python src/main.py
   ```
4. Keep the process running (consider using a tool like `screen` or `tmux`)

### Server Deployment

For deploying on a dedicated server:

1. Set up a Linux server (Ubuntu recommended)
2. Install dependencies:
   ```
   sudo apt-get update
   sudo apt-get install python3 python3-pip ffmpeg
   ```
3. Clone the repository and install Python dependencies
4. Set up a systemd service for automatic startup:

   Create a file `/etc/systemd/system/youtube-automation.service`:
   ```
   [Unit]
   Description=YouTube Automation Service
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/youtube_automation
   ExecStart=/usr/bin/python3 /path/to/youtube_automation/src/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

5. Enable and start the service:
   ```
   sudo systemctl enable youtube-automation
   sudo systemctl start youtube-automation
   ```

6. Monitor the service:
   ```
   sudo systemctl status youtube-automation
   ```

### Docker Deployment

For deploying with Docker:

1. Build the Docker image:
   ```
   docker build -t youtube-automation .
   ```

2. Run the container:
   ```
   docker run -d \
     --name youtube-automation \
     -v /path/to/input:/app/input \
     -v /path/to/output:/app/output \
     -v /path/to/data:/app/data \
     -v /path/to/client_secret.json:/app/client_secret.json \
     youtube-automation
   ```

3. Monitor the container:
   ```
   docker logs -f youtube-automation
   ```

## Maintenance

### Regular Maintenance Tasks

1. **Monitor API Quotas**: Check YouTube API usage regularly
2. **Update Dependencies**: Keep Python packages and FFmpeg updated
3. **Backup Data**: Regularly backup the data directory
4. **Review Logs**: Check logs for errors or performance issues
5. **Update Strategies**: Adjust promotion and optimization strategies based on performance

### Scaling

As your channel grows:

1. Consider upgrading to a more powerful server
2. Implement a distributed processing system for video generation
3. Use a database for system state instead of JSON files
4. Implement a proper monitoring and alerting system

## Support and Contribution

For support or to contribute to the project:

1. Open an issue on GitHub
2. Submit a pull request with improvements
3. Contact the maintainers at support@example.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Quick Start Guide

1. **Install the system**:
   ```
   git clone https://github.com/yourusername/youtube-automation.git
   cd youtube-automation
   pip install -r requirements.txt
   ```

2. **Set up YouTube API**:
   - Create credentials and save as `client_secret.json`

3. **Add your AI-generated music**:
   - Place audio files in the `input` directory

4. **Start the system**:
   ```
   python src/main.py
   ```

5. **Monitor progress**:
   ```
   python src/main.py --status
   ```

That's it! The system will handle everything else automatically.
