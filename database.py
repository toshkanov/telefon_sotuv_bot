import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
        # Bot ishga tushganda avtomatik jadvallarni yaratamiz
        self.create_tables()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    # --- JADVALLARNI YARATISH ---
    def create_tables(self):
        # 1. USERS jadvali
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         telegram_id
                         INTEGER
                         UNIQUE,
                         full_name
                         TEXT
                     );
                     """, commit=True)

        # 2. CATEGORIES jadvali
        self.execute("""
                     CREATE TABLE IF NOT EXISTS categories
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         name
                         TEXT
                     );
                     """, commit=True)

        # 3. PRODUCTS jadvali
        self.execute("""
                     CREATE TABLE IF NOT EXISTS products
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT,
                         name
                         TEXT,
                         price
                         TEXT,
                         category_id
                         INTEGER,
                         image
                         TEXT,
                         seller_id
                         INTEGER,
                         description
                         TEXT
                     );
                     """, commit=True)

    # --- QO'SHIMCHA FUNKSIYALAR ---

    def add_user(self, telegram_id: int, full_name: str):
        self.execute("INSERT OR IGNORE INTO users(telegram_id, full_name) VALUES(?, ?)",
                     (telegram_id, full_name), commit=True)

    def add_category(self, name: str):
        self.execute("INSERT INTO categories(name) VALUES(?)", (name,), commit=True)

    def add_product(self, name, price, category_id, image, seller_id):
        # description hozircha 'no_desc' bo'lib turadi
        self.execute("""
                     INSERT INTO products(name, price, category_id, image, seller_id, description)
                     VALUES (?, ?, ?, ?, ?, 'no_desc')
                     """, (name, price, category_id, image, seller_id), commit=True)

    def get_table_data(self, table_name):
        return self.execute(f"SELECT * FROM {table_name}", fetchall=True)

    # ... (tepadagi kodlar turaversin) ...

    # --- YANGI KUCHAYTIRILGAN STATISTIKA ---

    def get_full_statistics(self):
        # 1. Jami foydalanuvchilar soni
        users_count = self.execute("SELECT COUNT(*) FROM users", fetchone=True)[0]

        # 2. Jami telefonlar soni
        products_count = self.execute("SELECT COUNT(*) FROM products", fetchone=True)[0]

        # 3. Kategoriya bo'yicha telefonlar soni (Eng muhimi!)
        # Bu so'rov har bir kategoriyada nechta telefon borligini sanaydi
        cat_stats = self.execute("""
                                 SELECT c.name, COUNT(p.id)
                                 FROM categories c
                                          LEFT JOIN products p ON c.id = p.category_id
                                 GROUP BY c.id
                                 """, fetchall=True)

        # 4. Oxirgi 5 ta qo'shilgan foydalanuvchi
        last_users = self.execute("SELECT full_name, telegram_id FROM users ORDER BY id DESC LIMIT 5", fetchall=True)

        # 5. Oxirgi 5 ta qo'shilgan telefon
        last_products = self.execute("SELECT name, price FROM products ORDER BY id DESC LIMIT 5", fetchall=True)

        return {
            "users_count": users_count,
            "products_count": products_count,
            "categories": cat_stats,
            "last_users": last_users,
            "last_products": last_products
        }