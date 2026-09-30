# GraphRAG POC

A GraphRAG Proof of Concept built using:

- Python
- Neo4j
- FAISS
- Ollama
- LangChain
- Streamlit

## Features

- Document ingestion
- Chunking
- Embedding generation
- FAISS Vector Database
- Entity & Relationship Extraction
- Neo4j Knowledge Graph
- Hybrid Retrieval (Vector + Graph)
- Multi-hop Graph Traversal
- Question Answering

## Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1

## Run Ollama

```bash
ollama serve
```

## Pull models

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run ingestion

```bash
python ingest.py
```

## Run UI

```bash
streamlit run app.py
```

## See the Graph at Neo4j Desktop

```bash
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;
```