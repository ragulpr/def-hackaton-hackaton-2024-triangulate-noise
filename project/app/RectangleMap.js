import React from 'react';

const RectangleMap = ({ objects }) => {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div
        className="relative bg-white border border-gray-300"
        style={{
          width: '800px',
          height: '600px',
        }}
      >
        {objects.map((object, index) => (
          <div
            key={index}
            className={`absolute rounded-full ${
              object.type === 'user' ? 'bg-blue-500' : 'bg-red-500'
            }`}
            style={{
              width: `${object.size}px`,
              height: `${object.size}px`,
              top: `${object.y}px`,
              left: `${object.x}px`,
              transform: 'translate(-50%, -50%)',
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default RectangleMap;