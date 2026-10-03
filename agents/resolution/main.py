from fastapi import FastAPI

from common.a2a import (
    A2AMessage,
    A2ARequest,
    A2AResponse
)

from .agent import ResolutionAgent


app = FastAPI(
    title="Resolution Agent"
)

agent = ResolutionAgent()


@app.get("/")
async def root():

    return {
        "agent": agent.name,
        "status": "running"
    }


@app.get("/.well-known/agent-card.json")
async def agent_card():

    return {
        "protocolVersion": "0.3.0",
        "name": "Resolution Agent",
        "description": (
            "Determines appropriate customer "
            "support resolutions."
        ),
        "url": "http://localhost:8002/a2a",
        "preferredTransport": "JSONRPC",
        "skills": [
            {
                "id": "resolve_complaint",
                "name": "Complaint Resolution",
                "description": (
                    "Determines the next support action."
                )
            }
        ]
    }


@app.post("/a2a")
async def a2a_endpoint(
    request: A2ARequest
):

    result = await agent.process(
        request.params
    )

    return A2AResponse(
        id=request.id,
        result=result
    )