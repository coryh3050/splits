'use client';

import React from 'react';
import { ArrowUp } from 'lucide-react';

const TrendingTopics = () => {
  // Mock data - would come from API in real implementation
  const topics = [
    { name: 'Kendrick Lamar', score: 98 },
    { name: 'Unreleased Music', score: 92 },
    { name: 'Leaked Tracks', score: 87 },
    { name: 'Hip Hop 2025', score: 82 },
    { name: 'New Beats', score: 76 }
  ];

  return (
    <div className="mt-4">
      <ul className="divide-y divide-gray-200">
        {topics.map((topic, index) => (
          <li key={index} className="py-3 flex justify-between items-center">
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-900">{topic.name}</span>
            </div>
            <div className="flex items-center">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                topic.score >= 90 ? 'bg-green-100 text-green-800' :
                topic.score >= 80 ? 'bg-blue-100 text-blue-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {topic.score}/100
              </span>
              <ArrowUp className={`ml-1 h-4 w-4 ${
                topic.score >= 90 ? 'text-green-500' :
                topic.score >= 80 ? 'text-blue-500' :
                'text-yellow-500'
              }`} />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TrendingTopics;
