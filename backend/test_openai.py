import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(".env")

async def test_openai():
    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    
    print("Testing OpenAI API...")
    try:
        response = await client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "gpt-5.5-2026-04-23"),
            messages=[{"role": "user", "content": "Say 'hello world'"}]
        )
        print("✅ OpenAI API is working!")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print("❌ OpenAI API failed!")
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(test_openai())
