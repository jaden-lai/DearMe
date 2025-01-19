from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
import ssl

# Ensure SSL context works for NLTK if needed
ssl._create_default_https_context = ssl._create_unverified_context

CHROMA_PATH = "chroma"

def query_chroma(query: str, session_id: str):
    try:
        # Embedding function
        embedding = FastEmbedEmbeddings()

        # Create Chroma DB and retriever
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,  # Adjust based on the number of relevant docs you want to retrieve
                "score_threshold": 0.3,
            },
        )
        
        # Define the prompt template
        prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are going to write a journal entry according to the QUESTION which will be what the user experienced during the day. 
            Make sure to include the date on top, and start with: Dear Me, .[/INST] </s> 
            [EXAMPLE]1. User: "Today, I've been thinking a lot about what my cores values are. I got in trouble today because I was honest about my wrongdoings, but it defintely felt better being honest"
                        AI Response:
                        Date: January 15, 2023

                        Dear Me, 

                        Today I’ve been considering my core values and how they impact the decisions I make in my life. I realize that my values are an essential part of who I am, and they play a significant role in shaping my thoughts, actions, and choices.

                        One of my core values is honesty. I believe that it’s essential to be truthful with myself and others, even when it’s difficult. When I’m faced with a decision, I always try to consider whether it aligns with my values of honesty and integrity. If I feel that a decision would compromise these values, I know that it’s not the right choice for me.

                        Another value that’s important to me is kindness. I believe that everyone deserves to be treated with respect and compassion, regardless of their background or circumstances. When I’m making a decision, I try to consider how it will impact others and whether it aligns with my values of kindness and empathy.

                        Finally, I value personal growth and self-improvement. I believe that life is a journey of learning and self-discovery, and I always strive to grow and evolve as a person. When I’m making a decision, I try to consider whether it will help me grow and develop as a person, both personally and professionally.

                        Reflecting on my core values has helped me gain clarity on what’s important to me and how I can make decisions that align with my values. I know that when I make choices that align with my values, I feel more fulfilled, purposeful, and true to myself.
                    2. User: "Bruh therer were so many meetings today at work I was working like a dog. I met a friend to dinner today but we vibed and chilled and talked baout the future. It was nice having a nice social time let sgooo"
                        AI Response:
                        Date: April 27, 2022

                        Dear Me,

                        Today was a busy day at work. I had a lot of meetings and deadlines to meet, which kept me on my toes all day. I felt a little bit stressed at times, but overall, I was able to stay focused and get everything done that needed to be done.

                        During my lunch break, I went for a walk around the park near my office. It was a beautiful day outside, and I felt grateful for the opportunity to get some fresh air and sunshine. As I walked, I listened to a podcast about mindfulness and tried to focus on being present in the moment.

                        After work, I met up with a friend for dinner. We caught up on each other’s lives and talked about our plans for the future. It was nice to have some social time after a busy day at work.

                        Before bed, I took some time to reflect on the day. I thought about the things that went well and the areas where I could improve. I also wrote down some goals for tomorrow, including getting up a little bit earlier and taking a few moments to meditate before starting my day.

                        Overall, today was a good day. I feel grateful for the opportunities and experiences that came my way, and I’m looking forward to what tomorrow will bring.

            [EXAMPLE]
            [INST] Make it a journal entry where it has date, and summary of the day. No listing activities. Also make sure you include all of the "moments" in the QUESTION. Do not restate the CONTEXT questions, they are to help you to write your journal by provoking your thoughts.
            Question: {question} 
            Here are some questions that will help as a journaling template: {context} 
            Answer: [/INST]
            """
        )

        # Initialize the model once
        model = ChatOllama(model="mistral")

        retrieval_input = f"Query: {query}\nPrompt: {prompt}"

        # Retrieve relevant documents based on the query using invoke
        documents = retriever.invoke(retrieval_input)
        
        # Prepare context by joining the document contents
        context_text = "\n".join([doc.page_content for doc in documents])
        print(context_text)
        print(retrieval_input)
        # Format the prompt with the question and context
        input_data = prompt.format(question=query, context=context_text)

        # Create a list of messages as strings
        messages = [input_data]

        # Pass the list of messages (strings) to model.invoke
        response = model.invoke(messages)

        # Access the content of the response
        return response.content  # Accessing the content directly
    
    except Exception as e:
        return f"Error during query: {e}"

if __name__ == "__main__":
    query = "Today I ate my booger and I don't want to tell anyone.. I think one of my friends saw it and didn't say anything LOL. I just ate lunch with my dad and it was pretty good pankcakes ahha., "  # Replace with an actual query
    print(query_chroma(query))
