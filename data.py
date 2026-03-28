# data.py

class TestData:
    """Тестовые данные для авторизации"""
    
    # Аккаунт зарегистрированного пользователя
    REGISTERED_USER = {
        "email": "lev_spivak_32_125@yandex.ru",
        "password": "123456",
        "name": "Lev_Spivak_32_125@yandex.ru"
    }
    
    # Базовый URL
    BASE_URL = "https://stellarburgers.education-services.ru/"
    
    # URL страницы ленты заказов
    FEED_URL = f"{BASE_URL}feed"
   