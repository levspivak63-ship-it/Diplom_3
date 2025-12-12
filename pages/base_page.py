# base_page.py

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        """Открыть URL"""
        self.driver.get(url)

    def find_element(self, locator):
        """Найти элемент"""
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        """Найти все элементы"""
        return self.driver.find_elements(*locator)

    def wait_for_element_visible(self, locator, timeout=10):
        """Ждать видимости элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=10):
        """Ждать кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        """Универсальный клик через JavaScript для двух браузеров"""
        element = self.wait_for_element_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.wait_for_element_visible(locator)
        return element.text

    def send_keys(self, locator, text):
        """Ввести текст в поле"""
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def scroll_to_element(self, locator):
        """Скролл к элементу"""
        element = self.wait_for_element_visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def element_exists(self, locator, timeout=5):
        """Проверить существование элемента в DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False