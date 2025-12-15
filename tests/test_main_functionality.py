# test_main_functionality.py

import pytest
import allure

from pages.main_page import MainPage
from pages.feed_page import FeedPage
from data import TestData

@allure.suite("Основная функциональность")
class TestMainFunctionality:
    
    @allure.title("Переход по клику на 'Конструктор'")
    @allure.step("Проверка перехода в конструктор")
    def test_constructor_navigation(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            main_page = MainPage(driver)
            main_page.open(TestData.FEED_URL)
        
        with allure.step("Кликнуть на вкладку 'Конструктор'"):
            main_page.go_to_constructor()
        
        with allure.step("Проверить видимость страницы конструктора"):
            assert main_page.is_constructor_page_visible()
    
    @allure.title("Переход по клику на 'Лента заказов'")
    @allure.step("Проверка перехода в ленту заказов")
    def test_feed_navigation(self, driver):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open(TestData.BASE_URL)
        
        with allure.step("Кликнуть на вкладку 'Лента Заказов'"):
            main_page.go_to_order_feed()
        
        with allure.step("Проверить видимость страницы ленты заказов"):
            feed_page = FeedPage(driver)
            assert feed_page.is_feed_page_visible()

    @allure.title("Открытие модального окна с деталями ингредиента")
    @allure.step("Проверка открытия модального окна ингредиента")
    def test_ingredient_modal_opens(self, driver):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open(TestData.BASE_URL)
        
        with allure.step("Кликнуть на ингредиент 'булка'"):
            main_page.click_ingredient("bun")
        
        with allure.step("Проверить наличие модального окна"):
            assert main_page.element_exists(main_page.INGREDIENT_MODAL)

    @allure.title("Закрытие модального окна кликом по крестику")
    @allure.step("Проверка закрытия модального окна ингредиента")
    def test_ingredient_modal_closes(self, driver):
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)
            main_page.open(TestData.BASE_URL)
        
        with allure.step("Открыть модальное окно ингредиента"):
            main_page.click_ingredient("bun")
        
        with allure.step("Получить элемент модального окна"):
            modal = main_page.get_ingredient_modal()
        
        with allure.step("Закрыть модальное окно кликом по крестику"):
            main_page.close_ingredient_modal()
        
        with allure.step("Дождаться исчезновения модального окна"):
            main_page.wait_for_element_invisible(modal)
        
        with allure.step("Проверить, что модальное окно не отображается"):
            assert not modal.is_displayed()
    
    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    @allure.step("Проверка увеличения счетчика ингредиента")
    def test_ingredient_counter_increment(self, driver, login):
        main_page = login
        
        with allure.step("Получить начальное значение счетчика булки"):
            initial_count = main_page.get_ingredient_counter("bun")
        
        with allure.step("Добавить булку в конструктор"):
            main_page.add_ingredient_to_constructor("bun")
        
        with allure.step("Получить конечное значение счетчика булки"):
            new_count = main_page.get_ingredient_counter("bun")
        
        with allure.step("Проверить увеличение счетчика"):
            assert new_count > initial_count