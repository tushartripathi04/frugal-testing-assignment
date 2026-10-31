
/*
 * Frugal Testing
 * Shadow DOM Pathfinding Utilities
 *
 * Supports nested OPEN Shadow DOM roots.
 * Does not attempt to bypass CLOSED Shadow DOM.
 */

// --------------------------------------------------
// RECURSIVE OPEN SHADOW DOM TRAVERSAL
// --------------------------------------------------

function findElementInOpenShadowDOM(
    root,
    predicate
) {

    if (!root) {
        return null;
    }

    // Check elements in the current root.
    const elements = root.querySelectorAll("*");

    for (const element of elements) {

        if (predicate(element)) {
            return element;
        }

        // Recursively inspect nested open roots.
        if (element.shadowRoot) {

            const result = findElementInOpenShadowDOM(
                element.shadowRoot,
                predicate
            );

            if (result) {
                return result;
            }
        }
    }

    return null;
}


// --------------------------------------------------
// FIND ELEMENT USING ACCESSIBLE ATTRIBUTES
// --------------------------------------------------

function findByAccessibleLabel(label) {

    return findElementInOpenShadowDOM(
        document,
        element => {

            const ariaLabel =
                element.getAttribute("aria-label");

            const role =
                element.getAttribute("role");

            return (
                ariaLabel === label ||
                (role === "button" && ariaLabel === label)
            );

        }
    );
}


// --------------------------------------------------
// FIND SHADOW HOSTS
// --------------------------------------------------

function inspectShadowHosts(root = document) {

    const hosts = [];

    const elements = root.querySelectorAll("*");

    for (const element of elements) {

        if (element.shadowRoot) {

            hosts.push({
                host: element.tagName.toLowerCase(),
                mode: "open"
            });

            hosts.push(
                ...inspectShadowHosts(element.shadowRoot)
            );

        }

    }

    return hosts;
}


// --------------------------------------------------
// TEST CLOSED SHADOW ROOT BOUNDARY
// --------------------------------------------------

function checkClosedShadowBoundary() {

    const securityHost =
        findElementInOpenShadowDOM(
            document,
            element =>
                element.tagName.toLowerCase() ===
                "security-sandbox"
        );

    if (!securityHost) {
        return {
            found: false
        };
    }

    return {
        found: true,
        shadowRootAccessible:
            securityHost.shadowRoot !== null,
        boundary: "closed"
    };
}


// --------------------------------------------------
// EXPORT FUNCTIONS
// --------------------------------------------------

window.ShadowDOMUtils = {
    findElementInOpenShadowDOM,
    findByAccessibleLabel,
    inspectShadowHosts,
    checkClosedShadowBoundary
};
