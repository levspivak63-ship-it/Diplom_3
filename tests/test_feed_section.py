# test_feed_section.py

import pytest
import allure

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.feed_page import FeedPage
from data import TestData

@allure.suite("Раздел 'Лента заказов'")
class TestFeedSection:

    @allure.title("Увеличение счетчика 'Выполнено за всё время' при создании заказа")
    @allure.step("Проверка увеличения счетчика всех заказов")
    def test_total_orders_counter_increment(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            feed_page = FeedPage(driver)
            feed_page.open(TestData.FEED_URL)
        
        with allure.step("Получить начальное количество заказов"):
            total_before = feed_page.get_total_orders_count()
        
        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            main_page.open(TestData.BASE_URL)
        
        with allure.step("Кликнуть на кнопку входа в аккаунт"):
            main_page.click_login_button()
        
        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.login(
                TestData.REGISTERED_USER["email"],
                TestData.REGISTERED_USER["password"]
            )
        
        with allure.step("Добавить булку в конструктор"):
            main_page.add_ingredient_to_constructor("bun")
        
        with allure.step("Добавить соус в конструктор"):
            main_page.add_ingredient_to_constructor("sauce")
        
        with allure.step("Оформить заказ"):
            main_page.create_order()
        
        with allure.step("Дождаться номера заказа"):
            main_page.wait_for_order_number()
        
        with allure.step("Закрыть модальное окно заказа"):
            main_page.close_order_modal()
        
        with allure.step("Вернуться на страницу ленты заказов"):
            feed_page.open(TestData.FEED_URL)
        
        with allure.step("Получить конечное количество заказов"):
            total_after = feed_page.get_total_orders_count()
        
        with allure.step("Проверить увеличение счетчика"):
            assert total_after > total_before

    @allure.title("Увеличение счетчика 'Выполнено за сегодня' при создании заказа")
    @allure.step("Проверка увеличения счетчика заказов за сегодня")
    def test_today_orders_counter_increment(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            feed_page = FeedPage(driver)
            feed_page.open(TestData.FEED_URL)
        
        with allure.step("Получить начальное количество заказов за сегодня"):
            today_before = feed_page.get_today_orders_count()

        with allure.step("Перейти на главную страницу"):
            main_page = MainPage(driver)
            main_page.open(TestData.BASE_URL)
        
        with allure.step("Кликнуть на кнопку входа в аккаунт"):
            main_page.click_login_button()
        
        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.login(
                TestData.REGISTERED_USER["email"],
                TestData.REGISTERED_USER["password"]
            )
        
        with allure.step("Добавить булку в конструктор"):
            main_page.add_ingredient_to_constructor("bun")
        
        with allure.step("Добавить начинку в конструктор"):
            main_page.add_ingredient_to_constructor("filling")
        
        with allure.step("Оформить заказ"):
            main_page.create_order()
        
        with allure.step("Дождаться номера заказа"):
            main_page.wait_for_order_number()
        
        with allure.step("Закрыть модальное окно заказа"):
            main_page.close_order_modal()
        
        with allure.step("Вернуться на страницу ленты заказов"):
            feed_page.open(TestData.FEED_URL)
        
        with allure.step("Получить конечное количество заказов за сегодня"):
            today_after = feed_page.get_today_orders_count()

        with allure.step("Проверить увеличение счетчика"):
            assert today_after > today_before

    @allure.title("Появление номера заказа в разделе 'В работе'")
    @allure.step("Проверка появления номера заказа в разделе 'В работе'")
    def test_order_appears_in_progress(self, driver, login):
        main_page = login
        
        with allure.step("Перейти в конструктор"):
            main_page.go_to_constructor()
        
        with allure.step("Добавить булку в конструктор"):
            main_page.add_ingredient_to_constructor("bun")
        
        with allure.step("Добавить начинку в конструктор"):
            main_page.add_ingredient_to_constructor("filling")
        
        with allure.step("Оформить заказ"):
            main_page.create_order()
        
        with allure.step("Получить номер заказа"):
            order_number = main_page.get_order_number()
        
        with allure.step("Закрыть модальное окно заказа"):
            main_page.close_order_modal()
        
        with allure.step("Перейти в ленту заказов"):
            main_page.go_to_order_feed()
        
        with allure.step("Получить текст списка заказов в работе"):
            feed_page = FeedPage(driver)
            orders_text = feed_page.wait_for_order_appear(timeout=30)
        
        with allure.step("Проверить наличие номера заказа в списке"):
            assert order_number in orders_text or f"0{order_number}" in orders_text