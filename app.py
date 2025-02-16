from data.db import fetch_travel_knowledge_base_table, update_embeding, fetch_embedings
from embedings.embedings import create_embeding
from response_generator.generate_response import generate_response_from_llama
from data.prompts import prompt_guardrails, prompt_travel_recomendation
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


"""
    This function updates the travel knowledge base with embeddings.
    It fetches the rows from the travel knowledge base table, creates embeddings
    for each row using the 'create_embedding' function, and then updates the 
    respective entries in the knowledge base with the newly created embeddings.
"""


def update_travel_knowledge_base_with_embedings():
    rows = fetch_travel_knowledge_base_table()
    for row in rows:
        embeding = create_embeding(row)
        update_embeding(row[0], embedding=embeding)


"""
    This function generates embeddings for the travel knowledge base using
    the SentenceTransformer model. It fetches the rows from the knowledge base,
    generates embeddings for the content of each row, and then updates the knowledge
    base with the generated embeddings. It also prints relevant information for debugging.
"""


def generate_embedings():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedings = []
    rows = fetch_travel_knowledge_base_table()
    print("rows -> ", rows)
    for row in rows:
        embeding = model.encode(row[1]).tolist()
        print("\n embeding -> ", embeding)
        print("row_id -> ", row[0])
        update_embeding(row[0], embeding)
        embedings.append(embeding)


"""
    This function updates the vector database by fetching embeddings from the
    knowledge base and adding them to a FAISS index for similarity search.
    It uses the pre-trained SentenceTransformer model to generate embeddings
    and stores them in the FAISS index, which is optimized for efficient vector search.
"""


def update_vector_db():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    ids, destinations, descriptions, details, metadata, db_embeddings = (
        fetch_embedings()
    )
    index = faiss.IndexFlatL2(db_embeddings.shape[1])
    index.add(db_embeddings)


"""
    This function searches a vector database for the most similar destinations
    to the input query. It uses a pre-trained SentenceTransformer model to encode
    the query into an embedding and compares it with the existing embeddings stored
    in the FAISS index using Euclidean (L2) distance. The function returns the
    top k most similar results based on the search.
"""


def search_vector_db(query="best place to visit in rome"):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query, convert_to_tensor=False).astype("float32")
    ids, destinations, descriptions, details, metadata, db_embeddings = (
        fetch_embedings()
    )

    top_k = 3
    dimension = db_embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(db_embeddings)
    distances, indices = faiss_index.search(np.array([query_embedding]), top_k)
    results = []
    for i in range(top_k):
        idx = indices[0][i]
        results.append(
            {
                "id": ids[idx],
                "destination": destinations[idx],
                "description": descriptions[idx],
                "details": details[idx],
                "metadata": metadata[idx],
                "distance": distances[0][i],
            }
        )

    print("result -->> ", results)
    return results


"""
    This function simulates a chatbot-like interaction, allowing the user to ask
    for trip details or quit the conversation. It presents a menu for the user to 
    choose from and responds based on the selected option. If the user asks for trip 
    details, the query is processed using a model and a vector search to return 
    relevant travel recommendations.
"""


def chat_with_genie():
    flag = True
    print(" Chat window started ".center(100, "-"))
    while flag:

        print("Please select one choice from below options. ")
        print("1. Ask a trip details,")
        print("2. Quit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                query = input("Ask me anything: ")
                is_safe = generate_response_from_llama(
                    prompt_guardrails.format(query=query)
                )
                # safe=is_safe['message']['content'].strip()
                safe = is_safe.strip()
                # print("is safe --->> ", is_safe)
                if safe == "UNSAFE":
                    print("\nGenie -> Sorry, I can not assit you with that.\n")
                    print("".center(100, "-"))
                    continue

                else:
                    print("It si safe")
                    context = search_vector_db(query=query)
                    # print("context================================",context)
                    res = generate_response_from_llama(
                        prompt_travel_recomendation.format(query=query, context=context)
                    )
                    print(res)
                    print()
                    print("".center(100, "-"))
                    continue
            elif choice == 2:
                flag = False
            else:
                print("Please enter a valide number.")
                continue
        except ValueError as e:
            print()
            print("Please enter only number as a choice. ".ljust(100, "-"))
            print()
            continue


"""
=========================== MAIN FUNCTION =========================
This is the main entry point for the program. It initiates the chat window
where users can interact with the Genie to ask for trip details or quit.
The other functions for generating embeddings, updating the vector database, 
and searching the vector database are commented out but can be activated 
as needed for different functionalities.
"""


def main():
    print()
    # generate_embedings()
    # update_vector_db()
    # search_vector_db()
    chat_with_genie()


if __name__ == "__main__":
    main()
