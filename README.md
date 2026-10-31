# Frugal Testing — AI-Native Software Engineer Intern Assignment

**Candidate:** Tushar Tripathi

This repository contains my practical implementations for the Frugal Testing AI-Native Software Engineer Intern assignment.

The project demonstrates browser automation, cryptographic API replay protection, and automation across nested Shadow DOM components.

## Technology Stack

- Python 3.14.2
- FastAPI
- Playwright
- Pytest
- Requests
- WebSockets
- HTML, CSS and JavaScript

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
│   └── Readme.md
│
├── .gitignore
└── README.md
```

## Implemented Assignments

### Q1 — Dynamic Canvas Automation

Implemented using FastAPI, WebSockets, Python and Playwright.

Key features:

- WebSocket message interception.
- Fibonacci-based dynamic delays.
- Active pixel detection using requestAnimationFrame.
- Hover, drag and click automation.
- Circuit breaker for repeated failures.
- Corrupted mathematical state validation.

### Q2 — API Transaction Replay Protection

Implemented using FastAPI, Python, Requests and HMAC-SHA512.

Key features:

- Transaction creation and authentication.
- Server-generated challenge tokens.
- Timestamp and salt validation.
- HMAC-SHA512 request authentication.
- Duplicate request replay detection.
- Invalid signature rejection.
- Expired timestamp rejection.

**Automated tests:** 3 passed.

### Q3 — Nested Shadow DOM Automation

Implemented using HTML, JavaScript and Playwright.

Key features:

- Nested open Shadow DOM traversal.
- Dynamic CSS class handling.
- Closed Shadow DOM boundary verification.
- Public component event validation.
- Accessibility-oriented automation.

**Automated tests:** 1 passed.

## Verification

The combined test suite was executed successfully:

```text
q2_api_replay/test_replay.py::test_replay_protection PASSED
q2_api_replay/test_replay.py::test_invalid_signature PASSED
q2_api_replay/test_replay.py::test_expired_timestamp PASSED

q3_shadow_dom/test_shadow_dom.py::test_nested_shadow_dom PASSED

4 passed in 15.52s
```

Q1 was also implemented and tested separately.

## Running the Project

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install fastapi uvicorn playwright pytest requests websockets
playwright install chromium
```

Run individual assignment tests:

```powershell
python -m pytest q2_api_replay/test_replay.py -v
python -m pytest q3_shadow_dom/test_shadow_dom.py -v
```

For Q2, start the server from its directory:

```powershell
cd q2_api_replay
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

Run the tests in a second terminal.

Refer to the individual README files for Q1, Q2 and Q3 setup and execution instructions.

## Evidence

Screenshots and demonstration videos will be organized in the respective assignment folders as they are finalized.

## AI Assistance Disclosure

AI tools were used for development assistance, debugging, code review and documentation. The implementations were tested locally, and the results are documented in the respective assignment folders.

## Author

**Tushar Tripathi**

GitHub: https://github.com/tushartripathi04
