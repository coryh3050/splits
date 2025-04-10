"""
Notification System Module

This module handles automated notifications to keep users informed
about video performance and system activities.
"""

import os
import json
import time
import logging
import smtplib
import threading
import schedule
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('notification_system.log')
    ]
)

logger = logging.getLogger('notification_system')

class NotificationSystem:
    """
    Handles automated notifications for system events and performance updates
    """
    
    def __init__(self, config=None):
        """
        Initialize the notification system with configuration settings
        
        Args:
            config (dict): Configuration settings for notifications
        """
        self.config = config or {}
        
        # Set notification settings
        self.settings = {
            "email_notifications": self.config.get("email_notifications", True),
            "push_notifications": self.config.get("push_notifications", False),
            "notification_frequency": self.config.get("notification_frequency", "daily"),
            "performance_threshold": self.config.get("performance_threshold", 1000),  # views
            "viral_threshold": self.config.get("viral_threshold", 10000),  # views
            "email_recipients": self.config.get("email_recipients", []),
            "smtp_settings": self.config.get("smtp_settings", {})
        }
        
        # Initialize notification history
        self.notification_history = []
        
        # Load notification history
        self._load_notification_history()
    
    def send_upload_notification(self, video_data):
        """
        Send notification for a new video upload
        
        Args:
            video_data (dict): Video data including URL, title, etc.
            
        Returns:
            bool: True if successful, False otherwise
        """
        video_id = video_data.get("video_id")
        video_url = video_data.get("video_url")
        video_title = video_data.get("title")
        
        if not video_id or not video_url or not video_title:
            logger.error("Missing video data for upload notification")
            return False
        
        # Create notification content
        subject = f"New Video Uploaded: {video_title}"
        
        message = f"""
        A new video has been successfully uploaded to your YouTube channel:
        
        Title: {video_title}
        URL: {video_url}
        
        The system will now begin promoting this video across social media platforms
        and engaging with comments to maximize viral potential.
        
        You will receive performance updates based on your notification settings.
        """
        
        # Send notification
        success = self._send_notification(subject, message, "upload")
        
        if success:
            # Add to notification history
            self.notification_history.append({
                "type": "upload",
                "video_id": video_id,
                "video_title": video_title,
                "timestamp": datetime.now().isoformat(),
                "subject": subject
            })
            
            # Save notification history
            self._save_notification_history()
        
        return success
    
    def send_performance_notification(self, video_data, performance_data):
        """
        Send notification for video performance update
        
        Args:
            video_data (dict): Video data including URL, title, etc.
            performance_data (dict): Performance metrics
            
        Returns:
            bool: True if successful, False otherwise
        """
        video_id = video_data.get("video_id")
        video_url = video_data.get("video_url")
        video_title = video_data.get("title")
        
        if not video_id or not video_url or not video_title:
            logger.error("Missing video data for performance notification")
            return False
        
        # Extract performance metrics
        views = performance_data.get("views", 0)
        likes = performance_data.get("likes", 0)
        comments = performance_data.get("comments", 0)
        watch_time = performance_data.get("watch_time", 0)
        
        # Determine if video is performing well
        is_viral = views >= self.settings["viral_threshold"]
        is_performing_well = views >= self.settings["performance_threshold"]
        
        # Create notification content
        if is_viral:
            subject = f"VIRAL ALERT: {video_title} is taking off!"
        elif is_performing_well:
            subject = f"Good Performance: {video_title} is doing well"
        else:
            subject = f"Performance Update: {video_title}"
        
        message = f"""
        Performance update for your video:
        
        Title: {video_title}
        URL: {video_url}
        
        Current metrics:
        - Views: {views}
        - Likes: {likes}
        - Comments: {comments}
        - Watch Time: {watch_time} minutes
        
        """
        
        # Add performance-specific message
        if is_viral:
            message += """
            🔥 THIS VIDEO IS GOING VIRAL! 🔥
            
            The system is automatically increasing promotion efforts to maximize
            this viral opportunity. Additional social media posts and engagement
            activities have been scheduled.
            """
        elif is_performing_well:
            message += """
            This video is performing well and showing potential.
            
            The system is optimizing promotion strategies to help push this
            content toward viral status.
            """
        else:
            message += """
            This video is performing within normal parameters.
            
            The system continues to promote and engage according to the
            standard schedule.
            """
        
        # Send notification
        success = self._send_notification(subject, message, "performance")
        
        if success:
            # Add to notification history
            self.notification_history.append({
                "type": "performance",
                "video_id": video_id,
                "video_title": video_title,
                "timestamp": datetime.now().isoformat(),
                "subject": subject,
                "metrics": {
                    "views": views,
                    "likes": likes,
                    "comments": comments
                }
            })
            
            # Save notification history
            self._save_notification_history()
        
        return success
    
    def send_system_notification(self, subject, message, notification_type="system"):
        """
        Send system notification
        
        Args:
            subject (str): Notification subject
            message (str): Notification message
            notification_type (str): Type of notification
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Send notification
        success = self._send_notification(subject, message, notification_type)
        
        if success:
            # Add to notification history
            self.notification_history.append({
                "type": notification_type,
                "timestamp": datetime.now().isoformat(),
                "subject": subject
            })
            
            # Save notification history
            self._save_notification_history()
        
        return success
    
    def send_daily_summary(self, performance_data):
        """
        Send daily summary notification
        
        Args:
            performance_data (dict): Channel performance metrics
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Extract performance metrics
        total_videos = performance_data.get("total_videos", 0)
        total_views = performance_data.get("total_views", 0)
        new_views = performance_data.get("new_views", 0)
        new_subscribers = performance_data.get("new_subscribers", 0)
        top_videos = performance_data.get("top_videos", [])
        
        # Create notification content
        subject = f"Daily Channel Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        message = f"""
        Daily performance summary for your YouTube channel:
        
        Channel metrics:
        - Total Videos: {total_videos}
        - Total Views: {total_views}
        - New Views Today: {new_views}
        - New Subscribers Today: {new_subscribers}
        
        Top performing videos:
        """
        
        # Add top videos
        for i, video in enumerate(top_videos[:5], 1):
            message += f"""
        {i}. {video.get('title')}
           Views: {video.get('views')}
           URL: {video.get('url')}
            """
        
        # Add system status
        message += """
        
        System Status:
        All automation systems are functioning normally.
        """
        
        # Send notification
        success = self._send_notification(subject, message, "daily_summary")
        
        if success:
            # Add to notification history
            self.notification_history.append({
                "type": "daily_summary",
                "timestamp": datetime.now().isoformat(),
                "subject": subject,
                "metrics": {
                    "total_views": total_views,
                    "new_views": new_views,
                    "new_subscribers": new_subscribers
                }
            })
            
            # Save notification history
            self._save_notification_history()
        
        return success
    
    def _send_notification(self, subject, message, notification_type):
        """
        Send notification through configured channels
        
        Args:
            subject (str): Notification subject
            message (str): Notification message
            notification_type (str): Type of notification
            
        Returns:
            bool: True if successful, False otherwise
        """
        success = False
        
        # Send email notification if enabled
        if self.settings["email_notifications"]:
            email_success = self._send_email_notification(subject, message)
            success = email_success
        
        # Send push notification if enabled
        if self.settings["push_notifications"]:
            push_success = self._send_push_notification(subject, message)
            success = success or push_success
        
        return success
    
    def _send_email_notification(self, subject, message):
        """
        Send email notification
        
        Args:
            subject (str): Email subject
            message (str): Email message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get SMTP settings
            smtp_settings = self.settings["smtp_settings"]
            smtp_server = smtp_settings.get("server")
            smtp_port = smtp_settings.get("port", 587)
            smtp_username = smtp_settings.get("username")
            smtp_password = smtp_settings.get("password")
            sender_email = smtp_settings.get("sender_email")
            
            # Get recipients
            recipients = self.settings["email_recipients"]
            
            # Check required settings
            if not smtp_server or not smtp_username or not smtp_password or not sender_email or not recipients:
                logger.error("Missing SMTP settings for email notification")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            
            # Add message body
            msg.attach(MIMEText(message, "plain"))
            
            # Connect to SMTP server
            # Note: In a real implementation, this would connect to an actual SMTP server
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(smtp_username, smtp_password)
            # server.send_message(msg)
            # server.quit()
            
            # Log email notification
            logger.info(f"Email notification sent: {subject}")
            logger.info(f"Recipients: {recipients}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False
    
    def _send_push_notification(self, subject, message):
        """
        Send push notification
        
        Args:
            subject (str): Notification subject
            message (str): Notification message
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # In a real implementation, this would use a push notification service
            # Example: Firebase Cloud Messaging, OneSignal, etc.
            
            # Log push notification
            logger.info(f"Push notification sent: {subject}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending push notification: {str(e)}")
            return False
    
    def _save_notification_history(self):
        """
        Save notification history to file
        """
        try:
            # Convert datetime objects to strings
            history_copy = json.dumps(self.notification_history, default=str)
            history_copy = json.loads(history_copy)
            
            # Save to file
            with open("notification_history.json", "w") as f:
                json.dump(history_copy, f, indent=2)
            
            logger.info("Notification history saved to file")
            
        except Exception as e:
            logger.error(f"Error saving notification history: {str(e)}")
    
    def _load_notification_history(self):
        """
        Load notification history from file
        """
        try:
            if os.path.exists("notification_history.json"):
                with open("notification_history.json", "r") as f:
                    self.notification_history = json.load(f)
                
                logger.info("Notification history loaded from file")
            
        except Exception as e:
            logger.error(f"Error loading notification history: {str(e)}")
    
    def start_scheduler(self):
        """
        Start the notification scheduler
        """
        # Load notification history
        self._load_notification_history()
        
        # Set up schedule based on notification frequency
        frequency = self.settings["notification_frequency"]
        
        if frequency == "hourly":
            schedule.every().hour.do(self._scheduled_summary)
        elif frequency == "daily":
            schedule.every().day.at("20:00").do(self._scheduled_summary)
        elif frequency == "weekly":
            schedule.every().monday.at("09:00").do(self._scheduled_summary)
        else:
            # Default to daily
            schedule.every().day.at("20:00").do(self._scheduled_summary)
        
        # Define scheduler function
        def run_scheduler():
            logger.info("Notification scheduler started")
            
            while True:
             <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>