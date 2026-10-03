from fastapi import FastAPI

from common.a2a import (
    A2AMessage,
    A2ARequest,
    A2AResponse
)

from .agent import ClassifierAgent


app = FastAPI(
    title="Classifier Agent"
)

agent = ClassifierAgent()


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
        "name": "Classifier Agent",
        "description": (
            "Classifies customer support complaints."
        ),
        "url": "http://localhost:8001/a2a",
        "preferredTransport": "JSONRPC",
        "skills": [
            {
                "id": "classify_complaint",
                "name": "Complaint Classification",
                "description": (
                    "Classifies customer complaints."
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