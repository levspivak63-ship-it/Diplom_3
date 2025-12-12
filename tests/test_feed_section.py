# test_feed_section.py

import pytest
import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.feed_page import FeedPage
from data import TestData

@allure.suite("Раздел 'Лента заказов'")
class TestFeedSection:

    @allure.title("Увеличение счетчика 'Выполнено за всё время' при создании заказа")
    def test_total_orders_counter_increment(self, driver):
        driver.get(TestData.FEED_URL)
        time.sleep(2)
        
        feed_page = FeedPage(driver)
        total_before = feed_page.get_total_orders_count()
        
        driver.get(TestData.BASE_URL)
        time.sleep(2)
        
        main_page = MainPage(driver)
        main_page.click_login_button()
        
        login_page = LoginPage(driver)
        login_page.login(
            TestData.REGISTERED_USER["email"],
            TestData.REGISTERED_USER["password"]
        )
        
        main_page.add_ingredient_to_constructor("bun")
        main_page.add_ingredient_to_constructor("sauce")
        main_page.create_order()
        
        WebDriverWait(driver, 30).until(
            lambda d: d.find_element(*main_page.ORDER_NUMBER).text.strip() != "9999"
        )
        
        close_button = driver.find_element(*main_page.ORDER_MODAL_CLOSE)
        driver.execute_script("arguments[0].click();", close_button)
        
        driver.get(TestData.FEED_URL)
        time.sleep(2)
        
        total_after = feed_page.get_total_orders_count()
        
        assert total_after > total_before

    @allure.title("Увеличение счетчика 'Выполнено за сегодня' при создании заказа")
    def test_today_orders_counter_increment(self, driver):
        driver.get(TestData.FEED_URL)
        time.sleep(2)
        
        feed_page = FeedPage(driver)
        today_before = feed_page.get_today_orders_count()

        driver.get(TestData.BASE_URL)
        time.sleep(2)
        
        main_page = MainPage(driver)
        main_page.click_login_button()
        
        login_page = LoginPage(driver)
        login_page.login(
            TestData.REGISTERED_USER["email"],
            TestData.REGISTERED_USER["password"]
        )
        
        main_page.add_ingredient_to_constructor("bun")
        main_page.add_ingredient_to_constructor("filling")
        main_page.create_order()
        
        WebDriverWait(driver, 30).until(
            lambda d: d.find_element(*main_page.ORDER_NUMBER).text.strip() != "9999"
        )
        
        close_button = driver.find_element(*main_page.ORDER_MODAL_CLOSE)
        driver.execute_script("arguments[0].click();", close_button)
        
        driver.get(TestData.FEED_URL)
        time.sleep(2)
        
        today_after = feed_page.get_today_orders_count()

        assert today_after > today_before

    @allure.title("Появление номера заказа в разделе 'В работе'")
    def test_order_appears_in_progress(self, driver, login):
        main_page = login
        
        main_page.go_to_constructor()
        main_page.add_ingredient_to_constructor("bun")
        main_page.add_ingredient_to_constructor("filling")
        main_page.create_order()
        
        WebDriverWait(driver, 30).until(
            lambda d: d.find_element(*main_page.ORDER_NUMBER).text.strip() != "9999"
        )
        
        order_number = driver.find_element(*main_page.ORDER_NUMBER).text.strip()
        
        close_button = driver.find_element(*main_page.ORDER_MODAL_CLOSE)
        driver.execute_script("arguments[0].click();", close_button)
        
        main_page.go_to_order_feed()
        time.sleep(10)
        
        order_list = driver.find_element(By.CLASS_NAME, "OrderFeed_orderListReady__1YFem")
        orders_text = order_list.text
        
        assert order_number in orders_text or f"0{order_number}" in orders_text 