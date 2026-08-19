# UPSC AI — RAG Knowledge Assistant

An AI-powered UPSC information assistant built using
Retrieval-Augmented Generation (RAG).

The application retrieves relevant information from a focused
UPSC knowledge base and uses Ollama to generate responses based
on the retrieved context.

## Features

- UPSC-focused knowledge base
- Semantic embedding-based retrieval
- Cosine similarity ranking
- Top relevant context retrieval
- Ollama-powered response generation
- Retrieval similarity scores
- Responsive product interface
- Desktop and mobile layouts

## Architecture

```text
User Question
      |
      v
Question Embedding
      |
      v
Similarity Search
      |
      v
Top Relevant UPSC Chunks
      |
      v
Retrieved Context
      |
      v
Ollama / Llama 3
      |
      v
Generated Answer