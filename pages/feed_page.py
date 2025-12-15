# feed_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re
import allure

class FeedPage(BasePage):
    FEED_PAGE_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[contains(., 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(., 'Выполнено за сегодня')]/following-sibling::p")
    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//*[contains(text(), 'В работе:')]")
    ORDERS_IN_PROGRESS_LIST = (By.CLASS_NAME, "OrderFeed_orderListReady__1YFem")
    
    @allure.step("Проверить видимость страницы ленты заказов")
    def is_feed_page_visible(self):
        return self.element_exists(self.FEED_PAGE_TITLE)

    @allure.step("Получить общее количество заказов")
    def get_total_orders_count(self):
        element = self.wait_for_element_visible(self.TOTAL_ORDERS_COUNTER)
        text = element.text.strip()
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        element = self.wait_for_element_visible(self.TODAY_ORDERS_COUNTER)
        text = element.text.strip()
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    @allure.step("Ждать появления заказа в разделе 'В работе'")
    def wait_for_order_appear(self, timeout=30):
        """Ждать, пока в разделе 'В работе' появится заказ"""
        element = self.wait_for_element_visible(self.ORDERS_IN_PROGRESS_LIST, timeout)
        
        # Запоминаем начальный текст
        initial_text = element.text.strip()
        
        def text_changed(driver):
            return element.text.strip() != initial_text
        
        # Ждем изменения текста
        self.wait.until(text_changed)
        
        # Возвращаем новый текст (а не элемент)
        return element.text.strip()