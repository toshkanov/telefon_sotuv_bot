import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        try:
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Baza bilan ishlashda xatolik: {e}")
        finally:
            connection.close()
        return data

    def add_user(self, telegram_id: int, full_name: str):
        sql = """
        INSERT OR IGNORE INTO users(telegram_id, full_name) VALUES(?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users", fetchone=True)[0]