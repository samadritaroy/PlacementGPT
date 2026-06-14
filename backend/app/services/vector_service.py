from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = None
stored_chunks = []
stored_metadata = []

def create_vector_store(chunks,filename):

    global index
    global stored_chunks
    global stored_metadata

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(
            dimension
        )
    index.add(
        np.array(embeddings)
    )

    stored_chunks.extend(chunks)
    start = len(stored_metadata)
    stored_metadata.extend([
        {
            "file": filename,
            "chunk_id": start + i
        }
        for i in range(len(chunks))
    ])
    print("Total Chunks:", len(stored_chunks))
    print("FAISS Vectors:", index.ntotal)

def search_chunks(question):
    global index

    if index is None:
        return {
            "context": "",
            "sources": []
        }

    embedding = model.encode(
        [question]
    )

    distances, indices = index.search(
        np.array(embedding),
        3
    )

    results = []
    sources = []

    for i in indices[0]:

        results.append(
            stored_chunks[i]
        )

        sources.append(
            stored_metadata[i]
        )

    return {
        "context": "\n".join(results),
        "sources": sources
    }