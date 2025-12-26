-- 1. Foydalanuvchilar jadvali
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id BIGINT UNIQUE NOT NULL,
    full_name TEXT,
    phone_number TEXT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Kategoriyalar jadvali
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- 3. Mahsulotlar jadvali
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    photo_id TEXT,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- 4. Savatcha (Vaqtinchalik saqlash joyi)
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- 5. Buyurtmalar (Asosiy chek)
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'pending', -- pending, paid, delivered, canceled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
);

-- 6. Buyurtma ichidagi mahsulotlar (Tarix uchun)
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_moment REAL NOT NULL, -- Mahsulot narxi o'zgarsa ham, tarixda eski narx qoladi
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- 7. To'lovlar
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    telegram_payment_charge_id TEXT, -- Telegram to'lov IDsi
    provider_payment_charge_id TEXT, -- Click/Payme IDsi
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'UZS',
    is_successful BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (id)
);