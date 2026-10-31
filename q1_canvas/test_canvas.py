import asyncio
import time

from playwright.async_api import async_playwright


APP_URL = "http://127.0.0.1:8000"
GREEN_COLOR = (22, 163, 74)

DRAG_DISTANCE = 15
MAX_COORDINATE_DEVIATION = 40
MAX_INTERACTION_LATENCY_MS = 100
PIXEL_TIMEOUT_MS = 20000


class CircuitBreaker:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.failures = 0
        self.is_open = False

    def record_failure(self):
        self.failures += 1

        if self.failures >= self.threshold:
            self.is_open = True
            print("CIRCUIT BREAKER OPEN: Too many failures.")

    def record_success(self):
        self.failures = 0

    def allow_request(self):
        return not self.is_open


async def wait_for_active_pixel(page):
    """
    Detect the active green target using requestAnimationFrame.
    Require three consecutive stable pixel detections.
    """

    result = await page.evaluate(
        """async ({timeoutMs}) => {
            const canvas = document.querySelector("canvas");
            if (!canvas) {
                throw new Error("Canvas element not found");
            }

            const ctx = canvas.getContext("2d");
            const width = canvas.width;
            const height = canvas.height;

            const targetColor = [22, 163, 74];
            const start = performance.now();

            let previous = null;
            let stableFrames = 0;

            return await new Promise((resolve, reject) => {
                function scanFrame() {
                    if (performance.now() - start > timeoutMs) {
                        reject(new Error("Active pixel detection timed out"));
                        return;
                    }

                    const image = ctx.getImageData(
                        0, 0, width, height
                    );

                    let sumX = 0;
                    let sumY = 0;
                    let count = 0;

                    for (let y = 0; y < height; y++) {
                        for (let x = 0; x < width; x++) {
                            const i = (y * width + x) * 4;

                            if (
                                image.data[i] === targetColor[0] &&
                                image.data[i + 1] === targetColor[1] &&
                                image.data[i + 2] === targetColor[2] &&
                                image.data[i + 3] > 0
                            ) {
                                sumX += x;
                                sumY += y;
                                count++;
                            }
                        }
                    }

                    if (count > 20) {
                        const center = {
                            x: sumX / count,
                            y: sumY / count
                        };

                        if (previous) {
                            const drift = Math.hypot(
                                center.x - previous.x,
                                center.y - previous.y
                            );

                            if (drift <= 2) {
                                stableFrames++;
                            } else {
                                stableFrames = 0;
                            }
                        }

                        previous = center;

                        if (stableFrames >= 2) {
                            resolve({
                                x: center.x,
                                y: center.y,
                                validationTime: performance.now(),
                                stableFrames: stableFrames + 1
                            });
                            return;
                        }
                    } else {
                        previous = null;
                        stableFrames = 0;
                    }

                    requestAnimationFrame(scanFrame);
                }

                requestAnimationFrame(scanFrame);
            });
        }""",
        {"timeoutMs": PIXEL_TIMEOUT_MS},
    )

    print(
        f"Active pixel detected at "
        f"({result['x']:.1f}, {result['y']:.1f})"
    )

    return result


async def calculate_target_coordinates(page, pixel):
    """
    Convert Canvas pixel coordinates into browser viewport coordinates.
    """

    canvas = page.locator("canvas")
    box = await canvas.bounding_box()

    if not box:
        raise RuntimeError("Unable to obtain Canvas bounding box")

    dimensions = await canvas.evaluate(
        """element => ({
            width: element.width,
            height: element.height
        })"""
    )

    scale_x = box["width"] / dimensions["width"]
    scale_y = box["height"] / dimensions["height"]

    viewport_x = box["x"] + pixel["x"] * scale_x
    viewport_y = box["y"] + pixel["y"] * scale_y

    return {
        "x": viewport_x,
        "y": viewport_y,
        "canvas_box": box
    }


async def validate_coordinate_state(page, coordinates, pixel):
    """
    Reject coordinates outside the Canvas or too close to its boundary.
    """

    box = coordinates["canvas_box"]

    x = coordinates["x"]
    y = coordinates["y"]

    inside_canvas = (
        box["x"] <= x <= box["x"] + box["width"]
        and box["y"] <= y <= box["y"] + box["height"]
    )

    if not inside_canvas:
        raise RuntimeError("Detected target is outside the Canvas")

    margin = 25

    near_boundary = (
        x < box["x"] + margin
        or x > box["x"] + box["width"] - margin
        or y < box["y"] + margin
        or y > box["y"] + box["height"] - margin
    )

    if near_boundary:
        raise RuntimeError("Detected target is too close to Canvas boundary")

    if not all(
        isinstance(pixel[key], (int, float))
        for key in ("x", "y")
    ):
        raise RuntimeError("Invalid pixel coordinates")

    return True


