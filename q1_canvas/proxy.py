
import asyncio
import json
import logging
from urllib.parse import urlparse, parse_qs

import websockets


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8766

UPSTREAM_URL = "ws://127.0.0.1:8000/ws"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("CanvasProxy")


# --------------------------------------------------
# FIBONACCI JITTER CONTROLLER
# --------------------------------------------------

class FibonacciJitter:

    def __init__(self):

        self.a = 1
        self.b = 1

    def next_delay(self):

        current = self.a

        self.a, self.b = (
            self.b,
            min(self.a + self.b, 8)
        )

        return min(current, 8) * 1.0


# --------------------------------------------------
# WEBSOCKET PROXY
# --------------------------------------------------

async def proxy_handler(browser):

    request_path = browser.request.path

    query = parse_qs(
        urlparse(request_path).query
    )

    corrupt_mode = (
        query.get("corrupt", ["0"])[0] == "1"
    )

    logger.info(
        "New browser connection. Corrupt mode=%s",
        corrupt_mode,
    )

    jitter = FibonacciJitter()

    async with websockets.connect(
        UPSTREAM_URL
    ) as upstream:

        async def browser_to_server():

            async for message in browser:

                await upstream.send(message)

        async def server_to_browser():

            corrupted = False

            async for message in upstream:

                # Calculate dynamic Fibonacci delay.
                delay = jitter.next_delay()

                logger.info(
                    "Injecting %.0f ms WebSocket delay",
                    delay * 1000,
                )

                await asyncio.sleep(delay)

                # Inject deliberately corrupted data.
                if corrupt_mode and not corrupted:

                    data = json.loads(message)

                    if data.get("status") == "active":

                        data["balance"] = "1e+7"

                        message = json.dumps(data)

                        corrupted = True

                        logger.warning(
                            "Injected corrupted balance: 1e+7"
                        )

                await browser.send(message)

        tasks = [
            asyncio.create_task(browser_to_server()),
            asyncio.create_task(server_to_browser()),
        ]

        try:

            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()

            await asyncio.gather(
                *pending,
                return_exceptions=True,
            )

            for task in done:
                exception = task.exception()

                if exception:
                    raise exception

        finally:

            for task in tasks:
                if not task.done():
                    task.cancel()


# --------------------------------------------------
# START PROXY
# --------------------------------------------------

async def main():

    logger.info(
        "Starting WebSocket proxy on %s:%s",
        PROXY_HOST,
        PROXY_PORT,
    )

    async with websockets.serve(
        proxy_handler,
        PROXY_HOST,
        PROXY_PORT,
        max_size=1024 * 1024,
    ):

        logger.info("WebSocket proxy running.")

        await asyncio.Future()


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Proxy stopped.")
