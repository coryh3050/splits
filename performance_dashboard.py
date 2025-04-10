"""
Performance Dashboard Module

This module creates a visual dashboard for monitoring channel performance
and tracking the effectiveness of the AI-generated music videos.
"""

import os
import json
import time
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from matplotlib.ticker import FuncFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('performance_dashboard.log')
    ]
)

logger = logging.getLogger('performance_dashboard')

class PerformanceDashboard:
    """
    Creates visual dashboards for monitoring channel and video performance
    """
    
    def __init__(self, youtube_analytics=None, trend_analyzer=None, config=None):
        """
        Initialize the performance dashboard with configuration settings
        
        Args:
            youtube_analytics: YouTube Analytics API client
            trend_analyzer: Trend Analyzer instance
            config (dict): Configuration settings for the dashboard
        """
        self.config = config or {}
        self.youtube_analytics = youtube_analytics
        self.trend_analyzer = trend_analyzer
        
        # Set dashboard settings
        self.settings = {
            "output_dir": self.config.get("output_dir", "dashboards"),
            "data_window_days": self.config.get("data_window_days", 30),
            "update_frequency": self.config.get("update_frequency", 24),  # hours
            "dashboard_types": self.config.get("dashboard_types", ["channel", "videos", "trends", "audience"])
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(self.settings["output_dir"], exist_ok=True)
        
        # Set style for plots
        sns.set(style="darkgrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def set_youtube_analytics(self, youtube_analytics):
        """
        Set YouTube Analytics client
        
        Args:
            youtube_analytics: YouTube Analytics API client
        """
        self.youtube_analytics = youtube_analytics
    
    def set_trend_analyzer(self, trend_analyzer):
        """
        Set Trend Analyzer instance
        
        Args:
            trend_analyzer: Trend Analyzer instance
        """
        self.trend_analyzer = trend_analyzer
    
    def generate_dashboards(self, force_refresh=False):
        """
        Generate all dashboards
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            dict: Paths to generated dashboard files
        """
        if not self.youtube_analytics:
            logger.error("YouTube Analytics client not set")
            return {"error": "YouTube Analytics client not set"}
        
        dashboard_paths = {}
        
        # Generate dashboards based on settings
        dashboard_types = self.settings["dashboard_types"]
        
        if "channel" in dashboard_types:
            channel_path = self.generate_channel_dashboard(force_refresh)
            dashboard_paths["channel"] = channel_path
        
        if "videos" in dashboard_types:
            videos_path = self.generate_videos_dashboard(force_refresh)
            dashboard_paths["videos"] = videos_path
        
        if "trends" in dashboard_types and self.trend_analyzer:
            trends_path = self.generate_trends_dashboard(force_refresh)
            dashboard_paths["trends"] = trends_path
        
        if "audience" in dashboard_types:
            audience_path = self.generate_audience_dashboard(force_refresh)
            dashboard_paths["audience"] = audience_path
        
        logger.info(f"Generated {len(dashboard_paths)} dashboards")
        
        return dashboard_paths
    
    def generate_channel_dashboard(self, force_refresh=False):
        """
        Generate channel performance dashboard
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            str: Path to generated dashboard file
        """
        try:
            # Get channel stats
            channel_stats = self.youtube_analytics.get_channel_stats(days=self.settings["data_window_days"])
            if "error" in channel_stats:
                logger.error(f"Error getting channel stats: {channel_stats['error']}")
                return None
            
            # Create figure with subplots
            fig, axs = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Channel Performance Dashboard', fontsize=16)
            
            # Plot 1: Views over time
            self._plot_views_over_time(axs[0, 0], channel_stats)
            
            # Plot 2: Subscribers gained over time
            self._plot_subscribers_over_time(axs[0, 1], channel_stats)
            
            # Plot 3: Engagement metrics
            self._plot_engagement_metrics(axs[1, 0], channel_stats)
            
            # Plot 4: Watch time over time
            self._plot_watch_time_over_time(axs[1, 1], channel_stats)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure
            output_path = os.path.join(self.settings["output_dir"], "channel_dashboard.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)
            
            logger.info(f"Generated channel dashboard: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating channel dashboard: {str(e)}")
            return None
    
    def generate_videos_dashboard(self, force_refresh=False):
        """
        Generate videos performance dashboard
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            str: Path to generated dashboard file
        """
        try:
            # Get top videos
            top_videos = self.youtube_analytics.get_top_videos(days=self.settings["data_window_days"], limit=10)
            if isinstance(top_videos, dict) and "error" in top_videos:
                logger.error(f"Error getting top videos: {top_videos['error']}")
                return None
            
            # Create figure with subplots
            fig, axs = plt.subplots(2, 1, figsize=(16, 14))
            fig.suptitle('Video Performance Dashboard', fontsize=16)
            
            # Plot 1: Top videos by views
            self._plot_top_videos_by_views(axs[0], top_videos)
            
            # Plot 2: Video engagement comparison
            self._plot_video_engagement_comparison(axs[1], top_videos)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure
            output_path = os.path.join(self.settings["output_dir"], "videos_dashboard.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)
            
            logger.info(f"Generated videos dashboard: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating videos dashboard: {str(e)}")
            return None
    
    def generate_trends_dashboard(self, force_refresh=False):
        """
        Generate trends dashboard
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            str: Path to generated dashboard file
        """
        if not self.trend_analyzer:
            logger.error("Trend Analyzer not set")
            return None
        
        try:
            # Get trend analysis
            trends = self.trend_analyzer.analyze_channel_trends(force_refresh)
            if "error" in trends:
                logger.error(f"Error getting trend analysis: {trends['error']}")
                return None
            
            # Get trending topics
            trending_topics = self.trend_analyzer.identify_trending_topics(force_refresh)
            if "error" in trending_topics:
                logger.error(f"Error getting trending topics: {trending_topics['error']}")
                trending_topics = {"trending_topics": [], "topic_performance": []}
            
            # Create figure with subplots
            fig, axs = plt.subplots(2, 2, figsize=(16, 14))
            fig.suptitle('Trend Analysis Dashboard', fontsize=16)
            
            # Plot 1: Content trends
            self._plot_content_trends(axs[0, 0], trends)
            
            # Plot 2: Trending topics
            self._plot_trending_topics(axs[0, 1], trending_topics)
            
            # Plot 3: Growth trends
            self._plot_growth_trends(axs[1, 0], trends)
            
            # Plot 4: Engagement trends
            self._plot_engagement_trends(axs[1, 1], trends)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure
            output_path = os.path.join(self.settings["output_dir"], "trends_dashboard.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)
            
            logger.info(f"Generated trends dashboard: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating trends dashboard: {str(e)}")
            return None
    
    def generate_audience_dashboard(self, force_refresh=False):
        """
        Generate audience demographics dashboard
        
        Args:
            force_refresh (bool): Whether to force refresh data from API
            
        Returns:
            str: Path to generated dashboard file
        """
        try:
            # Get audience demographics
            demographics = self.youtube_analytics.get_audience_demographics()
            if "error" in demographics:
                logger.error(f"Error getting audience demographics: {demographics['error']}")
                return None
            
            # Get traffic sources
            traffic_sources = self.youtube_analytics.get_traffic_sources(days=self.settings["data_window_days"])
            if "error" in traffic_sources:
                logger.error(f"Error getting traffic sources: {traffic_sources['error']}")
                traffic_sources = []
            
            # Create figure with subplots
            fig, axs = plt.subplots(2, 2, figsize=(16, 14))
            fig.suptitle('Audience Demographics Dashboard', fontsize=16)
            
            # Plot 1: Age and gender distribution
            self._plot_age_gender_distribution(axs[0, 0], demographics)
            
            # Plot 2: Geographic distribution
            self._plot_geographic_distribution(axs[0, 1], demographics)
            
            # Plot 3: Traffic sources
            self._plot_traffic_sources(axs[1, 0], traffic_sources)
            
            # Plot 4: Viewer retention
            self._plot_viewer_retention(axs[1, 1])
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure
            output_path = os.path.join(self.settings["output_dir"], "audience_dashboard.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)
            
            logger.info(f"Generated audience dashboard: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating audience dashboard: {str(e)}")
            return None
    
    def generate_video_performance_report(self, video_id):
        """
        Generate performance report for a specific video
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            str: Path to generated report file
        """
        if not self.youtube_analytics or not self.trend_analyzer:
            logger.error("YouTube Analytics or Trend Analyzer not set")
            return None
        
        try:
            # Get video stats
            video_stats = self.youtube_analytics.get_video_stats(video_id)
            if "error" in video_stats:
                logger.error(f"Error getting video stats: {video_stats['error']}")
                return None
            
            # Get video performance analysis
            performance = self.trend_analyzer.analyze_video_performance(video_id)
            if "error" in performance:
                logger.error(f"Error getting video performance analysis: {performance['error']}")
                return None
            
            # Create figure with subplots
            fig, axs = plt.subplots(2, 2, figsize=(16, 14))
            fig.suptitle(f'Video Performance Report: {video_stats["title"]}', fontsize=16)
            
            # Plot 1: Views and engagement over time
            self._plot_video_views_over_time(axs[0, 0], video_stats)
            
            # Plot 2: Performance metrics
            self._plot_video_performance_metrics(axs[0, 1], performance)
            
            # Plot 3: Strengths and weaknesses
            self._plot_video_strengths_weaknesses(axs[1, 0], performance)
            
            # Plot 4: Recommendations
            self._plot_video_recommendations(axs[1, 1], performance)
            
            # Adjust layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure
            output_path = os.path.join(self.settings["output_dir"], f"video_report_{video_id}.png")
            plt.savefig(output_path, dpi=150)
            plt.close(fig)
            
            logger.info(f"Generated video performance report: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating video performance report: {str(e)}")
            return None
    
    def _plot_views_over_time(self, ax, channel_stats):
        """
        Plot views over time
        
        Args:
            ax: Matplotlib axis
            channel_stats (dict): Channel statistics
        """
        daily_stats = channel_stats.get("daily_stats", [])
        
        if not daily_stats:
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            ax.set_title("Views Over Time")
            return
        
        # Extract data
        dates = []
        views = []
        
        for day in daily_stats:
            date_str = day.get("day", "")
            if date_str:
                dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
                views.append(day.get("views", 0))
        
        # Plot data
        ax.plot(dates, views, marker='o', linestyle='-', color='#1f77b4', linewidth=2)
        
        # Add trend line
        if len(dates) > 1:
            z = np.polyfit(range(len(dates)), views, 1)
            p = np.poly1d(z)
            ax.plot(dates, p(range(len(dates))), linestyle='--', color='#ff7f0e', linewidth=2)
        
        # Format axis
        ax.set_title("Views Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Views")
        
        # Format y-axis with K for thousands
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x/1000)}K' if x >= 1000 else str(int(x))))
        
        # Add total views annotation
        total_views = channel_stats.get("total_views", 0)
        ax.annotate(f'Total Views: {total_views:,}', 
                   xy=(0.02, 0.95), xycoords='axes fraction',
                   bbox=dict(boxstyle="round,pad=0.3", fc="#d3d3d3", ec="black", alpha=0.8))
    
    def _plot_subscri<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>