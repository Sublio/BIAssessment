import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

MAIN_ENDPOINT = "https://www.britinsurance.com"


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get(MAIN_ENDPOINT)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    yield driver

    driver.quit()


def test_search_results(driver):
    time.sleep(2)
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[aria-label="Search button"]')
        )
    )
    search_button.click()

    time.sleep(1)
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='k']"))
    )
    search_input.send_keys("IFRS 17")

    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result"))
    )

    suggestions = [result.find_element(By.TAG_NAME, "a").text for result in results]

    expected_suggestions = [
        "Financials",
        "Interim results for the six months ended 30 June 2022",
        "Results for the year ended 31 December 2023",
        "Interim Report 2023",
        "Kirstin Simon",
    ]

    assert len(expected_suggestions) == len(
        suggestions
    ), f"Expected {len(expected_suggestions)} suggestions, but got {len(suggestions)}"

    for actual, expected in zip(suggestions, expected_suggestions):
        assert actual == expected, f"Expected '{expected}', but got '{actual}'"

    print("All suggestions match the expected list!")
