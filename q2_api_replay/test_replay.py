
import hashlib
import hmac
import json
import os
import time

import requests


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_URL = "http://127.0.0.1:8001"

SECRET_KEY = os.getenv(
    "FRUGAL_TEST_SECRET",
    "local-assignment-demo-secret-change-me",
).encode("utf-8")


# --------------------------------------------------
# HMAC-SHA512 GENERATOR
# --------------------------------------------------

def make_signature(
    raw_body,
    client_timestamp,
    salt,
    challenge,
    server_timestamp,
):

    canonical_message = b"\n".join([
        raw_body,
        client_timestamp.encode("utf-8"),
        salt.encode("utf-8"),
        challenge.encode("utf-8"),
        server_timestamp.encode("utf-8"),
    ])

    return hmac.new(
        SECRET_KEY,
        canonical_message,
        hashlib.sha512,
    ).hexdigest()


# --------------------------------------------------
# CREATE TRANSACTION HELPER
# --------------------------------------------------

def create_test_transaction():

    response = requests.post(
        f"{BASE_URL}/transactions",
        timeout=5,
    )

    assert response.status_code == 201, response.text

    transaction_id = response.headers["X-Transaction-ID"]
    challenge = response.headers["X-Frugal-Challenge"]
    server_timestamp = response.headers["X-Server-Timestamp"]
    salt = response.headers["X-Salt-Sequence"]

    return (
        transaction_id,
        challenge,
        server_timestamp,
        salt,
    )


# --------------------------------------------------
# PREPARE SIGNED REQUEST
# --------------------------------------------------

def prepare_signed_request(
    challenge,
    server_timestamp,
    salt,
    timestamp=None,
):

    payload = {
        "amount": 1250.50,
        "currency": "INR",
        "description": "Frugal Testing API security test",
    }

    raw_body = json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")

    if timestamp is None:
        timestamp = str(time.time_ns() // 1000)

    signature = make_signature(
        raw_body,
        timestamp,
        salt,
        challenge,
        server_timestamp,
    )

    headers = {
        "Content-Type": "application/json",
        "X-Client-Timestamp": timestamp,
        "X-Frugal-Mac": signature,
    }

    return raw_body, headers


# --------------------------------------------------
# TEST 1: SUCCESSFUL UPDATE AND REPLAY ATTACK
# --------------------------------------------------

def test_replay_protection():

    print("\nTEST 1: Cryptographic replay protection")

    # Step 1: Create transaction.
    (
        transaction_id,
        challenge,
        server_timestamp,
        salt,
    ) = create_test_transaction()

    print("Transaction created:", transaction_id)

    # Step 2: Generate signed payload.
    raw_body, headers = prepare_signed_request(
        challenge,
        server_timestamp,
        salt,
    )

    # Step 3: Send original PUT request.
    first_response = requests.put(
        f"{BASE_URL}/transactions/{transaction_id}",
        data=raw_body,
        headers=headers,
        timeout=5,
    )

    assert first_response.status_code == 200, (
        first_response.text
    )

    print("Original request accepted: HTTP 200")

    # Capture the exact completion time of the first request.
    first_completed_at = time.perf_counter()

    # Step 4: Immediately resend the exact same request.
    replay_start = time.perf_counter()

    replay_response = requests.put(
        f"{BASE_URL}/transactions/{transaction_id}",
        data=raw_body,
        headers=headers,
        timeout=5,
    )

    replay_delay_ms = (
        replay_start - first_completed_at
    ) * 1000

    print(
        f"Replay initiated after: {replay_delay_ms:.3f} ms"
    )

    assert replay_delay_ms <= 150, (
        f"Replay timing exceeded 150 ms: {replay_delay_ms:.3f}"
    )

    # Step 5: Verify replay rejection.
    assert replay_response.status_code == 409, (
        "HIGH-RISK SECURITY ALERT: Replay was accepted! "
        f"Response: {replay_response.text}"
    )

    print("Replay rejected: HTTP 409")
    print("PASS: Replay protection verified.")


# --------------------------------------------------
# TEST 2: INVALID HMAC SIGNATURE
# --------------------------------------------------

def test_invalid_signature():

    print("\nTEST 2: Invalid signature validation")

    (
        transaction_id,
        challenge,
        server_timestamp,
        salt,
    ) = create_test_transaction()

    raw_body, headers = prepare_signed_request(
        challenge,
        server_timestamp,
        salt,
    )

    # Replace the correct signature with an invalid one.
    headers["X-Frugal-Mac"] = "invalid_signature"

    response = requests.put(
        f"{BASE_URL}/transactions/{transaction_id}",
        data=raw_body,
        headers=headers,
        timeout=5,
    )

    assert response.status_code == 401, response.text

    print("Invalid signature rejected: HTTP 401")
    print("PASS: HMAC validation verified.")


# --------------------------------------------------
# TEST 3: EXPIRED TIMESTAMP
# --------------------------------------------------

def test_expired_timestamp():

    print("\nTEST 3: Expired timestamp validation")

    (
        transaction_id,
        challenge,
        server_timestamp,
        salt,
    ) = create_test_transaction()

    # Generate a timestamp older than 60 seconds.
    expired_timestamp = str(
        (time.time_ns() // 1000) - 120_000_000
    )

    raw_body, headers = prepare_signed_request(
        challenge,
        server_timestamp,
        salt,
        timestamp=expired_timestamp,
    )

    response = requests.put(
        f"{BASE_URL}/transactions/{transaction_id}",
        data=raw_body,
        headers=headers,
        timeout=5,
    )

    assert response.status_code == 422, response.text

    print("Expired timestamp rejected: HTTP 422")
    print("PASS: Timestamp validation verified.")


# --------------------------------------------------
# RUN TESTS USING PYTEST
# --------------------------------------------------
