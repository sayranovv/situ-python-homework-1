import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Товары (
            id_товара INTEGER PRIMARY KEY AUTOINCREMENT,
            категория TEXT NOT NULL,
            наименование TEXT NOT NULL,
            количество_в_упаковке INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Магазины (
            id_магазина INTEGER PRIMARY KEY AUTOINCREMENT,
            район TEXT NOT NULL,
            адрес TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Движение_товаров (
            id_операции INTEGER PRIMARY KEY AUTOINCREMENT,
            дата_совершения DATE NOT NULL,
            id_товара INTEGER NOT NULL,
            id_магазина INTEGER NOT NULL,
            тип_операции TEXT NOT NULL,
            количество_упаковок INTEGER NOT NULL,
            цена REAL NOT NULL,
            FOREIGN KEY (id_товара) REFERENCES Товары(id_товара) ON DELETE CASCADE,
            FOREIGN KEY (id_магазина) REFERENCES Магазины(id_магазина) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("База данных и таблицы созданы успешно")

def add_good(category, name, quantity):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM Товары WHERE категория = ? AND наименование = ? AND количество_в_упаковке = ?
    ''', (category, name, quantity))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Дубликат товара")
    cursor.execute('''
        INSERT INTO Товары (категория, наименование, количество_в_упаковке)
        VALUES (?, ?, ?)
    ''', (category, name, quantity))
    conn.commit()
    conn.close()

def get_all_goods():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Товары')
    results = cursor.fetchall()
    conn.close()
    return results

def update_good(id, category, name, quantity):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM Товары WHERE категория = ? AND наименование = ? AND количество_в_упаковке = ? AND id_товара != ?
    ''', (category, name, quantity, id))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Дубликат товара")
    cursor.execute('''
        UPDATE Товары SET категория = ?, наименование = ?, количество_в_упаковке = ?
        WHERE id_товара = ?
    ''', (category, name, quantity, id))
    conn.commit()
    conn.close()

def delete_good(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Товары WHERE id_товара = ?', (id,))
    conn.commit()
    conn.close()

def add_store(district, address):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM Магазины WHERE район = ? AND адрес = ?
    ''', (district, address))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Дубликат магазина")
    cursor.execute('''
        INSERT INTO Магазины (район, адрес)
        VALUES (?, ?)
    ''', (district, address))
    conn.commit()
    conn.close()

def get_all_stores():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Магазины')
    results = cursor.fetchall()
    conn.close()
    return results

def update_store(id, district, address):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM Магазины WHERE район = ? AND адрес = ? AND id_магазина != ?
    ''', (district, address, id))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Дубликат магазина")
    cursor.execute('''
        UPDATE Магазины SET район = ?, адрес = ?
        WHERE id_магазина = ?
    ''', (district, address, id))
    conn.commit()
    conn.close()

def delete_store(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Магазины WHERE id_магазина = ?', (id,))
    conn.commit()
    conn.close()

def add_movement(date, good_id, store_id, op_type, quantity, price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Движение_товаров (дата_совершения, id_товара, id_магазина, тип_операции, количество_упаковок, цена)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, good_id, store_id, op_type, quantity, price))
    conn.commit()
    conn.close()

def get_all_movements():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Движение_товаров')
    return cursor.fetchall()
    conn.close()

def update_movement(id, date, good_id, store_id, op_type, quantity, price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Движение_товаров SET дата_совершения = ?, id_товара = ?, id_магазина = ?, тип_операции = ?, количество_упаковок = ?, цена = ?
        WHERE id_операции = ?
    ''', (date, good_id, store_id, op_type, quantity, price, id))
    conn.commit()
    conn.close()

def delete_movement(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Движение_товаров WHERE id_операции = ?', (id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
