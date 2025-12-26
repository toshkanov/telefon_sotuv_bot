import sqlite3


def create_tables():
    # 1. Bazaga ulanamiz (agar fayl yo'q bo'lsa, o'zi yaratadi)
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()

    # 2. SQL faylni ochib o'qiymiz
    try:
        with open("database_setup.sql", "r") as file:
            sql_script = file.read()

        # 3. SQL buyruqlarni bajaramiz
        cursor.executescript(sql_script)
        connection.commit()
        print("✅ Jadvallar muvaffaqiyatli yaratildi! (main.db fayli paydo bo'ldi)")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()