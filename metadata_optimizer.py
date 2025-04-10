"""
Metadata Optimizer Module

This module optimizes video metadata (titles, descriptions, tags) 
to maximize viral potential and search engine visibility.
"""

import os
import json
import random
import logging
from datetime import datetime
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('metadata_optimizer.log')
    ]
)

logger = logging.getLogger('metadata_optimizer')

class MetadataOptimizer:
    """
    Optimizes video metadata for maximum viral potential and discoverability
    """
    
    def __init__(self, config=None):
        """
        Initialize the metadata optimizer with configuration settings
        
        Args:
            config (dict): Configuration settings for metadata optimization
        """
        self.config = config or {}
        
        # Load title templates
        self.title_templates = self.config.get("title_templates", [
            "LEAKED: Kendrick Lamar - {track_name} [Unreleased 2025]",
            "EXCLUSIVE: Kendrick Lamar - {track_name} [LEAKED 2025]",
            "Kendrick Lamar - {track_name} [UNRELEASED TRACK 2025]",
            "NEW LEAK: Kendrick Lamar - {track_name} [Never Released]",
            "Kendrick Lamar UNRELEASED: {track_name} [Leaked Studio Session]",
            "LEAKED STUDIO SESSION: Kendrick Lamar - {track_name} [2025]",
            "Kendrick Lamar - {track_name} [LEAKED Before Official Release]",
            "RARE FIND: Kendrick Lamar - {track_name} [Unreleased Track]",
            "Kendrick Lamar HIDDEN GEM: {track_name} [Leaked 2025]",
            "MUST HEAR: Kendrick Lamar - {track_name} [Unreleased Material]"
        ])
        
        # Load description templates
        self.description_templates = self.config.get("description_templates", [
            "Exclusive unreleased Kendrick Lamar track '{track_name}' that hasn't been heard before.\n\n" +
            "🔥 Listen before it gets taken down! 🔥\n\n" +
            "Subscribe for more exclusive tracks: {channel_link}\n\n" +
            "Timestamps:\n" +
            "0:00 - Intro\n" +
            "0:15 - Verse 1\n" +
            "1:05 - Hook\n" +
            "1:35 - Verse 2\n" +
            "2:25 - Outro\n\n" +
            "#KendrickLamar #LeakedMusic #Exclusive",
            
            "LEAKED Kendrick Lamar track '{track_name}' - this unreleased gem was never officially released.\n\n" +
            "⚠️ This might be removed soon - make sure to subscribe for more: {channel_link} ⚠️\n\n" +
            "This track shows a different side of Kendrick's artistry that fans rarely get to hear.\n\n" +
            "Timestamps:\n" +
            "0:00 - Intro\n" +
            "0:20 - First Verse\n" +
            "1:10 - Chorus\n" +
            "1:40 - Second Verse\n" +
            "2:30 - Outro\n\n" +
            "#KendrickLamar #UnreleasedMusic #RareTrack",
            
            "'{track_name}' - A rare unreleased Kendrick Lamar track that never made it to an official album.\n\n" +
            "👀 Share this before it disappears! 👀\n\n" +
            "Hit subscribe for more exclusive content: {channel_link}\n\n" +
            "This track was recorded during the sessions for his upcoming album but was left off the final tracklist.\n\n" +
            "Timestamps:\n" +
            "0:00 - Beat Intro\n" +
            "0:15 - Opening Lines\n" +
            "0:45 - First Verse\n" +
            "1:30 - Hook\n" +
            "2:00 - Second Verse\n" +
            "2:45 - Outro\n\n" +
            "#KendrickLamar #LeakedTrack #UnreleasedMusic"
        ])
        
        # Load tag sets
        self.tag_sets = self.config.get("tag_sets", [
            [
                "kendrick lamar", "leaked music", "unreleased", "exclusive", "new kendrick", 
                "2025 music", "rare tracks", "studio session", "kendrick leaks", "hip hop"
            ],
            [
                "kendrick lamar unreleased", "leaked tracks", "exclusive music", "rare kendrick", 
                "new hip hop", "kendrick 2025", "unreleased gems", "rap leaks", "studio recordings"
            ],
            [
                "kendrick new music", "leaked album", "unreleased songs", "exclusive content", 
                "kendrick studio sessions", "hip hop leaks", "rap exclusives", "2025 leaks"
            ]
        ])
        
        # Load viral phrases
        self.viral_phrases = self.config.get("viral_phrases", [
            "Listen before it gets taken down!",
            "This might be removed soon!",
            "Share this before it disappears!",
            "Exclusive content you won't find anywhere else!",
            "Never-before-heard Kendrick track!",
            "Rare studio recording leaked!",
            "This track was supposed to stay hidden!",
            "The track Kendrick didn't want you to hear!",
            "Limited time - this will be removed soon!",
            "Leaked from the vault - hear it while you can!"
        ])
        
        # Load emojis for viral content
        self.viral_emojis = self.config.get("viral_emojis", [
            "🔥", "👀", "🚨", "💯", "🔊", "⚠️", "🤫", "😱", "🤯", "💥"
        ])
    
    def optimize_metadata(self, track_name, duration=None, channel_id=None):
        """
        Generate optimized metadata for a track
        
        Args:
            track_name (str): Name of the track
            duration (float, optional): Duration of the track in seconds
            channel_id (str, optional): YouTube channel ID
            
        Returns:
            dict: Optimized metadata
        """
        # Clean track name
        clean_track_name = self._clean_track_name(track_name)
        
        # Generate title
        title = self._generate_title(clean_track_name)
        
        # Generate description
        description = self._generate_description(clean_track_name, duration, channel_id)
        
        # Generate tags
        tags = self._generate_tags(clean_track_name)
        
        # Create metadata
        metadata = {
            "title": title,
            "description": description,
            "tags": tags,
            "category": "10",  # Music category
            "privacyStatus": "public",
            "track_name": clean_track_name,
            "optimization_time": datetime.now().isoformat()
        }
        
        logger.info(f"Generated optimized metadata for: {clean_track_name}")
        
        return metadata
    
    def _clean_track_name(self, track_name):
        """
        Clean track name for better presentation
        
        Args:
            track_name (str): Original track name
            
        Returns:
            str: Cleaned track name
        """
        # Remove file extension if present
        track_name = os.path.splitext(os.path.basename(track_name))[0]
        
        # Remove common prefixes/suffixes
        prefixes_to_remove = ["kendrick", "lamar", "kendrick lamar", "leaked", "unreleased"]
        for prefix in prefixes_to_remove:
            pattern = f"^{prefix}\\s*[-_]\\s*"
            track_name = re.sub(pattern, "", track_name, flags=re.IGNORECASE)
        
        # Remove brackets, parentheses and their contents
        track_name = re.sub(r"\[.*?\]|\(.*?\)", "", track_name)
        
        # Replace underscores and multiple spaces
        track_name = track_name.replace("_", " ")
        track_name = re.sub(r"\s+", " ", track_name)
        
        # Title case
        track_name = track_name.title()
        
        # Trim
        track_name = track_name.strip()
        
        # If empty after cleaning, use a default
        if not track_name:
            track_name = "Untitled Track"
        
        return track_name
    
    def _generate_title(self, track_name):
        """
        Generate optimized title
        
        Args:
            track_name (str): Track name
            
        Returns:
            str: Optimized title
        """
        # Select random title template
        template = random.choice(self.title_templates)
        
        # Format template
        title = template.format(track_name=track_name)
        
        # Add emoji for extra viral potential (50% chance)
        if random.random() < 0.5:
            emoji = random.choice(self.viral_emojis)
            title = f"{emoji} {title} {emoji}"
        
        # Ensure title is not too long (YouTube limit is 100 characters)
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title
    
    def _generate_description(self, track_name, duration=None, channel_id=None):
        """
        Generate optimized description
        
        Args:
            track_name (str): Track name
            duration (float, optional): Duration of the track in seconds
            channel_id (str, optional): YouTube channel ID
            
        Returns:
            str: Optimized description
        """
        # Create channel link
        channel_link = f"https://www.youtube.com/channel/{channel_id}" if channel_id else "https://www.youtube.com"
        
        # Select random description template
        template = random.choice(self.description_templates)
        
        # Format template
        description = template.format(track_name=track_name, channel_link=channel_link)
        
        # Add custom timestamps if duration is provided
        if duration:
            description = self._add_timestamps(description, duration)
        
        # Add random viral phrase
        viral_phrase = random.choice(self.viral_phrases)
        description = f"{viral_phrase}\n\n{description}"
        
        # Add random emojis
        emoji_count = random.randint(2, 5)
        emojis = random.sample(self.viral_emojis, emoji_count)
        emoji_str = " ".join(emojis)
        
        # Add emojis at beginning and end
        description = f"{emoji_str}\n{description}\n{emoji_str}"
        
        return description
    
    def _add_timestamps(self, description, duration):
        """
        Add custom timestamps based on track duration
        
        Args:
            description (str): Description text
            duration (float): Duration in seconds
            
        Returns:
            str: Description with updated timestamps
        """
        # Check if description already has timestamps
        if "Timestamps:" in description:
            # Extract timestamps section
            timestamp_pattern = r"Timestamps:.*?(?=\n\n|$)"
            timestamp_match = re.search(timestamp_pattern, description, re.DOTALL)
            
            if timestamp_match:
                original_timestamps = timestamp_match.group(0)
                
                # Generate new timestamps
                new_timestamps = self._generate_timestamps(duration)
                
                # Replace original timestamps with new ones
                description = description.replace(original_timestamps, new_timestamps)
        
        return description
    
    def _generate_timestamps(self, duration):
        """
        Generate realistic timestamps based on track duration
        
        Args:
            duration (float): Duration in seconds
            
        Returns:
            str: Formatted timestamps section
        """
        # Convert duration to minutes and seconds
        total_seconds = int(duration)
        
        # Define sections
        sections = ["Intro", "Verse 1", "Hook", "Verse 2", "Bridge", "Outro"]
        
        # Calculate approximate section durations
        section_count = min(len(sections), 4 + int(duration / 60))  # More sections for longer tracks
        section_duration = total_seconds / section_count
        
        # Generate timestamps
        timestamps = ["Timestamps:"]
        current_time = 0
        
        for i in range(section_count):
            # Format current time as MM:SS
            minutes = int(current_time / 60)
            seconds = int(current_time % 60)
            time_str = f"{minutes}:{seconds:02d}"
            
            # Add timestamp
            timestamps.append(f"{time_str} - {sections[i]}")
            
            # Update current time
            current_time += section_duration
        
        return "\n".join(timestamps)
    
    def _generate_tags(self, track_name):
        """
        Generate optimized tags
        
        Args:
            track_name (str): Track name
            
        Returns:
            list: Optimized tags
        """
        # Select random tag set
        base_tags = random.choice(self.tag_sets)
        
        # Add track-specific tags
        track_words = track_name.lower().split()
        track_tags = []
        
        # Add individual words as tags
        for word in track_words:
            if len(word) > 2 and word not in ["the", "and", "for", "but"]:
                track_tags.append(word)
        
        # Add combinations
        if len(track_words) > 1:
            track_tags.append(" ".join(track_words))
        
        # Add with "kendrick" prefix
        track_tags.append(f"kendrick {track_name.lower()}")
        
        # Combine tags
        all_tags = base_tags + track_tags
        
        # Remove duplicates and ensure uniqueness
        unique_tags = list(set(all_tags))
        
        # Limit to 500 characters total (YouTube limit)
        tags = []
        total_length = 0
        
        for tag in unique_tags:
            # Add 1 for the comma separator
            tag_length = len(tag) + 1
            
            if total_length + tag_length <= 500:
                tags.append(tag)
                total_length += tag_length
            else:
                break
        
        return tags


if __name__ == "__main__":
    # Example usage
    config = {
        "title_templates": [
            "LEAKED: Kendrick Lamar - {track_name} [Unreleased 2025]",
            "EXCLUSIVE: Kendrick Lamar - {track_name} [LEAKED 2025]"
        ]
    }
    
    optimizer = MetadataOptimizer(config)
    
    # Generate metadata
    metadata = optimizer.optimize_metadata("The Heart Part 6", 240, "UC-example123")
    
    print(f"Title: {metadata['title']}")
    print(f"Description: {metadata['description']}")
    print(f"Tags: {metadata['tags']}")
