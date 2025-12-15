# main_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class MainPage(BasePage):
    """
    Page Object для главной страницы Stellar Burgers
    """
    
    # Навигация в шапке
    CONSTRUCTOR_TAB = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_TAB = (By.XPATH, "//p[text()='Лента Заказов']")
    
    # Кнопки
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    
    # Ингредиенты
    FIRST_BUN = (By.XPATH, "(//a[contains(@href, '/ingredient/')])[1]")
    FIRST_SAUCE = (By.XPATH, "(//a[contains(@href, '/ingredient/')])[3]")
    FIRST_FILLING = (By.XPATH, "(//a[contains(@href, '/ingredient/')])[5]")
    
    # Счетчики ингредиентов
    INGREDIENT_COUNTER = (By.CLASS_NAME, "counter_counter__num__3nue1")
    
    # Заголовок конструктора
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")
    
    # Конструктор (правая часть)
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__l9dp_')]")
    
    # Модальное окно заказа
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//h2[contains(@class, 'digits')]")
    ORDER_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal')]/button")
    
    # Модальное окно ингредиента
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    INGREDIENT_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal')]/button")

    @allure.step("Перейти в конструктор")
    def go_to_constructor(self):
        """Перейти в конструктор"""
        self.click(self.CONSTRUCTOR_TAB)
    
    @allure.step("Перейти в ленту заказов")
    def go_to_order_feed(self):
        """Перейти в ленту заказов"""
        self.click(self.ORDER_FEED_TAB)
    
    @allure.step("Кликнуть на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        """Кликнуть на кнопку 'Войти в аккаунт'"""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Кликнуть на ингредиент {ingredient_type}")
    def click_ingredient(self, ingredient_type="bun"):
        """Кликнуть на ингредиент по типу"""
        if ingredient_type == "bun":
            self.click(self.FIRST_BUN)
        elif ingredient_type == "sauce":
            self.click(self.FIRST_SAUCE)
        elif ingredient_type == "filling":
            self.click(self.FIRST_FILLING)
    
    @allure.step("Получить значение счетчика ингредиента {ingredient_type}")
    def get_ingredient_counter(self, ingredient_type="bun"):
        """Получить значение счетчика ингредиента"""
        try:
            if ingredient_type == "bun":
                element = self.find_element(self.FIRST_BUN)
            elif ingredient_type == "sauce":
                element = self.find_element(self.FIRST_SAUCE)
            elif ingredient_type == "filling":
                element = self.find_element(self.FIRST_FILLING)
            
            counter = element.find_element(*self.INGREDIENT_COUNTER)
            return int(counter.text) if counter.text else 0
        except:
            return 0
    
    @allure.step("Добавить ингредиент {ingredient_type} в конструктор")
    def add_ingredient_to_constructor(self, ingredient_type="bun"):
        """Добавить ингредиент в конструктор"""
        if ingredient_type == "bun":
            source_locator = self.FIRST_BUN
        elif ingredient_type == "sauce":
            source_locator = self.FIRST_SAUCE
        elif ingredient_type == "filling":
            source_locator = self.FIRST_FILLING
        
        source = self.wait_for_element_visible(source_locator)
        target = self.wait_for_element_visible(self.CONSTRUCTOR_DROP_AREA)
        
        self.scroll_to_element(source_locator)
        
        browser = self.driver.capabilities['browserName']
        
        if browser == 'firefox':
            # Упрощенный JavaScript для Firefox
            js_code = """
            var source = arguments[0];
            var target = arguments[1];
            
            // Получаем данные ингредиента
            var ingredientData = {
                id: source.getAttribute('href')?.split('/').pop() || '60d3b41abdacab0026a733c6'
            };
            
            // Просто добавляем ингредиент через клик и перенос
            var event = new MouseEvent('mousedown', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            source.dispatchEvent(event);
            
            // Имитируем перенос
            var dragEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            source.dispatchEvent(dragEvent);
            
            // Дроп на цель
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            target.dispatchEvent(dropEvent);
            
            // Клик на цель для активации
            var clickEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true
            });
            target.dispatchEvent(clickEvent);
            """
            
            try:
                self.execute_script(js_code, source, target)
            except Exception:
                # Альтернативный способ для Firefox
                self.execute_script("""
                    var source = arguments[0];
                    var target = arguments[1];
                    
                    // Просто перемещаем элемент в target
                    var clone = source.cloneNode(true);
                    target.appendChild(clone);
                    
                    // Триггерим событие изменения
                    var event = new Event('change', { bubbles: true });
                    target.dispatchEvent(event);
                """, source, target)
        
        else:  
            # Для Chrome используем стандартный drag-and-drop
            from selenium.webdriver import ActionChains
            ActionChains(self.driver).drag_and_drop(source, target).perform()

    @allure.step("Оформить заказ")
    def create_order(self):
        """Оформить заказ"""
        self.click(self.ORDER_BUTTON)
    
    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрыть модальное окно заказа"""
        self.click(self.ORDER_MODAL_CLOSE)
    
    @allure.step("Закрыть модальное окно заказа через JS")
    def click_order_modal_close_js(self):
        """Закрыть модальное окно заказа через JS"""
        close_button = self.find_element(self.ORDER_MODAL_CLOSE)
        self.click_js(close_button)
    
    @allure.step("Кликнуть на оверлей модального окна")
    def click_modal_overlay_js(self):
        """Кликнуть на оверлей модального окна"""
        js_code = """
            var overlay = document.querySelector('.Modal_modal_overlay__x2ZCr');
            if (overlay) overlay.click();
        """
        self.execute_script(js_code)
    
    @allure.step("Проверить, что страница конструктора видна")
    def is_constructor_page_visible(self):
        """Проверить, что страница конструктора видна"""
        return self.element_exists(self.CONSTRUCTOR_TITLE)
    
    @allure.step("Получить элемент модального окна ингредиента")
    def get_ingredient_modal(self):
        """Получить элемент модального окна ингредиента"""
        return self.wait_for_element_visible(self.INGREDIENT_MODAL)
    
    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        """Закрыть модальное окно ингредиента"""
        self.click(self.INGREDIENT_MODAL_CLOSE)
    
    @allure.step("Ждать загрузки номера заказа")
    def wait_for_order_number(self, timeout=30):
        """Ждать загрузки номера заказа"""
        element = self.wait_for_element_visible(self.ORDER_NUMBER, timeout)
        self.wait.until(
            lambda driver: element.text.strip() != "9999" and element.text.strip() != ""
        )
        return element
    
    @allure.step("Получить номер заказа")
    def get_order_number(self):
        """Получить номер заказа"""
        element = self.wait_for_order_number()
        return element.text.strip()
    
    @allure.step("Закрыть модальное окно заказа через JS")
    def close_order_modal_js(self):
        """Закрыть модальное окно заказа через JS"""
        close_button = self.find_element(self.ORDER_MODAL_CLOSE)
        self.click_js(close_button)