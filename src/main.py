from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()


async def startup_db_client():
    settings = get_settings()

    app.mongodb_conn = AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client = app.mongodb_conn[settings.MONGODB_DATABASE]

    LLMProviderFactory_instance = LLMProviderFactory(settings)
    # generation client
    app.gereation_client = LLMProviderFactory_instance.create(
        provider=settings.GENERATION_BACKEND
    )
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    # embedding client
    app.embedding_client = LLMProviderFactory_instance.create(
        provider=settings.EMBEDDING_BACKEND
    )
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID)


async def shutdown_db_client():
    app.mongodb_conn.close()


app.router.lifespan.onstartup.append(startup_db_client)
app.router.lifespan.onshutdown.append(shutdown_db_client)

app.include_router(base.baserouter)
app.include_router(data.data_router)
