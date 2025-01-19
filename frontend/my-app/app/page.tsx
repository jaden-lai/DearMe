"use client";  // Mark this file as a client component

import { useState } from "react";
import LampDemo from "@/components/ui/lamp";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect"; // Import TextGenerateEffect
import logoPng from './logo.png';


export default function Home() {
  const [inputValue, setInputValue] = useState("");  // Track input value

  const placeholders = [
    "Type your thoughts here...",
    "What's on your mind?",
    "Start typing something interesting..."
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form submitted with value:", inputValue);
  };

  return (
    <div className="relative h-[100vh] w-[100vw]">
      {/* LampDemo stays in the background */}
      <img 
        src={logoPng.src} 
        alt="App Logo" 
        className="absolute top-[2vh] left-[2vw] h-[5vh] z-50"
      />
      <LampDemo />

      {/* TextGenerateEffect placed above the input */}
      <div className="absolute bottom-[20vh] left-1/2 transform -translate-x-1/2 z-10">
        <TextGenerateEffect words="How are you?" duration={1} filter={true} />
      </div>

      {/* PlaceholdersAndVanishInput stays at the bottom */}
      <div className="absolute bottom-[2vh] w-full px-[4vw]">
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}
