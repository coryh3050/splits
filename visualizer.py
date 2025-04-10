"""
Visualizer Module for AI-Generated Music Videos

This module creates dynamic visualizations for music tracks to enhance
viewer engagement and increase viral potential.
"""

import os
import numpy as np
import librosa
import cv2
from PIL import Image, ImageDraw, ImageFont
import random
import math

class MusicVisualizer:
    """
    Creates dynamic music visualizations synced to audio features
    """
    
    def __init__(self, config=None):
        """
        Initialize the visualizer with configuration settings
        
        Args:
            config (dict): Configuration settings for visualization
        """
        self.config = config or {
            "resolution": (1920, 1080),
            "fps": 30,
            "visualizer_type": "waveform",
            "color_scheme": "high_contrast",
            "intro_duration": 5,
            "outro_duration": 10
        }
        
        # Color schemes for different visualization styles
        self.color_schemes = {
            "high_contrast": {
                "background": (0, 0, 0),
                "primary": (255, 0, 0),
                "secondary": (0, 0, 255),
                "accent": (255, 255, 0),
                "text": (255, 255, 255)
            },
            "monochrome": {
                "background": (0, 0, 0),
                "primary": (255, 255, 255),
                "secondary": (200, 200, 200),
                "accent": (150, 150, 150),
                "text": (255, 255, 255)
            },
            "artist_themed": {
                "background": (20, 20, 20),
                "primary": (212, 175, 55),  # Gold
                "secondary": (128, 0, 128),  # Purple
                "accent": (255, 255, 255),
                "text": (212, 175, 55)
            }
        }
        
    def analyze_audio(self, audio_path):
        """
        Extract audio features for visualization
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Audio features including tempo, beats, and spectral features
        """
        print(f"Analyzing audio: {audio_path}")
        
        # Load audio file
        y, sr = librosa.load(audio_path)
        
        # Extract tempo and beat information
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Extract spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        # Extract harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # Normalize features for visualization
        duration = librosa.get_duration(y=y, sr=sr)
        total_frames = int(duration * self.config["fps"])
        
        # Resample features to match video frame rate
        beat_frames_resampled = np.zeros(total_frames)
        for beat in beat_times:
            frame_idx = int(beat * self.config["fps"])
            if frame_idx < total_frames:
                beat_frames_resampled[frame_idx] = 1.0
        
        # Resample spectral features to match video frame rate
        spec_cent_resampled = np.interp(
            np.linspace(0, len(spectral_centroids), total_frames),
            np.arange(len(spectral_centroids)),
            spectral_centroids
        )
        
        spec_rolloff_resampled = np.interp(
            np.linspace(0, len(spectral_rolloff), total_frames),
            np.arange(len(spectral_rolloff)),
            spectral_rolloff
        )
        
        # Normalize features
        spec_cent_resampled = (spec_cent_resampled - np.min(spec_cent_resampled)) / (np.max(spec_cent_resampled) - np.min(spec_cent_resampled))
        spec_rolloff_resampled = (spec_rolloff_resampled - np.min(spec_rolloff_resampled)) / (np.max(spec_rolloff_resampled) - np.min(spec_rolloff_resampled))
        
        # Create amplitude envelope
        hop_length = 512
        amplitude_envelope = np.array([
            np.max(abs(y[i:i+hop_length])) for i in range(0, len(y), hop_length)
        ])
        
        # Resample amplitude envelope to match video frame rate
        amplitude_envelope_resampled = np.interp(
            np.linspace(0, len(amplitude_envelope), total_frames),
            np.arange(len(amplitude_envelope)),
            amplitude_envelope
        )
        
        # Normalize amplitude envelope
        amplitude_envelope_resampled = (amplitude_envelope_resampled - np.min(amplitude_envelope_resampled)) / (np.max(amplitude_envelope_resampled) - np.min(amplitude_envelope_resampled))
        
        return {
            "tempo": tempo,
            "beat_frames": beat_frames_resampled,
            "spectral_centroids": spec_cent_resampled,
            "spectral_rolloff": spec_rolloff_resampled,
            "amplitude_envelope": amplitude_envelope_resampled,
            "duration": duration,
            "total_frames": total_frames,
            "sample_rate": sr,
            "y_harmonic": y_harmonic,
            "y_percussive": y_percussive
        }
    
    def create_waveform_visualization(self, audio_features, output_path, track_name):
        """
        Create waveform visualization video
        
        Args:
            audio_features (dict): Audio features extracted from analyze_audio
            output_path (str): Path to save the output video
            track_name (str): Name of the track for text overlays
            
        Returns:
            str: Path to the generated video file
        """
        print(f"Creating waveform visualization for: {track_name}")
        
        # Get configuration
        width, height = self.config["resolution"]
        fps = self.config["fps"]
        colors = self.color_schemes[self.config["color_scheme"]]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Generate intro frames
        intro_frames = int(self.config["intro_duration"] * fps)
        for i in range(intro_frames):
            # Create a fade-in effect
            fade_factor = i / intro_frames
            
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add text overlay
            cv2_frame = self._add_text_overlay(
                frame, 
                f"LEAKED: Kendrick Lamar", 
                position=(width//2, height//3),
                font_scale=2.0 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["text"]]),
                thickness=2,
                center=True
            )
            
            cv2_frame = self._add_text_overlay(
                cv2_frame, 
                track_name, 
                position=(width//2, height//2),
                font_scale=1.5 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["accent"]]),
                thickness=2,
                center=True
            )
            
            cv2_frame = self._add_text_overlay(
                cv2_frame, 
                "UNRELEASED 2025", 
                position=(width//2, 2*height//3),
                font_scale=1.0 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["secondary"]]),
                thickness=2,
                center=True
            )
            
            video_writer.write(cv2_frame)
        
        # Generate main visualization frames
        total_frames = audio_features["total_frames"]
        
        for frame_idx in range(total_frames):
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Get audio features for current frame
            amplitude = audio_features["amplitude_envelope"][frame_idx]
            spectral = audio_features["spectral_centroids"][frame_idx]
            beat = audio_features["beat_frames"][frame_idx]
            
            # Draw waveform
            bar_count = 64
            bar_width = (width - 100) // bar_count
            max_bar_height = height // 2
            
            # Generate bar heights with some randomness influenced by audio features
            bar_heights = []
            for i in range(bar_count):
                # Base height from amplitude
                base_height = amplitude * max_bar_height
                
                # Add variation based on position and spectral content
                variation = math.sin(i / bar_count * math.pi * 4 + frame_idx * 0.05) * 0.3
                spectral_influence = spectral * 0.5
                
                # Combine factors
                height_factor = base_height * (1 + variation + spectral_influence)
                
                # Add beat emphasis
                if beat > 0.5:
                    height_factor *= 1.3
                
                bar_heights.append(min(max_bar_height, height_factor))
            
            # Draw bars
            for i, bar_height in enumerate(bar_heights):
                x = 50 + i * bar_width
                y_center = height // 2
                
                # Determine bar color based on position and audio features
                if i % 4 == 0 and beat > 0.5:
                    color = colors["accent"]
                elif i % 2 == 0:
                    color = colors["primary"]
                else:
                    color = colors["secondary"]
                
                # Draw mirrored bars
                cv2.rectangle(
                    frame,
                    (x, y_center - int(bar_height // 2)),
                    (x + bar_width - 2, y_center + int(bar_height // 2)),
                    color,
                    -1
                )
            
            # Add subtle particle effects during high energy moments
            if amplitude > 0.7 or beat > 0.5:
                particle_count = int(amplitude * 50)
                for _ in range(particle_count):
                    px = random.randint(0, width-1)
                    py = random.randint(0, height-1)
                    size = random.randint(1, 3)
                    cv2.circle(frame, (px, py), size, colors["accent"], -1)
            
            # Add text overlay
            frame = self._add_text_overlay(
                frame, 
                f"LEAKED: Kendrick Lamar - {track_name}", 
                position=(width//2, 50),
                font_scale=1.0,
                color=colors["text"],
                thickness=2,
                center=True
            )
            
            # Add "UNRELEASED" watermark
            frame = self._add_text_overlay(
                frame, 
                "UNRELEASED", 
                position=(width//2, height-50),
                font_scale=0.8,
                color=colors["secondary"],
                thickness=1,
                center=True
            )
            
            video_writer.write(frame)
        
        # Generate outro frames
        outro_frames = int(self.config["outro_duration"] * fps)
        for i in range(outro_frames):
            # Create a fade-out effect
            fade_factor = 1 - (i / outro_frames)
            
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add text overlay
            cv2_frame = self._add_text_overlay(
                frame, 
                "Subscribe for more exclusive tracks", 
                position=(width//2, height//3),
                font_scale=1.5 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["text"]]),
                thickness=2,
                center=True
            )
            
            cv2_frame = self._add_text_overlay(
                cv2_frame, 
                "More leaks coming soon...", 
                position=(width//2, height//2),
                font_scale=1.0 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["accent"]]),
                thickness=2,
                center=True
            )
            
            video_writer.write(cv2_frame)
        
        # Release video writer
        video_writer.release()
        
        print(f"Visualization created: {output_path}")
        return output_path
    
    def create_circular_visualization(self, audio_features, output_path, track_name):
        """
        Create circular visualization video
        
        Args:
            audio_features (dict): Audio features extracted from analyze_audio
            output_path (str): Path to save the output video
            track_name (str): Name of the track for text overlays
            
        Returns:
            str: Path to the generated video file
        """
        print(f"Creating circular visualization for: {track_name}")
        
        # Get configuration
        width, height = self.config["resolution"]
        fps = self.config["fps"]
        colors = self.color_schemes[self.config["color_scheme"]]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Generate intro frames (similar to waveform)
        intro_frames = int(self.config["intro_duration"] * fps)
        for i in range(intro_frames):
            # Create a fade-in effect
            fade_factor = i / intro_frames
            
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add text overlay
            cv2_frame = self._add_text_overlay(
                frame, 
                f"LEAKED: Kendrick Lamar", 
                position=(width//2, height//3),
                font_scale=2.0 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["text"]]),
                thickness=2,
                center=True
            )
            
            cv2_frame = self._add_text_overlay(
                cv2_frame, 
                track_name, 
                position=(width//2, height//2),
                font_scale=1.5 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["accent"]]),
                thickness=2,
                center=True
            )
            
            cv2_frame = self._add_text_overlay(
                cv2_frame, 
                "UNRELEASED 2025", 
                position=(width//2, 2*height//3),
                font_scale=1.0 * fade_factor,
                color=tuple([int(c * fade_factor) for c in colors["secondary"]]),
                thickness=2,
                center=True
            )
            
            video_writer.write(cv2_frame)
        
        # Generate main visualization frames
        total_frames = audio_features["total_frames"]
        center_x, center_y = width // 2, height // 2
        
        for frame_idx in range(total_frames):
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Get audio features for current frame
            amplitude = audio_features["amplitude_envelope"][frame_idx]
            spectral = audio_features["spectral_centroids"][frame_idx]
            beat = audio_features["beat_frames"][frame_idx]
            
            # Draw circular visualizer
            num_circles = 3
            max_radius = min(width, height) // 3
            
            for circle_idx in range(num_circles):
                # Base radius affected by amplitude and circle index
                base_radius = max_radius * (0.4 + 0.6 * (circle_idx + 1) / num_circles)
                
                # Radius var<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>