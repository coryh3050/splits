"""
Automated Upload Scheduler Module

This module handles the scheduling and management of video uploads
to maximize viral potential through optimal timing.
"""

import os
import json
import time
import logging
import threading
import schedule
from datetime import datetime, timedelta
import random
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uploader.youtube_api import YouTubeUploader
from config.system_architecture import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('upload_scheduler.log')
    ]
)

logger = logging.getLogger('upload_scheduler')

class UploadScheduler:
    """
    Manages the scheduling and execution of video uploads
    """
    
    def __init__(self, config=None):
        """
        Initialize the upload scheduler with configuration settings
        
        Args:
            config (dict): Configuration settings for scheduling
        """
        self.config = config or DEFAULT_CONFIG
        
        # Initialize YouTube uploader
        youtube_config = self.config.get("youtube", {})
        youtube_config["scheduling"] = self.config.get("scheduling", {})
        self.uploader = YouTubeUploader(youtube_config)
        
        # Set up directories
        self.queue_dir = os.path.join(self.config.get("output_folder", "./output"), "queue")
        self.uploaded_dir = os.path.join(self.config.get("output_folder", "./output"), "uploaded")
        self.failed_dir = os.path.join(self.config.get("output_folder", "./output"), "failed")
        
        os.makedirs(self.queue_dir, exist_ok=True)
        os.makedirs(self.uploaded_dir, exist_ok=True)
        os.makedirs(self.failed_dir, exist_ok=True)
        
        # Initialize queue
        self.queue = []
        self.load_queue()
        
        # Initialize scheduler thread
        self.scheduler_thread = None
        self.stop_event = threading.Event()
    
    def load_queue(self):
        """
        Load queue from queue directory
        """
        self.queue = []
        
        # Get all metadata files in queue directory
        metadata_files = list(Path(self.queue_dir).glob("*.json"))
        
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Check if video and thumbnail files exist
                video_path = metadata.get("video_path")
                thumbnail_path = metadata.get("thumbnail_path")
                
                if not os.path.exists(video_path):
                    logger.warning(f"Video file not found: {video_path}")
                    continue
                
                if thumbnail_path and not os.path.exists(thumbnail_path):
                    logger.warning(f"Thumbnail file not found: {thumbnail_path}")
                    thumbnail_path = None
                
                # Add to queue
                self.queue.append({
                    "metadata": metadata,
                    "metadata_file": str(metadata_file),
                    "video_path": video_path,
                    "thumbnail_path": thumbnail_path,
                    "scheduled_time": metadata.get("scheduled_time")
                })
            
            except Exception as e:
                logger.error(f"Error loading metadata file {metadata_file}: {str(e)}")
        
        logger.info(f"Loaded {len(self.queue)} items into upload queue")
    
    def add_to_queue(self, metadata, video_path, thumbnail_path=None, schedule_time=None):
        """
        Add a video to the upload queue
        
        Args:
            metadata (dict): Video metadata
            video_path (str): Path to video file
            thumbnail_path (str, optional): Path to thumbnail file
            schedule_time (str, optional): ISO 8601 formatted timestamp for scheduled upload
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate queue item ID
            item_id = f"upload_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Set scheduled time if not provided
            if not schedule_time:
                # Determine if we should schedule immediately or at optimal time
                if self.config.get("immediate_upload", False):
                    schedule_time = datetime.now().isoformat() + "Z"
                else:
                    # Get optimal upload time
                    days_ahead = self.config.get("scheduling", {}).get("days_ahead", 1)
                    schedule_time = self.uploader.get_optimal_upload_time(days_ahead)
            
            # Update metadata with scheduled time
            metadata["scheduled_time"] = schedule_time
            
            # Save metadata to queue directory
            metadata_file = os.path.join(self.queue_dir, f"{item_id}.json")
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Add to queue
            queue_item = {
                "metadata": metadata,
                "metadata_file": metadata_file,
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "scheduled_time": schedule_time
            }
            
            self.queue.append(queue_item)
            
            logger.info(f"Added video to upload queue: {os.path.basename(video_path)}")
            logger.info(f"Scheduled upload time: {schedule_time}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding to queue: {str(e)}")
            return False
    
    def process_queue(self):
        """
        Process the upload queue
        """
        if not self.queue:
            logger.info("Upload queue is empty")
            return
        
        logger.info(f"Processing upload queue ({len(self.queue)} items)")
        
        # Get current time
        now = datetime.now().isoformat() + "Z"
        
        # Find items that are due for upload
        due_items = []
        remaining_items = []
        
        for item in self.queue:
            scheduled_time = item.get("scheduled_time")
            
            if not scheduled_time or scheduled_time <= now:
                due_items.append(item)
            else:
                remaining_items.append(item)
        
        # Update queue
        self.queue = remaining_items
        
        # Process due items
        for item in due_items:
            self._upload_item(item)
    
    def _upload_item(self, item):
        """
        Upload a queue item
        
        Args:
            item (dict): Queue item to upload
        """
        metadata = item["metadata"]
        video_path = item["video_path"]
        thumbnail_path = item["thumbnail_path"]
        metadata_file = item["metadata_file"]
        
        logger.info(f"Uploading video: {os.path.basename(video_path)}")
        
        # Authenticate if needed
        if not self.uploader.youtube:
            if not self.uploader.authenticate():
                logger.error("Authentication failed")
                self._handle_failed_upload(item, "Authentication failed")
                return
        
        # Upload video
        result = self.uploader.upload_video(video_path, metadata, thumbnail_path)
        
        if result["success"]:
            # Update metadata with video ID and URL
            metadata["video_id"] = result["video_id"]
            metadata["video_url"] = result["url"]
            metadata["upload_time"] = datetime.now().isoformat() + "Z"
            
            # Move files to uploaded directory
            self._handle_successful_upload(item, metadata)
            
            logger.info(f"Video uploaded successfully: {result['url']}")
        else:
            # Handle failed upload
            self._handle_failed_upload(item, result.get("error", "Unknown error"))
    
    def _handle_successful_upload(self, item, updated_metadata):
        """
        Handle successful upload
        
        Args:
            item (dict): Queue item
            updated_metadata (dict): Updated metadata with upload results
        """
        try:
            # Generate success ID
            success_id = f"success_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Save updated metadata
            success_metadata_file = os.path.join(self.uploaded_dir, f"{success_id}.json")
            with open(success_metadata_file, 'w') as f:
                json.dump(updated_metadata, f, indent=2)
            
            # Move video and thumbnail files if configured to keep them
            if self.config.get("keep_uploaded_files", True):
                video_filename = os.path.basename(item["video_path"])
                success_video_path = os.path.join(self.uploaded_dir, video_filename)
                
                # Copy instead of move to avoid issues if files are still needed
                import shutil
                shutil.copy2(item["video_path"], success_video_path)
                
                if item["thumbnail_path"]:
                    thumbnail_filename = os.path.basename(item["thumbnail_path"])
                    success_thumbnail_path = os.path.join(self.uploaded_dir, thumbnail_filename)
                    shutil.copy2(item["thumbnail_path"], success_thumbnail_path)
            
            # Delete queue metadata file
            if os.path.exists(item["metadata_file"]):
                os.remove(item["metadata_file"])
            
            logger.info(f"Upload processed successfully: {updated_metadata['video_url']}")
            
        except Exception as e:
            logger.error(f"Error handling successful upload: {str(e)}")
    
    def _handle_failed_upload(self, item, error):
        """
        Handle failed upload
        
        Args:
            item (dict): Queue item
            error (str): Error message
        """
        try:
            # Generate failure ID
            failure_id = f"failure_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Update metadata with error
            failed_metadata = item["metadata"].copy()
            failed_metadata["error"] = error
            failed_metadata["failure_time"] = datetime.now().isoformat() + "Z"
            
            # Save failed metadata
            failed_metadata_file = os.path.join(self.failed_dir, f"{failure_id}.json")
            with open(failed_metadata_file, 'w') as f:
                json.dump(failed_metadata, f, indent=2)
            
            # Move video and thumbnail files
            if self.config.get("keep_failed_files", True):
                video_filename = os.path.basename(item["video_path"])
                failed_video_path = os.path.join(self.failed_dir, video_filename)
                
                # Copy instead of move to avoid issues if files are still needed
                import shutil
                shutil.copy2(item["video_path"], failed_video_path)
                
                if item["thumbnail_path"]:
                    thumbnail_filename = os.path.basename(item["thumbnail_path"])
                    failed_thumbnail_path = os.path.join(self.failed_dir, thumbnail_filename)
                    shutil.copy2(item["thumbnail_path"], failed_thumbnail_path)
            
            # Delete queue metadata file
            if os.path.exists(item["metadata_file"]):
                os.remove(item["metadata_file"])
            
            logger.error(f"Upload failed: {error}")
            
        except Exception as e:
            logger.error(f"Error handling failed upload: {str(e)}")
    
    def start_scheduler(self):
        """
        Start the scheduler thread
        """
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            logger.warning("Scheduler already running")
            return
        
        # Reset stop event
        self.stop_event.clear()
        
        # Set up schedule
        check_interval = self.config.get("queue_check_interval", 5)  # minutes
        schedule.every(check_interval).minutes.do(self.process_queue)
        
        # Define scheduler function
        def run_scheduler():
            logger.info("Upload scheduler started")
            
            # Run initial queue processing
            self.process_queue()
            
            while not self.stop_event.is_set():
                schedule.run_pending()
                time.sleep(1)
            
            logger.info("Upload scheduler stopped")
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        logger.info(f"Upload scheduler started (check interval: {check_interval} minutes)")
    
    def stop_scheduler(self):
        """
        Stop the scheduler thread
        """
        if not self.scheduler_thread or not self.scheduler_thread.is_alive():
            logger.warning("Scheduler not running")
            return
        
        # Set stop event
        self.stop_event.set()
        
        # Wait for thread to stop
        self.scheduler_thread.join(timeout=10)
        
        logger.info("Upload scheduler stopped")
    
    def get_queue_status(self):
        """
        Get status of the upload queue
        
        Returns:
            dict: Queue status
        """
        # Count items by scheduled time
        now = datetime.now().isoformat() + "Z"
        due_count = 0
        scheduled_count = 0
        
        for item in self.queue:
            scheduled_time = item.get("scheduled_time")
            
            if not scheduled_time or scheduled_time <= now:
                due_count += 1
            else:
                scheduled_count += 1
        
        # Get counts of uploaded and failed items
        uploaded_count = len(list(Path(self.uploaded_dir).glob("*.json")))
        failed_count = len(list(Path(self.failed_dir).glob("*.json")))
        
        return {
            "queue_total": len(self.queue),
            "due_now": due_count,
            "scheduled": scheduled_count,
            "uploaded_total": uploaded_count,
            "failed_total": failed_count
        }


if __name__ == "__main__":
    # Example usage
    config = DEFAULT_CONFIG
    
    scheduler = UploadScheduler(config)
    
    # Start scheduler
    scheduler.start_scheduler()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(60)
            status = scheduler.get_queue_status()
            print(f"Queue status: {status}")
    except KeyboardInterrupt:
        # Stop scheduler on keyboard interrupt
        scheduler.stop_scheduler()
