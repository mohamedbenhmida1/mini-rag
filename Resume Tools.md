# Resume Tools

This file summarizes the main tools, libraries, and platforms used in this project in a résumé-friendly way.

## Project Summary

Built a mini RAG application in Python that:

- uploads files
- extracts and splits text into chunks
- stores structured records in Postgres
- stores embeddings in Qdrant
- performs semantic search
- generates answers with LLMs

## Programming Language

### Python

What it does:
- Main programming language used to build the backend and RAG pipeline.

How I used it:
- Built the FastAPI backend
- Implemented file upload and processing logic
- Connected Postgres, Qdrant, OpenAI, and Cohere
- Created the chunking, indexing, search, and answer-generation flow

## Backend Framework

### FastAPI

What it does:
- Modern Python web framework for building APIs quickly with automatic validation and documentation support.

How I used it:
- Created API endpoints for upload, processing, indexing, search, and question answering
- Organized the backend with route modules like `data.py`, `nlp.py`, and `base.py`
- Used request handling and JSON responses for the application workflow

### Uvicorn

What it does:
- ASGI server used to run FastAPI applications.

How I used it:
- Ran the backend server locally during development
- Served the FastAPI application with hot reload support

## Data Validation and Configuration

### Pydantic

What it does:
- Data validation library for Python models and request schemas.

How I used it:
- Defined request bodies for endpoints such as chunk processing and search
- Structured typed models for API input validation

### pydantic-settings

What it does:
- Extension for loading application settings from environment variables.

How I used it:
- Managed application configuration from `.env`
- Loaded database settings, API keys, model settings, chunking settings, and vector DB settings

### python-dotenv

What it does:
- Loads environment variables from a `.env` file.

How I used it:
- Supported local configuration for API keys and database credentials

## File Handling

### python-multipart

What it does:
- Enables file upload handling in FastAPI.

How I used it:
- Supported multipart form uploads for user documents

### aiofiles

What it does:
- Asynchronous file I/O library.

How I used it:
- Saved uploaded files asynchronously to disk
- Improved file handling inside FastAPI endpoints

### PyMuPDF

What it does:
- PDF parsing and text extraction library.

How I used it:
- Read uploaded PDF files before chunking them into smaller text segments

## RAG and Text Processing

### LangChain

What it does:
- Framework that provides utilities for document loading, text splitting, prompt workflows, and LLM-based application building.

How I used it:
- Used `PyMuPDFLoader` to load PDF content
- Used `TextLoader` to load text files
- Used `RecursiveCharacterTextSplitter` to split file content into chunks
- Integrated LangChain as the document processing layer of the RAG pipeline

### Prompt Templates

What it does:
- Controls how retrieved chunks and user questions are formatted before being sent to the language model.

How I used it:
- Stored prompt templates in localized files under `src/stores/llm/templates`
- Built the final RAG prompt by combining retrieved chunks and the user query

## LLM and Embedding Tools

### OpenAI Python SDK

What it does:
- Official SDK for using OpenAI models for text generation and embeddings.

How I used it:
- Connected OpenAI as an LLM provider
- Used OpenAI models for answer generation
- Used OpenAI embeddings in the semantic search workflow

### Cohere Python SDK

What it does:
- SDK for using Cohere language and embedding models.

How I used it:
- Added Cohere as an alternative provider in the provider layer
- Built support for switching between model providers from configuration

### HTTPX

What it does:
- HTTP client library for Python.

How I used it:
- Used indirectly in the LLM integration stack and API communication dependencies

## Vector Database

### Qdrant

What it does:
- Vector database for storing embeddings and performing similarity search.

How I used it:
- Created collections for project-specific embeddings
- Inserted chunk vectors after processing documents
- Searched similar chunks for semantic retrieval
- Used Qdrant as the retrieval layer of the RAG system

### qdrant-client

What it does:
- Python client for interacting with Qdrant.

How I used it:
- Created and deleted collections
- Inserted vectors with metadata
- Queried vectors during semantic search

## Relational Database and ORM

