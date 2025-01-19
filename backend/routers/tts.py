import requests, os
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 1024
VOICE_ID = "onwK4e9ZLuTAKqWW03F9"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": os.environ.get("ELEVENLABS_API_KEY")
}

def generateVoice(text, exportPath):
    data = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(exportPath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
        print(f'Audio content written to file {exportPath}')

# with open("sample.txt", 'r') as file:
#     text = file.read()
# generateVoice(text, "./output.wav")