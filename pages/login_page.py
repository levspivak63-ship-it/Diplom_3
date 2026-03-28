# login_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """
    Page Object для страницы авторизации Stellar Burgers
    """
    
    # Поля формы входа
    EMAIL_INPUT = (By.XPATH, "//input[@type='text']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")

    @allure.step("Авторизовать пользователя {email}")
    def login(self, email, password):
        """Авторизовать пользователя"""
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)