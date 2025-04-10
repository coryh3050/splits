"""
Main Controller for Video Generation System

This module integrates the visualizer and thumbnail creator components
to generate complete videos for AI-generated music tracks.
"""

import os
import sys
import argparse
import json
import time
import shutil
from pathlib import Path
import subprocess
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_generator.visualizer import MusicVisualizer
from video_generator.thumbnail_creator import ThumbnailCreator
from config.system_architecture import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('video_generator.log')
    ]
)

logger = logging.getLogger('video_generator')

class VideoGenerator:
    """
    Main controller for generating videos from audio files
    """
    
    def __init__(self, config=None):
        """
        Initialize the video generator with configuration settings
        
        Args:
            config (dict): Configuration settings for video generation
        """
        self.config = config or DEFAULT_CONFIG
        
        # Initialize components
        self.visualizer = MusicVisualizer(self.config.get("video_settings", {}))
        self.thumbnail_creator = ThumbnailCreator({
            "resolution": (1280, 720),
            "style": self.config.get("video_settings", {}).get("color_scheme", "high_contrast"),
            "text_overlay": True,
            "emoji_use": True
        })
        
        # Ensure output directories exist
        self.output_dir = self.config.get("output_folder", "./output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create subdirectories
        self.videos_dir = os.path.join(self.output_dir, "videos")
        self.thumbnails_dir = os.path.join(self.output_dir, "thumbnails")
        self.metadata_dir = os.path.join(self.output_dir, "metadata")
        
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def process_audio_file(self, audio_path, track_name=None, visualizer_type=None):
        """
        Process a single audio file to generate video and thumbnail
        
        Args:
            audio_path (str): Path to audio file
            track_name (str, optional): Name of the track. If None, extracted from filename
            visualizer_type (str, optional): Type of visualizer to use. If None, uses config setting
            
        Returns:
            dict: Paths to generated files and metadata
        """
        # Extract track name from filename if not provided
        if track_name is None:
            track_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        logger.info(f"Processing audio file: {audio_path} (Track: {track_name})")
        
        # Create safe filename
        safe_name = "".join([c if c.isalnum() or c in ['-', '_'] else '_' for c in track_name])
        timestamp = int(time.time())
        
        # Set output paths
        video_path = os.path.join(self.videos_dir, f"{safe_name}_{timestamp}.mp4")
        thumbnail_path = os.path.join(self.thumbnails_dir, f"{safe_name}_{timestamp}.jpg")
        metadata_path = os.path.join(self.metadata_dir, f"{safe_name}_{timestamp}.json")
        
        # Override visualizer type if provided
        if visualizer_type:
            original_type = self.visualizer.config["visualizer_type"]
            self.visualizer.config["visualizer_type"] = visualizer_type
        
        try:
            # Generate visualization
            logger.info(f"Generating visualization for {track_name}")
            temp_video_path = os.path.join(self.videos_dir, f"temp_{safe_name}_{timestamp}.mp4")
            self.visualizer.create_visualization(audio_path, temp_video_path, track_name)
            
            # Generate thumbnail
            logger.info(f"Generating thumbnail for {track_name}")
            self.thumbnail_creator.create_thumbnail(thumbnail_path, track_name)
            
            # Combine audio with video
            logger.info(f"Combining audio with video for {track_name}")
            self._combine_audio_video(audio_path, temp_video_path, video_path)
            
            # Clean up temporary files
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            
            # Generate metadata
            metadata = self._generate_metadata(track_name, video_path, thumbnail_path)
            
            # Save metadata
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Processing complete for {track_name}")
            
            return {
                "track_name": track_name,
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "metadata_path": metadata_path,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error processing {track_name}: {str(e)}")
            raise
        finally:
            # Restore original visualizer type if changed
            if visualizer_type:
                self.visualizer.config["visualizer_type"] = original_type
    
    def process_directory(self, input_dir):
        """
        Process all audio files in a directory
        
        Args:
            input_dir (str): Directory containing audio files
            
        Returns:
            list: Results for each processed file
        """
        logger.info(f"Processing all audio files in {input_dir}")
        
        results = []
        
        # Get all audio files
        audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(list(Path(input_dir).glob(f"*{ext}")))
        
        logger.info(f"Found {len(audio_files)} audio files")
        
        # Process each file
        for audio_file in audio_files:
            try:
                result = self.process_audio_file(str(audio_file))
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing {audio_file}: {str(e)}")
        
        return results
    
    def _combine_audio_video(self, audio_path, video_path, output_path):
        """
        Combine audio and video files using ffmpeg
        
        Args:
            audio_path (str): Path to audio file
            video_path (str): Path to video file
            output_path (str): Path to save combined file
        """
        try:
            # Check if ffmpeg is installed
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Combine audio and video
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                '-y',
                output_path
            ]
            
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            logger.info(f"Successfully combined audio and video: {output_path}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error combining audio and video: {str(e)}")
            raise
        except FileNotFoundError:
            logger.error("ffmpeg not found. Please install ffmpeg.")
            raise
    
    def _generate_metadata(self, track_name, video_path, thumbnail_path):
        """
        Generate metadata for YouTube upload
        
        Args:
            track_name (str): Name of the track
            video_path (str): Path to video file
            thumbnail_path (str): Path to thumbnail file
            
        Returns:
            dict: Metadata for YouTube upload
        """
        # Get YouTube config
        youtube_config = self.config.get("youtube", {})
        
        # Format title and description
        title_template = youtube_config.get("default_title_template", "LEAKED Kendrick Lamar - {track_name} [Unreleased 2025]")
        description_template = youtube_config.get("default_description_template", "Exclusive unreleased Kendrick Lamar track.")
        
        title = title_template.format(track_name=track_name)
        description = description_template.format(
            track_name=track_name,
            channel_link="https://www.youtube.com/channel/" + youtube_config.get("channel_id", "")
        )
        
        # Get default tags
        tags = youtube_config.get("default_tags", [])
        
        # Add track-specific tags
        track_tags = track_name.lower().split()
        tags.extend(track_tags)
        
        # Ensure tags are unique
        tags = list(set(tags))
        
        return {
            "title": title,
            "description": description,
            "tags": tags,
            "category": "10",  # Music category
            "privacyStatus": "public",
            "video_path": video_path,
            "thumbnail_path": thumbnail_path,
            "track_name": track_name,
            "timestamp": int(time.time())
        }


def main():
    """
    Main function for command-line usage
    """
    parser = argparse.ArgumentParser(description='Generate videos for AI-generated music')
    parser.add_argument('--input', '-i', required=True, help='Input audio file or directory')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--config', '-c', help='Path to config file')
    parser.add_argument('--track-name', '-t', help='Track name (if processing single file)')
    parser.add_argument('--visualizer', '-v', choices=['waveform', 'circular', 'spectrum'], help='Visualizer type')
    
    args = parser.parse_args()
    
    # Load config
    config = DEFAULT_CONFIG
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config.update(json.load(f))
        except Exception as e:
            logger.error(f"Error loading config file: {str(e)}")
    
    # Override output directory if provided
    if args.output:
        config["output_folder"] = args.output
    
    # Initialize video generator
    video_generator = VideoGenerator(config)
    
    # Process input
    if os.path.isdir(args.input):
        # Process directory
        results = video_generator.process_directory(args.input)
        logger.info(f"Processed {len(results)} files")
    else:
        # Process single file
        result = video_generator.process_audio_file(args.input, args.track_name, args.visualizer)
        logger.info(f"Processed file: {result['track_name']}")
        logger.info(f"Video: {result['video_path']}")
        logger.info(f"Thumbnail: {result['thumbnail_path']}")


if __name__ == "__main__":
    main()
