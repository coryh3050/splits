#!/usr/bin/env python3
"""
Installation Script for YouTube Automation System

This script automates the installation process for the YouTube Automation system,
including dependency installation, directory setup, and initial configuration.
"""

import os
import sys
import json
import argparse
import subprocess
import platform
import shutil
from pathlib import Path

# Configuration
DEFAULT_CONFIG = {
    "general": {
        "working_dir": os.path.abspath(os.path.dirname(__file__)),
        "input_dir": "input",
        "output_dir": "output",
        "temp_dir": "temp",
        "data_dir": "data"
    },
    "video_generator": {
        "resolution": "1080p",
        "fps": 30,
        "transition_style": "beat_sync",
        "visual_effects": ["zoom", "pulse", "glitch"],
        "color_scheme": "high_contrast"
    },
    "uploader": {
        "schedule_strategy": "optimal_time",
        "upload_frequency": "daily",
        "max_daily_uploads": 1,
        "client_secrets_file": "client_secret.json",
        "credentials_file": "youtube_credentials.json"
    },
    "promotion": {
        "platforms": ["twitter", "reddit", "tiktok"],
        "comment_response_rate": 0.7,
        "auto_engagement": True,
        "notification_frequency": "daily"
    },
    "analytics": {
        "data_window_days": 30,
        "update_frequency": 24,
        "viral_threshold": 10000,
        "dashboard_types": ["channel", "videos", "trends", "audience"]
    },
    "automation": {
        "process_frequency": 1,
        "upload_time_slots": ["15:00", "18:00", "21:00"],
        "promotion_delay": 15,
        "analysis_frequency": 24
    }
}

REQUIREMENTS = [
    "google-api-python-client",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "oauth2client",
    "ffmpeg-python",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "schedule",
    "requests",
    "pillow",
    "pydub",
    "moviepy",
    "tqdm"
]

def print_header(message):
    """Print a formatted header message"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def run_command(command, error_message=None):
    """Run a shell command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if error_message:
            print(f"ERROR: {error_message}")
            print(f"Command: {command}")
            print(f"Error details: {e.stderr}")
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python version")
    
    required_version = (3, 8)
    current_version = sys.version_info
    
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    print(f"Required Python version: {required_version[0]}.{required_version[1]} or higher")
    
    if current_version.major < required_version[0] or \
       (current_version.major == required_version[0] and current_version.minor < required_version[1]):
        print("ERROR: Python version is too old")
        print(f"Please install Python {required_version[0]}.{required_version[1]} or higher")
        return False
    
    print("Python version check: PASSED")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print_header("Checking FFmpeg installation")
    
    success, output = run_command("ffmpeg -version", "FFmpeg is not installed or not in PATH")
    
    if not success:
        print("FFmpeg is required for video processing.")
        print("Please install FFmpeg:")
        print("  - Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  - macOS: brew install ffmpeg")
        print("  - Windows: Download from https://ffmpeg.org/download.html")
        return False
    
    print("FFmpeg is installed:")
    version_line = output.split('\n')[0]
    print(f"  {version_line}")
    print("FFmpeg check: PASSED")
    return True

def install_python_dependencies():
    """Install required Python packages"""
    print_header("Installing Python dependencies")
    
    # Create requirements.txt file
    with open("requirements.txt", "w") as f:
        f.write("\n".join(REQUIREMENTS))
    
    print(f"Installing {len(REQUIREMENTS)} packages...")
    success, output = run_command("pip install -r requirements.txt", "Failed to install Python dependencies")
    
    if not success:
        print("ERROR: Failed to install required Python packages")
        return False
    
    print("Python dependencies installed successfully")
    return True

def create_directories(config):
    """Create required directories"""
    print_header("Creating directories")
    
    directories = [
        config["general"]["input_dir"],
        config["general"]["output_dir"],
        config["general"]["temp_dir"],
        config["general"]["data_dir"],
        os.path.join(config["general"]["input_dir"], "processed"),
        "dashboards",
        "logs"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            print(f"Creating directory: {directory}")
            path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"Directory already exists: {directory}")
    
    print("Directory setup: COMPLETED")
    return True

