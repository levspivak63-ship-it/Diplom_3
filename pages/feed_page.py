# feed_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import re

class FeedPage(BasePage):
    FEED_PAGE_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[contains(., 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(., 'Выполнено за сегодня')]/following-sibling::p")
    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//*[contains(text(), 'В работе:')]")
    ORDERS_IN_PROGRESS_LIST = (By.CLASS_NAME, "OrderFeed_orderListReady__1YFem")
    
    def is_feed_page_visible(self):
        return self.element_exists(self.FEED_PAGE_TITLE)

    def get_total_orders_count(self):
        element = self.wait_for_element_visible(self.TOTAL_ORDERS_COUNTER)
        text = element.text.strip()
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0

    def get_today_orders_count(self):
        element = self.wait_for_element_visible(self.TODAY_ORDERS_COUNTER)
        text = element.text.strip()
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    
    