Devpost Link: https://devpost.com/software/dear-me-8emch1

### 🛠️ Tech Stack  
🗣️ XTTS-V2, Ollama Mistral (local) 
📂 Redis, Chroma  
🎨 Next.js, React, TailwindCSS  
⚙️ Python, FastAPI  
📝 Custom algorithms  
📴 Local device support  

## Inspiration  
The inspiration for **Dear Me** came from the idea of making self-reflection more accessible and meaningful in today’s busy world. Journaling is a proven way to boost mental well-being and track personal growth, but many people struggle to maintain the habit... (like us who built DearMe)! We wanted to create a solution that feels natural, effortless, and secure, encouraging people to reflect without added stress.  

## What it does  
**Dear Me** is a private, offline conversational AI that acts as your personal companion throughout the day. By running on a local LLM, speech models, and database, it ensures all your data belongs **to yourself, for yourself**!   You can share your thoughts, feelings, and experiences in natural spoken and written conversations throughout the day, and at the end of the day, it generates a personalized journal entry summarizing your interactions. 

## How we built it  
We designed and built **Dear Me** with a strong focus on privacy and usability:  
- **AI Model:** Two locally fine-tuned LLMs for natural conversations and journal entries. Both LLMs use Retrieval Augmented Generation and accurate prompt engineering.
- **Voice Text-to-speech:** Enabled real-time speech-to-speech conversations by leveraging XTTS-V2 locally.
- **Database:** A dockerized local Redis database to keep information private. Also we used a local Chroma Database, made with embeddings of hand-picked research papers, articles, and blogs for Retrieval Augmented Generation. 
- **Frontend:** Built with **NextJS/React** and **TailwindCSS** to deliver a clean and intuitive user experience.  
- **Backend:** Developed using **Python** and **FastAPI** for efficient conversational flow and local data handling.  
- **Summarization Logic:** Designed algorithms to extract meaningful insights and craft journal entries in a cohesive, personalized style.  
- **Offline Optimization:** Focused on ensuring the app runs smoothly on local devices without compromising performance.  

## Challenges we ran into  
- **Fine-Tuning the Model:** Balancing conversational naturalness with effective summarization required extensive experimentation.
- **Local Performance:** Ensuring the AI runs efficiently on diverse hardware setups while staying offline was technically demanding, required a lot of testing.  
- **User Experience:** Designing an interface and conversational flow that felt engaging yet simple took multiple iterations.  

## Accomplishments that we're proud of  
- Successfully creating an offline, secure conversational AI that protects user privacy.  
- Building an engine capable of transforming conversations into meaningful, personalized journal entries.  
- Designing an intuitive and polished user interface that makes the app enjoyable to use.  

## What we learned  
- How to fine-tune and optimize LLMs for specific tasks like summarization and conversational flow.  
- First time using FastAPI + React tech stack, but learned swiftly to make & test API endpoints.
- Front-end standard design practices to make the app scalable.
- GIT GIT GIT

## What's next for Dear Me  
We have exciting plans for **Dear Me** in the future:  
- **Customization Options:** Let users personalize the tone and style of their journal entries.  
- **Insights Dashboard:** Provide users with emotional trends and reflections over time, like a "monthly wrapped".
- **Voice Integration:** Complete hands-free, voice-based interaction for easier access.  
- **Mental Health Features:** Introduce mindfulness tips or guided prompts based on user interactions.  

With these features, **Dear Me** will continue to empower users to reflect, grow, and cherish their personal stories—all while keeping their data private and secure.
