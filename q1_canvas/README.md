# Q1 — Dynamic Canvas Automation and WebSocket Testing

## 1. Project Overview

This project demonstrates automated testing of a dynamically updated HTML Canvas application using Python, Playwright, FastAPI, and WebSockets.

A WebSocket proxy intercepts server messages and introduces Fibonacci-based dynamic delays to simulate asynchronous network conditions.

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
└── README.md
```

## 4. Implementation

### A. FastAPI WebSocket Server

The server generates continuously changing Canvas state messages containing:

- Sequence number
- Loading or active status
- Dynamic X and Y coordinates
- Balance value
- Microsecond timestamp

### B. WebSocket Interception Proxy

The proxy forwards messages between the browser and backend while introducing Fibonacci-based delays:

`1000 ms × Fibonacci sequence`, capped at 8000 ms.

The implemented delay sequence is 1, 1, 2, 3, 5, 8 seconds.

It also supports a corruption mode that injects an invalid mathematical balance value (`1e+7`).

### C. Dynamic Canvas Detection

Playwright uses JavaScript `requestAnimationFrame` to inspect Canvas pixel data.

The automation identifies the active green target by its RGB color and checks consecutive frames for stability.

### D. Chained Interaction

After pixel validation, the automation:

1. Hovers over the detected target.
2. Drags horizontally by 15 pixels.
3. Clicks the updated target position.
4. Verifies the successful interaction message.

The test measures the time from pixel validation to the first hover command.

### E. Structured Error Handling

The application validates incoming balance values and rejects invalid scientific notation.

The corrupted value `1e+7` is rejected with the structured error code `INVALID_BALANCE`.

## 5. Test Results

| Test | Result |
|---|---|
| WebSocket communication | Passed |
| Fibonacci delay injection | Passed |
| Active pixel detection | Passed |
| Stable frame validation | Passed |
| Hover timing | Passed |
| 15-pixel drag | Passed |
| Target click | Passed |
| Corrupted balance rejection | Passed |
| Structured exception handling | Passed |

### Recorded Execution Evidence

- Pixel-to-hover latency: 20.22 ms
- Drag distance: 15 pixels
- Normal Canvas interaction: Passed
- Corrupted mathematical state: Passed

## 6. Execution Instructions

Install dependencies:

```powershell
pip install fastapi "uvicorn[standard]" websockets playwright
python -m playwright install chromium
```

Terminal 1 — Start FastAPI:

```powershell
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

Terminal 2 — Start WebSocket proxy:

```powershell
python proxy.py
```

Terminal 3 — Run automated tests:

```powershell
python test_canvas.py
```

## 7. Limitations

- The backend uses a simulated WebSocket data stream.
- The proxy and server are intended for local testing.
- The circuit breaker stops repeated failed interaction attempts.
- The implementation demonstrates the specified interaction and corruption scenarios; it does not establish reliability under every possible browser, network, or rendering condition.

## 8. Conclusion

The implementation successfully demonstrates dynamic WebSocket interception, Fibonacci-based latency injection, pixel-based Canvas state detection, chained mouse interaction, and structured rejection of corrupted mathematical data.