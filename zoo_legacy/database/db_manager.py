import sqlite3
import json
from datetime import datetime
from config import DB_NAME

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            self.create_tables()
        except Exception as e:
            raise RuntimeError(f"Ошибка подключения к БД: {e}")

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, species TEXT, age INTEGER,
            genetics TEXT, health INTEGER, hunger INTEGER,
            rarity TEXT DEFAULT 'Обычное', income_per_day INTEGER DEFAULT 100,
            generation INTEGER DEFAULT 1, parent_id INTEGER DEFAULT 0,
            mutation TEXT DEFAULT '')""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY,
            day INTEGER DEFAULT 1,
            balance REAL DEFAULT 125450,
            energy INTEGER DEFAULT 100,
            max_energy INTEGER DEFAULT 100,
            reputation INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0,
            science_points INTEGER DEFAULT 0)""")

        cursor.execute('SELECT COUNT(*) FROM game_state')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO game_state (id, day, balance, energy, max_energy, reputation, level, experience, science_points) VALUES (1, 1, 125450, 100, 100, 0, 1, 0, 0)')

        cursor.execute("""CREATE TABLE IF NOT EXISTS events_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER, event_type TEXT, description TEXT, amount REAL)""")

        self.conn.commit()

    def get_game_state(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT day, balance, energy, max_energy, reputation, level, experience, science_points FROM game_state WHERE id = 1')
        return cursor.fetchone()

    def get_balance(self):
        state = self.get_game_state()
        return state[1] if state else 125450

    def get_day(self):
        state = self.get_game_state()
        return state[0] if state else 1

    def get_energy(self):
        state = self.get_game_state()
        return state[2] if state else 100

    def get_max_energy(self):
        state = self.get_game_state()
        return state[3] if state else 100

    def get_reputation(self):
        state = self.get_game_state()
        return state[4] if state else 0

    def get_level(self):
        state = self.get_game_state()
        return state[5] if state else 1

    def get_science_points(self):
        state = self.get_game_state()
        return state[7] if state else 0

    def update_balance(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET balance = balance + ? WHERE id = 1', (amount,))
        self.conn.commit()

    def use_energy(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET energy = MAX(0, energy - ?) WHERE id = 1', (amount,))
        self.conn.commit()

    def add_science_points(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET science_points = science_points + ? WHERE id = 1', (amount,))
        self.conn.commit()

    def use_science_points(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET science_points = MAX(0, science_points - ?) WHERE id = 1', (amount,))
        self.conn.commit()

    def restore_energy(self):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET energy = max_energy WHERE id = 1')
        self.conn.commit()

    def add_experience(self, xp):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET experience = experience + ? WHERE id = 1', (xp,))
        cursor.execute('SELECT experience, level FROM game_state WHERE id = 1')
        exp, lvl = cursor.fetchone()
        needed = lvl * 100
        if exp >= needed:
            cursor.execute('UPDATE game_state SET level = level + 1, experience = experience - ?, max_energy = max_energy + 10 WHERE id = 1', (needed,))
            cursor.execute('UPDATE game_state SET energy = max_energy WHERE id = 1')
            self.conn.commit()
            return True
        self.conn.commit()
        return False

    def add_reputation(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET reputation = reputation + ? WHERE id = 1', (amount,))
        self.conn.commit()

    def next_day(self):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET day = day + 1 WHERE id = 1')
        self.restore_energy()
        self.conn.commit()

    def add_animal(self, animal, price=0, parent_id=0, mutation=''):
        cursor = self.conn.cursor()
        genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
        cursor.execute('INSERT INTO animals (name, species, age, genetics, health, hunger, rarity, income_per_day, generation, parent_id, mutation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger, animal.rarity, animal.income_per_day, 1, parent_id, mutation))
        if price > 0:
            self.update_balance(-price)
        self.conn.commit()
        return cursor.lastrowid

    def get_all_animals(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, species, age, health, hunger, rarity, income_per_day, generation, parent_id, mutation FROM animals')
        return cursor.fetchall()

    def get_animal_genetics(self, animal_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT species, genetics, generation, parent_id FROM animals WHERE id = ?', (animal_id,))
        result = cursor.fetchone()
        if result:
            return result[0], json.loads(result[1]), result[2], result[3]
        return None, None, None, None

    def get_total_daily_income(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT SUM(income_per_day) FROM animals')
        result = cursor.fetchone()
        return result[0] if result[0] else 0

    def log_event(self, day, event_type, description, amount=0):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO events_log (day, event_type, description, amount) VALUES (?, ?, ?, ?)',
            (day, event_type, description, amount))
        self.conn.commit()

    def get_events_log(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute('SELECT day, event_type, description, amount FROM events_log ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()

    def save_game(self):
        self.conn.commit()

    def new_game(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM animals')
        cursor.execute('DELETE FROM events_log')
        cursor.execute('UPDATE game_state SET day=1, balance=125450, energy=100, reputation=0, level=1, experience=0, science_points=0 WHERE id=1')
        self.conn.commit()
