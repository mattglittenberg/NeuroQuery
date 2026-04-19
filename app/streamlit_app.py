import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="NeuroQuery",
    page_icon="🧠",
    layout="wide"
)

EMBEDDINGS_PATH = "data/embeddings/embeddings.npy"
DATA_PATH = "data/processed/cleaned.parquet"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5


@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)


@st.cache_data
def load_data():
    if not Path(DATA_PATH).exists():
        return None
    return pd.read_parquet(DATA_PATH)


@st.cache_data
def load_embeddings():
    if not Path(EMBEDDINGS_PATH).exists():
        return None
    return np.load(EMBEDDINGS_PATH)


def semantic_search(query, model, df, embeddings, top_k=TOP_K):
    query_embedding = model.encode(query)
    scores = util.cos_sim(query_embedding, embeddings)[0].cpu().numpy()

    top_indices = scores.argsort()[-top_k:][::-1]

    results = df.iloc[top_indices].copy()
    results["score"] = scores[top_indices]

    return results[["title", "abstract", "score"]]


def main():
    st.title("🧠 NeuroQuery")
    st.subheader("Semantic Search & Topic Discovery for Alzheimer's Disease Literature")

    st.markdown(
        "Search biomedical literature using transformer-based semantic search over PubMed abstracts."
    )

    with st.sidebar:
        st.header("About")
        st.write(
            "NeuroQuery ingests scientific literature, generates transformer-based embeddings, "
            "and enables semantic search across Alzheimer's Disease research."
        )

        st.divider()
        st.write("**Model:** Sentence-BERT")
        st.write("**Corpus:** PubMed abstracts")
        st.write(f"**Top Results:** {TOP_K}")

    df = load_data()
    embeddings = load_embeddings()
    model = load_model()

    if df is None or embeddings is None:
        st.warning(
            "Data or embeddings not found. Run the pipeline first:\n\n"
            "`python -m src.main --run_pipeline`"
        )
        st.stop()

    query = st.text_input(
        "Enter your research query",
        placeholder="e.g. Alzheimer's disease biomarkers"
    )

    search_clicked = st.button("Search")

    if search_clicked and query:
        with st.spinner("Searching scientific literature..."):
            results = semantic_search(query, model, df, embeddings)

        st.success(f"Found top {len(results)} relevant papers")

        for idx, row in results.iterrows():
            with st.container():
                st.markdown(f"## {row['title']}")
                st.markdown(f"**Relevance Score:** {row['score']:.3f}")
                st.write(row["abstract"])
                st.divider()

    elif not query:
        st.info("Enter a query above to begin semantic search.")

    st.divider()
    st.caption(
        "Built by Matthew Glittenberg | NLP Pipeline • Semantic Search • Biomedical Literature"
    )


if __name__ == "__main__":
    main()