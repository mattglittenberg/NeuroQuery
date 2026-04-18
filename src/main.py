import argparse
from src.utils.helpers import load_config
from src.ingestion.pubmed_fetch import fetch_pubmed_data
from src.preprocessing.clean_txt import preprocess
from src.embeddings.generate_embeddings import generate_embeddings
from src.clustering.topic_model import run_clustering
from src.search.semantic_search import SemanticSearch

def run_pipeline():
    config = load_config()

    print("Step 1: Getting PubMed data...")

    fetch_pubmed_data(
        query=config["ingestion"]["query"],
        output_path=config["data"]["raw_path"],
        retmax=config["ingestion"]["retmax"]
    )

    print("Step 2: Preprocessing data...")
    
    preprocess(
        input_path=config["data"]["raw_path"],
        output_path=config["data"]["processed_path"]
    )

    print("Step 3: Generating Embeddings...")

    generate_embeddings()

    print("Step 4: Clustering...")
    
    run_clustering()

def run_query(query):
    searcher = SemanticSearch()
    results = searcher.search(query)
    print(results)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_pipeline", action="store_true")
    parser.add_argument("--query", type=str, help="Search query")

    args = parser.parse_args()

    if args.run_pipeline:
        run_pipeline()

    if args.query:
        run_query(args.query)

