import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5500/app"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def _guardar_screenshot(driver, nombre_test: str, outcome: str):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{nombre_test}_{outcome}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("driver", None)
        if driver is None:
            return

        screenshot_path = _guardar_screenshot(driver, item.name, rep.outcome)

        extra = getattr(rep, "extra", [])
        try:
            from pytest_html import extras
            extra.append(extras.image(screenshot_path))
            rep.extra = extra
        except ImportError:
            pass
