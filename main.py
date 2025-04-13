#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2025 Steffen PFendtner (https://github.com/StuttgartNerd)
#
# This file is part of the Redmine API Bridge project.
# For licensing information, please refer to the LICENSE file.
import os

from fastapi import FastAPI
from routers import tickets, projects, users
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Redmine API Bridge",
    description="A simple FastAPI wrapper for Redmine ticket operations",
    version="1.0.0"
)

# Include routers from separate modules
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Override the OpenAPI generation to add the 'servers' entry and force version 3.1.0
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.1.0"  # Ensure the required version.
    # Get the public URL from the environment variable 'PUBLIC_URL'
    public_url = os.getenv("PUBLIC_URL", "https://default-url.example.com")
    openapi_schema["servers"] = [{"url": public_url}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
