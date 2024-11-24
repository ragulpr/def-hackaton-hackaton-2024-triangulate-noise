"use client"
import Image from "next/image";
import RectangleMap from "./RectangleMap";
// import UserLocation from "./components/UserLocation";

// const WIDTH = "1920"
// const HEIGHT = "1080"

// const FIRST_MIC = [0.2, 0]
// const SECOND_MIC = [0.8, 0]


export default function Home() {
  const objects = [
    { type: 'user', x: 100, y: 150, size: 20 },   // A blue user
    { type: 'object', x: 300, y: 400, size: 30 }, // A red object
    { type: 'user', x: 500, y: 200, size: 25 },   // Another blue user
  ];

  return (
    <main className="bg-gray-100 min-h-screen">
      <RectangleMap objects={objects} />
    </main>
  );
}
