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

# Retrieve the Redmine base URL from environment variables.
REDMINE_URL = os.getenv("REDMINE_URL", "https://redmine.example.com")


@router.get("/")
async def list_users(request: Request):
    """
    Retrieve a list of users from Redmine.

    The request must include the 'X-Redmine-API-Key' header.
    """
    # Extract the Redmine API key from the request header.
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    headers = {"X-Redmine-API-Key": redmine_api_key}
    # Construct the URL for listing users.
    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/users.json"

    try:
        response = requests.get(redmine_endpoint, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Redmine: {str(e)}")

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
        return {"result": "Users retrieved successfully, but response could not be parsed as JSON."}


@router.get("/{user_id}")
async def get_user(user_id: int, request: Request):
    """
    Retrieve details for a specific user from Redmine.

    The request must include the 'X-Redmine-API-Key' header.
    """
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    headers = {"X-Redmine-API-Key": redmine_api_key}
    # Construct the URL for retrieving the specified user.
    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/users/{user_id}.json"

    try:
        response = requests.get(redmine_endpoint, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Redmine: {str(e)}")

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
        return {"result": "User retrieved successfully, but response could not be parsed as JSON."}
