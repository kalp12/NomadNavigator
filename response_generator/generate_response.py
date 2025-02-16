import ollama


def generate_response_from_llama(query):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": query}]
        # ,
        # options={
        #     "num_predict": 100,  # Limit response length (faster)
        #     "top_k": 50,  # Sampling to make generation faster
        #     "top_p": 0.9,  # Nucleus sampling for better speed
        # },
    )
    # print(response)
    return response["message"]["content"]


def main():
    pass


import faiss


def save_faiss_index(embeddings, index_path="faiss_index"):
    """Save FAISS index after inserting new embeddings."""
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)  # Add vectors
    faiss.write_index(faiss_index, index_path)


if __name__ == "__main__":
    import sqlite3

    # def connect_db():
    #   conn = sqlite3.connect('travel.db')
    #   cursor = conn.cursor()
    #   return cursor
    # def fetch_embedings():
    # cursor = connect_db()
    # # cursor.execute("SELECT id, destination, description, details, metadata, embeding, typeof(embeding) FROM travel_knowledge_base")
    # cursor.execute("SELECT id, destination, description, details, metadata, embeding, typeof(embeding) FROM travel_knowledge_base")

    # rows = cursor.fetchall()
    # # print(rows)
    # ids, destinations, descriptions, details, metadata, embeddings = [], [], [], [], [], []
    # for row in rows:
    #     ids.append(row[0])
    #     destinations.append(row[1])
    #     descriptions.append(row[2])
    #     details.append(row[3])
    #     metadata.append(row[4])
    #     embedding_data = row[5]
    #     # print("type embeding -->> ", row[6])
    #     if isinstance(embedding_data, str):
    #         # embedding_data = json.loads(embedding_data)
    #         embedding_data = bytes.fromhex(embedding_data)
    #     embeddings.append(np.frombuffer(embedding_data, dtype=np.float32))
    # return ids, destinations, descriptions, details, metadata, np.vstack(embeddings)
    # ids, destinations, descriptions, details, metadata, db_embeddings = fetch_embedings()
    # db_embeddings = np.array(db_embeddings, dtype=np.float32)  # Ensure float32
    # save_faiss_index(db_embeddings)
    main()
