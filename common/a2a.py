from typing import Any

import httpx
from pydantic import BaseModel


class A2AMessage(BaseModel):
    task_id: str
    sender: str
    receiver: str
    message_type: str
    payload: Any


class A2ARequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str = "message/send"
    params: A2AMessage


class A2AResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Any


async def send_message(
    url: str,
    message: A2AMessage
) -> Any:

    request = A2ARequest(
        id=message.task_id,
        params=message
    )

    async with httpx.AsyncClient(timeout=120) as client:

        response = await client.post(
            f"{url}/a2a",
            json=request.model_dump()
        )

        response.raise_for_status()

        data = response.json()

        return data["result"]