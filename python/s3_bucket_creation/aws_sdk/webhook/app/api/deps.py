import base64
import hashlib
import hmac
from datetime import timedelta, timezone, datetime
from fastapi import Request, Header, HTTPException

from core.config import settings


async def verify_webhook(request: Request, x_port_timestamp: str = Header(), x_port_signature: str = Header()):
    try:
        body = await request.body()
        data = body if isinstance(body, str) else body.decode()
        to_sign = f"{x_port_timestamp}.{data}".encode()
        signature = hmac.new(settings.PORT_CLIENT_SECRET.encode(), to_sign, hashlib.sha256).digest()
        expected_sig = base64.b64encode(signature).decode()
        assert expected_sig == x_port_signature.split(",")[1]

        time_tolerance = timedelta(minutes=5)
        now = datetime.now(tz=timezone.utc)
        timestamp = datetime.fromtimestamp(float(x_port_timestamp) / 1000.0, tz=timezone.utc)
        assert (now - time_tolerance) <= timestamp <= (now + time_tolerance)
    except Exception:
        raise HTTPException(status_code=400, detail="x-port headers invalid")
