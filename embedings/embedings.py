from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv
import requests
import json
import os


load_dotenv()
api_key = os.getenv('FIREWORKS_API_KEY')


"""
    This function takes an embedding represented as a comma-separated string and converts it
    into a list of floats, representing the individual values in the embedding vector.
"""
def parse_embedding(embedding_text):
    # Assuming the embedding is returned as a comma-separated string
    embedding = [float(x) for x in embedding_text.split(",")]
    return embedding



"""
    This function generates an embedding for a given query by sending it to a model hosted 
    by Fireworks AI. The model returns a dense numerical vector representation of the 
    input text. The function constructs a prompt, sends the request to the API, processes 
    the response, and returns the parsed embedding.
"""
def generate_embeding(query):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    prompt = f"Provide a dense numerical vector representation for the following text: {query}"
    
    payload = {
        "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "max_tokens": 500,  # Adjust max tokens for embedding output
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    # Extract the response text containing the vector
    embedding_text = response_data["choices"][0]["message"]["content"]
    print("res -> ", embedding_text)
    return parse_embedding(embedding_text)

    

"""
    This function generates an embedding for the provided input data using a pre-trained
    SentenceTransformer model. The generated embedding is returned as a list.
"""
def create_embeding(data):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(data).tolist()
    return embedding



"""
    This function updates the vector database with embeddings from the provided rows.
    Each row contains an ID and an embedding, which are extracted and added to a FAISS index.
    The FAISS index is used for efficient similarity search in the vector space.
"""
def update_vector_db_with_embeding(rows):
    ids = [row[0] for row in rows]
    embeddings = np.array([eval(row[1]) for row in rows]).astype('float32')
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)



if __name__=="__main__":
    print("".center(100, "-"))
    # generate_embedings()