"use client"
import Image from "next/image";
import UserLocation from "./components/UserLocation";

const WIDTH = "1920"
const HEIGHT = "1080"

const FIRST_MIC = [0.2, 0]
const SECOND_MIC = [0.8, 0]

export default function Home() {
  return (
    <div className="inset-0 fixed bg-red-500">
      <div>
        <div style={{
          position: "absolute",
          top: 0,
          left: 0,
        }}>first mic</div>
        <div>Second mic</div>
      </div>
    </div>
  );
}
