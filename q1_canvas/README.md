# Q1 — Dynamic Canvas Automation and WebSocket Testing

## 1. Project Overview

This project demonstrates automated testing of a dynamically updated HTML5 Canvas application using Python, FastAPI, WebSockets and Playwright.

A WebSocket interception proxy forwards messages between the browser and backend while introducing Fibonacci-based dynamic delays. The implementation simulates asynchronous network conditions and validates dynamic Canvas interactions.

## 2. Technologies Used

- Python
- FastAPI
- WebSockets
- Playwright
- HTML5 Canvas
- JavaScript
- asyncio

## 3. Project Structure

```text
q1_canvas/
├── server.py
├── proxy.py
├── index.html
├── test_canvas.py
├── README.md
└── evidence/
    └── q1_complete_execution.png
```

## 4. Implementation Details

### A. FastAPI WebSocket Server

The FastAPI server generates continuously changing Canvas state messages containing:

- Sequence number.
- Loading or active status.
- Dynamic X and Y coordinates.
- Balance value.
- Microsecond timestamp.

### B. WebSocket Interception Proxy

The proxy forwards messages between the browser and backend while introducing Fibonacci-based delays.

The implemented sequence is:

| Fibonacci number |   Delay |
| ---------------- | ------: |
| 1                | 1000 ms |
| 1                | 1000 ms |
| 2                | 2000 ms |
| 3                | 3000 ms |
| 5                | 5000 ms |
| 8                | 8000 ms |

The proxy also supports a corruption mode that injects an invalid mathematical balance value:

```text
1e+7
```

### C. Dynamic Canvas Detection

Playwright uses JavaScript `requestAnimationFrame` to inspect Canvas pixel data.

The automation:

1. Reads the Canvas pixel state.
2. Identifies the active green target using its RGB color.
3. Checks consecutive frames for stable pixel state.
4. Determines the target's current coordinates.

### D. Automated Interaction

After successful pixel validation, the automation performs:

1. Hover over the detected target.
2. Drag horizontally by 15 pixels.
3. Click the updated target position.
4. Verify the successful interaction message.

The test also measures the time between pixel validation and the first hover command.

### E. Structured Error Handling

The application validates incoming balance values and rejects invalid scientific notation.

The corrupted mathematical value `1e+7` is rejected using the structured error code:

```text
INVALID_BALANCE
```

### F. Circuit Breaker

A circuit breaker prevents repeated failed interaction attempts from continuing indefinitely.

## 5. Test Results

| Test scenario                 | Result |
| ----------------------------- | ------ |
| WebSocket communication       | Passed |
| Fibonacci delay injection     | Passed |
| Active pixel detection        | Passed |
| Stable frame validation       | Passed |
| Hover timing                  | Passed |
| 15-pixel drag                 | Passed |
| Target click                  | Passed |
| Corrupted balance rejection   | Passed |
| Structured exception handling | Passed |

### Recorded Execution Evidence

- Pixel-to-hover latency: 20.22 ms.
- Drag distance: 15 pixels.
- Normal Canvas interaction: Passed.
- Corrupted mathematical state: Passed.

Screenshot:

`evidence/q1_complete_execution.png`

## 6. Execution Instructions

Install dependencies:

```powershell
pip install fastapi "uvicorn[standard]" websockets playwright
python -m playwright install chromium
```

Open three separate terminals.

**Terminal 1 — Start FastAPI server**

```powershell
cd q1_canvas
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Start WebSocket proxy**

```powershell
cd q1_canvas
python proxy.py
```

**Terminal 3 — Run the automated test**

```powershell
cd q1_canvas
python test_canvas.py
```

Use the project root's virtual environment when running these commands.

## 7. Limitations

- The backend uses a simulated WebSocket data stream.
- The proxy and server are intended for local testing.
- The circuit breaker stops repeated failed interaction attempts.
- The implementation demonstrates the specified interaction and corruption scenarios; it does not establish reliability under every possible browser, network or rendering condition.

## 8. Conclusion

The implementation demonstrates dynamic WebSocket interception, Fibonacci-based latency injection, pixel-based Canvas state detection, chained mouse interactions and structured rejection of corrupted mathematical data.
