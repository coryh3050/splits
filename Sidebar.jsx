'use client';

import React from 'react';
import Link from 'next/link';
import { Home, Upload, Video, BarChart2, Settings, LogOut } from 'lucide-react';

const Sidebar = () => {
  const menuItems = [
    { icon: Home, text: 'Dashboard', href: '/' },
    { icon: Upload, text: 'Upload', href: '/upload' },
    { icon: Video, text: 'Videos', href: '/videos' },
    { icon: BarChart2, text: 'Analytics', href: '/analytics' },
    { icon: Settings, text: 'Settings', href: '/settings' },
  ];

  return (
    <div className="bg-gray-900 text-white w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition duration-200 ease-in-out">
      <div className="flex items-center space-x-2 px-4">
        <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
          <span className="text-white font-bold">YT</span>
        </div>
        <span className="text-xl font-bold">YouTube Auto</span>
      </div>
      
      <nav>
        <ul className="space-y-2">
          {menuItems.map((item, index) => (
            <li key={index}>
              <Link href={item.href} className="flex items-center space-x-2 py-2.5 px-4 rounded hover:bg-gray-800 transition duration-200">
                <item.icon className="h-5 w-5" />
                <span>{item.text}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      
      <div className="px-4 mt-auto">
        <div className="pt-6 border-t border-gray-700">
          <button className="flex items-center space-x-2 py-2.5 px-4 rounded hover:bg-gray-800 transition duration-200 w-full">
            <LogOut className="h-5 w-5" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
