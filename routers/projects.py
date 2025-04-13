# MIT License
#
# Copyright (c) 2025 Steffen PFendtner (https://github.com/StuttgartNerd)
#
# This file is part of the Redmine API Bridge project.
# For licensing information, please refer to the LICENSE file.
from fastapi import APIRouter, Request, HTTPException
import requests
import os

router = APIRouter()

# Retrieve the Redmine base URL from an environment variable.
REDMINE_URL = os.getenv("REDMINE_URL", "https://redmine.example.com")


@router.get("/")
async def list_projects(request: Request):
    """
    Retrieve a list of projects from Redmine.

    The request must include the 'X-Redmine-API-Key' header.
    """
    # Extract the Redmine API key from the request header.
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    # Prepare headers for the outgoing GET request to Redmine.
    headers = {
        "X-Redmine-API-Key": redmine_api_key,
    }

    # Construct the URL for listing projects.
    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/projects.json"

    try:
        response = requests.get(redmine_endpoint, headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to Redmine: {str(e)}"
        )

    if response.status_code >= 400:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Redmine API error: {error_detail}"
        )

    try:
        return response.json()
    except Exception:
        return {"result": "Projects retrieved successfully, but response could not be parsed as JSON."}


@router.get("/{project_id}")
async def get_project(project_id: int, request: Request):
    """
    Retrieve details for a specific project from Redmine.

    - **project_id**: The unique identifier of the project.
    - The request must include the 'X-Redmine-API-Key' header.
    """
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    headers = {
        "X-Redmine-API-Key": redmine_api_key,
    }

    # Construct the URL for retrieving the specified project.
    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/projects/{project_id}.json"

    try:
        response = requests.get(redmine_endpoint, headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to Redmine: {str(e)}"
        )

    if response.status_code >= 400:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Redmine API error: {error_detail}"
        )

    try:
        return response.json()
    except Exception:
        return {"result": "Project retrieved successfully, but response could not be parsed as JSON."}