async def perform_chained_interaction(page, breaker):
    """
    Detect, validate, hover, drag 15px horizontally, and click.
    """

    for attempt in range(1, 4):
        if not breaker.allow_request():
            raise RuntimeError("Circuit breaker is open")

        try:
            print(f"Detection attempt: {attempt}")

            pixel = await wait_for_active_pixel(page)

            coordinates = await calculate_target_coordinates(
                page, pixel
            )

            await validate_coordinate_state(
                page, coordinates, pixel
            )

            start_x = coordinates["x"]
            start_y = coordinates["y"]

            destination_x = start_x + DRAG_DISTANCE
            destination_y = start_y

            # Start timing immediately after pixel validation.
            validation_completed = time.perf_counter()

            # Hover over the detected target.
            await page.mouse.move(start_x, start_y)

            hover_latency_ms = (
                time.perf_counter() - validation_completed
            ) * 1000

            # Drag horizontally by exactly 15 pixels.
            await page.mouse.down()
            await page.mouse.move(
                destination_x,
                destination_y,
                steps=1
            )
            await page.mouse.up()

            # Click the new target position.
            await page.mouse.click(
                destination_x,
                destination_y
            )

            print(
                f"Pixel-to-hover latency: "
                f"{hover_latency_ms:.2f} ms"
            )

            print(
                f"Drag distance: {DRAG_DISTANCE} pixels"
            )

            if hover_latency_ms > MAX_INTERACTION_LATENCY_MS:
                raise RuntimeError(
                    "Hover started more than 100ms after validation"
                )

            await page.locator(
                "#interaction"
            ).get_by_text(
                "Target successfully clicked",
                exact=False
            ).wait_for(timeout=5000)
            print("PASS: Target was successfully clicked.")

            breaker.record_success()

            print("PASS: Hover, drag and click completed.")

            return

        except Exception as error:
            breaker.record_failure()

            print(f"Attempt {attempt} failed: {error}")

            if not breaker.allow_request():
                raise RuntimeError(
                    "Circuit breaker stopped further attempts"
                ) from error

    raise RuntimeError("All interaction attempts failed")


async def validate_corrupted_balance(page):
    """
    Verify that corrupted scientific notation is rejected
    at the structured exception boundary.
    """

    error_boundary = page.locator("#errorBoundary")

    await error_boundary.wait_for(
        state="visible",
        timeout=20000
    )

    await page.wait_for_function(
        """() => {
            const element = document.querySelector("#errorBoundary");
            return element &&
                   element.textContent.includes("INVALID_BALANCE");
        }""",
        timeout=20000
    )

    error_text = await error_boundary.inner_text()

    print("PASS: Corrupted balance was rejected.")
    print("Structured error:", error_text)


async def run_normal_canvas_test(browser):
    print("\\n========== NORMAL CANVAS TEST ==========")

    page = await browser.new_page()

    await page.goto(
        APP_URL,
        wait_until="domcontentloaded"
    )

    await page.locator("canvas").wait_for(
        state="visible",
        timeout=10000
    )

    breaker = CircuitBreaker(threshold=3)

    await perform_chained_interaction(page, breaker)

    status = await page.locator(
        "#interaction"
    ).inner_text()

    print("Interaction status:", status)

    await page.close()


async def run_corruption_test(browser):
    print("\\n========== CORRUPTION TEST ==========")

    page = await browser.new_page()

    await page.goto(
        APP_URL + "?corrupt=1",
        wait_until="domcontentloaded"
    )

    await validate_corrupted_balance(page)

    await page.close()


async def main():
    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=False
        )

        try:
            await run_normal_canvas_test(browser)
            await run_corruption_test(browser)

            print("\\n========== Q1 TEST SUMMARY ==========")
            print("Normal Canvas interaction: PASSED")
            print("Corrupted mathematical state: PASSED")
            print("Q1 automated test execution completed.")

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())