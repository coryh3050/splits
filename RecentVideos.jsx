'use client';

import React from 'react';
import { Play, ExternalLink, BarChart2 } from 'lucide-react';

const RecentVideos = () => {
  // Mock data - would come from API in real implementation
  const videos = [
    {
      id: '1',
      title: 'LEAKED: Kendrick Lamar - Dark Thoughts [Unreleased 2025]',
      thumbnail: '/thumbnails/video1.jpg',
      views: '24.5K',
      likes: '1.2K',
      uploadDate: '2 days ago',
      status: 'published'
    },
    {
      id: '2',
      title: 'LEAKED: Kendrick Lamar - Midnight Flow [Unreleased 2025]',
      thumbnail: '/thumbnails/video2.jpg',
      views: '18.3K',
      likes: '956',
      uploadDate: '5 days ago',
      status: 'published'
    },
    {
      id: '3',
      title: 'LEAKED: Kendrick Lamar - Soul Searching [Unreleased 2025]',
      thumbnail: '/thumbnails/video3.jpg',
      views: '32.1K',
      likes: '1.7K',
      uploadDate: '1 week ago',
      status: 'published'
    },
    {
      id: '4',
      title: 'LEAKED: Kendrick Lamar - Future Vision [Unreleased 2025]',
      thumbnail: '/thumbnails/video4.jpg',
      views: '12.8K',
      likes: '645',
      uploadDate: '2 weeks ago',
      status: 'published'
    }
  ];

  return (
    <div className="mt-4">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Video
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Views
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Likes
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Uploaded
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {videos.map((video) => (
              <tr key={video.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10 bg-gray-200 rounded">
                      {/* Placeholder for thumbnail */}
                      <div className="h-full w-full flex items-center justify-center">
                        <Play className="h-5 w-5 text-gray-500" />
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{video.title}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{video.views}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{video.likes}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500">{video.uploadDate}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {video.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-2">
                    <button className="text-blue-600 hover:text-blue-900">
                      <ExternalLink className="h-4 w-4" />
                    </button>
                    <button className="text-blue-600 hover:text-blue-900">
                      <BarChart2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecentVideos;
