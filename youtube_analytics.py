"""
YouTube Analytics Integration Module

This module handles integration with YouTube Analytics API to fetch
performance data for videos and the channel.
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('youtube_analytics.log')
    ]
)

logger = logging.getLogger('youtube_analytics')

class YouTubeAnalytics:
    """
    Handles integration with YouTube Analytics API
    """
    
    def __init__(self, config=None):
        """
        Initialize the YouTube Analytics integration with configuration settings
        
        Args:
            config (dict): Configuration settings for YouTube Analytics
        """
        self.config = config or {}
        self.youtube = None
        self.youtube_analytics = None
        
        # Set API scopes
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly"
        ]
        
        # Set client secrets file path
        self.client_secrets_file = self.config.get("client_secrets_file", "client_secret.json")
        
        # Set credentials file path
        self.credentials_file = self.config.get("credentials_file", "youtube_credentials.json")
        
        # Set channel ID
        self.channel_id = self.config.get("channel_id")
    
    def authenticate(self, headless=True):
        """
        Authenticate with YouTube API and YouTube Analytics API
        
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
            
            # Create YouTube Analytics API client
            self.youtube_analytics = googleapiclient.discovery.build(
                "youtubeAnalytics", "v2", credentials=credentials)
            
            # Get channel ID if not provided
            if not self.channel_id:
                self.channel_id = self._get_channel_id()
            
            logger.info("Successfully authenticated with YouTube API and YouTube Analytics API")
            return True
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def _get_channel_id(self):
        """
        Get channel ID for the authenticated user
        
        Returns:
            str: Channel ID
        """
        try:
            # Get channel info
            request = self.youtube.channels().list(
                part="id",
                mine=True
            )
            
            # Execute request
            response = request.execute()
            
            if "items" in response and len(response["items"]) > 0:
                channel_id = response["items"][0]["id"]
                logger.info(f"Retrieved channel ID: {channel_id}")
                return channel_id
            else:
                logger.error("No channel found")
                return None
            
        except Exception as e:
            logger.error(f"Error getting channel ID: {str(e)}")
            return None
    
    def get_channel_stats(self, days=30):
        """
        Get channel statistics for the specified time period
        
        Args:
            days (int): Number of days to include in the statistics
            
        Returns:
            dict: Channel statistics
        """
        if not self.youtube or not self.youtube_analytics:
            if not self.authenticate():
                return {"error": "Authentication failed"}
        
        try:
            # Calculate start and end dates
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get channel statistics
            request = self.youtube_analytics.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,dislikes,comments",
                dimensions="day",
                sort="day"
            )
            
            # Execute request
            response = request.execute()
            
            # Process response
            stats = {
                "channel_id": self.channel_id,
                "start_date": start_date,
                "end_date": end_date,
                "total_views": 0,
                "total_watch_time": 0,
                "total_subscribers_gained": 0,
                "total_subscribers_lost": 0,
                "total_likes": 0,
                "total_dislikes": 0,
                "total_comments": 0,
                "daily_stats": []
            }
            
            # Extract column headers
            headers = response.get("columnHeaders", [])
            header_names = [h.get("name") for h in headers]
            
            # Process rows
            for row in response.get("rows", []):
                day_stats = {}
                
                # Map values to headers
                for i, value in enumerate(row):
                    header = header_names[i]
                    day_stats[header] = value
                
                # Add to daily stats
                stats["daily_stats"].append(day_stats)
                
                # Update totals
                stats["total_views"] += day_stats.get("views", 0)
                stats["total_watch_time"] += day_stats.get("estimatedMinutesWatched", 0)
                stats["total_subscribers_gained"] += day_stats.get("subscribersGained", 0)
                stats["total_subscribers_lost"] += day_stats.get("subscribersLost", 0)
                stats["total_likes"] += day_stats.get("likes", 0)
                stats["total_dislikes"] += day_stats.get("dislikes", 0)
                stats["total_comments"] += day_stats.get("comments", 0)
            
            # Calculate net subscribers
            stats["net_subscribers"] = stats["total_subscribers_gained"] - stats["total_subscribers_lost"]
            
            # Calculate engagement rate
            if stats["total_views"] > 0:
                stats["engagement_rate"] = (stats["total_likes"] + stats["total_comments"]) / stats["total_views"]
            else:
                stats["engagement_rate"] = 0
            
            logger.info(f"Retrieved channel statistics for {days} days")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting channel statistics: {str(e)}")
            return {"error": str(e)}
    
    def get_video_stats(self, video_id):
        """
        Get statistics for a specific video
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video statistics
        """
        if not self.youtube:
            if not self.authenticate():
                return {"error": "Authentication failed"}
        
        try:
            # Get video statistics
            request = self.youtube.videos().list(
                part="statistics,snippet,contentDetails",
                id=video_id
            )
            
            # Execute request
            response = request.execute()
            
            if "items" in response and len(response["items"]) > 0:
                video = response["items"][0]
                
                # Extract statistics
                stats = {
                    "video_id": video_id,
                    "title": video["snippet"]["title"],
                    "published_at": video["snippet"]["publishedAt"],
                    "views": int(video["statistics"].get("viewCount", 0)),
                    "likes": int(video["statistics"].get("likeCount", 0)),
                    "dislikes": int(video["statistics"].get("dislikeCount", 0)) if "dislikeCount" in video["statistics"] else 0,
                    "comments": int(video["statistics"].get("commentCount", 0)),
                    "duration": video["contentDetails"]["duration"]
                }
                
                # Get detailed analytics
                detailed_stats = self._get_video_analytics(video_id)
                
                # Merge statistics
                stats.update(detailed_stats)
                
                logger.info(f"Retrieved statistics for video ID: {video_id}")
                
                return stats
            else:
                logger.error(f"Video not found: {video_id}")
                return {"error": "Video not found"}
            
        except Exception as e:
            logger.error(f"Error getting video statistics: {str(e)}")
            return {"error": str(e)}
    
    def _get_video_analytics(self, video_id):
        """
        Get detailed analytics for a specific video
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video analytics
        """
        if not self.youtube_analytics:
            if not self.authenticate():
                return {}
        
        try:
            # Calculate start and end dates (from publish date to now)
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Get video publish date
            request = self.youtube.videos().list(
                part="snippet",
                id=video_id
            )
            
            response = request.execute()
            
            if "items" in response and len(response["items"]) > 0:
                published_at = response["items"][0]["snippet"]["publishedAt"]
                published_date = published_at.split("T")[0]
            else:
                # Default to 30 days ago
                published_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Get video analytics
            request = self.youtube_analytics.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=published_date,
                endDate=end_date,
                metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,dislikes,comments,shares",
                filters=f"video=={video_id}",
                dimensions="day",
                sort="day"
            )
            
            # Execute request
            response = request.execute()
            
            # Process response
            analytics = {
                "total_watch_time": 0,
                "average_view_duration": 0,
                "subscribers_gained": 0,
                "shares": 0,
                "daily_stats": []
            }
            
            # Extract column headers
            headers = response.get("columnHeaders", [])
            header_names = [h.get("name") for h in headers]
            
            # Process rows
            for row in response.get("rows", []):
                day_stats = {}
                
                # Map values to headers
                for i, value in enumerate(row):
                    header = header_names[i]
                    day_stats[header] = value
                
                # Add to daily stats
                analytics["daily_stats"].append(day_stats)
                
                # Update totals
                analytics["total_watch_time"] += day_stats.get("estimatedMinutesWatched", 0)
                analytics["subscribers_gained"] += day_stats.get("subscribersGained", 0)
                analytics["shares"] += day_stats.get("shares", 0)
            
            # Calculate average view duration
            if len(response.get("rows", [])) > 0:
                analytics["average_view_duration"] = sum(day.get("averageViewDuration", 0) for day in analytics["daily_stats"]) / len(analytics["daily_stats"])
            
            # Calculate engagement rate
            views = sum(day.get("views", 0) for day in analytics["daily_stats"])
            likes = sum(day.get("likes", 0) for day in analytics["daily_stats"])
            comments = sum(day.get("comments", 0) for day in analytics["daily_stats"])
            
            if views > 0:
                analytics["engagement_rate"] = (likes + comments) / views
            else:
                analytics["engagement_rate"] = 0
            
            # Calculate retention rate
            analytics["retention_rate"] = analytics["average_view_duration"] / 60  # Convert to minutes
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting video analytics: {str(e)}")
            return {}
    
    def get_top_videos(self, days=30, limit=10):
        """<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>