import os

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api-prod.nex-ad.com")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-mpnet-base-v2")

app = FastAPI(title="Nexad API Proxy Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model = SentenceTransformer(EMBEDDING_MODEL)
model.encode("Initialize the model to avoid cold start")


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
)
async def proxy(request: Request, path: str):
    # Get the target URL
    target_url = f"{BASE_URL}/{path}"

    # Get request headers
    headers = dict(request.headers.items())

    if request.headers.get("Content-Type") != "application/json":
        raise HTTPException(
            status_code=400, detail="Content-Type must be application/json"
        )

    body = await request.json()

    if path == "ad/request/v2":
        if "chatbot_context" in body:
            body["chatbot_context"]["use_embedding_conversation"] = True

            for conversation in body["chatbot_context"]["conversations"]:
                conversation["content_embedding"] = {
                    "model": EMBEDDING_MODEL,
                    "vector": model.encode(conversation["content"]).tolist(),
                }
                conversation.pop("content", None)

    # Remove headers that should not be forwarded
    headers.pop("host", None)
    headers.pop("content-length", None)

    try:
        # Create a client and send the request with configured timeouts
        async with httpx.AsyncClient(timeout=httpx.Timeout(30)) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                json=body,
                params=request.query_params,
            )

            # Filter out compression-related headers to avoid decompression issues
            response_headers = dict(response.headers)
            response_headers.pop("content-encoding", None)
            response_headers.pop("transfer-encoding", None)

            # Return the response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,
            )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504, detail="Request to upstream server timed out"
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with upstream server: {str(exc)}",
        )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
