import speech_recognition as sr
import pyaudio 
import wave

def audio_to_text(audio_file: str) -> str:
    """
    Converts an audio file to text using SpeechRecognition.

    Parameters:
        audio_file (str): Path to the audio file.

    Returns:
        str: Transcribed text from the audio file.
    """
    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            print("Loading audio file...")
            audio_data = recognizer.record(source)  # Record the entire audio

        # Perform speech recognition
        print("Transcribing audio to text...")
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text

    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Speech recognition request failed; {e}"
    except FileNotFoundError:
        return "Audio file not found."
    except Exception as e:
        return f"An error occurred: {e}"

def record():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    OUTPUT_PATH = "backend/data/ai_voice/"
    OUTPUT_FILENAME = OUTPUT_PATH + "recording.wav"

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        pass


    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
