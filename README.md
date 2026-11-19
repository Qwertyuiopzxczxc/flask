# Flask + MySQL: авторизация

Реализация задания по подключению MySQL к Flask-приложению.

## Что сделано (по пунктам задания)

1. **Схема и таблица `users`**  
   Файл `schema.sql` создаёт БД `flask_auth` и таблицу:
   ```sql
   id INT AUTO_INCREMENT PRIMARY KEY,
   user_name VARCHAR(64) NOT NULL UNIQUE,
   user_password VARCHAR(255) NOT NULL
   ```
   + тестовый пользователь `Vladimir Putin` / `123456789`.

2. **Класс `Database`**  
   - `__init__` + `connect()` — `pymysql.connect(...)`
   - хранит `connection` и `cursor`
   - `close()` — корректное закрытие

3. **Метод `get_user(username)`**  
   Возвращает словарь `{id, user_name, user_password}` или `None`.

4. **Проверка в route `/login`**  
   - получает данные через `Database().get_user()`
   - сверяет пароль
   - обрабатывает ошибки
   - при успехе ставит cookie `auth_token` и делает редирект

- **Вход**: `Vladimir Putin` / `123456789`

## Структура

```
flask/
├── app.py              # основное приложение + класс Database
├── schema.sql          # SQL для создания БД и таблицы
├── requirements.txt
├── README.md
└── templates/
    ├── index.html
    ├── login.html
    └── register.html
```
