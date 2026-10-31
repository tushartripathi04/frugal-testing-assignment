# Q3 — Nested Shadow DOM Automation

## 1. Project Overview

This project demonstrates automated testing of web components containing nested Shadow DOM structures using Python, Playwright, HTML and JavaScript.

The implementation focuses on reliable element discovery across nested open Shadow DOM boundaries, dynamic CSS classes, accessibility-oriented automation and verification of public component behavior.

It also verifies the boundary of a closed Shadow DOM without attempting to directly access its internal elements.

## 2. Technologies Used

- Python
- Playwright
- Pytest
- HTML5
- JavaScript
- Shadow DOM
- Accessibility-oriented automation

## 3. Project Structure

```text
q3_shadow_dom/
├── index.html
├── shadow_utils.js
├── test_shadow_dom.py
├── accessibility_prompt.txt
└── README.md
```

## 4. Implementation Details

### A. Nested Open Shadow DOM Traversal

The implementation handles nested open Shadow DOM components.

Open Shadow DOM roots can be accessed through the browser's component structure, allowing automation to traverse multiple nested boundaries.

The automation uses the provided Shadow DOM utilities to locate and interact with the required elements.

### B. Dynamic CSS Class Handling

The implementation addresses components whose CSS classes may change dynamically.

The automation strategy avoids depending on unstable implementation-specific selectors.

### C. Closed Shadow DOM Boundary Verification

Closed Shadow DOM components restrict direct access to their internal shadow root.

The implementation respects this encapsulation boundary.

It does not attempt to directly access the internal button of a closed Shadow DOM component.

Instead, it verifies the public component event contract and checks the expected externally observable behavior.

### D. Public Component Event Validation

The test verifies that the component exposes the expected public interaction behavior.

This provides a way to validate functionality without depending on inaccessible internal implementation details.

### E. Accessibility-Oriented Automation

The project includes `accessibility_prompt.txt`, which defines an automation strategy that avoids relying on:

- Element IDs.
- XPath selectors.
- CSS tag selectors.
- Text matching.

The objective is to encourage more robust automation based on accessible and public component behavior.

## 5. Test Results

The project contains an automated Playwright test.

| Test scenario                       | Result           |
| ----------------------------------- | ---------------- |
| Nested Shadow DOM automation        | Passed           |
| Open Shadow DOM traversal           | Verified by test |
| Closed Shadow DOM boundary handling | Verified by test |
| Public component event validation   | Verified by test |

Verified execution:

```text
q3_shadow_dom/test_shadow_dom.py::test_nested_shadow_dom PASSED

========================= 1 passed =========================
```

Combined Q2 and Q3 test execution:

```text
========================= 4 passed in 15.52s =========================
```

## 6. Execution Instructions

### Step 1 — Install dependencies

```powershell
pip install playwright pytest
```

Install the Chromium browser:

```powershell
python -m playwright install chromium
```

### Step 2 — Navigate to the Q3 directory

```powershell
cd q3_shadow_dom
```

### Step 3 — Execute the automated test

```powershell
python -m pytest test_shadow_dom.py -v
```

Alternatively, from the repository root:

```powershell
python -m pytest q3_shadow_dom/test_shadow_dom.py -v
```

## 7. Important Technical Consideration

Open and closed Shadow DOM have different accessibility characteristics for automation.

Open Shadow DOM allows the automation to inspect its exposed shadow root and traverse nested components.

Closed Shadow DOM intentionally restricts direct access to internal implementation details.

This implementation respects that boundary and validates the component through its public event behavior rather than attempting to bypass encapsulation.

## 8. Conclusion

The implementation demonstrates nested open Shadow DOM traversal, handling of dynamic CSS classes, closed Shadow DOM boundary verification and public component event validation.

It emphasizes robust automation strategies while respecting web component encapsulation.
