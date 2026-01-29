import React from 'react';

const MasteryMomentum = ({ current, target, label }) => {
  return (
    <div className="rounded-xl p-4 border border-blue-100" style={{background: 'linear-gradient(to right, #eff6ff, #eef2ff)'}}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-900">{label}</h3>
        <div className="text-2xl font-bold text-blue-600">{current}%</div>
      </div>
      <div className="relative w-full bg-gray-200 rounded-full h-3">
        <div
          className="h-3 rounded-full transition-all duration-1000 ease-out" style={{background: 'linear-gradient(to right, #3b82f6, #22c55e)'}}
          style={{ width: `${current}%` }}
        ></div>
      </div>
      {target && (
        <div className="mt-2 text-sm text-gray-600">
          Next milestone: {target}% ({target - current} points to go)
        </div>
      )}
    </div>
  );
};

export default MasteryMomentum;