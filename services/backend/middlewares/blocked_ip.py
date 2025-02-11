from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List
import ipaddress

class BlockedIPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, blocked_ips: List[str]):
        super().__init__(app)
        self.blocked_ips = [ipaddress.ip_network(ip, strict=False) for ip in blocked_ips]

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        print(client_ip)
        ip_obj = ipaddress.ip_address(client_ip)

        if any(ip_obj in blocked_ip for blocked_ip in self.blocked_ips):
            return JSONResponse(
                status_code=403,
                content={"detail": "Access forbidden from your IP address"}
            )

        response = await call_next(request)
        return response