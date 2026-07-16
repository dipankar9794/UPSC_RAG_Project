An AI-powered **UPSC Exam Information Assistant** built using **Retrieval-Augmented Generation (RAG)**, **Ollama**, **Llama 3**, **nomic-embed-text**, and **Streamlit**.

The application answers UPSC-related questions by retrieving relevant information from a custom knowledge base (`upsc.txt`) and then generating accurate, context-aware responses using Llama 3.

---

## 🚀 Features

- AI-powered UPSC question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- Cosine similarity-based document retrieval
- Llama 3 for answer generation
- Streamlit web interface
- Displays retrieved context with similarity scores
- Reduces hallucinations by answering only from the knowledge base

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit
- Ollama
- Llama 3
- nomic-embed-text
- Natural Language Processing (NLP)
- Retrieval-Augmented Generation (RAG)

---

## 📂 Project Structure

```
UPSC_RAG_Project/
│
├── app.py                 # Streamlit application
├── upsc.txt               # UPSC knowledge base
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore
```

---

# 📋 Prerequisites

Before running the project, install the following:

- Python 3.10 or later
- Git
- Ollama

---

# Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/UPSC_RAG_Project.git
```

Move into the project directory.

```bash
cd UPSC_RAG_Project
```

---

# Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# Step 3: Install Python Dependencies

Install all required packages.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install streamlit ollama
```

---

# Step 4: Install Ollama

Download and install Ollama from:

https://ollama.com/download

Verify installation:

```bash
ollama --version
```

---

# Step 5: Download Required Models

Download the embedding model:

```bash
ollama pull nomic-embed-text
```

Download Llama 3:

```bash
ollama pull llama3
```

Verify installed models:

```bash
ollama list
```

Expected output:

```
llama3
nomic-embed-text
```

---

# Step 6: Start Ollama

Open a terminal and ensure the Ollama service is running.

On most systems, installing Ollama starts the service automatically.

You can verify by running:

```bash
ollama list
```

---

# Step 7: Add the Knowledge Base

Place the UPSC knowledge file inside the project folder.

Example:

```
UPSC_RAG_Project/
    app.py
    upsc.txt
```

If your application uses a different path, update:

```python
DATASET_PATH = "path/to/upsc.txt"
```

---

# Step 8: Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser.

If it doesn't, open:

```
http://localhost:8501
```

---

# 💬 Example Questions

- What is UPSC?
- What is the UPSC eligibility criteria?
- How many attempts are allowed for UPSC?
- What is the age limit for IAS?
- What is the syllabus of UPSC Prelims?
- What are the stages of the Civil Services Examination?
- What is the qualification required for UPSC?

---

# 🔄 Project Workflow

1. Load the UPSC knowledge base (`upsc.txt`).
2. Generate vector embeddings using **nomic-embed-text**.
3. Store embeddings in an in-memory vector database.
4. Accept a user query.
5. Convert the query into an embedding.
6. Calculate cosine similarity.
7. Retrieve the most relevant knowledge chunks.
8. Pass the retrieved context to **Llama 3**.
9. Generate a context-aware response.
10. Display the response and similarity scores in Streamlit.

---

# 📷 Application Features

- Interactive Streamlit interface
- Semantic retrieval
- Similarity score display
- Context-aware AI responses
- Fast local inference using Ollama

---

# 📌 Future Improvements

- PDF and DOCX knowledge base support
- FAISS or Chroma vector database integration
- Conversation history
- Multi-document retrieval
- Voice-based interaction
- Admin panel for uploading documents
- Hybrid search (keyword + semantic search)

---

# 👨‍💻 Author

**Dipankar Yadav**

B.Tech Computer Science & Engineering

Project: UPSC Exam Information Assistant using Retrieval-Augmented Generation (RAG)
