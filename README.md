# 🤖 Enterprise IT SOP & Policy RAG Assistant

An enterprise-grade Retrieval-Augmented Generation (RAG) agent built with Python, Streamlit, ChromaDB, and the Google GenAI SDK. This application allows IT support specialists and operations teams to query internal standard operating procedures (SOPs) and policy documentation in real time, receiving grounded answers accompanied by collapsible source citations.

---

## 📌 Features

- **Document Ingestion & Chunking:** Processes raw PDF documentation (IT SOPs, security guidelines, onboarding policies) into clean text chunks.
- **Vector Database Storage:** Stores high-dimensional document embeddings locally using **ChromaDB** for efficient similarity searches.
- **Semantic Retrieval:** Queries the vector database to extract top relevant excerpts based on user intent rather than simple keyword matching.
- **Grounded Answer Generation:** Constructs strict system prompts paired with the **Google GenAI SDK** (Gemini) to prevent hallucinations and generate accurate, context-aware responses.
- **Streamlit Chat Interface:** Features an intuitive chat interface with persistent session memory (`st.session_state`), typing indicator spinners (`st.spinner`), and collapsible source citations (`st.expander`).

---

## 🏗️ System Architecture

The following diagram illustrates the complete end-to-end data flow:

```text
+-----------------------------------------------------------------------------------+
|                                 1. INGESTION PHASE                                |
|                                                                                   |
|  [ PDF Documents ] ---> ( Text Extraction ) ---> ( Recursive Text Chunking )      |
|                                                                 |                 |
|                                                                 v                 |
|                                                      [ Text Chunks ]              |
+-----------------------------------------------------------------------------------+
|
v
+-----------------------------------------------------------------------------------+
|                                2. VECTORIZATION PHASE                             |
|                                                                                   |
|  [ Text Chunks ] ---> ( Embedding Generation ) ---> [ ChromaDB Vector Database ]  |
+-----------------------------------------------------------------------------------+
|
v
+-----------------------------------------------------------------------------------+
|                             3. QUERY & RETRIEVAL PHASE                            |
|                                                                                   |
|  [ User Prompt via Streamlit ] ---> ( Vector Search ) ---> [ Top Relevant Chunks ]|
+-----------------------------------------------------------------------------------+
|
v
+-----------------------------------------------------------------------------------+
|                            4. GENERATION & UI PHASE                               |
|                                                                                   |
|  [ Grounded Prompt + Chunks ] ---> ( Google Gemini API ) ---> [ Streamlit UI ]    |
|                                                                |                  |
|                                                                +-- Grounded Answer|
|                                                                +-- Collapsible    |
|                                                                    Source Excerpts|
+-----------------------------------------------------------------------------------+
```

### Architectural Breakdown
1. **Document Ingestion:** Raw PDFs are ingested, extracted, and segmented into semantic text chunks to maximize retrieval relevance.
2. **Vector Indexing:** Chunks are converted into vector embeddings and stored in a persistent local **ChromaDB** collection.
3. **Semantic Querying:** When a user inputs a query via `st.chat_input`, ChromaDB identifies and extracts the top $k$ (k = 3) relevant context blocks using cosine similarity.
4. **Grounded Generation:** The user query and retrieved context chunks are wrapped in a strict prompt template sent to Gemini, ensuring the LLM answers *only* using supplied enterprise documentation.
5. **Interactive UI:** The response is streamed to the user with a collapsible `st.expander` view for exact citation transparency.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** Streamlit
- **LLM API:** Google GenAI SDK (Gemini)
- **Vector Database:** ChromaDB
- **Text Processing:** PyPDF2 / LangChain Text Splitters
- **Environment Management:** Python 3.10+ / `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A Google Gemini API key ([Get an API Key](https://aistudio.google.com/))

### 2. Repository Setup
Clone the repository and open in VS code:
```bash
git clone https://github.com/justinchin24/justins-enterprise-rag.git
cd justins-enterprise-rag
code .
```

### 3. Virtual Environment Setup
Create and activate an isolated Python virtual environment:
```bash
py -m venv .venv

# On Windows:
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a .env file in the root directory and add your Google Gemini API key:
```bash
echo GEMINI_API_KEY=your_actual_api_key_here > .env
```

### 6. Ingest sample document into Vector database
```bash
python ingest.py
```

### 7. Running the Application
Launch the Streamlit web application:
```bash
streamlit run app.py
```

---
## 📁 Repository Structure

```text
enterprise-it-rag-agent/
│
├── chroma_db/             # Local ChromaDB vector database directory (ignored in git)
├── docs/                  # Sample IT SOP and Policy PDF documents
├── .env                   # Environment variables and API keys (ignored in git)
├── .gitignore             # Git ignore file
├── app.py                 # Streamlit UI implementation & chat logic
├── rag_engine.py          # Vector search, ingestion, and GenAI query logic
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```
