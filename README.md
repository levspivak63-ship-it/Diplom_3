## Проект по автоматизации тестирования
1. Реализованы задачи по автоматизации тестов для Stellar Burgers:
- Проект разработан с помощью паттерна Page Object.
- Обеспечено кросс-браузерное тестирование (Chrome, Firefox)
- Результаты тестирования представлены в Allure отчете.

2. Использованные технологии указаны в файле requirements.txt.

3. Структура проекта:
📂 tests/ # Тестовые сценарии
│ ├── test_feed_section.py # Тесты раздела "Лента заказов"
│ └── test_main_functionality.py # Тесты основной функциональности
├── 📂 pages/ # Page Object классы
│ ├── base_page.py # Базовый класс страницы
│ ├── main_page.py # Главная страница
│ ├── login_page.py # Страница авторизации
│ └── feed_page.py # Страница ленты заказов
├── data.py # Тестовые данные
├── conftest.py # Фикстуры Pytest
├── requirements.txt # Зависимости проекта
├── allure-report/ # Готовый Allure отчёт
└── README.md # Документация

text

4. Тестовые сценарии:

**test_main_functionality.py:**
1. `test_constructor_navigation` - переход по клику на «Конструктор»
2. `test_feed_navigation` - переход по клику на раздел «Лента заказов»
3. `test_ingredient_modal_opens` - открытие модального окна ингредиента с деталями при клике на ингредиент
4. `test_ingredient_modal_closes` - закрытие модального окна кликом по крестику
5. `test_ingredient_counter_increment` - увеличение счетчика ингредиента при добавлении его в заказ

**test_feed_section.py:**
6. `test_total_orders_counter_increment` - увеличение счетчика «Выполнено за всё время» при создании нового заказа
7. `test_today_orders_counter_increment` - увеличение счетчика «Выполнено за сегодня» при создании нового заказа
8. `test_order_appears_in_progress` - появление номера заказ после его оформления в разделе «В работе»

5. **Запуск тестов:**
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов с генерацией Allure отчёта
pytest --alluredir=allure-results

# Просмотр отчёта
allure serve allure-results

