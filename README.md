# 🧾 Insurance Chatbot - README

This project is a simple, intelligent chatbot that helps users interactively query insurance policy details extracted from PDF documents. Built using **Python**, **LangChain**, **Gemini**, **Mistral**, and **Streamlit**, this chatbot utilizes LLMs to understand user questions and provide accurate, context-related answers

---
## Demo

https://github.com/user-attachments/assets/90748730-017b-40f0-8f77-0a963751fa56

---
## 📌 Features
- Upload insurance policy PDFs.
- Ask natural language questions about the policy.
- Retrieves relevant policy info using a vector database (qdrant).
- Uses Gemini LLMs for response generation.
- Web-based UI using Streamlit.
- Fallback detection for human escalation.

---

## 🛠️ Step-by-Step Setup & Development Guide

### 1. **Environment Setup**
- Install Python (>=3.10): [https://www.python.org/](https://www.python.org/)
- Install the requirements from requirements.txt

### 2. **Models**
- Create Gemini API key
- Create Mistral API key
- Create sqlite3 cloud API key.
- Create qdrant API key.

---

### 3. **Run Application**
- Clone the project from github
- Go to app directory and run the command: streamlit run streamlit_app.py
- Go to api directory and run the command: uvicorn main:app --reload

---

## 📄 Working
- When PDF's are uploaded they are chunked into paragraphs and passed to the mistral embedding model.
- The embedder then creates vector embeddings for the chunks, which are then stored in qdrant (vector database).
- When user inputs a query, the query is also converted to a vector embedding.
- A similarity search is performed to retrieve documents from the vector db that are semantically similar to the query.
- Then the query along with the retrieved document is sent to Gemini LLM, which then generates an appropriate response to the query.
- This is then stored as chat history in a sqlite db.
- When another query is passed, it then uses the chat history also to generate further responses.


---

## 📚 Free Tools Used
- **Python + LangChain** for backend logic
- **Streamlit** for frontend
- **Gemini** (Free API tier) LLM model
- **Mistral** (Free API tier) Embedding model
- **qdrant** for vectordb
- **sqlite3** for chat history

---

