# mini-rag Project Overview

## What is mini-rag?
`mini-rag` is a small demo project for Retrieval-Augmented Generation (RAG).
It is built with `FastAPI` and shows how to:
- upload files
- split text into chunks
- store chunk vectors in a vector database
- search for relevant text
- generate answers with a language model

## Project structure
- `src/main.py`: starts the app and loads settings
- `src/routes/data.py`: upload files, validate them, and process them
- `src/routes/nlp.py`: create index, search, and answer questions
- `src/controllers/ProcessController.py`: read files and split them into chunks
- `src/controllers/NLPController.py`: embed chunks and return answers
- `src/stores/VectorDB/providers/QdrantDBProvider.py`: handle vector database operations
- `src/stores/llm/providers/OpenAIProvider.py`: handle OpenAI generation and embeddings
- `src/helpers/config.py`: load environment variables from `.env`

## Main steps
1. Upload a file.
2. Process the file into chunks.
3. Save chunks in MongoDB.
4. Convert chunks into vectors and store them in Qdrant.
5. Search with a question.
6. Generate an answer using the best chunks.

## Each step in simple terms
### 1. Upload
- Use `POST /api/v1/data/upload/{project_id}`
- The app checks the file type and size
- It saves the file in a project folder
- It records the file in MongoDB

### 2. Process
- Use `POST /api/v1/data/process/{project_id}`
- The app reads the saved file
- It splits the text into small pieces called chunks
- It stores each chunk in MongoDB

### 3. Index chunks
- Use `POST /api/v1/nlp/index/push/{project_id}`
- The app reads chunks from MongoDB
- It converts each chunk to a vector using the embedding model
- It stores those vectors in Qdrant

### 4. Search and answer
- Search endpoint: `POST /api/v1/nlp/index/search/{project_id}`
  - the question is converted into a vector
  - Qdrant finds the most similar chunks
- Answer endpoint: `POST /api/v1/nlp/index/answer/{project_id}`
  - the app uses the top chunks to build a prompt
  - it asks the LLM for the final answer

## Chunk settings
- `chunk_size = 100`
- `overlap_size = 20`

What that means:
- The text is split into pieces of about 100 characters.
- Adjacent chunks overlap by 20 characters.
- Overlap helps keep text context when one sentence spans chunks.

## Where data is stored
- MongoDB stores:
  - projects
  - file metadata
  - text chunks
- Qdrant stores:
  - vector embeddings for chunks
  - search index for similarity matching

## Simple end-to-end flow
1. Upload file
2. Split text into chunks
3. Save chunks in MongoDB
4. Create vectors for chunks and save them in Qdrant
5. Ask a question
6. Use top chunks to build the answer

## Key files to mention
- `src/main.py`
- `src/routes/data.py`
- `src/routes/nlp.py`
- `src/controllers/ProcessController.py`
- `src/controllers/NLPController.py`
- `src/stores/VectorDB/providers/QdrantDBProvider.py`
- `src/stores/llm/providers/OpenAIProvider.py`
- `src/helpers/config.py`

## Note
- This is a demo project, not a production system.
- The chunk size is small for simplicity.
- The prompt template needs cleanup before real use.
