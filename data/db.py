import sqlite3
import json
import numpy as np

"""
    This function establishes a connection to the SQLite database and returns a cursor object
    that can be used to execute SQL queries on the connected database. The database file used is 'travel.db'.
"""


def connect_db():
    conn = sqlite3.connect("travel.db")
    cursor = conn.cursor()
    return cursor


"""
    This function creates the 'travel_knowledge_base' table in the SQLite database.
    It checks if the table already exists, and if not, it creates a new table with
    the specified schema. The table stores information related to travel destinations, 
    including metadata and embeddings for future use.
"""


def create_travel_knowledge_base_table():

    cursor = connect_db()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS travel_knowledge_base (
            id INTEGER PRIMARY KEY,
            destination TEXT,
            description TEXT,
            details TEXT,
            metadata TEXT,
            embeding BLOB
        )
    """
    )
    print("created")


"""
    This function inserts data into the 'travel_knowledge_base' table in the SQLite database.
    It iterates over a list of data, where each item is expected to contain details about a travel destination.
    It inserts the information into the table and handles any exceptions such as duplicates or missing keys.
"""


def update_travel_knowledge_base_table(data):
    cursor = connect_db()
    for item in data:
        print("item -> ", item)
        try:
            cursor.execute(
                """
                INSERT INTO travel_knowledge_base (id, destination, description, details, metadata)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    item["Id"],
                    item["destination"],
                    item["description"],
                    item["details"],
                    item["metadata"],
                ),
            )
        except sqlite3.IntegrityError:
            print(f"Error: Destination '{item['destination']}' already exists.")
        except KeyError as e:
            print(f"Error: Missing key '{e}' in data.")
        else:
            print(f"inserted data with id {item.get('Id')}")
    cursor.connection.commit()
    cursor.close()


"""
    This function retrieves all rows from the 'travel_knowledge_base' table.
    It combines the 'description', 'details', and 'metadata' columns into one field 
    and returns the results as a list of tuples. Each tuple contains the id and the concatenated string.
"""


def fetch_travel_knowledge_base_table():
    cursor = connect_db()
    cursor.execute(
        "SELECT id, description || ' ' || details || ' ' || metadata FROM travel_knowledge_base"
    )
    rows = cursor.fetchall()
    return rows


"""
    This function updates the 'embedding' column for a specific row in the 'travel_knowledge_base' table.
    It takes an 'id' and the new 'embedding' (a list or array), serializes the embedding into binary format, 
    and updates the corresponding row in the table.
"""


def update_embeding(id, embedding):
    cursor = connect_db()
    serialized_embedding = np.array(embedding, dtype=np.float32).tobytes()
    cursor.execute(
        "UPDATE travel_knowledge_base SET embeding = ? WHERE id = ?",
        (serialized_embedding, id),
    )
    cursor.connection.commit()


"""
    This function fetches all relevant data from the 'travel_knowledge_base' table,
    including the 'embedding' column which contains serialized embeddings in binary format.
    It extracts the information into separate lists for easy use and returns the processed data.
"""


def fetch_embedings():
    cursor = connect_db()
    cursor.execute(
        "SELECT id, destination, description, details, metadata, embeding, typeof(embeding) FROM travel_knowledge_base"
    )

    rows = cursor.fetchall()
    # print(rows)
    ids, destinations, descriptions, details, metadata, embeddings = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    for row in rows:
        ids.append(row[0])
        destinations.append(row[1])
        descriptions.append(row[2])
        details.append(row[3])
        metadata.append(row[4])
        embedding_data = row[5]
        # print("type embeding -->> ", row[6])
        if isinstance(embedding_data, str):
            # embedding_data = json.loads(embedding_data)
            embedding_data = bytes.fromhex(embedding_data)
        embeddings.append(np.frombuffer(embedding_data, dtype=np.float32))
    return ids, destinations, descriptions, details, metadata, np.vstack(embeddings)


"""
    This is the main function of the script. It loads data from a JSON file and creates or updates 
    the travel knowledge base table in the SQLite database with the contents of the loaded data.
"""


def main():
    from embedings.embedings import generate_embedding

    create_travel_knowledge_base_table()
    with open(
        r"C:\Users\kp121\Documents\vs code project\NomadNavigator\data\knowledge_base.json",
        "r",
    ) as f:
        data = json.loads(f.read())
        update_travel_knowledge_base_table(data)
    rows = fetch_travel_knowledge_base_table()

    # Generate and store embeddings
    for id, text in rows:
        print(id, text)
        embedding = generate_embedding(text)  # Generate embedding
        update_embeding(id, embedding)


if __name__ == "__main__":
    print(" Started ".center(100, "-"))
    main()
