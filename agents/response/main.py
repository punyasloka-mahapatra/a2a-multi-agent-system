from fastapi import FastAPI

from common.a2a import (
    A2AMessage,
    A2ARequest,
    A2AResponse
)

from .agent import ResponseAgent


app = FastAPI(
    title="Response Agent"
)

agent = ResponseAgent()


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
        "name": "Response Agent",
        "description": (
            "Generates final customer-facing responses."
        ),
        "url": "http://localhost:8003/a2a",
        "preferredTransport": "JSONRPC",
        "skills": [
            {
                "id": "generate_response",
                "name": "Customer Response Generation",
                "description": (
                    "Creates the final customer response."
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