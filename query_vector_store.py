import os
import chromadb

# Takes in the user's question/query and looks for the top 3 most relevant results based on vector coordinate match
def query_vector_store(query_text, n_results=3, db_path="./chroma_db", collection_name="it_policies"):

    # Tells ChromaDB to open a connection to the folder path that the database on your hard drive is in (specified by the 'db_path' parameter).  Without calling the PersistentClient function, it will create an in-memory database that disappears after the script runs or if the terminal is closed.
    client = chromadb.PersistentClient(path=db_path)
    
    # Provides a gateway to work with the it_policies collection by assigning a handle to the 'collection' variable
    collection = client.get_or_create_collection(name=collection_name)
    
    # ChromaDB takes the user entered question/query and converts it into a vector coordinate.  It then looks through the vector database to find the top 3 closest matches and stores it in 'results'. 'query_texts' ('texts' is plural so that the user can ask multiple questions in a single request) is the pre-defined parameter name that passes the user's text through the embedding model.
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Stores the top 3 matching chunks from vector_store.py for the first query by the user into matched_chunks. The "documents" keyword is what stores the text chunks ("ids" stores the unique chunk IDs, "distances" stores the similarity scores, and "metadatas" stores any extra data that is attached to the chunks)
    matched_chunks = results["documents"][0] if results["documents"] else []
    
    return matched_chunks

if __name__ == "__main__":
    test_query = "What is the policy for password resets and multi-factor authentication?"
    
    print(f"Querying vector store for: '{test_query}'\n")
    retrieved_excerpts = query_vector_store(test_query, n_results=3)
    
    print(f"Retrieved {len(retrieved_excerpts)} relevant excerpts:\n")
    for idx, excerpt in enumerate(retrieved_excerpts): # Enumerate assigns an id number to each chunk (idx) and each chunk is stored in 'excerpt'
        print(f"--- Excerpt {idx + 1} ---")
        print(excerpt)
        print("\n")