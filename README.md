# NeuroQuery — Semantic Search & Topic Discovery for Scientific Literature

SciQuery is an end-to-end natural language processing (NLP) pipeline for ingesting, processing, and analyzing large-scale biomedical literature. It enables **semantic search** and **topic discovery** over thousands of research abstracts using transformer-based embeddings.

Built to mirror real-world ML systems, SciQuery emphasizes **reproducibility, modular pipeline design, and scalable data processing**.

---

## Key Features

* **Automated Data Ingestion**

  * Pulls real-time data from PubMed via the NCBI E-utilities API
* **Text Processing Pipeline**

  * Cleans and structures raw scientific text for downstream modeling
* **Transformer-Based Embeddings**

  * Uses Sentence-BERT (PyTorch-backed) to encode abstracts into dense vectors
* **Semantic Search**

  * Retrieve relevant papers based on meaning, not keywords
* **Topic Modeling / Clustering**

  * Discover latent research themes across large corpora
* **Reproducible Pipeline**

  * Config-driven workflow with modular components

---

## System Architecture

```text
PubMed API → ETL Pipeline → Cleaned Text → Embeddings → Search + Clustering
```

---

## Tech Stack

* **Python**
* **PyTorch** (via SentenceTransformers)
* **Hugging Face Transformers**
* **scikit-learn**
* **Pandas / NumPy**
* **YAML (config-driven pipelines)**

---

## Project Structure

```
scientific-nlp-pipeline/
│
├── config/              # Configuration files (YAML)
├── data/                # Raw, processed, and embedding outputs
├── src/
│   ├── ingestion/       # PubMed API ingestion
│   ├── preprocessing/   # Text cleaning and transformation
│   ├── embeddings/      # Embedding generation
│   ├── search/          # Semantic search
│   ├── clustering/      # Topic modeling
│   ├── utils/           # Shared utilities
│   └── main.py          # Pipeline entry point
│
├── notebooks/           # Exploration and prototyping
├── tests/               # Basic tests
└── app/                 # Streamlit interface
```

---

## Installation

```bash
git clone https://github.com/mattglittenberg/neuroquery.git
cd neuroquery

pip install -r requirements.txt
```

---

## Usage

### 1. Run Full Pipeline

```bash
python -m src.main --run_pipeline
```

This will:

* Fetch data from PubMed
* Clean and preprocess text
* Generate embeddings
* Perform clustering

---

### 2. Run Semantic Search

```bash
python -m src.main --query "alzheimers disease biomarkers"
```

Example Output:

```
Title: Plasma tau levels in early Alzheimer’s disease...
Score: 0.89

Title: Biomarker progression in neurodegenerative disorders...
Score: 0.86
```

---

## Example Use Cases

* Literature review acceleration
* Identifying emerging research trends
* Discovering related work across domains
* Supporting hypothesis generation in Alzheimer's Disease research

---

## Reproducibility

* Config-driven pipeline (`config.yaml`)
* Deterministic preprocessing steps
* Modular architecture for easy experimentation

---

## Future Improvements

* FAISS-based vector search for scalability
* Real-time API (FastAPI)
* Fine-tuned domain-specific transformer models
* Cloud deployment (AWS/GCP)
* User-facing interface (Streamlit)

---

## Author

Matthew Glittenberg
Data Scientist | Computational Biology | Machine Learning | Personalized Medicine

---

## License

MIT License
