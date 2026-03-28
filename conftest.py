# conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.login_page import LoginPage
from pages.main_page import MainPage
from data import TestData

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    """Фикстура для инициализации драйвера браузеров Chrome и Firefox"""
    browser = request.param
    
    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    """Фикстура для авторизации пользователя и возврата на главную страницу"""
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    
    main_page.open(TestData.BASE_URL)
    main_page.click_login_button()
    login_page.login(
        TestData.REGISTERED_USER["email"],
        TestData.REGISTERED_USER["password"]
    )
    
    return main_page

