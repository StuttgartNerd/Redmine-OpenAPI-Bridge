# Redmine API Bridge

A FastAPI-based REST API wrapper for interfacing with a Redmine instance. This bridge is designed to be used with ChatGPT Custom GPTs by forwarding an API key (provided via a custom authentication header) directly from ChatGPT to Redmine without storing it locally.

## Overview

This project acts as a proxy between ChatGPT and Redmine, exposing endpoints for:

- Tickets: Create, retrieve, and search for tickets.
- Projects: List projects and get project details.
- Users: List users and get user details.

The FastAPI application automatically generates an OpenAPI schema (with a dynamic `servers` entry taken from an environment variable) that enables ChatGPT to understand and interact with the API.

## Features

- API Key Pass-Through via `X-Redmine-API-Key` header.
- Ticket, project, and user operations supported.
- Dynamic OpenAPI schema with `servers` from environment.
- Easy integration with ChatGPT Custom GPTs.

## Installation

1. Clone the Repository:
```sh
   git clone https://github.com/StuttgartNerd/Redmine-OpenAPI-Bridge.git
   cd Redmine-OpenAPI-Bridge.git
```

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install fastapi uvicorn requests

## Environment Variables

- `REDMINE_URL`: Base URL of your Redmine instance.
- `PUBLIC_URL`: Public URL of this bridge (used in the OpenAPI schema).

## Running

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Example curl Usage - Test

Create Ticket:

```sh
curl -X POST http://localhost:8000/tickets/create \\
     -H "Content-Type: application/json" \\
     -H "X-Redmine-API-Key: YOUR_KEY" \\
     -d '{"project_id":1,"subject":"Example Ticket","description":"From API"}'
```

Get Ticket:

```sh
curl http://localhost:8000/tickets/1 \\
     -H "X-Redmine-API-Key: YOUR_KEY"
```

## ChatGPT Custom GPT Integration

1. Put the bridge on to a public domain or IP address or use a service like ngrok.com (for testing only!)
2. Use the OpenAPI URL of your deployed API (e.g. https://yourdomain.com/openapi.json).
3. Set up Custom Authentication:
   - Header name: `X-Redmine-API-Key`
   - Header value: your Redmine API key

## License

MIT License
