"use client";  // Mark this file as a client component

import { useState } from "react";
import LampDemo from "@/components/ui/lamp";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";


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
    <div className="relative min-h-screen">
      {/* LampDemo stays in the background */}
      <LampDemo />
      
      {/* PlaceholdersAndVanishInput stays at the bottom */}
      <div className="absolute bottom-0 w-full p-4">
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}
