db_code = """import sqlite3
import json
from datetime import datetime
from config import DB_NAME

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.create_tables()
        except Exception as e:
            raise RuntimeError(f"Критическая ошибка подключения к базе данных: {e}")

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, species TEXT, age INTEGER,
            genetics TEXT, health INTEGER, hunger INTEGER)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, visitor_name TEXT,
            adult_tickets INTEGER, discount_tickets INTEGER,
            total_amount REAL, timestamp TEXT)''')
        
        self.conn.commit()

    def add_animal(self, animal):
        try:
            cursor = self.conn.cursor()
            genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
            cursor.execute('INSERT INTO animals (name, species, age, genetics, health, hunger) VALUES (?, ?, ?, ?, ?, ?)',
                (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise RuntimeError(f"Не удалось сохранить животное: {e}")

    def get_all_animals(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, species, age, health, hunger FROM animals')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить животных: {e}")

    def get_animal_genetics(self, animal_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT species, genetics FROM animals WHERE id = ?', (animal_id,))
            result = cursor.fetchone()
            if result:
                return result[0], json.loads(result[1])
            return None, None
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить генетику: {e}")

    def add_ticket_sale(self, visitor_name, adult_tickets, discount_tickets, total_amount):
        try:
            cursor = self.conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO ticket_sales (date, visitor_name, adult_tickets, discount_tickets, total_amount, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
                (today, visitor_name, adult_tickets, discount_tickets, total_amount, timestamp))
            self.conn.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Не удалось записать продажу: {e}")

    def get_ticket_sales_by_date(self, date=None):
        try:
            cursor = self.conn.cursor()
            if date:
                cursor.execute('SELECT * FROM ticket_sales WHERE date = ?', (date,))
            else:
                cursor.execute('SELECT * FROM ticket_sales ORDER BY timestamp DESC')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить продажи: {e}")

    def get_total_revenue(self, date=None):
        try:
            cursor = self.conn.cursor()
            if date:
                cursor.execute('SELECT SUM(total_amount) FROM ticket_sales WHERE date = ?', (date,))
            else:
                cursor.execute('SELECT SUM(total_amount) FROM ticket_sales')
            result = cursor.fetchone()
            return result[0] if result[0] else 0
        except Exception as e:
            raise RuntimeError(f"Не удалось подсчитать доход: {e}")

    def get_sales_statistics(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) as total_sales, SUM(adult_tickets) as total_adult, SUM(discount_tickets) as total_discount, SUM(total_amount) as total_revenue FROM ticket_sales')
            return cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Не удалось получить статистику: {e}")
"""

with open('database/db_manager.py', 'w', encoding='utf-8') as f:
    f.write(db_code)

print("✅ DatabaseManager обновлен")