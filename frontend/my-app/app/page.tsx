"use client";  // Mark this file as a client component

import { useState } from "react";
import LampDemo from "@/components/ui/lamp";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect"; // Import TextGenerateEffect
import { ElevenLabsClient, stream } from "elevenlabs";
import { Readable } from "stream";
import logoPng from './logo.png';
import { DatePickerDemo } from "@/components/ui/datepicker";


export default function Home() {
  const [inputValue, setInputValue] = useState("");  // Track input value
  const [displayText, setDisplayText] = useState("Tell me about it");  // Add this state
  const [date, setDate] = useState<Date | undefined>(new Date());

  const client = new ElevenLabsClient({
    apiKey: ELEVENLABS_API_KEY,
  });

  const placeholders = [
    "Type your thoughts here...",
    "What's on your mind?",
    "Start typing something interesting..."
  ];

  const playAudioStream = async (audioStream: Readable) => {
    const chunks: BlobPart[] = [];
  
    // Collect all chunks from the stream
    for await (const chunk of audioStream) {
      chunks.push(chunk);
    }
  
    // Create a Blob from the chunks
    const audioBlob = new Blob(chunks, { type: "audio/mpeg" });
  
    // Generate a Blob URL
    const audioUrl = URL.createObjectURL(audioBlob);
  
    // Play the audio
    const audio = new Audio(audioUrl);
    audio.play();
  
    // Optionally, release the URL once playback is done
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
    };
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Submitting:", inputValue); // Debug log
    
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      console.log("Server response:", data.response);
      
      setDisplayText(data.response);  // Update display text immediately
      setInputValue(""); // Clear input after submission

      const audioStream = await client.textToSpeech.convertAsStream(
        "JBFqnCBsd6RMkjVDRZzb",
        {
          text: data.response,
          model_id: "eleven_flash_v2",
        }
      );
      
      await playAudioStream(Readable.from(audioStream));
      
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <div className="fixed inset-0 overflow-hidden bg-slate-950">
      {/* Logo on very top */}
      <img 
        src={logoPng.src} 
        alt="App Logo" 
        className="absolute top-[3vh] left-[3vw] h-[min(5vh,50px)] z-50"
      />
      
      {/* LampDemo in background */}
      <div className="absolute inset-0 z-0 transform -translate-y-32">
        <LampDemo />
      </div>

      {/* TextGenerateEffect above lamp but below input */}
      <div className="absolute bottom-[40vh] left-1/2 transform -translate-x-1/2 z-20 w-[min(90vw,800px)] text-center">
        <TextGenerateEffect 
          key={displayText}
          words={displayText} 
          duration={1} 
          filter={true} 
        />
      </div>

      {/* PlaceholdersAndVanishInput on top */}
      <div className="absolute bottom-[20vh] left-1/2 transform -translate-x-1/2 w-[min(90vw,800px)] z-30">
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={handleSubmit}
        />
      </div>

      <div className="absolute top-[3vh] right-[3vw] z-50">
        <DatePickerDemo />
      </div>
    </div>
  );
}