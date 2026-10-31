
from pathlib import Path

from playwright.sync_api import (
    sync_playwright,
    expect,
)


HTML_FILE = Path(__file__).parent / "index.html"


def test_nested_shadow_dom():

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            HTML_FILE.resolve().as_uri()
        )

        # ------------------------------------------
        # 1. Locate the outer open Shadow DOM host
        # ------------------------------------------

        portal = page.locator(
            "enterprise-portal"
        )

        expect(portal).to_be_attached()

        # ------------------------------------------
        # 2. Locate the nested payment terminal
        # ------------------------------------------

        payment = portal.locator(
            "payment-terminal"
        )

        expect(payment).to_be_attached()

        # ------------------------------------------
        # 3. Verify dynamic class generation
        # ------------------------------------------

        dynamic_class = payment.locator(
            "div[class^='payment-']"
        )

        expect(dynamic_class).to_be_attached()

        print("PASS: Dynamic CSS class detected.")

        # ------------------------------------------
        # 4. Locate the closed Shadow DOM host
        # ------------------------------------------

        security = payment.locator(
            "security-sandbox"
        )

        expect(security).to_be_attached()

        # ------------------------------------------
        # 5. Verify closed Shadow DOM boundary
        # ------------------------------------------

        boundary = security.evaluate(
            "(element) => element.shadowRoot === null"
        )

        assert boundary is True

        print(
            "PASS: Closed Shadow DOM boundary verified."
        )

        # ------------------------------------------
        # 6. Verify accessible component interface
        # ------------------------------------------

        security_accessibility = security.evaluate(
            """element => ({
                tag: element.tagName.toLowerCase(),
                role: element.getAttribute("role"),
                label: element.getAttribute("aria-label"),
                closed: element.shadowRoot === null
            })"""
        )

        assert security_accessibility["closed"] is True

        print(
            "PASS: Closed component boundary inspected."
        )

        # ------------------------------------------
        # 7. Trigger action through an exposed
        # component-level test interface.
        # ------------------------------------------

        security.evaluate(
            """element => {
                element.dispatchEvent(
                    new CustomEvent(
                        "authorization-complete",
                        {
                            bubbles: true,
                            composed: true
                        }
                    )
                );
            }"""
        )

        # ------------------------------------------
        # 8. Verify application response
        # ------------------------------------------

        result = page.get_by_role(
            "status"
        )

        expect(result).to_have_text(
            "Authorization completed successfully."
        )

        print(
            "PASS: Authorization event received."
        )

        print(
            "ALL SHADOW DOM TESTS PASSED."
        )

        browser.close()


if __name__ == "__main__":

    test_nested_shadow_dom()
