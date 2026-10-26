import os
from google import genai
import logging
from dotenv import load_dotenv
from query_vector_store import query_vector_store

# Look for the .env file and find the API key to make it accessible to the application
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_rag_answer(user_query: str) -> str:
    # Retrieve the top 3 matching chunks from ChromaDB
    retrieved_excerpts = query_vector_store(user_query, n_results=3)
    
    # Combine the retrieved chunks into a single context block
    context_text = "\n\n---\n\n".join(retrieved_excerpts)
    
    # Prompt template for Gemini
    prompt = f"""
You are an expert Enterprise IT Assistant. Answer the user's question using ONLY the provided policy excerpts below. 
If the answer cannot be found in the excerpts, state clearly: "I cannot find the answer in the provided IT policies." Do not make up answers.

Context Excerpts:
{context_text}

User Question: {user_query}

Answer:
    """

    # Attach API key to each request
    client = genai.Client()

    try:
        logging.info("Sending query to Gemini for response...")

    # Call Gemini and tells it to return the output in a structured format and follow the fields, types, and rules in EnterpriseTicketExtraction
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )

        logging.info("Successfully processed query.")
    
        return response.text, retrieved_excerpts

    except Exception as e:
        logging.error(f"An error occurred while processing the query: {e}")
        raise

# Test it directly in the terminal
if __name__ == "__main__":
    test_query = "What is the policy for password resets and multi-factor authentication?"
    
    print(f"Generating grounded RAG answer for: '{test_query}'\n")
    answer, sources = generate_rag_answer(test_query)
    
    print("--- Gemini Grounded Answer ---")
    print(answer)
    print("\n" + "="*40 + "\n")
    print(f"Derived from {len(sources)} source chunks retrieved from ChromaDB.")