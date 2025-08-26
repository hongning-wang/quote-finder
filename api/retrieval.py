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

INDEX_PATH = os.path.join(settings.BASE_DIR, "faiss_index.bin")
MAP_PATH = os.path.join(settings.BASE_DIR, "faiss_map.pkl")

def build_index():
    """
    Returns the existing FAISS index if it exists, or creates a new one from the Quotes database.
    """
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    quotes = Quote.objects.exclude(embedding=[])
    if not quotes.exists():
        # Handle case where there are no quotes with embeddings
        dim = 768
        return faiss.IndexIDMap(faiss.IndexFlatL2(dim))
    dim = len(quotes.first().embedding)
    index = faiss.IndexIDMap(faiss.IndexFlatL2(dim))

    vectors = np.array([np.array(q.embedding, dtype=np.float32) for q in quotes])
    ids = np.array([q.pkid for q in quotes], dtype=np.int64)

    index.add_with_ids(np.vstack(vectors), np.array(ids, dtype=np.int64))
    faiss.write_index(index, INDEX_PATH)
    return index


load_dotenv()
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
def embed_text(content, type = "RETRIEVAL_DOCUMENT"):
    """
    Generates an embedding for a plain text.
    """
    resp = client.models.embed_content(
        model = "gemini-embedding-001",
        contents=content,
        config=types.EmbedContentConfig(task_type=type)
    )
    return resp
            
def add_quote(quoteObject):
    """Add a new entry in Quote database into FAISS index and return the index object."""
    global index
    if not hasattr(quoteObject, 'embedding') or quoteObject.embedding == []:
        return index
    vec = np.array(quoteObject.embedding, dtype=np.float32).reshape(1, -1)
    faiss_id = int(quoteObject.pkid)
    index.add_with_ids(vec, np.array([faiss_id], dtype=np.int64))
    faiss.write_index(index, INDEX_PATH)
    return index

def search_quotes(query, k=5):
    """Search FAISS for nearest neighbors and return Quote objects."""
    global index
    query_vector = embed_text(query, type="RETRIEVAL_QUERY").embeddings[0].values
    q = np.array(query_vector, dtype=np.float32).reshape(1, -1)
    _, faiss_ids = index.search(q, k)

    results = Quote.objects.filter(pkid__in=faiss_ids[0])
    return results

index = build_index()