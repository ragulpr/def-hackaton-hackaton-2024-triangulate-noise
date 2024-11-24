"use client"
import Image from "next/image";

const WIDTH = "1920"
const HEIGHT = "1080"

import RectangleMap from './RectangleMap';

export default function Home() {
  const objects = [
    { type: 'user', x: 0.125, y: 0.25, size: 0.025 },   // A blue user (x: 12.5%, y: 25%, size: 2.5% of container width)
    { type: 'object', x: 0.5, y: 0.5, size: 0.0375 }, // A red object (x: 37.5%, y: 50%, size: 3.75% of container width)
    { type: 'user', x: 0.625, y: 0.333, size: 0.03125 }, // Another blue user (x: 62.5%, y: 33.3%, size: 3.125% of container width)
  ];

  return (
    <main className="bg-gray-100 min-h-screen">
      <RectangleMap objects={objects} />
    </main>
  );
}
