from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, settings

baserouter = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)
@baserouter.get("/")
async def welcome(app_settings: settings = Depends(get_settings)):
    #app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_Version

    return {
        "app_name": app_name,
        "app_version": app_version,
    }
