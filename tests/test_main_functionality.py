# test_main_functionality.py

import pytest
import allure

from pages.main_page import MainPage
from pages.feed_page import FeedPage
from data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.suite("Основная функциональность")
class TestMainFunctionality:
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_constructor_navigation(self, driver):
        main_page = MainPage(driver)
        main_page.open(TestData.FEED_URL)
        main_page.go_to_constructor()
        assert main_page.is_constructor_page_visible()
    
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_feed_navigation(self, driver):
        main_page = MainPage(driver)
        main_page.open(TestData.BASE_URL)
        main_page.go_to_order_feed()
        feed_page = FeedPage(driver)
        assert feed_page.is_feed_page_visible()

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.open(TestData.BASE_URL)
        main_page.click_ingredient("bun")
        assert main_page.element_exists(main_page.INGREDIENT_MODAL)

    @allure.title("Закрытие модального окна кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.open(TestData.BASE_URL)
        main_page.click_ingredient("bun")
        
        modal = main_page.get_ingredient_modal()
        main_page.close_ingredient_modal()
        
               
        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element(modal)
        )
        
        assert not modal.is_displayed()
    
    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increment(self, driver, login):
        main_page = login
        initial_count = main_page.get_ingredient_counter("bun")
        main_page.add_ingredient_to_constructor("bun")
        new_count = main_page.get_ingredient_counter("bun")
        assert new_count > initial_count