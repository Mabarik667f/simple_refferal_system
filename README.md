- create logs dir in src:
```mkdir logs```

- create log file:
```touch log.log```

- create *SECRET_KEY*:
```from django.core.management.utils import get_random_secret_key```
```print(get_random_secret_key()```

API:
- docs/ GET 
- docs/redoc GET - OpenAPI, сгенерированный ReDoc
- docs/swagger GET - OpenAPI, сгенерированный Swagger
- v1/user/
    - auth/ POST - Попытка авторизации, мы отправляем телефон и получаем код авторизации
    - verify-code/ POST - Проверка кода авторизации для пользователя 
    - activate-invite-code/ POST - Активация инвайт-кода 
    - <int:pk>/ GET - Получение данных о пользователе
    - list/ GET - Получение списка номеров телефонов пользователей,
    которые актвировали инвайт-код текущего пользователя
