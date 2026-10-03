from ollama import AsyncClient

from common.config import OLLAMA_HOST


class LLM:
    def __init__(self, model: str):
        self.model = model

        self.client = AsyncClient(
            host=OLLAMA_HOST
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> str:

        response = await self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.message.content.strip()