"""wrapped_driver.py

Module for all webdriver classes and methods
"""
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import CHROME_DRIVER_PATH
from _logger import LOGGER

chrome_driver_path = CHROME_DRIVER_PATH
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")


class WrappedWebDriver:
    """Class used to wrap selenium webdriver"""

    def __init__(self, browser: str = "chrome"):
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        elif browser == "headless":
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                executable_path=chrome_driver_path, chrome_options=chrome_options
            )

    def open(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def quit_driver(self):
        self.driver.quit()

    def get_element_by_id(self, element_id) -> WebElement:
        return self.driver.find_element_by_id(element_id)

    def get_element_by_css(self, locator: str) -> Optional[WebElement]:
        self.wait_for_element_to_be_present_by_css(locator=locator)
        self.wait_for_element_to_be_visible(by=By.CSS_SELECTOR, locator=locator)
        try:
            return self.driver.find_element_by_css_selector(css_selector=locator)
        except TimeoutException as e:
            LOGGER.error(f"{e} timed out looking for: {locator}")

    def wait_for_element_to_be_present_by_css(self, locator) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_present(by=By.CSS_SELECTOR, locator=locator)

    def wait_for_element_to_be_visible_by_css(self, locator) -> bool:
        """Wait for element to be present using CSS locator"""
        return self.wait_for_element_to_be_visible(by=By.CSS_SELECTOR, locator=locator)

    def wait_for_element_to_be_present(self, by, locator) -> bool:
        """Wait for element to be present"""
        LOGGER.debug(msg=f"Waiting for locator to be present: {locator}")
        return WebDriverWait(driver=self.driver, timeout=60, poll_frequency=3).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_for_element_to_be_visible(self, by, locator) -> bool:
        """Wait for element to be visible"""
        if not self.wait_for_element_to_be_present(by=by, locator=locator):
            LOGGER.info(f"Locator: {locator} was not present.")

        LOGGER.debug(msg=f"Waiting for locator to be visible: {locator}")
        return WebDriverWait(driver=self.driver, timeout=60, poll_frequency=3).until(
            EC.visibility_of_element_located((by, locator))
        )


def scroll_to_element(driver: WrappedWebDriver, element: WebElement):
    """Helper method to scroll down to element"""
    LOGGER.debug(f"Scrolling to {element}")
    raw_driver = driver.driver
    # raw_driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(raw_driver)
    actions.move_to_element(element).perform()
