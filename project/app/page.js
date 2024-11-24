"use client"
import Image from "next/image";
import RectangleMap from "./RectangleMap";
// import UserLocation from "./components/UserLocation";

// const WIDTH = "1920"
// const HEIGHT = "1080"

// const FIRST_MIC = [0.2, 0]
// const SECOND_MIC = [0.8, 0]

export default function Home() {
  // creating coordinate systems 
  const objects = [
    { x: 0, y: 150 }, // Object 1
    { x: 300, y: 400 }, // Object 2
    { x: 700, y: 500 }, // Object 3
  ];

  return (
    <>
      <main className="bg-gray-100 min-h-screen">
        <RectangleMap objects={objects} />
      </main>
    </>
  );


}