def create_config_file(config_path="config.json"):
    """Create default configuration file"""
    print_header("Creating configuration file")
    
    if os.path.exists(config_path):
        print(f"Configuration file already exists: {config_path}")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower() == 'y'
        if not overwrite:
            print("Keeping existing configuration file")
            return True
    
    print(f"Creating default configuration file: {config_path}")
    with open(config_path, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    
    print("Configuration file created successfully")
    print("You can customize the configuration by editing this file")
    return True

def check_youtube_credentials():
    """Check for YouTube API credentials"""
    print_header("Checking YouTube API credentials")
    
    client_secrets_file = "client_secret.json"
    
    if os.path.exists(client_secrets_file):
        print(f"Found YouTube API credentials: {client_secrets_file}")
        return True
    
    print(f"YouTube API credentials not found: {client_secrets_file}")
    print("\nTo set up YouTube API credentials:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable the YouTube Data API v3")
    print("4. Create OAuth 2.0 credentials")
    print("5. Download the client secrets file and save as 'client_secret.json' in this directory")
    
    return False

def create_sample_script():
    """Create a sample script to run the system"""
    print_header("Creating sample scripts")
    
    # Create run script for the current platform
    if platform.system() == "Windows":
        with open("run.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting YouTube Automation System...\n")
            f.write("python src/main.py\n")
            f.write("pause\n")
        print("Created Windows batch file: run.bat")
    else:
        with open("run.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"Starting YouTube Automation System...\"\n")
            f.write("python3 src/main.py\n")
        os.chmod("run.sh", 0o755)
        print("Created shell script: run.sh")
    
    # Create background run script
    if platform.system() == "Windows":
        with open("run_background.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting YouTube Automation System in background...\n")
            f.write("start /B pythonw src/main.py > automation.log 2>&1\n")
        print("Created Windows background batch file: run_background.bat")
    else:
        with open("run_background.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"Starting YouTube Automation System in background...\"\n")
            f.write("nohup python3 src/main.py > automation.log 2>&1 &\n")
            f.write("echo $! > automation.pid\n")
            f.write("echo \"Process started with PID: $(cat automation.pid)\"\n")
        os.chmod("run_background.sh", 0o755)
        print("Created background shell script: run_background.sh")
    
    # Create status check script
    if platform.system() == "Windows":
        with open("check_status.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Checking YouTube Automation System status...\n")
            f.write("python src/main.py --status\n")
            f.write("pause\n")
        print("Created Windows status check script: check_status.bat")
    else:
        with open("check_status.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo \"Checking YouTube Automation System status...\"\n")
            f.write("python3 src/main.py --status\n")
        os.chmod("check_status.sh", 0o755)
        print("Created status check script: check_status.sh")
    
    print("Sample scripts created successfully")
    return True

def create_sample_audio():
    """Create a sample audio file for testing"""
    print_header("Creating sample audio file")
    
    try:
        # Check if we have numpy and create a simple sine wave audio file
        import numpy as np
        from scipy.io import wavfile
        
        print("Generating sample audio file...")
        
        # Generate a simple beat pattern
        sample_rate = 44100
        duration = 30  # seconds
        
        # Create a simple beat pattern
        t = np.linspace(0, duration, sample_rate * duration, False)
        
        # Generate a sine wave with some beats
        freq = 440  # A4 note
        signal = np.sin(2 * np.pi * freq * t) * 0.3
        
        # Add some beats
        beat_freq = 1  # 1 beat per second
        beats = np.sin(2 * np.pi * beat_freq * t)
        beats = (beats > 0.9).astype(float) * 0.7
        
        # Combine signals
        signal = signal + beats
        
        # Normalize
        signal = signal / np.max(np.abs(signal))
        
        # Convert to 16-bit PCM
        signal = (signal * 32767).astype(np.int16)
        
        # Save as WAV file
        sample_dir = os.path.join(DEFAULT_CONFIG["general"]["input_dir"])
        os.makedirs(sample_dir, exist_ok=True)
        
        sample_path = os.path.join(sample_dir, "Sample_Beat_Track.wav")
        wavfile.write(sample_path, sample_rate, signal)
        
        print(f"Sample audio file created: {sample_path}")
        return True
        
    except ImportError:
        print("Could not create sample audio file (numpy or scipy not installed)")
        print("You'll need to add your own audio files to the input directory")
        return True
    except Exception as e:
        print(f"Error creating sample audio file: {str(e)}")
        print("You'll need to add your own audio files to the input directory")
        return True

def main():
    """Main installation function"""
    parser = argparse.ArgumentParser(description="Install YouTube Automation System")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    parser.add_argument("--skip-ffmpeg", action="store_true", help="Skip FFmpeg check")
    parser.add_argument("--config", type=str, default="config.json", help="Path for configuration file")
    
    args = parser.parse_args()
    
    print_header("YouTube Automation System Installation")
    print("This script will set up the YouTube Automation System for AI-generated music")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check FFmpeg installation
    if not args.skip_ffmpeg and not check_ffmpeg():
        print("WARNING: FFmpeg check failed, but installation will continue")
        print("You will need to install FFmpeg before using the system")
    
    # Install Python dependencies
    if not args.skip_deps and not install_python_dependencies():
        return False
    
    # Create configuration file
    if not create_config_file(args.config):
        return False
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    # Create directories
    if not create_directories(config):
        return False
    
    # Check YouTube credentials
    has_credentials = check_youtube_credentials()
    if not has_credentials:
        print("WARNING: YouTube API credentials not found")
        print("You will need to set up credentials before using the system")
    
    # Create sample scripts
    if not create_sample_script():
        return False
    
    # Create sample audio file
    create_sample_audio()
    
    print_header("Installation Complete")
    print("The YouTube Automation System has been successfully installed!")
    print("\nNext steps:")
    
    if not has_credentials:
        print("1. Set up YouTube API credentials (see instructions above)")
    
    print(f"1. Place your AI-generated music files in the '{config['general']['input_dir']}' directory")
    
    if platform.system() == "Windows":
        print("2. Run the system using run.bat or run_background.bat")
    else:
        print("2. Run the system using ./run.sh or ./run_background.sh")
    
    print("3. Check the documentation in the docs directory for more information")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
