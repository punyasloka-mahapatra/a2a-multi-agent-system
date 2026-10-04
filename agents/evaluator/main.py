from fastapi import FastAPI

from common.a2a import (
    A2ARequest,
    A2AResponse
)

from .agent import EvaluatorAgent


app = FastAPI(
    title="Evaluator Agent"
)

agent = EvaluatorAgent()


@app.get("/")
async def health():

    return {
        "agent": agent.name,
        "status": "running"
    }


@app.get("/.well-known/agent-card.json")
async def agent_card():

    return {
        "protocolVersion": "1.0.0",
        "name": "Evaluator Agent",
        "description":
            "Evaluates and improves agent responses.",
        "url":
            "http://localhost:8004/a2a",
        "preferredTransport": "JSONRPC",
        "skills": [
            {
                "id": "evaluate",
                "name": "Response Evaluation",
                "description":
                    "Evaluates response quality, "
                    "groundedness and policy compliance."
            }
        ]
    }


@app.post("/a2a")
async def a2a(
    request: A2ARequest
):

    result = await agent.process(
        request.params
    )

    return A2AResponse(
        id=request.id,
        result=result
    )