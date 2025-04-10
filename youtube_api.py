"""
YouTube Uploader Module

This module handles the automated uploading of videos to YouTube
using the YouTube Data API v3.
"""

import os
import time
import json
import random
import logging
from datetime import datetime, timedelta
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('youtube_uploader.log')
    ]
)

logger = logging.getLogger('youtube_uploader')

class YouTubeUploader:
    """
    Handles uploading videos to YouTube and managing metadata
    """
    
    def __init__(self, config=None):
        """
        Initialize the YouTube uploader with configuration settings
        
        Args:
            config (dict): Configuration settings for YouTube uploads
        """
        self.config = config or {}
        self.youtube = None
        
        # Set API scopes
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.force-ssl"
        ]
        
        # Set client secrets file path
        self.client_secrets_file = self.config.get("client_secrets_file", "client_secret.json")
        
        # Set credentials file path
        self.credentials_file = self.config.get("credentials_file", "youtube_credentials.json")
    
    def authenticate(self, headless=True):
        """
        Authenticate with YouTube API
        
        Args:
            headless (bool): Whether to use headless authentication
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Check if credentials file exists
            if os.path.exists(self.credentials_file):
                # Load credentials from file
                with open(self.credentials_file, 'r') as f:
                    creds_data = json.load(f)
                
                credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
                    creds_data, self.scopes)
                
                # Check if credentials are expired
                if credentials.expired:
                    logger.info("Credentials expired, refreshing...")
                    credentials.refresh(google.auth.transport.requests.Request())
                    
                    # Save refreshed credentials
                    with open(self.credentials_file, 'w') as f:
                        creds_dict = {
                            'token': credentials.token,
                            'refresh_token': credentials.refresh_token,
                            'token_uri': credentials.token_uri,
                            'client_id': credentials.client_id,
                            'client_secret': credentials.client_secret,
                            'scopes': credentials.scopes
                        }
                        json.dump(creds_dict, f)
            else:
                # No credentials file, need to authenticate
                if not os.path.exists(self.client_secrets_file):
                    logger.error(f"Client secrets file not found: {self.client_secrets_file}")
                    return False
                
                # Create flow instance
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes)
                
                if headless:
                    # Headless authentication
                    credentials = flow.run_console()
                else:
                    # Local server authentication
                    credentials = flow.run_local_server(port=8080)
                
                # Save credentials
                with open(self.credentials_file, 'w') as f:
                    creds_dict = {
                        'token': credentials.token,
                        'refresh_token': credentials.refresh_token,
                        'token_uri': credentials.token_uri,
                        'client_id': credentials.client_id,
                        'client_secret': credentials.client_secret,
                        'scopes': credentials.scopes
                    }
                    json.dump(creds_dict, f)
            
            # Create YouTube API client
            self.youtube = googleapiclient.discovery.build(
                "youtube", "v3", credentials=credentials)
            
            logger.info("Successfully authenticated with YouTube API")
            return True
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def upload_video(self, video_path, metadata, thumbnail_path=None, retry_count=3):
        """
        Upload a video to YouTube
        
        Args:
            video_path (str): Path to video file
            metadata (dict): Video metadata
            thumbnail_path (str, optional): Path to thumbnail image
            retry_count (int): Number of retry attempts
            
        Returns:
            dict: Upload result with video ID and status
        """
        if not self.youtube:
            if not self.authenticate():
                return {"success": False, "error": "Authentication failed"}
        
        try:
            # Prepare metadata
            body = {
                "snippet": {
                    "title": metadata.get("title", ""),
                    "description": metadata.get("description", ""),
                    "tags": metadata.get("tags", []),
                    "categoryId": metadata.get("category", "10")  # 10 is Music
                },
                "status": {
                    "privacyStatus": metadata.get("privacyStatus", "public"),
                    "selfDeclaredMadeForKids": False
                }
            }
            
            # Add notification settings if specified
            if "notifySubscribers" in metadata:
                body["status"]["publishAt"] = None  # Publish immediately
                body["status"]["notifySubscribers"] = metadata["notifySubscribers"]
            
            # Add scheduled publishing if specified
            if "publishAt" in metadata and metadata["publishAt"]:
                body["status"]["privacyStatus"] = "private"  # Set to private initially
                body["status"]["publishAt"] = metadata["publishAt"]
            
            # Prepare media file upload
            media = googleapiclient.http.MediaFileUpload(
                video_path,
                chunksize=1024*1024,
                resumable=True
            )
            
            # Create upload request
            request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Execute upload with progress tracking
            response = None
            retries = 0
            
            while response is None and retries < retry_count:
                try:
                    logger.info(f"Uploading video: {os.path.basename(video_path)}")
                    status, response = request.next_chunk()
                    
                    if status:
                        progress = int(status.progress() * 100)
                        logger.info(f"Upload progress: {progress}%")
                        
                except googleapiclient.errors.HttpError as e:
                    if e.resp.status in [500, 502, 503, 504]:
                        retries += 1
                        logger.warning(f"Retrying upload ({retries}/{retry_count})")
                        time.sleep(5 * retries)  # Exponential backoff
                    else:
                        logger.error(f"Upload error: {str(e)}")
                        return {"success": False, "error": str(e)}
            
            if not response:
                return {"success": False, "error": "Upload failed after retries"}
            
            video_id = response["id"]
            logger.info(f"Video uploaded successfully. Video ID: {video_id}")
            
            # Upload thumbnail if provided
            if thumbnail_path:
                self.set_thumbnail(video_id, thumbnail_path)
            
            # Add to playlist if specified
            if "playlist_id" in metadata and metadata["playlist_id"]:
                self.add_to_playlist(video_id, metadata["playlist_id"])
            
            return {
                "success": True,
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }
            
        except googleapiclient.errors.HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def set_thumbnail(self, video_id, thumbnail_path, retry_count=3):
        """
        Set a custom thumbnail for a video
        
        Args:
            video_id (str): YouTube video ID
            thumbnail_path (str): Path to thumbnail image
            retry_count (int): Number of retry attempts
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.youtube:
            if not self.authenticate():
                return False
        
        try:
            # Prepare media file upload
            media = googleapiclient.http.MediaFileUpload(
                thumbnail_path,
                mimetype="image/jpeg",
                resumable=True
            )
            
            # Create upload request
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            )
            
            # Execute upload with retries
            response = None
            retries = 0
            
            while response is None and retries < retry_count:
                try:
                    logger.info(f"Uploading thumbnail for video ID: {video_id}")
                    status, response = request.next_chunk()
                    
                    if status:
                        progress = int(status.progress() * 100)
                        logger.info(f"Thumbnail upload progress: {progress}%")
                        
                except googleapiclient.errors.HttpError as e:
                    if e.resp.status in [500, 502, 503, 504]:
                        retries += 1
                        logger.warning(f"Retrying thumbnail upload ({retries}/{retry_count})")
                        time.sleep(5 * retries)  # Exponential backoff
                    else:
                        logger.error(f"Thumbnail upload error: {str(e)}")
                        return False
            
            if not response:
                return False
            
            logger.info(f"Thumbnail uploaded successfully for video ID: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Thumbnail upload error: {str(e)}")
            return False
    
    def add_to_playlist(self, video_id, playlist_id):
        """
        Add a video to a playlist
        
        Args:
            video_id (str): YouTube video ID
            playlist_id (str): YouTube playlist ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.youtube:
            if not self.authenticate():
                return False
        
        try:
            # Create playlist item
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            
            # Execute request
            response = request.execute()
            
            logger.info(f"Added video ID {video_id} to playlist ID {playlist_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding video to playlist: {str(e)}")
            return False
    
    def get_optimal_upload_time(self, days_ahead=1):
        """
        Calculate optimal upload time based on configuration
        
        Args:
            days_ahead (int): Number of days ahead to schedule
            
        Returns:
            str: ISO 8601 formatted timestamp for optimal upload time
        """
        # Get scheduling config
        scheduling = self.config.get("scheduling", {})
        timezone = scheduling.get("timezone", "America/Los_Angeles")
        preferred_days = scheduling.get("preferred_days", ["Friday", "Saturday", "Sunday"])
        preferred_hours = scheduling.get("preferred_hours", [15, 16, 17, 18, 19, 20])  # 3PM to 8PM
        
        # Convert day names to integers (0 = Monday, 6 = Sunday)
        day_map = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
            "Friday": 4, "Saturday": 5, "Sunday": 6
        }
        preferred_day_nums = [day_map[day] for day in preferred_days if day in day_map]
        
        # Get current time
        now = datetime.now()
        
        # Find next preferred day
        days_to_add = 0
        current_weekday = now.weekday()
        
        if not preferred_day_nums:
            # No preferred days, use tomorrow
            days_to_add = 1
        else:
            # Find next preferred day
            for i in range(1, 8):  # Check next 7 days
                check_day = (current_weekday + i) % 7
                if check_day in preferred_day_nums:
                    days_to_add = i
                    break
        
        # Add days_ahead to days_to_add
        days_to_add += (days_ahead - 1)
        
        # Calculate target date
        target_date = now + timedelta(days=days_to_add)
        
        # Choose random preferred hour
        if not preferred_hours:
            hour = random.randint(15, 20)  # Default to 3PM-8PM
        else:
            hour = random.choice(preferred_hours)
        
        # Set minute to a random value
        minute = random.randint(0, 59)
        
        # Create datetime with target date and time
        target_datetime = datetime(
            target_date.year, target_date.month, target_date.day,
            hour, minute, 0
        )
        
        # Format as ISO 8601
        return target_datetime.isoformat() + "Z"
    
    def create_playlist(self, title, description=""):
        """
        Create a new playlist
        
        Args:
            title (str): Playlist title
            description (str): Playlist description
            
        Returns:
            str: Playlist ID if successful, None otherwise
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        try:
            # Create playlist
            request = self.youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                }
       <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>