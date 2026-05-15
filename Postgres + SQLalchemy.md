# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Data migration from mongodb to Postgres + SQLAlchemy

This project originally followed a document-database style for storing project data. It has now been moved to **PostgreSQL** and the application uses **SQLAlchemy** for database access and **Alembic** for schema migrations.

The goal of this change is simple:

- keep data storage more structured
- make relationships between records explicit
- make schema changes safer over time
- improve maintainability as the project grows

### What Changed

Before this change, the project was designed around a MongoDB-style approach, where records were expected to be handled as flexible documents.

Now, the main application data is stored in PostgreSQL using relational tables:

- `projects`
- `assets`
- `chunks`

These tables are defined with SQLAlchemy models inside:

- `src/models/db_schemes/minirag/schemes/project.py`
- `src/models/db_schemes/minirag/schemes/asset.py`
- `src/models/db_schemes/minirag/schemes/datachunk.py`

The database schema itself is versioned with Alembic in:

- `src/models/db_schemes/minirag/alembic/`

### Why PostgreSQL Was Chosen

MongoDB is flexible, which is useful early in a project, but this application has clear relationships between its core records:

- one project can have many assets
- one project can have many chunks
- one asset belongs to one project
- one chunk belongs to one project and one asset

That kind of structure maps naturally to a relational database.

PostgreSQL gives the project:

- stronger data consistency through primary keys and foreign keys
- easier querying for linked records
- better long-term schema control
- a cleaner foundation for reporting, debugging, and future features

### Why SQLAlchemy Was Added

SQLAlchemy is the ORM layer used to talk to PostgreSQL from Python.

In this project, SQLAlchemy is responsible for:

- defining tables as Python classes
- creating async database sessions
- inserting and querying records without writing raw SQL for every operation

The SQLAlchemy engine is created in:

- `src/main.py`

At startup, the app builds an async PostgreSQL connection like this conceptually:

- FastAPI starts
- a PostgreSQL connection string is built from environment variables
- `create_async_engine(...)` is used
- `sessionmaker(..., class_=AsyncSession)` provides sessions to the models

This means the app now uses an **async SQLAlchemy workflow** instead of a Mongo client workflow.

### Why Alembic Was Added

Alembic is the migration tool used with SQLAlchemy.

Its job is to keep the database schema under version control.

Instead of manually creating or changing tables in PostgreSQL, the project now tracks schema changes through migration files. That makes it easier for different developers and environments to stay in sync.

The current initial migration is:

- `src/models/db_schemes/minirag/alembic/versions/88cbbd1b59f6_initial_commit.py`

That migration creates:

- the `projects` table
- the `assets` table
- the `chunks` table
- indexes for commonly queried fields
- foreign key relationships between the tables

### New Data Model

The relational model in this project is straightforward.

#### 1. Projects

The `projects` table is the top-level record.

It stores:

- `project_id` as the integer primary key
- `project_uuid` as a public unique UUID
- timestamps like `created_at` and `updated_at`

#### 2. Assets

The `assets` table stores uploaded files and links each file to a project.

It stores:

- `asset_id` as the integer primary key
- `asset_uuid` as a unique UUID
- file metadata such as type, name, and size
- `asset_config` as JSONB for optional structured configuration
- `asset_project_id` as a foreign key to `projects.project_id`

#### 3. Chunks

The `chunks` table stores processed text chunks generated from files.

It stores:

- `chunk_id` as the integer primary key
- `chunk_uuid` as a unique UUID
- `chunk_text`
- `chunk_metadata` as JSONB
- `chunk_order`
- `chunk_project_id` as a foreign key to the project
- `chunk_asset_id` as a foreign key to the source asset

### How the Application Flow Changed

The migration is not only about changing the database engine. It also changed how the application saves and retrieves data.

#### Upload Flow

When a file is uploaded through:

- `POST /api/v1/data/upload/{project_id}`

the application now:

1. checks whether the project exists in PostgreSQL
2. creates the project if it does not exist
3. saves the uploaded file on disk
4. creates an `Asset` row in PostgreSQL for that file

This logic is handled across:

- `src/routes/data.py`
- `src/models/ProjectModel.py`
- `src/models/AssetModel.py`

#### Processing Flow

When a file is processed through:

- `POST /api/v1/data/process/{project_id}`

the application now:

1. reads uploaded files for the project
2. splits file content into chunks
3. creates `DataChunk` rows in PostgreSQL
4. links every chunk to both the project and the asset it came from

This is a major improvement over a loose document structure because the source of every chunk is now clearly traceable.

#### Indexing and RAG Flow

PostgreSQL now stores the structured metadata, but it does **not** replace the vector database in this project.

Important distinction:

- **PostgreSQL** stores projects, files, and text chunks
- **Qdrant** still stores vector embeddings used for semantic search

That means this project now uses:

- PostgreSQL for relational application data
- Qdrant for vector search

The indexing flow works like this:

1. chunks are read from PostgreSQL
2. embeddings are generated
3. embeddings are inserted into Qdrant
4. search queries retrieve relevant chunks for answer generation

This logic is mainly in:

- `src/controllers/NLPController.py`
- `src/routes/nlp.py`

### Configuration Changes

The old MongoDB environment settings were replaced by PostgreSQL settings in `src/helpers/config.py`.

The app now expects:

- `POSTGRES_USERNAME`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_MAIN_DATABASE`

The runtime connection string is built in `src/main.py` using:

```python
postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>
```

### Migration Files and Commands

Alembic configuration for this project lives in:

- `src/models/db_schemes/minirag/alembic.ini`
- `src/models/db_schemes/minirag/alembic/`

Typical commands are:

```bash
alembic current
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

Run those commands from:

```bash
src/models/db_schemes/minirag
```

### Benefits of This Migration

This move from MongoDB to PostgreSQL improves the project in several ways:

- data relationships are explicit and enforced
- schema changes can be tracked safely with Alembic
- application queries are clearer and easier to reason about
- file, project, and chunk records now have a more predictable lifecycle
- the codebase is easier to maintain for a team

### Important Notes

There are still a few legacy traces from the previous MongoDB approach in the repository:

- some old Mongo-related imports still exist in a few model files
- `docker/docker-compose.yml` still contains a `mongodb` service
- commented Mongo settings are still visible in `src/helpers/config.py`

So the migration is already reflected in the active application code, but some cleanup is still possible.

Also, this repository currently shows the **application-layer migration to PostgreSQL**, but it does not include a dedicated script that copies old MongoDB records into PostgreSQL automatically. If historical MongoDB data needs to be preserved, a one-time data migration script would still need to be written.

### In One Sentence

This project moved from a document-oriented MongoDB-style persistence layer to a relational PostgreSQL design, using SQLAlchemy for async database access and Alembic for safe, repeatable schema management, while keeping Qdrant as the vector store for RAG search.

## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)
