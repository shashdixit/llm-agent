import httpx
import os
from ..utils.logger import logger

class LLMClient:
    def __init__(self):
        self.token = os.getenv("AIPROXY_TOKEN")
        self.api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        
    async def generate(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"LLM API error: {response.text}")
                    raise Exception(f"LLM API error: {response.text}")
                    
                return response.json()["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"Error in LLM client: {str(e)}")
            raise

    async def generate_vision(self, messages: list) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"LLM API error: {response.text}")
                    raise Exception(f"LLM API error: {response.text}")
                    
                return response.json()["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"Error in LLM vision client: {str(e)}")
            raise