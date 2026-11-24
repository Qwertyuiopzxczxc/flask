import pymysql
import pymysql.cursors


class Database:
    def __init__(self, host="localhost", user="root", password="admin", database="academy"):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    def create_user(self, name, password):
        """Метод из урока: INSERT пользователя"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                (name, password)
            )
        self.conn.commit()
        return cur.lastrowid

    def get_user(self, name):
        """Нужен для проверки дубля имени"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE user_name = %s",
                (name,)
            )
            return cur.fetchone()
