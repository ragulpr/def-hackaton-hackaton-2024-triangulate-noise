import React from 'react';

const RectangleMap = ({ objects }) => {
  const width = 800;
  const height = 600;

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div
        className="relative bg-white border border-gray-300"
        style={{
          width: `${width}px`,
          height: `${height}px`,
        }}
      >
        {objects.map((object, index) => (
          <div
            key={index}
            className="absolute bg-blue-500 rounded-full"
            style={{
              width: '20px',
              height: '20px',
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