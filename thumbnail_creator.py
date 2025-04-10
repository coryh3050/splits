"""
Thumbnail Creator Module for AI-Generated Music Videos

This module creates eye-catching thumbnails optimized for click-through rate
to maximize viral potential of AI-generated music videos.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

class ThumbnailCreator:
    """
    Creates eye-catching thumbnails optimized for click-through rate
    """
    
    def __init__(self, config=None):
        """
        Initialize the thumbnail creator with configuration settings
        
        Args:
            config (dict): Configuration settings for thumbnails
        """
        self.config = config or {
            "resolution": (1280, 720),  # YouTube thumbnail resolution
            "style": "high_contrast",   # Options: high_contrast, minimalist, dramatic
            "text_overlay": True,
            "emoji_use": True,
            "font_path": None  # Will use default fonts if None
        }
        
        # Define color schemes for different styles
        self.color_schemes = {
            "high_contrast": {
                "background": (0, 0, 0),
                "primary": (255, 0, 0),
                "secondary": (255, 255, 0),
                "text": (255, 255, 255)
            },
            "minimalist": {
                "background": (20, 20, 20),
                "primary": (220, 220, 220),
                "secondary": (180, 180, 180),
                "text": (255, 255, 255)
            },
            "dramatic": {
                "background": (20, 20, 20),
                "primary": (212, 175, 55),  # Gold
                "secondary": (128, 0, 128),  # Purple
                "text": (255, 255, 255)
            }
        }
        
        # Define emojis for viral thumbnails
        self.viral_emojis = ["🔥", "👀", "🚨", "💯", "🔊", "⚠️", "🤫", "😱", "🤯", "💥"]
        
    def create_thumbnail(self, output_path, track_name, style=None):
        """
        Create a thumbnail for the given track
        
        Args:
            output_path (str): Path to save the thumbnail
            track_name (str): Name of the track
            style (str, optional): Thumbnail style. If None, uses the style from config
            
        Returns:
            str: Path to the generated thumbnail
        """
        print(f"Creating thumbnail for: {track_name}")
        
        # Get style from config if not provided
        if style is None:
            style = self.config["style"]
        
        # Get color scheme
        colors = self.color_schemes.get(style, self.color_schemes["high_contrast"])
        
        # Create base image
        width, height = self.config["resolution"]
        image = Image.new("RGB", (width, height), colors["background"])
        draw = ImageDraw.Draw(image)
        
        # Choose thumbnail style based on configuration
        if style == "high_contrast":
            image = self._create_high_contrast_thumbnail(image, draw, colors, track_name)
        elif style == "minimalist":
            image = self._create_minimalist_thumbnail(image, draw, colors, track_name)
        elif style == "dramatic":
            image = self._create_dramatic_thumbnail(image, draw, colors, track_name)
        else:
            # Default to high contrast
            image = self._create_high_contrast_thumbnail(image, draw, colors, track_name)
        
        # Save thumbnail
        image.save(output_path)
        print(f"Thumbnail created: {output_path}")
        
        return output_path
    
    def _create_high_contrast_thumbnail(self, image, draw, colors, track_name):
        """
        Create a high contrast thumbnail with bold text and colors
        
        Args:
            image (PIL.Image): Base image
            draw (PIL.ImageDraw): ImageDraw object
            colors (dict): Color scheme
            track_name (str): Name of the track
            
        Returns:
            PIL.Image: Generated thumbnail
        """
        width, height = image.size
        
        # Create background with gradient
        for y in range(height):
            r = int(colors["primary"][0] * (1 - y/height) + colors["secondary"][0] * (y/height))
            g = int(colors["primary"][1] * (1 - y/height) + colors["secondary"][1] * (y/height))
            b = int(colors["primary"][2] * (1 - y/height) + colors["secondary"][2] * (y/height))
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Apply blur to create more dynamic background
        image = image.filter(ImageFilter.GaussianBlur(radius=5))
        draw = ImageDraw.Draw(image)
        
        # Add diagonal stripes for visual interest
        for i in range(-2 * width, 2 * width, 40):
            draw.line([(i, 0), (i + width, height)], fill=colors["primary"], width=10)
        
        # Add "LEAKED" text at the top
        try:
            # Try to load a bold font
            font_large = ImageFont.truetype("Arial Bold", 120)
            font_medium = ImageFont.truetype("Arial Bold", 80)
            font_small = ImageFont.truetype("Arial", 60)
        except IOError:
            # Fall back to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add "LEAKED" text with shadow effect
        leaked_text = "LEAKED"
        text_width = draw.textlength(leaked_text, font=font_large)
        x = (width - text_width) // 2
        y = 50
        
        # Draw shadow
        draw.text((x+5, y+5), leaked_text, fill=(0, 0, 0), font=font_large)
        # Draw text
        draw.text((x, y), leaked_text, fill=colors["text"], font=font_large)
        
        # Add track name
        track_text = track_name.upper()
        if len(track_text) > 20:
            # Truncate long track names
            track_text = track_text[:17] + "..."
        
        text_width = draw.textlength(track_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 - 40
        
        # Draw shadow
        draw.text((x+4, y+4), track_text, fill=(0, 0, 0), font=font_medium)
        # Draw text
        draw.text((x, y), track_text, fill=colors["text"], font=font_medium)
        
        # Add "KENDRICK LAMAR" text
        artist_text = "KENDRICK LAMAR"
        text_width = draw.textlength(artist_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 + 60
        
        # Draw shadow
        draw.text((x+4, y+4), artist_text, fill=(0, 0, 0), font=font_medium)
        # Draw text
        draw.text((x, y), artist_text, fill=colors["primary"], font=font_medium)
        
        # Add "UNRELEASED 2025" text
        unreleased_text = "UNRELEASED 2025"
        text_width = draw.textlength(unreleased_text, font=font_small)
        x = (width - text_width) // 2
        y = height - 120
        
        # Draw shadow
        draw.text((x+3, y+3), unreleased_text, fill=(0, 0, 0), font=font_small)
        # Draw text
        draw.text((x, y), unreleased_text, fill=colors["secondary"], font=font_small)
        
        # Add emojis if enabled
        if self.config["emoji_use"]:
            # Add fire emoji at the beginning and end of track name
            emoji = random.choice(self.viral_emojis)
            emoji_text = f"{emoji} {emoji}"
            text_width = draw.textlength(emoji_text, font=font_medium)
            x = (width - text_width) // 2
            y = height // 2 - 130
            
            draw.text((x, y), emoji_text, font=font_medium)
        
        # Add a semi-transparent overlay at the bottom for better text visibility
        overlay = Image.new('RGBA', (width, 150), (0, 0, 0, 180))
        image.paste(overlay, (0, height - 150), overlay)
        
        return image
    
    def _create_minimalist_thumbnail(self, image, draw, colors, track_name):
        """
        Create a minimalist thumbnail with clean design
        
        Args:
            image (PIL.Image): Base image
            draw (PIL.ImageDraw): ImageDraw object
            colors (dict): Color scheme
            track_name (str): Name of the track
            
        Returns:
            PIL.Image: Generated thumbnail
        """
        width, height = image.size
        
        # Create solid background
        draw.rectangle([(0, 0), (width, height)], fill=colors["background"])
        
        # Add subtle texture
        for _ in range(5000):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            brightness = random.randint(30, 60)
            draw.point((x, y), fill=(brightness, brightness, brightness))
        
        # Add minimalist border
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), (width-border_width, height-border_width)],
            outline=colors["primary"],
            width=border_width
        )
        
        try:
            # Try to load fonts
            font_large = ImageFont.truetype("Arial", 100)
            font_medium = ImageFont.truetype("Arial", 70)
            font_small = ImageFont.truetype("Arial", 50)
        except IOError:
            # Fall back to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add "LEAKED" text
        leaked_text = "LEAKED"
        text_width = draw.textlength(leaked_text, font=font_large)
        x = (width - text_width) // 2
        y = 80
        draw.text((x, y), leaked_text, fill=colors["text"], font=font_large)
        
        # Add track name
        track_text = track_name.upper()
        if len(track_text) > 20:
            # Truncate long track names
            track_text = track_text[:17] + "..."
        
        text_width = draw.textlength(track_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 - 35
        draw.text((x, y), track_text, fill=colors["text"], font=font_medium)
        
        # Add horizontal line separator
        line_y = height // 2 + 50
        draw.line([(width//4, line_y), (3*width//4, line_y)], fill=colors["primary"], width=3)
        
        # Add "KENDRICK LAMAR" text
        artist_text = "KENDRICK LAMAR"
        text_width = draw.textlength(artist_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 + 80
        draw.text((x, y), artist_text, fill=colors["primary"], font=font_medium)
        
        # Add "UNRELEASED 2025" text
        unreleased_text = "UNRELEASED 2025"
        text_width = draw.textlength(unreleased_text, font=font_small)
        x = (width - text_width) // 2
        y = height - 100
        draw.text((x, y), unreleased_text, fill=colors["secondary"], font=font_small)
        
        return image
    
    def _create_dramatic_thumbnail(self, image, draw, colors, track_name):
        """
        Create a dramatic thumbnail with intense visual elements
        
        Args:
            image (PIL.Image): Base image
            draw (PIL.ImageDraw): ImageDraw object
            colors (dict): Color scheme
            track_name (str): Name of the track
            
        Returns:
            PIL.Image: Generated thumbnail
        """
        width, height = image.size
        
        # Create dark background with vignette effect
        draw.rectangle([(0, 0), (width, height)], fill=colors["background"])
        
        # Create radial gradient for vignette effect
        center_x, center_y = width // 2, height // 2
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # Convert to numpy array for faster processing
        img_array = np.array(image)
        
        for y in range(height):
            for x in range(width):
                # Calculate distance from center
                dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                # Calculate vignette factor
                factor = 1 - (dist / max_dist) ** 2
                factor = max(0.4, factor)  # Limit darkening
                
                # Apply vignette
                img_array[y, x] = (
                    int(img_array[y, x, 0] * factor),
                    int(img_array[y, x, 1] * factor),
                    int(img_array[y, x, 2] * factor)
                )
        
        # Convert back to PIL image
        image = Image.fromarray(img_array)
        draw = ImageDraw.Draw(image)
        
        # Add dramatic diagonal lines
        for i in range(0, width*2, 40):
            line_color = colors["primary"] if i % 80 == 0 else colors["secondary"]
            draw.line([(i-width, 0), (i, height)], fill=line_color, width=5)
        
        try:
            # Try to load fonts
            font_large = ImageFont.truetype("Impact", 120)
            font_medium = ImageFont.truetype("Impact", 80)
            font_small = ImageFont.truetype("Arial Bold", 60)
        except IOError:
            # Fall back to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add "LEAKED" text with dramatic styling
        leaked_text = "LEAKED"
        text_width = draw.textlength(leaked_text, font=font_large)
        x = (width - text_width) // 2
        y = 50
        
        # Draw text with multiple outlines for dramatic effect
        for offset in range(5, 0, -1):
            draw.text((x+offset, y+offset), leaked_text, fill=(0, 0, 0), font=font_large)
        
        draw.text((x, y), leaked_text, fill=colors["primary"], font=font_large)
        
        # Add track name
        track_text = track_name.upper()
        if len(track_text) > 20:
            # Truncate long track names
            track_text = track_text[:17] + "..."
        
        text_width = draw.textlength(track_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 - 40
        
        # Draw text with outline
        for offset in range(3, 0, -1):
            draw.text((x+offset, y+offset), track_text, fill=(0, 0, 0), font=font_medium)
        
        draw.text((x, y), track_text, fill=colors["text"], font=font_medium)
        
        # Add "KENDRICK LAMAR" text
        artist_text = "KENDRICK LAMAR"
        text_width = draw.textlength(artist_text, font=font_medium)
        x = (width - text_width) // 2
        y = height // 2 + 60
        
        # Draw text with outline
        for offset in range(3, 0, -1):
            draw.text((x+offset, y+offset), artist_text, fill=(0, 0, 0), font=font_medium)
        
        draw.text((x, y), artist_text, fill=colors["secondary"], font=font_medium)
        
        # Add "UNRELEASED 2025" text
        unreleased_text = "UNRELEASED 2025"
        text_width = draw.textlength(unreleased_text, font=font_small)
        x = (width - text_width) // 2
        y = height - 120
        
        # Draw text with outline
        for offset in range(2, 0, -1):
            draw.text((x+offset, y+offset), unreleased_text, fill=(0, 0, 0), font=font_small)
        
        draw.text((x, y), unreleased_text, fill=colors["primary"], font=font_small)
        
        # Add emojis if enabled
        if self.config["emoji_use"]:
            # Add warning emoji for dramatic effect
            emoji = "⚠️"
            emoji_text = f"{emoji} {emoji}"
            text_width = draw.textlength(emoji_text, font=font_large)
            x = (width - text_width) // 2
            y = height // 2 - 150
            
            draw.text((x, y), emoji_text, font=font_large)
        
        # Add dramatic light rays
        for i in range(12):
            angle = i * 30
            radian = np.radians(angle)
            x1 = center_x
            y1 = center_y
            x2 = int(center_x + np.cos(radian) * max_dist)<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>