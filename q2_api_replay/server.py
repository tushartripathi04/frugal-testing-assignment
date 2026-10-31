
import hashlib
import hmac
import json
import os
import secrets
import time
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Request, Response


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="Frugal Testing - Replay Protection API",
    description="Cryptographic API authentication and replay protection",
    version="1.0.0",
)

SECRET_KEY = os.getenv(
    "FRUGAL_TEST_SECRET",
    "local-assignment-demo-secret-change-me",
).encode("utf-8")

# In-memory storage for this local demonstration.
transactions = {}
used_challenges = set()

# Protect shared state against concurrent requests.
state_lock = Lock()


# --------------------------------------------------
# HMAC-SHA512 SIGNATURE GENERATION
# --------------------------------------------------

def create_signature(
    raw_body: bytes,
    client_timestamp: str,
    salt: str,
    challenge: str,
    server_timestamp: str,
) -> str:

    canonical_message = b"\n".join([
        raw_body,
        client_timestamp.encode("utf-8"),
        salt.encode("utf-8"),
        challenge.encode("utf-8"),
        server_timestamp.encode("utf-8"),
    ])

    signature = hmac.new(
        SECRET_KEY,
        canonical_message,
        hashlib.sha512,
    ).hexdigest()

    return signature


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "Frugal Testing Replay API",
    }


# --------------------------------------------------
# STEP 1: CREATE TRANSACTION
# --------------------------------------------------

@app.post("/transactions", status_code=201)
def create_transaction(response: Response):

    transaction_id = str(uuid4())

    # Generate cryptographic challenge and salt.
    challenge = secrets.token_urlsafe(32)
    salt = secrets.token_hex(16)

    # Server timestamp in microseconds.
    server_timestamp = str(time.time_ns() // 1000)

    with state_lock:

        transactions[transaction_id] = {
            "challenge": challenge,
            "salt": salt,
            "server_timestamp": server_timestamp,
            "updated": False,
        }

    # Return dynamic values through HTTP response headers.
    response.headers["X-Transaction-ID"] = transaction_id
    response.headers["X-Frugal-Challenge"] = challenge
    response.headers["X-Server-Timestamp"] = server_timestamp
    response.headers["X-Salt-Sequence"] = salt

    return {
        "transaction_id": transaction_id,
        "status": "created",
        "message": "Transaction created successfully",
    }


# --------------------------------------------------
# STEP 2: UPDATE TRANSACTION
# --------------------------------------------------

@app.put("/transactions/{transaction_id}")
async def update_transaction(
    transaction_id: str,
    request: Request,
    x_frugal_mac: str = Header(...),
    x_client_timestamp: str = Header(...),
):

    # Read the original request bytes.
    raw_body = await request.body()

    # Validate JSON.
    try:
        payload = json.loads(raw_body)

    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        )

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=400,
            detail="JSON payload must be an object",
        )

    with state_lock:

        # Find transaction.
        transaction = transactions.get(transaction_id)

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found",
            )

        challenge = transaction["challenge"]

        # REPLAY PROTECTION.
        # A previously consumed challenge cannot be reused.
        if challenge in used_challenges:
            raise HTTPException(
                status_code=409,
                detail="Replay attack detected",
            )

        # Validate client timestamp.
        try:
            timestamp_value = int(x_client_timestamp)

        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid client timestamp",
            )

        current_timestamp = time.time_ns() // 1000

        # Reject timestamps older or newer than 60 seconds.
        if abs(current_timestamp - timestamp_value) > 60_000_000:
            raise HTTPException(
                status_code=422,
                detail="Timestamp expired or invalid",
            )

        # Calculate expected HMAC.
        expected_signature = create_signature(
            raw_body=raw_body,
            client_timestamp=x_client_timestamp,
            salt=transaction["salt"],
            challenge=challenge,
            server_timestamp=transaction["server_timestamp"],
        )

        # Secure constant-time signature comparison.
        if not hmac.compare_digest(
            expected_signature,
            x_frugal_mac,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid cryptographic signature",
            )

        # Consume challenge atomically.
        used_challenges.add(challenge)

        transaction["updated"] = True
        transaction["payload"] = payload

    return {
        "transaction_id": transaction_id,
        "status": "updated",
        "message": "Transaction updated successfully",
    }
