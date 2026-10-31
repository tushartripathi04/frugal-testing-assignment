# Q2 — API Transaction Replay and HMAC Validation

## 1. Project Overview

This project demonstrates API transaction creation, authenticated transaction updates, timestamp validation, and replay-attack prevention using Python and FastAPI.

A local mock API server is used to simulate transaction workflows and security controls.

## 2. Technologies Used

- Python
- FastAPI
- Requests
- Pytest
- HMAC-SHA512
- JSON
- Threading locks

## 3. Project Structure

```text
q2_api_replay/
├── server.py
├── test_replay.py
└── README.md
```

## 4. Implementation

### A. Transaction Creation

The POST endpoint creates a transaction and returns:

- Transaction ID
- Server challenge token
- Server timestamp
- Salt sequence

### B. Authenticated Transaction Update

The PUT endpoint validates the transaction update using:

- HMAC-SHA512 signature
- Raw transaction request body
- Server challenge token
- Timestamp validation
- One-time challenge validation

### C. Replay Attack Prevention

After a valid transaction update, the same request payload, timestamp, and MAC are replayed.

The server rejects the duplicate transaction update with HTTP 409 Conflict.

### D. Additional Security Tests

The test suite also checks invalid signatures and expired timestamps.

## 5. Test Results

| Test scenario | Result |
|---|---|
| Transaction creation | Passed |
| Valid authenticated update | Passed |
| Duplicate request replay | Passed |
| Invalid HMAC signature | Passed |
| Expired timestamp | Passed |

Recorded execution: 3 passed in 1.21 seconds.

## 6. Execution Instructions

Install dependencies:

```powershell
pip install fastapi "uvicorn[standard]" requests pytest
```

Start the API server:

```powershell
uvicorn server:app --host 127.0.0.1 --port 8000
```

Run tests in another terminal:

```powershell
pytest -v
```

## 7. Limitations

- The implementation uses in-memory transaction and challenge storage.
- It is designed as a local testing demonstration.
- Production deployment would require shared persistent storage and atomic replay protection across server instances.

## 8. Conclusion

The implementation demonstrates transaction authentication, HMAC-SHA512 verification, timestamp validation, and prevention of duplicate API transaction updates through replay detection.