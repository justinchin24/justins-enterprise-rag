import os
import chromadb
from ingest import load_text_from_file, chunk_text

# Function expects 2 variables: 'chunks' (a list of text strings) and db_path (this is optional due to a default value being assigned)
def initialize_vector_store(chunks: list[str], db_path: str = "./chroma_db"):
    
    # Creates a SQLite database and stores it either in a folder that the user passes when calling the function or in a folder called chroma_db (default if nothing is specified). The db stores unique IDs, the raw text chunks, and metadata dictionaries. The db object is assigned to 'client'.
    client = chromadb.PersistentClient(path=db_path)
    
    collection_name = "it_policies"
    
    # Either creates a new collection called it_policies or brings up the existing collection. It attaches a default open-source embedding model (all-MiniLM-L6-v2) to prepare it for conversion into vectors
    collection = client.get_or_create_collection(name=collection_name)
    
    # Generate and assign unique IDs to each chunk (e.g., "chunk_0", "chunk_1", etc.) that is in the list from the chunk_text function
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # Generates the vector embeddings for each chunk and writes them to the database.  Each position (index) is paired with an id (from the 'ids' variable above) and chunk of text (denoted by chunks[x], where x is the position number starting with 0)
    collection.add(
        documents=chunks,
        ids=ids
    )
    
    print(f"Successfully stored {len(chunks)} chunks in ChromaDB collection '{collection_name}'.")
    return collection

if __name__ == "__main__":
    sample_path = os.path.join("data", "it_policy.txt")
    
    if os.path.exists(sample_path):
        raw_text = load_text_from_file(sample_path)
        chunks = chunk_text(raw_text, chunk_size=400, chunk_overlap=80)
        
        # Build the vector database
        collection = initialize_vector_store(chunks)
        
        # Displays the count of chunks in the collection
        print(f"Total items currently in vector store: {collection.count()}")
    else:
        print(f"File not found at {sample_path}.")