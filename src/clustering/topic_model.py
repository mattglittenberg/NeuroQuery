import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from src.utils.helpers import load_config

def run_clustering():
    config = load_config()

    df = pd.read_parquet(config["data"]["processed_path"])
    embeddings = np.load(config["embedding"]["output_path"])

    n_clusters = min(config["clustering"]["n_clusters"], len(embeddings))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    df["cluster"] = clusters

    df.to_parquet("data/processed/clustered.parquet", index=False)

    print("Clustering complete")

if __name__ == "__main__":
    run_clustering()