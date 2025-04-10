"""
Trend Analysis Module

This module analyzes YouTube trends and provides optimization recommendations
to maximize viral potential for AI-generated music videos.
"""

import os
import json
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trend_analysis.log')
    ]
)

logger = logging.getLogger('trend_analysis')

class TrendAnalyzer:
    """
    Analyzes trends and provides optimization recommendations
    """
    
    def __init__(self, youtube_analytics=None, config=None):
        """
        Initialize the trend analyzer with configuration settings
        
        Args:
            youtube_analytics: YouTube Analytics API client
            config (dict): Configuration settings for trend analysis
        """
        self.config = config or {}
        self.youtube_analytics = youtube_analytics
        
        # Set analysis settings
        self.settings = {
            "trend_window_days": self.config.get("trend_window_days", 30),
            "min_views_threshold": self.config.get("min_views_threshold", 1000),
            "viral_threshold": self.config.get("viral_threshold", 10000),
            "data_cache_time": self.config.get("data_cache_time", 24)  # hours
        }
        
        # Initialize data cache
        self.data_cache = {
            "channel_stats": {"data": None, "timestamp": None},
            "top_videos": {"data": None, "timestamp": None},
            "audience_demographics": {"data": None, "timestamp": None},
            "traffic_sources": {"data": None, "timestamp": None}
        }
    
    def set_youtube_analytics(self, youtube_analytics):
        """
        Set YouTube Analytics client
        
        Args:
            youtube_analytics: YouTube Analytics API client
        """
        self.youtube_analytics = youtube_analytics
    
    def analyze_channel_trends(self, force_refresh=False):
        """
        Analyze channel trends
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            dict: Channel trend analysis
        """
        if not self.youtube_analytics:
            logger.error("YouTube Analytics client not set")
            return {"error": "YouTube Analytics client not set"}
        
        # Get channel stats
        channel_stats = self._get_cached_data("channel_stats", force_refresh)
        if "error" in channel_stats:
            return channel_stats
        
        # Get top videos
        top_videos = self._get_cached_data("top_videos", force_refresh)
        if "error" in top_videos:
            return top_videos
        
        # Analyze trends
        trends = {
            "overall_performance": self._analyze_overall_performance(channel_stats),
            "content_trends": self._analyze_content_trends(top_videos),
            "growth_trends": self._analyze_growth_trends(channel_stats),
            "engagement_trends": self._analyze_engagement_trends(channel_stats, top_videos),
            "recommendations": []
        }
        
        # Generate recommendations
        trends["recommendations"] = self._generate_recommendations(trends)
        
        logger.info("Channel trend analysis completed")
        
        return trends
    
    def analyze_video_performance(self, video_id):
        """
        Analyze performance of a specific video
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video performance analysis
        """
        if not self.youtube_analytics:
            logger.error("YouTube Analytics client not set")
            return {"error": "YouTube Analytics client not set"}
        
        try:
            # Get video stats
            video_stats = self.youtube_analytics.get_video_stats(video_id)
            if "error" in video_stats:
                return video_stats
            
            # Analyze performance
            analysis = {
                "video_id": video_id,
                "title": video_stats.get("title", "Unknown"),
                "views": video_stats.get("views", 0),
                "performance_metrics": {
                    "engagement_rate": video_stats.get("engagement_rate", 0),
                    "retention_rate": video_stats.get("retention_rate", 0),
                    "subscribers_gained": video_stats.get("subscribers_gained", 0)
                },
                "is_viral": video_stats.get("views", 0) >= self.settings["viral_threshold"],
                "performance_score": self._calculate_performance_score(video_stats),
                "strengths": [],
                "weaknesses": [],
                "recommendations": []
            }
            
            # Identify strengths and weaknesses
            self._identify_video_strengths_weaknesses(analysis, video_stats)
            
            # Generate recommendations
            analysis["recommendations"] = self._generate_video_recommendations(analysis, video_stats)
            
            logger.info(f"Video performance analysis completed for video ID: {video_id}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing video performance: {str(e)}")
            return {"error": str(e)}
    
    def identify_trending_topics(self, force_refresh=False):
        """
        Identify trending topics based on top performing videos
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            dict: Trending topics analysis
        """
        if not self.youtube_analytics:
            logger.error("YouTube Analytics client not set")
            return {"error": "YouTube Analytics client not set"}
        
        # Get top videos
        top_videos = self._get_cached_data("top_videos", force_refresh)
        if "error" in top_videos:
            return top_videos
        
        # Extract topics from video titles and descriptions
        topics = self._extract_topics(top_videos)
        
        # Analyze topic performance
        topic_performance = self._analyze_topic_performance(topics, top_videos)
        
        # Identify trending topics
        trending_topics = self._identify_trending_topics(topic_performance)
        
        logger.info(f"Identified {len(trending_topics)} trending topics")
        
        return {
            "trending_topics": trending_topics,
            "topic_performance": topic_performance,
            "recommendations": self._generate_topic_recommendations(trending_topics, topic_performance)
        }
    
    def generate_optimization_suggestions(self, video_data):
        """
        Generate optimization suggestions for a video
        
        Args:
            video_data (dict): Video data including title, description, etc.
            
        Returns:
            dict: Optimization suggestions
        """
        if not self.youtube_analytics:
            logger.error("YouTube Analytics client not set")
            return {"error": "YouTube Analytics client not set"}
        
        try:
            # Get trending topics
            trending_topics = self.identify_trending_topics()
            if "error" in trending_topics:
                trending_topics = {"trending_topics": []}
            
            # Get audience demographics
            demographics = self._get_cached_data("audience_demographics", False)
            if "error" in demographics:
                demographics = {"age_gender": [], "geography": []}
            
            # Analyze video data
            title = video_data.get("title", "")
            description = video_data.get("description", "")
            tags = video_data.get("tags", [])
            
            # Generate suggestions
            suggestions = {
                "title_suggestions": self._generate_title_suggestions(title, trending_topics),
                "description_suggestions": self._generate_description_suggestions(description, trending_topics),
                "tag_suggestions": self._generate_tag_suggestions(tags, trending_topics),
                "thumbnail_suggestions": self._generate_thumbnail_suggestions(demographics),
                "scheduling_suggestions": self._generate_scheduling_suggestions()
            }
            
            logger.info("Generated optimization suggestions")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating optimization suggestions: {str(e)}")
            return {"error": str(e)}
    
    def _get_cached_data(self, data_type, force_refresh=False):
        """
        Get data from cache or refresh from API
        
        Args:
            data_type (str): Type of data to get
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            dict: Requested data
        """
        cache = self.data_cache.get(data_type)
        
        # Check if cache is valid
        cache_valid = (
            cache and 
            cache["data"] and 
            cache["timestamp"] and 
            (datetime.now() - cache["timestamp"]).total_seconds() < self.settings["data_cache_time"] * 3600
        )
        
        if cache_valid and not force_refresh:
            return cache["data"]
        
        # Refresh data from API
        try:
            if data_type == "channel_stats":
                data = self.youtube_analytics.get_channel_stats(days=self.settings["trend_window_days"])
            elif data_type == "top_videos":
                data = self.youtube_analytics.get_top_videos(days=self.settings["trend_window_days"], limit=50)
            elif data_type == "audience_demographics":
                data = self.youtube_analytics.get_audience_demographics()
            elif data_type == "traffic_sources":
                data = self.youtube_analytics.get_traffic_sources(days=self.settings["trend_window_days"])
            else:
                return {"error": f"Unknown data type: {data_type}"}
            
            # Update cache
            self.data_cache[data_type] = {
                "data": data,
                "timestamp": datetime.now()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error refreshing {data_type} data: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_overall_performance(self, channel_stats):
        """
        Analyze overall channel performance
        
        Args:
            channel_stats (dict): Channel statistics
            
        Returns:
            dict: Overall performance analysis
        """
        # Extract key metrics
        total_views = channel_stats.get("total_views", 0)
        total_watch_time = channel_stats.get("total_watch_time", 0)
        net_subscribers = channel_stats.get("net_subscribers", 0)
        
        # Calculate daily averages
        days = self.settings["trend_window_days"]
        daily_views = total_views / days if days > 0 else 0
        daily_watch_time = total_watch_time / days if days > 0 else 0
        daily_subscribers = net_subscribers / days if days > 0 else 0
        
        # Calculate growth rates
        daily_stats = channel_stats.get("daily_stats", [])
        
        if len(daily_stats) >= 14:
            # Compare first half to second half
            half_point = len(daily_stats) // 2
            first_half = daily_stats[:half_point]
            second_half = daily_stats[half_point:]
            
            first_half_views = sum(day.get("views", 0) for day in first_half)
            second_half_views = sum(day.get("views", 0) for day in second_half)
            
            if first_half_views > 0:
                views_growth_rate = (second_half_views - first_half_views) / first_half_views
            else:
                views_growth_rate = 0
            
            first_half_subs = sum(day.get("subscribersGained", 0) for day in first_half)
            second_half_subs = sum(day.get("subscribersGained", 0) for day in second_half)
            
            if first_half_subs > 0:
                subs_growth_rate = (second_half_subs - first_half_subs) / first_half_subs
            else:
                subs_growth_rate = 0
        else:
            views_growth_rate = 0
            subs_growth_rate = 0
        
        return {
            "total_views": total_views,
            "total_watch_time": total_watch_time,
            "net_subscribers": net_subscribers,
            "daily_averages": {
                "views": daily_views,
                "watch_time": daily_watch_time,
                "subscribers": daily_subscribers
            },
            "growth_rates": {
                "views": views_growth_rate,
                "subscribers": subs_growth_rate
            },
            "performance_score": self._calculate_channel_performance_score(channel_stats)
        }
    
    def _analyze_content_trends(self, top_videos):
        """
        Analyze content trends based on top performing videos
        
        Args:
            top_videos (list): Top performing videos
            
        Returns:
            dict: Content trend analysis
        """
        if not top_videos or len(top_videos) == 0:
            return {
                "top_performing_videos": [],
                "common_elements": {},
                "title_patterns": {},
                "duration_analysis": {}
            }
        
        # Filter videos by minimum views threshold
        filtered_videos = [v for v in top_videos if v.get("views", 0) >= self.settings["min_views_threshold"]]
        
        # Sort by views
        sorted_videos = sorted(filtered_videos, key=lambda x: x.get("views", 0), reverse=True)
        
        # Get top 10 videos
        top_10_videos = sorted_videos[:10]
        
        # Analyze common elements
        title_words = []
        durations = []
        
        for video in filtered_videos:
            # Extract title words
            title = video.get("title", "").lower()
            words = re.findall(r'\b\w+\b', title)
            title_words.extend(words)
            
            # Extract duration
            duration = video.get("duration", "PT0S")
            duration_seconds = self._parse_duration(duration)
            durations.append(duration_seconds)
        
        # Analyze title patterns
        word_counts = Counter(title_words)
        common_words = word_counts.most_common(20)
        
        # Analyze duration patterns
        if durations:
            avg_duration = sum(durations) / len(durations)
            
            # Group durations
            short_videos = [d for d in durations if d < 180]  # < 3 minutes
            medium_videos = [d for d in durations if 180 <= d < 600]  # 3-10 minutes
            long_videos = [d for d in durations if d >= 600]  # >= 10 minutes
            
            # Calculate performance by duration
            short_avg_views = 0
            medium_avg_views = 0
            long_avg_views = 0
            
            for video in filtered_videos:
                duration = self._parse_duration(video.get("duration", "PT0S"))
                views = video.get("views", 0)
                
                if duration < 180:
                    short_avg_views += views
                elif 180 <= duration < 600:
                    medium_avg_views += views
                else:
                    long_avg_views += views
            
            short_count = len(short_videos) or 1
            medium_count = len(med<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>