"""Vocabulary — all text constants used in the bot.

## Трассируемость
Feature: P001 — PRD-first платформа
"""


class Vocab:
    # --- Messages ---
    WELCOME_TEXT = (
        "Welcome to Genesis Studio!\n\n"
        "I help you create products through a PRD-first workflow:\n"
        "idea \u2192 discovery \u2192 features \u2192 PRD \u2192 UX \u2192 use cases \u2192 "
        "requirements \u2192 tests \u2192 code \u2192 GitHub \u2192 deploy\n\n"
        "Choose an action below:"
    )

    CREATE_PRODUCT_TEXT = "Let's create a new product!"

    DESCRIBE_IDEA_TEXT = (
        "Describe your product idea in detail.\n"
        "Tell me what problem it solves, who the users are, and what it should do."
    )

    IDEA_TOO_SHORT_TEXT = (
        "Please provide a more detailed description (at least 10 characters)."
    )

    PRODUCT_CREATED_TEXT = "Product draft created!"

    DISCOVERY_COMPLETE_TEXT = (
        "Discovery complete! Your product is ready for feature map generation.\n"
        "Use 'My Products' to continue."
    )

    ERROR_TEXT = "Error: {error}"

    # --- Reply-keyboard button labels ---
    BTN_CREATE_PRODUCT = "Create Product"
    BTN_MY_PRODUCTS = "My Products"
    BTN_HELP = "Help"

    # --- Inline-keyboard button labels (feature actions) ---
    BTN_GEN_PRD = "Generate PRD Draft"
    BTN_APPROVE_STORIES = "Approve Stories"
    BTN_GEN_UX = "Generate UX Preview"
    BTN_GEN_UC = "Generate Use Cases"
    BTN_GEN_REQ = "Generate Requirements"
    BTN_GEN_TESTS = "Generate Tests"
    BTN_GEN_CODE = "Generate Code"
    BTN_PUSH_GH = "Push to GitHub"
    BTN_DEPLOY = "Deploy Locally"
