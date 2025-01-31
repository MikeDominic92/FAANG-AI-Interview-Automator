from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict

class ResumeKnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="../data/chroma")
        self.collection = self.client.get_or_create_collection("resume_data")

    def add_documents(self, documents: List[Dict]):
        embeddings = self.model.encode([doc["content"] for doc in documents])
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=[doc["content"] for doc in documents],
            metadatas=[{"type": doc["type"], "skills": doc["skills"]} for doc in documents],
            ids=[str(i) for i in range(len(documents))]
        )

    def query(self, text: str, n_results: int = 3) -> List[Dict]:
        query_embedding = self.model.encode(text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return [
            {
                "content": doc,
                "type": meta["type"],
                "skills": meta["skills"]
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