### PostgreSQL

What it does:
- Relational database used for structured application data.

How I used it:
- Stored projects, uploaded asset metadata, and processed chunks
- Replaced the earlier MongoDB-style persistence layer with a relational schema
- Organized data using tables and foreign key relationships

### SQLAlchemy

What it does:
- Python ORM and database toolkit used to map Python classes to database tables.

How I used it:
- Defined the main database models: `Project`, `Asset`, and `DataChunk`
- Built async database access with sessions
- Queried and inserted relational records from the application code
- Connected the FastAPI app to Postgres through an async engine

### asyncpg

What it does:
- High-performance async PostgreSQL driver for Python.

How I used it:
- Powered the async PostgreSQL connection used by SQLAlchemy in the FastAPI app

### Alembic

What it does:
- Database migration tool for SQLAlchemy.

How I used it:
- Managed schema versioning for the Postgres database
- Created the initial migration for `projects`, `assets`, and `chunks`
- Used Alembic to make schema changes repeatable and trackable

### psycopg2

What it does:
- PostgreSQL adapter for Python, commonly used by database tools and sync workflows.

How I used it:
- Included as part of the Postgres tooling stack for database compatibility and local development support

## Previous Database Stack

### MongoDB

What it does:
- NoSQL document database.

How I used it:
- Used as the original persistence approach before moving the project to Postgres
- The codebase still contains some legacy Mongo-related dependencies and import traces from the earlier version

### PyMongo

What it does:
- Official MongoDB driver for Python.

How I used it:
- Was part of the original database layer before the migration to SQLAlchemy and Postgres

### Motor

What it does:
- Async MongoDB driver for Python.

How I used it:
- Included for the earlier async MongoDB workflow before the project switched to Postgres

## Database Management Tools

### DBeaver

What it does:
- Universal database management tool for relational databases.

How I used it:
- Inspected Postgres tables and records
- Verified schema creation and relationships
- Checked data after migrations and application inserts
- Helped test the new Postgres + SQLAlchemy structure visually

### Studio 3T

What it does:
- GUI tool for working with MongoDB databases.

How I used it:
- Explored and managed MongoDB data during the earlier version of the project
- Compared the old MongoDB structure with the new Postgres relational design during the migration

## API Testing and Development Tools

### Postman

What it does:
- API testing and collaboration tool.

How I used it:
- Tested endpoints for upload, processing, indexing, search, and answer generation
- Saved request collections for repeatable API testing

### Docker Compose

What it does:
- Tool for defining and running multi-container development environments.

How I used it:
- Managed local database services from `docker/docker-compose.yml`
- Used containerized database services during development

## Architecture and Design Patterns

### Provider Pattern

What it does:
- A design pattern that makes it easy to switch between implementations behind one interface.

How I used it:
- Built pluggable providers for LLM backends and vector database backends
- Allowed the project to support both OpenAI and Cohere more cleanly

### Factory Pattern

What it does:
- Centralizes object creation and keeps service setup organized.

How I used it:
- Used `LLMProviderFactory` and `VectorDBProviderFactory` to instantiate the correct backend from configuration

## Key Technical Features Delivered

- Built a FastAPI-based RAG backend in Python
- Implemented document upload and asynchronous file storage
- Used LangChain for document loading and chunking
- Used OpenAI and Cohere provider abstractions for generation and embeddings
- Stored structured metadata in PostgreSQL
- Used SQLAlchemy for ORM-based async database access
- Used Alembic for schema migration management
- Used Qdrant for vector storage and semantic retrieval
- Tested APIs with Postman
- Inspected databases with DBeaver and Studio 3T

## Short Resume Version

Mini RAG backend built with Python, FastAPI, LangChain, OpenAI, Cohere, Qdrant, PostgreSQL, SQLAlchemy, and Alembic. Implemented file upload, PDF and text ingestion, chunking, vector indexing, semantic search, and answer generation. Used DBeaver and Studio 3T for database inspection and validation, Postman for API testing, and Docker Compose for local service setup.
