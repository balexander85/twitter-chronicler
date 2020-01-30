"""wrapped_driver.py

Module for all webdriver classes and methods
"""
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import CHROME_DRIVER_PATH, PROJECT_DIR_PATH
from _logger import LOGGER

chrome_driver_path = CHROME_DRIVER_PATH
headless_chrome_options = webdriver.ChromeOptions()
headless_chrome_options.add_argument("--window-size=1920,1080")
headless_chrome_options.add_argument("--disable-features=VizDisplayCompositor")
headless_chrome_options.add_argument("--start-maximized")
headless_chrome_options.add_argument("--disable-dev-shm-usage")
headless_chrome_options.add_argument("--disable-gpu")
headless_chrome_options.add_extension(
    os.path.join(PROJECT_DIR_PATH, "Old-Twitter-Layout_v1.0.0.crx.crx")
)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(
    os.path.join(PROJECT_DIR_PATH, "Old-Twitter-Layout_v1.0.0.crx.crx")
)


class WrappedWebDriver:
    """Class used to wrap selenium webdriver"""

    def __init__(self, browser: str = "headless"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(
                executable_path=chrome_driver_path, options=chrome_options
            )
        elif browser == "headless":
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                executable_path=chrome_driver_path, options=headless_chrome_options
            )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit_driver()

    def open(self, url: str):
        LOGGER.debug(f"self.open(): self.driver.get({url})")
        self.driver.get(url)

    def close(self):
        """Closes the current window."""
        LOGGER.debug("Closing window.")
        self.driver.close()

    def quit_driver(self):
        """Closes the browser and shuts down the ChromeDriver executable."""
        LOGGER.debug("Closing browser and shutting down ChromeDriver instance")
        self.driver.quit()

    def get_element_by_id(self, element_id: str) -> WebElement:
        return self.driver.find_element_by_id(element_id)

    def get_element_by_css(self, locator: str) -> WebElement:
        return self.driver.find_element_by_css_selector(css_selector=locator)

    def wait_for_element_to_be_present_by_id(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_present(
            by=By.ID, locator=locator, timeout=timeout, poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_present_by_css(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_present(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_visible_by_css(
        self, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_visible(
            by=By.CSS_SELECTOR,
            locator=locator,
            timeout=timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_element_to_be_present(
        self, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be present"""
        LOGGER.debug(msg=f"Waiting for locator to be present: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until(EC.presence_of_element_located((by, locator)))

    def wait_for_element_to_be_visible(
        self, by: By, locator: str, timeout: int = 60, poll_frequency: int = 3
    ) -> bool:
        """Wait for element to be visible"""
        if not self.wait_for_element_to_be_present(by=by, locator=locator):
            LOGGER.info(f"Locator: {locator} was not present.")

        LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        ).until(EC.visibility_of_element_located((by, locator)))


def scroll_to_element(driver: WrappedWebDriver, element: WebElement):
    """Helper method to scroll down to element"""
    LOGGER.debug(f"Scrolling to WebElement: {element}")
    raw_driver = driver.driver
    # raw_driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(raw_driver)
    actions.move_to_element(element).perform()
