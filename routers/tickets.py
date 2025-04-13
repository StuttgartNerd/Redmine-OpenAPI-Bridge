# MIT License
#
# Copyright (c) 2025 Steffen PFendtner (https://github.com/StuttgartNerd)
#
# This file is part of the Redmine API Bridge project.
# For licensing information, please refer to the LICENSE file.
from fastapi import APIRouter, Request, HTTPException
import requests
import os
from models.ticket import TicketCreateRequest
from typing import Optional

router = APIRouter()

# Retrieve the Redmine base URL from an environment variable.
REDMINE_URL = os.getenv("REDMINE_URL", "https://redmine.example.com")

@router.post("/create")
async def create_ticket(request: Request, ticket: TicketCreateRequest):
    """
    Create a new ticket in Redmine by forwarding the API key received in the
    'X-Redmine-API-Key' header to the Redmine API.
    """
    # Extract the Redmine API key from the request header.
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    # Prepare headers for the outgoing request to Redmine.
    headers = {
        "X-Redmine-API-Key": redmine_api_key,
        "Content-Type": "application/json",
    }

    # Build the payload for the Redmine issue.
    issue_data = {
        "project_id": ticket.project_id,
        "subject": ticket.subject,
    }
    if ticket.description:
        issue_data["description"] = ticket.description
    if ticket.tracker_id is not None:
        issue_data["tracker_id"] = ticket.tracker_id
    if ticket.assigned_to_id is not None:
        issue_data["assigned_to_id"] = ticket.assigned_to_id

    # Redmine's REST API expects the issue information to be nested under "issue".
    payload = {"issue": issue_data}

    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/issues.json"

    try:
        response = requests.post(redmine_endpoint, json=payload, headers=headers)
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
        # Fallback in case Redmine does not return JSON.
        location = response.headers.get("Location")
        if location:
            new_id = location.rstrip('.json').split('/')[-1]
            return {"issue_id": int(new_id), "location": location}
        return {"result": "Issue created successfully"}


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int, request: Request):
    """
    Retrieve details for a specific ticket (issue) from Redmine.

    - **ticket_id**: The unique identifier of the ticket in Redmine.
    - The request must include the 'X-Redmine-API-Key' header with the appropriate API key.
    """
    # Extract the Redmine API key from the request header.
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    # Prepare the headers for the outgoing GET request to Redmine.
    headers = {
        "X-Redmine-API-Key": redmine_api_key,
    }

    # Construct the Redmine API endpoint for the specific ticket.
    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/issues/{ticket_id}.json"

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
        return {"result": "Ticket retrieved successfully, but response could not be parsed as JSON."}


@router.get("/search")
async def search_tickets(
        request: Request,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        project_id: Optional[int] = None
):
    """
    Search Redmine tickets with optional filters: status, assigned_to (user ID or 'me'),
    and project_id. Requires the 'X-Redmine-API-Key' header.
    """
    # Extract the Redmine API key from the request header.
    redmine_api_key = request.headers.get("X-Redmine-API-Key")
    if not redmine_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing 'X-Redmine-API-Key' header"
        )

    headers = {
        "X-Redmine-API-Key": redmine_api_key,
    }

    # Build query parameters for the search. Map our query names to what Redmine expects.
    params = {}
    if status:
        params["status_id"] = status  # Redmine supports special keywords or numeric IDs.
    if assigned_to:
        params["assigned_to_id"] = assigned_to
    if project_id is not None:
        params["project_id"] = project_id

    redmine_endpoint = f"{REDMINE_URL.rstrip('/')}/issues.json"

    try:
        response = requests.get(redmine_endpoint, headers=headers, params=params)
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
        return {"result": "Search completed, but response could not be parsed as JSON."}
