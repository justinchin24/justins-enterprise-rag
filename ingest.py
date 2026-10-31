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
    data_dir = "data" # This is a string, but it helps define what folder path Python will need to look in

    # Check if the 'data' folder exists and creates an empty list for the text chunks to be stored in
    if os.path.exists(data_dir):
        print(f"Scanning directory: '{data_dir}/' for documents...")
        all_chunks = []
    
    # Dynamically loop through every file in the data folder. Insert the folder path and file name into 'file_path' (os.path.join ensures that the proper slash between the folder path and file name is used). 
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)

            # If the item being evaluated is truly a file, split the file name and extension and assign the extension to 'ext'.
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in [".txt", ".pdf"]:
                    print(f"-> Loading: {filename}...")
                    try:
                        raw_text = load_text_from_file(file_path) # Per the function above, if it’s a .pdf, use pypdf to read the pages. If it’s a .txt, read the text directly and return the entire file contents as a single large text string.
                        chunks = chunk_text(raw_text, chunk_size=400, chunk_overlap=80) # Generate the list of chunks from the text and assign it to 'chunks'.
                        print(f"   Extracted {len(raw_text)} chars -> Generated {len(chunks)} chunks.")
                        
                        # Package chunks as dictionaries with a unique ID, the chunk text itself, and the original file name -- and store it in the all_chunks variable (list).
                        for i, chunk in enumerate(chunks):
                            all_chunks.append({
                                "id": f"{filename}_chunk_{i}",
                                "document": chunk,
                                "metadata": {"source": filename}
                            })
                    except Exception as e:
                        print(f"   Error processing {filename}: {e}")
        
        if all_chunks:
            print(f"\nInitializing ChromaDB and storing {len(all_chunks)} total chunks...")
            
            # Initialize a persistent ChromaDB client and save it to a local folder named 'chroma_db'
            chroma_client = chromadb.PersistentClient(path="chroma_db")

            # Create a collection called 'it_policies' if it doesn't yet exist
            collection = chroma_client.get_or_create_collection(name="it_policies")
            
            # Use the Python feature called "list comprehensions" to unpack each dictionary in all_chunks into separate parallel lists to add to ChromaDB. Each line tells Python to 1) assign one dictionary item at a time to 'item', 2) lookup the dictionary value in double quotes, and 3) assign that value to the defined variable below.
            ids = [item["id"] for item in all_chunks]
            documents = [item["document"] for item in all_chunks]
            metadatas = [item["metadata"] for item in all_chunks]
            
            # Add the chunk text and chunk ids to the collection
            collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            
            print(f"Successfully stored {len(all_chunks)} chunks into ChromaDB vector database!")
        else:
            print(f"\nNo valid .txt or .pdf files found in '{data_dir}/'. Please add files and try again.")
    else:
        print(f"Data directory not found at '{data_dir}'. Please create it and add your documents.")