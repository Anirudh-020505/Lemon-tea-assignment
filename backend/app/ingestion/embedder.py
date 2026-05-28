from typing import List
from openai import AsyncOpenAI
from app.config import get_settings

class Embedder:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        self.model = settings.embedding_model

    async def embed_text(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            input=[text],
            model=self.model,
            dimensions=1536
        )
        return response.data[0].embedding

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        response = await self.client.embeddings.create(
            input=texts,
            model=self.model,
            dimensions=1536
        )
        return [data.embedding for data in response.data]
