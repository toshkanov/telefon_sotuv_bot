import psycopg2
from config import ADMINS  # Kerak bo'lsa


class Database:
    def __init__(self):
        # 1. BAZAGA ULANISH SOZLAMALARI
        # Boya terminalda yaratgan nom va parolni yozasiz
        self.db_params = {
            "dbname": "mobil_bozor",
            "user": "toshkanov",
            "password": "12345",
            "host": "localhost",
            "port": "5432"
        }
        self.create_tables()

    @property
    def connection(self):
        return psycopg2.connect(**self.db_params)

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
        except Exception as e:
            print(f"Xatolik: {e}")
        finally:
            connection.close()

        return data

    # --- JADVALLARNI YARATISH (POSTGRES SINTAKSISI) ---
    def create_tables(self):
        # 1. USERS (BIGINT - katta sonlar uchun, SERIAL - avtomatik raqam)
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users
                     (
                         id
                         SERIAL
                         PRIMARY
                         KEY,
                         telegram_id
                         BIGINT
                         UNIQUE
                         NOT
                         NULL,
                         full_name
                         VARCHAR
                     (
                         255
                     )
                         );
                     """, commit=True)

        # 2. CATEGORIES
        self.execute("""
                     CREATE TABLE IF NOT EXISTS categories
                     (
                         id
                         SERIAL
                         PRIMARY
                         KEY,
                         name
                         VARCHAR
                     (
                         255
                     ) NOT NULL
                         );
                     """, commit=True)

        # 3. PRODUCTS
        self.execute("""
                     CREATE TABLE IF NOT EXISTS products
                     (
                         id
                         SERIAL
                         PRIMARY
                         KEY,
                         name
                         VARCHAR
                     (
                         255
                     ),
                         price VARCHAR
                     (
                         50
                     ),
                         category_id INTEGER,
                         image VARCHAR
                     (
                         255
                     ),
                         seller_id BIGINT,
                         description TEXT
                         );
                     """, commit=True)

    # --- FUNKSIYALAR ---
    # DIQQAT: Postgresda "?" o'rniga "%s" ishlatiladi!

    def add_user(self, telegram_id: int, full_name: str):
        # ON CONFLICT - agar user bor bo'lsa, xato bermaslik uchun
        self.execute("""
                     INSERT INTO users(telegram_id, full_name)
                     VALUES (%s, %s) ON CONFLICT (telegram_id) DO NOTHING
                     """, (telegram_id, full_name), commit=True)

    def add_category(self, name: str):
        self.execute("INSERT INTO categories(name) VALUES(%s)", (name,), commit=True)

    def add_product(self, name, price, category_id, image, seller_id):
        self.execute("""
                     INSERT INTO products(name, price, category_id, image, seller_id, description)
                     VALUES (%s, %s, %s, %s, %s, 'no_desc')
                     """, (name, price, category_id, image, seller_id), commit=True)

    def get_table_data(self, table_name):
        # Xavfsizlik uchun faqat ruxsat etilgan jadvallar
        allowed = ["users", "products", "categories"]
        if table_name in allowed:
            return self.execute(f"SELECT * FROM {table_name}", fetchall=True)
        return []

    # STATISTIKA UCHUN
    def get_full_statistics(self):
        users_count = self.execute("SELECT COUNT(*) FROM users", fetchone=True)[0]
        products_count = self.execute("SELECT COUNT(*) FROM products", fetchone=True)[0]

        cat_stats = self.execute("""
                                 SELECT c.name, COUNT(p.id)
                                 FROM categories c
                                          LEFT JOIN products p ON c.id = p.category_id
                                 GROUP BY c.id
                                 """, fetchall=True)

        last_users = self.execute("SELECT full_name, telegram_id FROM users ORDER BY id DESC LIMIT 5", fetchall=True)
        last_products = self.execute("SELECT name, price FROM products ORDER BY id DESC LIMIT 5", fetchall=True)

        return {
            "users_count": users_count,
            "products_count": products_count,
            "categories": cat_stats,
            "last_users": last_users,
            "last_products": last_products
        }