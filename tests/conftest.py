"""
Pytest configuration and fixtures for Playwright tests.
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session.

    If Playwright browsers are not installed, skip E2E tests with a clear message.
    """
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as exc:  # noqa: BLE001
                pytest.skip(
                    "Playwright browsers are not installed. Run: 'python -m playwright install chromium'",
                    allow_module_level=True,
                )
            else:
                try:
                    yield browser
                finally:
                    browser.close()
    except Exception:
        pytest.skip(
            "Playwright is not available in this environment.",
            allow_module_level=True,
        )


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a browser context for each test."""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a page for each test."""
    page = context.new_page()
    yield page
    page.close()
