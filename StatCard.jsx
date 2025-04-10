'use client';

import React from 'react';

const StatCard = ({ title, value, icon, change, changeType }) => {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`p-3 rounded-md ${
              changeType === 'positive' ? 'bg-green-100' : 
              changeType === 'negative' ? 'bg-red-100' : 'bg-gray-100'
            }`}>
              {icon}
            </div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd>
                <div className="text-lg font-medium text-gray-900">{value}</div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div className={`bg-gray-50 px-5 py-3 ${
        changeType === 'positive' ? 'text-green-600' : 
        changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
      }`}>
        <div className="text-sm">
          {change} from last month
        </div>
      </div>
    </div>
  );
};

export default StatCard;
