# base_page.py

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть URL {url}")
    def open(self, url):
        """Открыть URL"""
        self.driver.get(url)

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator):
        """Найти элемент"""
        return self.driver.find_element(*locator)

    @allure.step("Найти все элементы {locator}")
    def find_elements(self, locator):
        """Найти все элементы"""
        return self.driver.find_elements(*locator)

    @allure.step("Ждать видимости элемента {locator}")
    def wait_for_element_visible(self, locator, timeout=10):
        """Ждать видимости элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ждать кликабельности элемента {locator}")
    def wait_for_element_clickable(self, locator, timeout=10):
        """Ждать кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator):
        """Универсальный клик через JavaScript для двух браузеров"""
        element = self.wait_for_element_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Кликнуть на элемент через JS {locator}")
    def click_js(self, element):
        """Кликнуть на элемент через JavaScript"""
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.wait_for_element_visible(locator)
        return element.text

    @allure.step("Ввести текст в поле {locator}")
    def send_keys(self, locator, text):
        """Ввести текст в поле"""
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Скролл к элементу {locator}")
    def scroll_to_element(self, locator):
        """Скролл к элементу"""
        element = self.wait_for_element_visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    @allure.step("Проверить существование элемента в DOM {locator}")
    def element_exists(self, locator, timeout=5):
        """Проверить существование элемента в DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Выполнить JavaScript код")
    def execute_script(self, script, *args):
        """Выполнить JavaScript код"""
        return self.driver.execute_script(script, *args)

    @allure.step("Ждать невидимости элемента")
    def wait_for_element_invisible(self, element, timeout=3):
        """Ждать невидимости элемента"""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element(element)
        )