import os
# PdfReader is what opens the PDF file, parses its internal structure, and allows the code to go through each page to extract raw text
from pypdf import PdfReader
import chromadb

# This function takes in a string (file path) and returns the raw text of the document being read (another string)
def load_text_from_file(file_path: str) -> str:
    # Splits the file path into separate values - the file path name and the file extension.  The '1' takes the second part of the split values (the file extension), converts it to lowercase characters, and assigns it to 'ext'.
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        reader = PdfReader(file_path) # Stores the metadata of the file and the pages as a structured Python object into 'reader'
        text = ""
        for page in reader.pages: # A loop that goes through each page from the Python object (.pages is a pypdf property) that is assigned to 'reader' and temporarily stores each page, one at a time, to the variable 'page' so that it can run the next few lines of code against it
            extracted = page.extract_text() # This built-in function reads all of the characters from 'page' and temporarily saves it as a text string in a variable called 'extracted'
            if extracted: # Only if there is text found on the page
                text += extracted + "\n" # Add the text that is found and append it to what is already stored in the 'text' variable with a line break at the end
        return text
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f: # Opens the file in read mode and forces utf-8 encoding.  'with' automatically closes the file after the reading is finished
            return f.read() # Reads the contents of the .txt file and returns a string
    else:
        raise ValueError(f"Unsupported file format: {ext}")

# Splits raw document text into overlapping chunks so context is preserved across boundaries during vector search.
def chunk_text(text: str, chunk_size: int = 400, chunk_overlap: int = 80) -> list[str]: # Returns a list of text strings, each with a max of 400 characters and an 80 character overlap between chunks
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip()) # Takes the chucnk and adds it as a new item in the chunks list
        start += chunk_size - chunk_overlap

    return chunks

if __name__ == "__main__":
    sample_path = os.path.join("data", "it_policy.txt") # Written for cross-platform compatibility
    
    if os.path.exists(sample_path):
        print(f"Loading document: {sample_path}...")
        raw_text = load_text_from_file(sample_path)
        print(f"Total raw text length: {len(raw_text)} characters.")

        chunks = chunk_text(raw_text, chunk_size=400, chunk_overlap=80)
        print(f"Successfully generated {len(chunks)} text chunks.")
        
        print("Initializing ChromaDB and storing embeddings...")
        
        # Initialize a persistent ChromaDB client and save it to a local folder named 'chroma_db'
        chroma_client = chromadb.PersistentClient(path="chroma_db")
        
        # Create a collection called 'it_policies' if it doesn't yet exist
        collection = chroma_client.get_or_create_collection(name="it_policies")
        
        # Take each chunk ID and put it in a list
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Add the chunk text and chunk ids to the collection
        collection.add(
            documents=chunks,
            ids=ids
        )
        
        print(f"Successfully stored {len(chunks)} chunks into ChromaDB vector database!")
    else:
        print(f"File not found at {sample_path}. Please place a sample file in data/")