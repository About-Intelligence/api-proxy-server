# Nexad API Proxy Server

This proxy server processes ad requests by generating embeddings for conversation content using sentence-transformers and forwards the enhanced requests to the target API.

## Features

- Processes API requests conforming to the Ad API specification
- Generates embeddings for conversation content using sentence-transformers
- Forwards processed requests to the target API
- Includes health check endpoint

## Setup

1. Make sure you have Python 3.13+ installed
2. Make sure you have Poetry (a modern Python package manager) installed

## Installation

Install Python packages:

```bash
poetry install
```

## Running the Server

Run with `main.py` directly

```bash
poetry run python main.py
```

Run with uvicorn

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

- `PORT`: The port number on which the server listens for incoming connections (default: 8000)
- `BASE_URL`: The target API endpoint where requests will be forwarded after processing (default: https://api-prod.nex-ad.com)
- `EMBEDDING_MODEL`: The sentence-transformers model identifier used for generating vector embeddings from conversation content (default: all-mpnet-base-v2)
