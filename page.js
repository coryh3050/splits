'use client';

import React from 'react';
import { ArrowUp, BarChart2, Users, Clock, TrendingUp } from 'lucide-react';
import StatCard from '@/components/StatCard';
import RecentVideos from '@/components/RecentVideos';
import PerformanceChart from '@/components/PerformanceChart';
import TrendingTopics from '@/components/TrendingTopics';

export default function Dashboard() {
  // Mock data - would come from API in real implementation
  const stats = [
    { title: 'Total Views', value: '124.5K', icon: <BarChart2 className="h-6 w-6" />, change: '+12.5%', changeType: 'positive' },
    { title: 'Subscribers', value: '2,340', icon: <Users className="h-6 w-6" />, change: '+7.2%', changeType: 'positive' },
    { title: 'Watch Time', value: '3,240 hrs', icon: <Clock className="h-6 w-6" />, change: '+14.3%', changeType: 'positive' },
    { title: 'Trending Score', value: '86/100', icon: <TrendingUp className="h-6 w-6" />, change: '+5 pts', changeType: 'positive' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          <ArrowUp className="h-4 w-4 mr-2" />
          Upload New
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <StatCard 
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            change={stat.change}
            changeType={stat.changeType}
          />
        ))}
      </div>

      {/* Charts and Recent Videos */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg lg:col-span-2">
          <div className="p-5">
            <h2 className="text-lg font-medium text-gray-900">Channel Performance</h2>
            <PerformanceChart />
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <h2 className="text-lg font-medium text-gray-900">Trending Topics</h2>
            <TrendingTopics />
          </div>
        </div>
      </div>

      {/* Recent Videos */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
          <h2 className="text-lg font-medium text-gray-900">Recent Videos</h2>
          <RecentVideos />
        </div>
      </div>
    </div>
  );
}
