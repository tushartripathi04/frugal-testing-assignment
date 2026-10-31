# Frugal Testing — AI-Native Software Engineer Intern Assignment

**Candidate:** Tushar Tripathi

This repository contains my practical implementations for the Frugal Testing AI-Native Software Engineer Intern assignment.

The project demonstrates three software testing challenges involving dynamic browser automation, cryptographic API security, and nested Shadow DOM automation.

## Technology Stack

- Python 3.14.2
- FastAPI
- Playwright
- Pytest
- Requests
- WebSockets
- HTML5 Canvas
- HTML, CSS and JavaScript
- HMAC-SHA512

## Project Structure

```text
frugal-testing-assignment/
│
├── q1_canvas/
│   ├── index.html
│   ├── proxy.py
│   ├── server.py
│   ├── test_canvas.py
│   ├── README.md
│   └── evidence/
│
├── q2_api_replay/
│   ├── server.py
│   ├── test_replay.py
│   ├── README.md
│   └── q2_test_result.png
│
├── q3_shadow_dom/
│   ├── index.html
│   ├── shadow_utils.js
│   ├── test_shadow_dom.py
│   ├── accessibility_prompt.txt
│   └── README.md
│
├── .gitignore
└── README.md
```

## Assignment Implementations

### Q1 — Dynamic Canvas Automation

**Technologies:** Python, FastAPI, WebSockets, Playwright and JavaScript.

Implemented features:

- WebSocket message interception through a proxy.
- Fibonacci-based dynamic delays: 1, 1, 2, 3, 5 and 8 seconds.
- Dynamic Canvas pixel detection using `requestAnimationFrame`.
- Stable pixel-state validation.
- Automated hover, 15-pixel horizontal drag and click.
- Circuit breaker for repeated failures.
- Corrupted mathematical state injection using scientific notation.
- Structured error handling with `INVALID_BALANCE`.

Recorded execution evidence:

- Pixel-to-hover latency: 20.22 ms.
- Drag distance: 15 pixels.
- Normal Canvas interaction: Passed.
- Corrupted mathematical state validation: Passed.

### Q2 — API Transaction Replay Protection

**Technologies:** Python, FastAPI, Requests, Pytest and HMAC-SHA512.

Implemented features:

- Transaction creation through a POST endpoint.
- Server-generated transaction challenge.
- Server timestamp and salt sequence.
- HMAC-SHA512 request authentication.
- Timestamp validation.
- One-time challenge validation.
- Duplicate request replay detection.
- HTTP 409 Conflict for duplicate replay.
- Invalid signature rejection.
- Expired timestamp rejection.

**Automated tests:** 3 passed.

### Q3 — Nested Shadow DOM Automation

**Technologies:** Python, Playwright, HTML and JavaScript.

Implemented features:

- Nested open Shadow DOM traversal.
- Dynamic CSS class detection.
- Closed Shadow DOM boundary verification.
- Public component event validation.
- Accessibility-oriented automation strategy.
- Automation approach that avoids reliance on IDs, XPath, CSS tags and text matching.

**Automated tests:** 1 passed.

## Test Verification

The combined Q2 and Q3 test suite was executed successfully.

```text
q2_api_replay/test_replay.py::test_replay_protection PASSED
q2_api_replay/test_replay.py::test_invalid_signature PASSED
q2_api_replay/test_replay.py::test_expired_timestamp PASSED

q3_shadow_dom/test_shadow_dom.py::test_nested_shadow_dom PASSED

========================= 4 passed in 15.52s =========================
```

Q1 was tested separately, with the execution evidence documented in its README.

## Installation and Setup

Create a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install fastapi "uvicorn[standard]" playwright pytest requests websockets
python -m playwright install chromium
```

## Running the Tests

From the repository root:

```powershell
python -m pytest q2_api_replay/test_replay.py -v
python -m pytest q3_shadow_dom/test_shadow_dom.py -v
```

To run the combined Q2 and Q3 tests:

```powershell
python -m pytest -v
```

### Running Q2 API Server

Open a terminal:

```powershell
cd q2_api_replay
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

Open another terminal to execute the Q2 tests.

The Q2 test configuration uses:

```text
http://127.0.0.1:8001
```

Refer to the individual README files for detailed execution instructions.

## Evidence and Demonstrations

Screenshots and workflow demonstration videos will be organized in the respective assignment folders as they are finalized.

## AI Assistance Disclosure

AI tools were used for development assistance, debugging, code review and documentation.

The implementations were executed and tested locally. Test results and implementation evidence are documented in the respective project directories.

## Author

**Tushar Tripathi**

GitHub: https://github.com/tushartripathi04
