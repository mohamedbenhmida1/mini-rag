# `mini-rag` Project Explained Simply

## What is this project?
`mini-rag` is a small RAG application built with `FastAPI`.
It lets you upload text or PDF files, split them into small pieces, store those pieces as vectors, and then answer questions using a language model.

## Simple structure
- `src/main.py`: starts the app and loads settings
- `src/routes/data.py`: handles upload and processing of files
- `src/routes/nlp.py`: handles indexing, searching, and answering questions
- `src/controllers/ProcessController.py`: reads files and splits text into chunks
- `src/controllers/NLPController.py`: embeds chunks, stores them in Qdrant, and builds answers
- `src/stores/VectorDB/providers/QdrantDBProvider.py`: talks to Qdrant for vector search
- `src/stores/llm/providers/OpenAIProvider.py`: talks to OpenAI for embeddings and answers
- `src/helpers/config.py`: loads `.env` settings

## The main steps
1. Upload file
2. Process file into chunks
3. Save chunks in MongoDB
4. Embed chunks and index them in Qdrant
5. Search with a question
6. Generate an answer from the best chunks

## Step-by-step flow
### 1. Upload
- Endpoint: `POST /api/v1/data/upload/{project_id}`
- The app checks file type and size
- It saves the file under a project folder
- It saves file metadata in MongoDB

### 2. Process file
- Endpoint: `POST /api/v1/data/process/{project_id}`
- It loads the file content from the project folder
- It splits the text into chunks
- It stores each chunk in MongoDB with metadata

### 3. Index chunks
- Endpoint: `POST /api/v1/nlp/index/push/{project_id}`
- It reads chunk records from MongoDB page by page
- It creates a vector for each chunk using the embedding model
- It stores chunk vectors in a Qdrant collection named `collection_{project_id}`

### 4. Search and answer
- Search endpoint: `POST /api/v1/nlp/index/search/{project_id}`
  - converts the question to a vector
  - finds the most similar chunk vectors
- Answer endpoint: `POST /api/v1/nlp/index/answer/{project_id}`
  - gets matching chunks
  - builds a prompt with those chunks
  - asks the LLM for a final answer

## Chunk size and why
- Default `chunk_size = 100`
- Default `overlap_size = 20`

Why this matters:
- The project splits text into small pieces so the vector search can work better.
- Overlap keeps meaning when one sentence crosses from one chunk to the next.
- This is a simple default; real systems usually use larger chunks or token-aware splitting.

## How the chunks are created
In `src/controllers/ProcessController.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=overlap_size,
    length_function=len
)
```
That means chunks are based on character count, not tokens.

## Important configuration values
Loaded from `.env` in `src/helpers/config.py`:
- `FILE_DEFAULT_CHUNK_SIZE`: upload buffer size
- `FILE_MAX_SIZE`: max file upload size
- `EMBEDDING_SIZE`: vector dimension (example `384`)
- `VECTOR_DB_BACKEND`: usually `QDRANT`
- `VECTOR_DB_DISTANCE_METHOD`: usually `Cosine`
- `GENERATION_BACKEND` + `EMBEDDING_BACKEND`: choose provider
- `GENERATION_MODEL_ID` + `EMBEDDING_MODEL_ID`: choose the model

## What the app stores
- MongoDB stores:
  - projects
  - uploaded file metadata
  - text chunks
- Qdrant stores:
  - chunk vectors
  - similarity search index

## Simple explanation of the whole system
1. You upload a file.
2. The system reads it and splits text into chunks.
3. Each chunk is stored in MongoDB.
4. The chunks are converted into vectors and stored in Qdrant.
5. When a user asks a question, the app finds the most related chunks.
6. The app gives those chunks to the LLM and returns a grounded answer.

## Files to mention
- `src/main.py`
- `src/routes/data.py`
- `src/routes/nlp.py`
- `src/controllers/ProcessController.py`
- `src/controllers/NLPController.py`
- `src/stores/VectorDB/providers/QdrantDBProvider.py`
- `src/stores/llm/providers/OpenAIProvider.py`
- `src/helpers/config.py`
- `src/stores/llm/templates/locales/en/rag.py`

## Important note
- This project is a small demo of RAG, not a full production system.
- Chunk size is set very low for simplicity.
- The prompt template should be cleaned for real use.
