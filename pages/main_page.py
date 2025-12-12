# main_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from pages.base_page import BasePage
import time


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
    CONSTRUCTOR_TITLE = (By.XPATH, "//*[@id='root']/div/main/section[1]/h1")
    
    # Конструктор (правая часть)
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__l9dp_')]")
    
    # Модальное окно заказа
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//h2[contains(@class, 'digits')]")
    ORDER_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal')]/button")
    
    # Модальное окно ингредиента
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    INGREDIENT_MODAL_CLOSE = (By.XPATH, "//div[contains(@class, 'Modal_modal')]/button")
    
    def go_to_constructor(self):
        """Перейти в конструктор"""
        self.click(self.CONSTRUCTOR_TAB)
    
    def go_to_order_feed(self):
        """Перейти в ленту заказов"""
        self.click(self.ORDER_FEED_TAB)
    
    def click_login_button(self):
        """Кликнуть на кнопку 'Войти в аккаунт'"""
        self.click(self.LOGIN_BUTTON)
    
    def click_ingredient(self, ingredient_type="bun"):
        """Кликнуть на ингредиент по типу"""
        if ingredient_type == "bun":
            self.click(self.FIRST_BUN)
        elif ingredient_type == "sauce":
            self.click(self.FIRST_SAUCE)
        elif ingredient_type == "filling":
            self.click(self.FIRST_FILLING)
    
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
    
    def add_ingredient_to_constructor(self, ingredient_type="bun"):
        """Добавить ингредиент в конструктор. Два отдельны способа для Firefox и Chrome"""
        if ingredient_type == "bun":
            source_locator = self.FIRST_BUN
        elif ingredient_type == "sauce":
            source_locator = self.FIRST_SAUCE
        elif ingredient_type == "filling":
            source_locator = self.FIRST_FILLING
        
        source = self.wait_for_element_visible(source_locator)
        target = self.wait_for_element_visible(self.CONSTRUCTOR_DROP_AREA)
        
        self.scroll_to_element(source_locator)
        time.sleep(0.5)
        
        browser = self.driver.capabilities['browserName']
        
        if browser == 'firefox':
            # Для Firefox используем JavaScript
            js_code = """
            // Получаем элемент ингредиента
            var source = arguments[0];
            var target = arguments[1];
            
            // Получаем ID ингредиента из атрибута href
            var href = source.getAttribute('href') || '';
            var ingredientId = href.split('/').pop() || '60d3b41abdacab0026a733c6';
            
            console.log('Drag ingredient ID:', ingredientId);
            
            // Создаем реальные события DragEvent
            function createDragEvent(type) {
                // Создаем DataTransfer
                var dataTransfer = new DataTransfer();
                dataTransfer.setData('text/plain', ingredientId);
                dataTransfer.setData('application/json', JSON.stringify({id: ingredientId}));
                dataTransfer.effectAllowed = 'move';
                dataTransfer.dropEffect = 'move';
                
                // Создаем DragEvent
                var event = new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                });
                
                return event;
            }
            
            // Диспатчим события в правильной последовательности
            var dragStart = createDragEvent('dragstart');
            source.dispatchEvent(dragStart);
            
            // Короткая задержка
            setTimeout(function() {
                var dragOver = createDragEvent('dragover');
                dragOver.preventDefault(); // Важно для разрешения drop
                target.dispatchEvent(dragOver);
                
                var drop = createDragEvent('drop');
                target.dispatchEvent(drop);
                
                var dragEnd = createDragEvent('dragend');
                source.dispatchEvent(dragEnd);
                
                // Триггерим изменение состояния
                var changeEvent = new Event('change', { bubbles: true });
                target.dispatchEvent(changeEvent);
            }, 50);
            """
            
            try:
                self.driver.execute_script(js_code, source, target)
                time.sleep(2)
            except Exception as e:
                print(f"Ошибка JavaScript drag-and-drop: {e}")
        
        else:  
            # Для Chrome используем стандартный drag-and-drop
            from selenium.webdriver import ActionChains
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            time.sleep(1)

    def create_order(self):
        """Оформить заказ"""
        self.click(self.ORDER_BUTTON)
    
    def close_order_modal(self):
        """Закрыть модальное окно заказа"""
        self.click(self.ORDER_MODAL_CLOSE)
        time.sleep(1)
    
    def is_constructor_page_visible(self):
        """Проверить, что страница конструктора видна"""
        return self.element_exists(self.CONSTRUCTOR_TITLE)
    
    def get_ingredient_modal(self):
        """Получить элемент модального окна ингредиента"""
        return self.wait_for_element_visible(self.INGREDIENT_MODAL)
    
    def close_ingredient_modal(self):
        """Закрыть модальное окно ингредиента"""
        self.click(self.INGREDIENT_MODAL_CLOSE)