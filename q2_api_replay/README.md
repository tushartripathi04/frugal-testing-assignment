# Q2 — API Transaction Replay Protection and HMAC Validation

## 1. Project Overview

This project demonstrates secure API transaction creation, authenticated transaction updates, timestamp validation and replay-attack prevention using Python and FastAPI.

A local mock API server simulates transaction workflows and implements cryptographic security controls to prevent unauthorized and duplicate requests.

## 2. Technologies Used

- Python 3.14.2
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
├── README.md
└── q2_test_result.png
```

## 4. API Implementation

### A. Transaction Creation

The POST endpoint creates a new transaction and returns the information required for subsequent authentication:

- Transaction ID.
- Server-generated challenge token.
- Server timestamp.
- Salt sequence.

### B. Authenticated Transaction Update

The PUT endpoint validates transaction updates using:

- HMAC-SHA512 signature verification.
- Transaction request body.
- Server challenge token.
- Timestamp validation.
- One-time challenge validation.

The server verifies the request authentication before accepting the transaction update.

### C. Cryptographic Replay Protection

The implementation prevents duplicate transaction updates.

After a valid transaction update, the test attempts to submit the same authenticated request again.

The server detects the previously used challenge and rejects the duplicate request with:

```text
HTTP 409 Conflict
```

### D. Invalid Signature Validation

The test submits a request containing an invalid HMAC signature.

The server rejects the request instead of accepting an unauthenticated transaction update.

### E. Expired Timestamp Validation

The implementation checks request timestamps to prevent the acceptance of expired authentication requests.

Requests containing timestamps outside the permitted validity window are rejected.

## 5. Security Mechanisms

| Security mechanism   | Purpose                                 |
| -------------------- | --------------------------------------- |
| HMAC-SHA512          | Request authentication                  |
| Challenge token      | One-time transaction validation         |
| Timestamp validation | Reject expired requests                 |
| Salt sequence        | Additional request authentication input |
| Replay detection     | Prevent duplicate transaction updates   |
| HTTP 409             | Identify duplicate replay attempts      |

## 6. Automated Test Results

The Q2 test suite contains three automated tests.

| Test                            | Result |
| ------------------------------- | ------ |
| Cryptographic replay protection | Passed |
| Invalid signature validation    | Passed |
| Expired timestamp validation    | Passed |

Verified execution:

```text
test_replay_protection PASSED
test_invalid_signature PASSED
test_expired_timestamp PASSED

========================= 3 passed =========================
```

The combined Q2 and Q3 test execution also completed successfully:

```text
4 passed in 15.52s
```

## 7. Execution Instructions

### Step 1 — Install dependencies

```powershell
pip install fastapi "uvicorn[standard]" requests pytest
```

### Step 2 — Start the FastAPI server

Open the first terminal:

```powershell
cd q2_api_replay
```

Start the server on port 8001:

```powershell
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

Expected server address:

```text
http://127.0.0.1:8001
```

### Step 3 — Open API documentation

Open:

```text
http://127.0.0.1:8001/docs
```

The application exposes:

| Method | Endpoint                         | Description                      |
| ------ | -------------------------------- | -------------------------------- |
| POST   | `/transactions`                  | Create transaction               |
| PUT    | `/transactions/{transaction_id}` | Update authenticated transaction |
| GET    | `/health`                        | Health check                     |

### Step 4 — Run automated tests

Open a second terminal and navigate to the project root.

Execute:

```powershell
python -m pytest q2_api_replay/test_replay.py -v
```

Alternatively, from inside the Q2 directory:

```powershell
python -m pytest -v
```

**Important:** Keep the Q2 server running while executing the tests. The test configuration uses:

```text
BASE_URL = http://127.0.0.1:8001
```

## 8. Limitations

- The implementation uses in-memory transaction and challenge storage.
- It is designed as a local testing demonstration.
- Production deployment would require persistent shared storage.
- Atomic replay protection would be required across multiple server instances.
- The implementation does not establish production-grade security certification.

## 9. Conclusion

The implementation demonstrates authenticated transaction updates, HMAC-SHA512 verification, timestamp validation, one-time challenge handling and prevention of duplicate API transaction updates through replay detection.
