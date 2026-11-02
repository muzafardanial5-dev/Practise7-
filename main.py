import psycopg2
import csv

# 1. Настройки подключения к вашей базе данных PostgreSQL
# Замените 'your_password' на ваш реальный пароль от PostgreSQL
DB_CONFIG = {
    "dbname": "postgres",       # Имя вашей базы данных (обычно postgres по умолчанию)
    "user": "postgres",         # Ваш пользователь (обычно postgres)
    "password": "your_password", # ВАШ ПАРОЛЬ
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    """Функция для создания подключения к базе данных"""
    return psycopg2.connect(**DB_CONFIG)


# --- ТРЕБОВАНИЕ 1: Создание таблицы для телефонной книги ---
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# --- ТРЕБОВАНИЕ 2: Вставка данных из CSV-файла ---
def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Пропускаем строку заголовков в CSV (например, имя, телефон)
            for row in reader:
                if row:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                        (row[0], row[1])
                    )
        conn.commit()
        print("Данные из CSV файла успешно добавлены в базу!")
    except Exception as e:
        print("Ошибка при чтении CSV:", e)
    finally:
        cur.close()
        conn.close()


# --- ТРЕБОВАНИЕ 3: Вставка данных вручную через консоль ---
def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт '{name}' успешно добавлен!")


# --- ТРЕБОВАНИЕ 4: Обновление контакта (имени или телефона) ---
def update_contact(target_name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE first_name = %s",
        (new_phone, target_name)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Номер для контакта '{target_name}' обновлен!")


# --- ТРЕБОВАНИЕ 5: Поиск контактов с фильтрами (по имени или префиксу номера) ---
def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()
    # Используем ILIKE для поиска по части имени или части номера телефона
    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone LIKE %s",
        (f"%{pattern}%", f"{pattern}%")
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    print("\n--- РЕЗУЛЬТАТЫ ПОИСКА ---")
    if not rows:
        print("Ничего не найдено.")
    for row in rows:
        print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    print("-------------------------\n")


# --- ТРЕБОВАНИЕ 6: Удаление контакта по имени или номеру телефона ---
def delete_contact(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM phonebook WHERE first_name = %s OR phone = %s",
        (pattern, pattern)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Контакт '{pattern}' удален (если он существовал).")


# --- Консольное меню для управления программой ---
def main():
    create_table() # Создаем таблицу при запуске, если её нет
    
    while True:
        print("\n=== ТЕЛЕФОННАЯ КНИГА (PhoneBook) ===")
        print("1. Импортировать контакты из CSV-файла")
        print("2. Добавить контакт вручную")
        print("3. Обновить номер телефона у контакта")
        print("4. Найти контакт (по имени или телефону)")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите пункт меню: ")
        
        if choice == "1":
            file_name = input("Введите имя CSV файла (например, contacts.csv): ")
            insert_from_csv(file_name)
        elif choice == "2":
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            insert_contact(name, phone)
        elif choice == "3":
            name = input("Введите имя контакта, чей номер нужно изменить: ")
            new_phone = input("Введите новый номер телефона: ")
            update_contact(name, new_phone)
        elif choice == "4":
            query = input("Введите текст для поиска (имя или часть номера): ")
            search_contacts(query)
        elif choice == "5":
            target = input("Введите имя или точный номер для удаления: ")
            delete_contact(target)
        elif choice == "0":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный ввод, выберите пункт от 0 до 5.")

if __name__ == "__main__":
    main()