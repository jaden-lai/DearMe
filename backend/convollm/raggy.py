from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
import ssl

# Ensure SSL context works for NLTK if needed
ssl._create_default_https_context = ssl._create_unverified_context

CHROMA_PATH = "chroma"

def query_chroma(query):
    """
    THIS IS THE ONE
    """
    try:
        # Embedding function
        embedding = FastEmbedEmbeddings()

        # Create Chroma DB and retriever
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,  # Adjust based on the number of relevant docs you want to retrieve
                "score_threshold": 0.4,
            },
        )
        
        # Define the prompt template
        prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an empathetic AI designed to facilitate journaling conversations. Respond like a supportive friend and an attentive listener. Show understanding, encourage reflection, and ask if there's anything else the user would like to share. Limit to 50 words.
            [/INST] </s> 
            [EXAMPLE]1. User: "I've been feeling really overwhelmed with work lately."
                        AI Response:
                        That sounds really tough. It’s not easy juggling everything when work feels overwhelming. You're doing your best, and that counts for a lot. Would you like to share more about what’s been making it so challenging, or is there anything specific you'd like to talk about?
                    2. User: "I had such a great time at the concert last night!"
                        AI Response:
                        That sounds amazing! It must have felt great to enjoy the energy of live music. What was your favorite part of the concert? Or is there anything else you'd like to talk about?
                    3. User: "I had a fight with my best friend, and I don’t know what to do."
                        AI Response:
                        I'm so sorry to hear that. Conflicts with people we care about can feel really upsetting. It shows how much they mean to you that this is on your mind. Do you want to talk about what happened or how you’re feeling about it? I’m here to listen if there’s anything else you want to share.
                    4. User: "I’m not sure if I made the right choice about switching my major."
                        AI Response:
                        It’s completely normal to feel uncertain after making a big decision like that. It shows you really care about your future. What’s been on your mind about the switch? Is there anything else you’d like to reflect on together?
                    5. User: "I’m really anxious about the presentation tomorrow."
                        AI Response:
                        It’s understandable to feel nervous about something important. It shows how much you care about doing well. Would you like to talk about what’s worrying you most, or maybe we can think about ways to make it feel a little easier? Is there anything else on your mind?
                    6. User: "No, I don't have more to talk about, thanks for listening"
                        AI Response: Okay, let me know if you want to talk more!

            [EXAMPLE]
            [INST] Question: {question} 
            Context: {context} 
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
        raise Exception(f"Error during query: {e}")

# if __name__ == "__main__":
#     query = "My mom deadd"  # Replace with an actual query
#     print(query_chroma(query))
