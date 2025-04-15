from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import pandas as pd
import time
import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client import QdrantClient
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_collection(client, collection_name, dim=384):
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )
        print(f"✅ Created collection: {collection_name}")


def upload_csv_to_qdrant(csv_path, collection_name, qdrant_path):
    df = pd.read_csv(csv_path)
    client = QdrantClient(path=qdrant_path)
    create_collection(client, collection_name)

    vectors = model.encode(df["text"].tolist()).tolist()
    points = []

    for idx, (vec, row) in enumerate(zip(vectors, df.itertuples(index=False))):
        realid = getattr(row, "realid")
        text = getattr(row, "text")
        role = getattr(row, "role", "user")

        point = PointStruct(
            id=int(idx),
            vector=vec,
            payload={
                "person_id": str(realid),  # ✅ important fix
                "text": text,
                "role": role,
                "type": "info"
            }
        )
        points.append(point)

    client.upsert(collection_name=collection_name, points=points)
    print("✅ Uploaded vectors to Qdrant")



def search_by_realid(realid, collection_name, qdrant_path):
    client = QdrantClient(path=qdrant_path)

    realid_filter = Filter(
        must=[
            FieldCondition(
                key="realid",
                match=MatchValue(value=int(realid))
            )
        ]
    )

    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=realid_filter,
        with_payload=True,
        limit=100  # Adjust based on max expected entries
    )[0]

    return [item.payload["text"] for item in results]

def store_memory(text: str, person_id: str, role: str, memory_type: str, collection_name: str, qdrant_path: str, language:str):
    vector = model.encode(text).tolist()
    client = QdrantClient(path=qdrant_path)

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "text": text,
            "person_id": person_id,
            "role": role,
            "timestamp": time.time(),
            "type": memory_type,
            "language": language  # ✅ store detected language
        }
    )
    client.upsert(collection_name=collection_name, points=[point])


def get_memory_context(person_id: str, collection_name: str, qdrant_path: str, max_exchanges=5):
    client = QdrantClient(path=qdrant_path)

    filter_by_id = Filter(
        must=[
            FieldCondition(key="person_id", match=MatchValue(value=person_id))
        ]
    )

    results, _ = client.scroll(
        collection_name=collection_name,
        scroll_filter=filter_by_id,
        with_payload=True,
        limit=200  # increase to make sure we get enough history
    )

    info = []
    chats = []

    for point in results:
        payload = point.payload
        if payload.get("type") == "info":
            info.append(payload["text"])
        elif payload.get("role") in ["user", "assistant"]:
            chats.append((payload.get("timestamp", 0), payload["role"], payload["text"]))

    # Sort by time ascending (oldest to newest)
    sorted_chats = sorted(chats, key=lambda x: x[0])

    # Group into user-assistant pairs
    dialog_pairs = []
    pair = []

    for entry in sorted_chats:
        _, role, text = entry
        pair.append((role.capitalize(), text))
        if len(pair) == 2:
            dialog_pairs.append(pair)
            pair = []

    # Get last N exchanges
    last_exchanges = dialog_pairs[-max_exchanges:]

    # Flatten to plain text lines
    chat_lines = [f"{role}: {text}" for pair in last_exchanges for role, text in pair]
    info_lines = [f"User Info: {line}" for line in info]

    return "\n".join(info_lines + chat_lines)

