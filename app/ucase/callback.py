from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import LLMResult
from typing import Any, Dict, List, Optional
import websockets

class OllamaCalbackHandler(AsyncCallbackHandler):
    def __init__(self, color: Optional[str] = None) -> None:
        self.color = color

    # async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
    #     """Run when LLM ends running."""
    #     print(f"response: {response.dict()['generations'][0][0]['text']}")
    
    # async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
    #     # print(token)
    #     # async with websockets.connect('ws://localhost:8081/ws') as websocket:
    #     #     try:
    #     #         await websocket.send(token)
    #     #     except websockets.exceptions.ConnectionClosedError:
    #     #         print("Connection closed with error")
    #     #     except websockets.exceptions.ConnectionClosedOK:
    #     #         print("Connection closed gracefully")
    #     #     except Exception as e:
    #     #         print("Error sending message:", e)
    #     #     except Exception as e:
    #     #         print(e)