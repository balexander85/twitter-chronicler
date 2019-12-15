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

from config import CHROME_DRIVER_PATH, dir_name
from util import LOGGER

chrome_driver_path = CHROME_DRIVER_PATH
chrome_options = webdriver.ChromeOptions()


class WrappedWebDriver:
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

    def get_element_by_css(self, locator: str) -> WebElement:
        self.wait_for_element_to_be_present(by=By.CSS_SELECTOR, locator=locator)
        return self.driver.find_element_by_css_selector(css_selector=locator)

    def wait_for_element_to_be_present(self, by, locator) -> bool:
        """Wait for element to be present"""
        return WebDriverWait(driver=self.driver, timeout=30).until(
            EC.presence_of_element_located((by, locator))
        )


def scroll_to_element(driver: WrappedWebDriver, element: WebElement):
    """Helper method to scroll down to element"""
    raw_driver = driver.driver
    # raw_driver.execute_script("arguments[0].scrollIntoView();", element)
    actions = ActionChains(raw_driver)
    actions.move_to_element(element).perform()


def screen_capture_element(element: WebElement, file_name: str):
    LOGGER.info(msg=f"Saving screen shot: {file_name}")
    file_path = os.path.join(dir_name, f"screen_shots/{file_name}")
    with open(file=file_path, mode="wb") as f:
        f.write(element.screenshot_as_png)
