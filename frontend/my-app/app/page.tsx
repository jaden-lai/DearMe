"use client";  // Mark this file as a client component

import { useState } from "react";
import LampDemo from "@/components/ui/lamp";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect"; // Import TextGenerateEffect
import { ElevenLabsClient, stream } from "elevenlabs";
import { Readable } from "stream";
import logoPng from './logo.png';
import { DatePickerDemo } from "@/components/ui/datepicker";
import { ELEVENLABS_API_KEY } from "@/config";  // Update import path
// import sample txt
import { text } from "@/app/sample";


export default function Home() {
  const [inputValue, setInputValue] = useState("");  // Track input value
  const [displayText, setDisplayText] = useState("To yourself, for yourself");  // Add this state
  const [date, setDate] = useState("");
  const [popupText, setPopupText] = useState<string | null>(null); // Popup text state


  const client = new ElevenLabsClient({
    apiKey: ELEVENLABS_API_KEY || "",  // Add fallback empty string
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

  const getSession = (): string => {
    const date = new Date();
  
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // Months are 0-based
    const day = String(date.getDate()).padStart(2, "0");
  
    return `${year}${month}${day}`;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Submitting:", inputValue); // Debug log
    
    try {
      const response = await fetch('http://localhost:8080/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue, session_id: getSession() }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      console.log("Server response:", data.response);
      
      setDisplayText(data.response);  // Update display text immediately
      setInputValue(""); // Clear input after submission

      const audioStream = await client.textToSpeech.convertAsStream(
        "cgSgspJ2msm6clMCkdW9",
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

// Popup Component
const Popup: React.FC<{ text: string; onClose: () => void }> = ({ text, onClose }) => (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70 backdrop-blur-sm z-50">
    <div className="bg-gray-800 text-gray-100 rounded-lg shadow-xl p-6 w-[50vw] max-w-2xl">
      <h1>Summary</h1>
      <p className="text-center text-lg font-medium">{text}</p>
      <button
        className="mt-4 w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-offset-2 focus:ring-offset-gray-800 transition-all"
        onClick={onClose}
      >
        Close
      </button>
    </div>
  </div>
);
  
const handleDateChange = async (newDate: string) => {
  if (!newDate) {
    return "Error: Invalid date";
  };

  if (newDate === "20250119") {
    setPopupText(text);
    return;
  }

  console.log(typeof(newDate));

  setDate(newDate ?? "");
  try {
    console.log(newDate);
    const response = await fetch('http://localhost:8080/journal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({query: "test", session_id: newDate}),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const data = await response.json();
    console.log("Server response:", data.response);
    
    // setDisplayText(data.response);  // Update display text immediately
    setPopupText("Journal entries for " + newDate + ":\n" + data.response);
    
  } catch (error) {
    console.error("Error submitting form:", error);
  }
}

  return (
    <div className="fixed inset-0 overflow-hidden bg-slate-950">
      {/* Logo on very top */}
      <img 
        src={logoPng.src} 
        alt="App Logo" 
        className="absolute top-[1vh] left-[1vw] h-[min(15vh,300px)] z-50"
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
        <DatePickerDemo onDateChange={handleDateChange} />
      </div>

      {popupText && <Popup text={popupText} onClose={() => setPopupText(null)} />}
    </div>
  );
}