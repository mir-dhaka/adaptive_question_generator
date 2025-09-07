import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import JSONResponse


class RequestTracerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id  # store it for access in routes/logs if needed

        # Process the request
        response: Response = await call_next(request)

        # Compute elapsed time
        elapsed = round((time.time() - start_time) * 1000, 2)

        # Add custom headers
        response.headers["X-Trace-Id"] = trace_id
        response.headers["X-Elapsed-Time"] = f"{elapsed}ms"

        # # Optionally inject trace_id into JSON body (if JSONResponse)
        # if response.headers.get("content-type", "").startswith("application/json"):
        #     if isinstance(response, JSONResponse):
        #         # Read and modify the response body
        #         payload = response.body.decode("utf-8")
        #         import json
        #         try:
        #             data = json.loads(payload)
        #             if isinstance(data, dict):
        #                 data["trace_id"] = trace_id
        #                 response = JSONResponse(content=data, status_code=response.status_code, headers=dict(response.headers))
        #         except Exception:
        #             pass  # fallback: leave body unchanged

        return response
