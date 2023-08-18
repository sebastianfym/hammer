Инструкция по использованию API
1. Аутентификация
    1.1. Запрос кода подтверждения
        Endpoint: /auth/auth/
        HTTP метод: POST
        Параметры:
        phone_number: Номер телефона пользователя. Должен содержать от 10 до 12 символов.
        Пример запроса:
            curl -X POST -H "Content-Type: application/json" -d '{"phone_number": "1234567890"}' http://localhost:8000/user/auth/auth/
    1.2. Авторизация пользователя с помощью кода
        Endpoint: /auth/accept_user/
        HTTP метод: POST
        Параметры:
        code: Код подтверждения, который был получен на предыдущем этапе.
        Пример запроса:
            curl -X POST -H "Content-Type: application/json" -d '{"code": "1234"}' http://localhost:8000/user/auth/accept_user/

2. Профиль
    2.1. Получение информации о профиле
        Endpoint: /profile/info/
        HTTP метод: GET
        Требования: Требуется аутентификация.
        Пример запроса:
            curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8000/user/profile/info/

    2.2. Изменение профиля
        Endpoint: /profile/change_profile/
        HTTP метод: POST
        Параметры:
        invite_code: Реферальный код другого пользователя.
        Требования: Требуется аутентификация.
        Пример запроса:
            curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -H "Content-Type: application/json" -d '{"invite_code": "ABC123"}' http://localhost:8000/user/profile/change_profile/

3. Обновление токена
    Endpoint: /token/refresh/
    HTTP метод: POST
    Параметры:
    refresh: Refresh токен пользователя.
    Пример запроса:
        curl -X POST -H "Content-Type: application/json" -d '{"refresh": "YOUR_REFRESH_TOKEN"}' http://localhost:8000/user/token/refresh/
