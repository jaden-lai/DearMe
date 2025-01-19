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
    <div className="relative h-[100vh] w-[100vw] flex flex-col items-center">
      {/* Logo on very top */}
      <img 
        src={logoPng.src} 
        alt="App Logo" 
        className="absolute top-[3vh] left-[3vw] h-[min(5vh,40px)] z-50"
      />
      
      {/* LampDemo in background */}
      <div className="absolute inset-0 z-0">
        <LampDemo />
      </div>

      {/* TextGenerateEffect above lamp but below input */}
      <div className="absolute bottom-[25vh] left-1/2 transform -translate-x-1/2 z-20 w-[min(90vw,800px)] text-center">
        <TextGenerateEffect words="How are you?" duration={1} filter={true} />
      </div>

      {/* PlaceholdersAndVanishInput on top */}
      <div className="absolute bottom-[5vh] w-[min(90vw,800px)] z-30">
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}