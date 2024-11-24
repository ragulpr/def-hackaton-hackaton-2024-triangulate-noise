const RectangleMap = ({ objects }) => {
  const aspectRatio = 16 / 9;  // 16:9 aspect ratio
  const containerWidth = 800;  // Container width in pixels
  const containerHeight = containerWidth / aspectRatio; // Calculate height based on aspect ratio

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div
        className="relative bg-white border border-gray-300"
        style={{
          width: `${containerWidth}px`,
          height: `${containerHeight}px`,
        }}
      >
        {objects.map((object, index) => {
          // Calculate the position using percentage (0 to 1 scale)
          const x = object.x * containerWidth;  // Convert x from 0-1 scale to pixels
          const y = object.y * containerHeight; // Convert y from 0-1 scale to pixels
          const size = object.size * containerWidth; // Convert size from 0-1 scale to pixels

          return (
            <div
              key={index}
              className={`absolute rounded-full ${
                object.type === 'user' ? 'bg-blue-500' : 'bg-red-500'
              }`}
              style={{
                width: `${size}px`,
                height: `${size}px`,
                top: `${y}px`,
                left: `${x}px`,
                transform: 'translate(-50%, -50%)',
              }}
            ></div>
          );
        })}
      </div>
    </div>
  );
};

export default RectangleMap;