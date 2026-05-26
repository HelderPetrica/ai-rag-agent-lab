# Demo Walkthrough

## 1. Start The API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## 2. Check Health

```bash
curl http://localhost:8000/health
```

Expected: service status, service name, version and indexed chunk count.

## 3. Index Sample Data

```bash
curl -X POST http://localhost:8000/documents/index \
  -H "Content-Type: application/json" \
  -d "{\"use_sample_data\": true}"
```

Expected: indexed document count, indexed chunk count and source names.

## 4. Query The Indexed Context

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"How does validation work?\",\"top_k\":2}"
```

Expected: answer, retrieved context, sources, confidence, warnings and metadata.

## 5. Run Tests

```bash
pytest
```

The tests cover API contracts, chunking, embeddings, retrieval, validation, docs consistency and security smoke checks.

