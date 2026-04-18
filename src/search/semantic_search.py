import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from src.utils.helpers import load_config

class SemanticSearch:
    def __init__(self):
        self.config = load_config()
        self.model = SentenceTransformer(self.config["embedding"]["model_name"])

        self.df = pd.read_parquet(self.config["data"]["processed_path"])
        self.embeddings = np.load(self.config["embedding"]["output_path"])

    def search(self, query, top_k=None):
        if top_k is None:
            top_k = self.config["search"]["top_k"]
        
        top_k = min(top_k, len(self.embeddings))

        query_embedding = self.model.encode(query)

        scores = util.cos_sim(query_embedding, self.embeddings)[0].cpu().numpy()

        top_indices = scores.argsort()[-top_k:][::-1]

        results = self.df.iloc[top_indices].copy()
        results["score"] = scores[top_indices]

        return results[["title", "abstract", "score"]]

if __name__ == "__main__":
    searcher = SemanticSearch()
    results = searcher.search("alzheimers biomarkers")

    print(results)