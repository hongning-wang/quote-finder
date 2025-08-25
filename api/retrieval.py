import faiss
import numpy as np
from api.models import Quote
from django.conf import settings
import os
import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pickle
INDEX_PATH = os.path.join(settings.BASE_DIR, "faiss_index.bin")
MAP_PATH = os.path.join(settings.BASE_DIR, "faiss_map.pkl")

def build_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)

    quotes = Quote.objects.exclude(embedding=[])

    dim = len(quotes.first().embedding)
    index = faiss.IndexIDMap(faiss.IndexFlatL2(dim))

    vectors, ids = [], []
    for q in quotes:
        vectors.append(np.array(q.embedding, dtype=np.float32))
        ids.append(q.pkid)  # use the new integer PK

    index.add_with_ids(np.vstack(vectors), np.array(ids, dtype=np.int64))
    faiss.write_index(index, INDEX_PATH)
    return index

load_dotenv()
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
def embed_text(content, type = "RETRIEVAL_DOCUMENT"):
    
    resp = client.models.embed_content(
        model = "gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(task_type=type)
    )
    return resp
            



def search_quotes(query, k=5):
    """Search FAISS for nearest neighbors and return Quote objects."""
    index = build_index()
    query_vector = embed_text(query, type="RETRIEVAL_QUERY").embeddings[0].values
    q = np.array(query_vector, dtype=np.float32).reshape(1, -1)
    _, faiss_ids = index.search(q, k)

    results = Quote.objects.filter(pkid__in=faiss_ids[0])
    return results