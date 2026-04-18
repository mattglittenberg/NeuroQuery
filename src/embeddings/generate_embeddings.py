import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.utils.helpers import load_config, ensure_dir

def generate_embeddings():
    """
    Generates embeddings from article abstract.

    Takes abstract text and generates representative embeddings 
    in batches using Sentence Transformers (aka. SBERT). 
    Embeddings are then saved as an npy file.

    Parameters
    ----------
    None
    """

    config = load_config()

    df = pd.read_parquet(config["data"]["processed_path"])
    texts = df["cleaned_text"].tolist()

    model = SentenceTransformer(config["embedding"]["model_name"])

    embeddings = model.encode(
        texts,
        batch_size=config["embedding"]["batch_size"],
        show_progress_bar=True
    )

    ensure_dir("data/embeddings")
    np.save(config["embedding"]["output_path"], embeddings)

    print(f"Saved embeddings: {embeddings.shape}")
    print(embeddings)
if __name__ == "__main__":
    generate_embeddings()