from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv
import requests
import json
import os


def generate_embedding(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text).astype(np.float32)
    return embedding


"""
    This function takes an embedding represented as a comma-separated string and converts it
    into a list of floats, representing the individual values in the embedding vector.
"""


def parse_embedding(embedding_text):
    # Assuming the embedding is returned as a comma-separated string
    embedding = [float(x) for x in embedding_text.split(",")]


"""
    This function generates an embedding for the provided input data using a pre-trained
    SentenceTransformer model. The generated embedding is returned as a list.
"""


def create_embeding(data):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(data).tolist()
    return embedding


"""
    This function updates the vector database with embeddings from the provided rows.
    Each row contains an ID and an embedding, which are extracted and added to a FAISS index.
    The FAISS index is used for efficient similarity search in the vector space.
"""


def update_vector_db_with_embeding(rows):
    ids = [row[0] for row in rows]
    embeddings = np.array([eval(row[1]) for row in rows]).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)


if __name__ == "__main__":
    print("".center(100, "-"))
    # generate_embedings()
