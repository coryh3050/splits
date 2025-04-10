'use client';

import React from 'react';
import { Line } from 'recharts';

const PerformanceChart = () => {
  // Mock data - would come from API in real implementation
  const data = [
    { name: 'Jan', views: 4000, subscribers: 240 },
    { name: 'Feb', views: 3000, subscribers: 198 },
    { name: 'Mar', views: 2000, subscribers: 120 },
    { name: 'Apr', views: 2780, subscribers: 160 },
    { name: 'May', views: 1890, subscribers: 110 },
    { name: 'Jun', views: 2390, subscribers: 140 },
    { name: 'Jul', views: 3490, subscribers: 210 },
    { name: 'Aug', views: 4000, subscribers: 240 },
    { name: 'Sep', views: 5000, subscribers: 300 },
    { name: 'Oct', views: 6000, subscribers: 350 },
    { name: 'Nov', views: 7000, subscribers: 400 },
    { name: 'Dec', views: 9000, subscribers: 450 },
  ];

  return (
    <div className="mt-4 h-80">
      <div className="text-center text-gray-500 py-10">
        Performance Chart Component
        <p className="mt-2 text-sm">
          (This would be implemented with Recharts in a real application)
        </p>
      </div>
    </div>
  );
};

export default PerformanceChart;
