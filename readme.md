# 🌍 NomadNavigator - Your AI-Powered Travel Companion  

Welcome to **NomadNavigator**, an intelligent travel recommendation system.  
This project leverages cutting-edge technologies like **LLMs**, **RAG**, and **Embeddings** to provide personalized travel recommendations. 


---

## 🚀 Features  

- 🗺️ **Comprehensive Travel Database**: Includes descriptions, details, and metadata for various destinations.  
- 🧠 **AI-Powered Recommendations**: Uses LLMs to generate personalized travel suggestions.  
- 🔍 **Efficient Similarity Search**: Implements FAISS for quick and accurate document retrieval.  
- 💬 **Fallback Support**: Handles queries for destinations not present in the database.  

---

## 📂 Project Structure  

```plaintext
📦 NomadNavigator  
├── 📁 data               # SQL scripts and sample data  
├── 📁 embeddings         # Code for generating embeddings  
├── 📁 response_generator # LLM-based response generation  
├── 📄 requirements.txt   # Project dependencies  
└── 📄 app.py             # Main application  
```

---

## 🛠️ Tech Stack

- Programming Language: Python 🐍
- Database: SQLite 🗄️
- Embeddings: Sentence Transformers 📘
- Vector Search: FAISS 🔍
- LLM: Hugging Face Transformers 🤗

---


## 🖥️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/NomadNavigator.git
   cd NomadNavigator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   ```bash
   python data/db.py
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

---

## 🎮 Demo
###  Here's how NomadNavigator works:

- Enter your travel query (e.g., "Top places to visit in Paris").
- The system retrieves the most relevant destinations using FAISS.
- AI generates personalized recommendations based on the retrieved data.
- You receive a detailed and engaging response!

---