import os

print("=== НАСТРОЙКА ИГРЫ ZOO LEGACY v2 ===\n")

# 1. Удаляем лишние экраны
print("1. Удаляем ненужные файлы...")
files_to_delete = ['ui/screens/staff_screen.py', 'ui/screens/finance_screen.py']
for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"   Удален: {f}")

# 2. Удаляем старую базу (чтобы создать новую с игровой структурой)
if os.path.exists('zoo_legacy.db'):
    os.remove('zoo_legacy.db')
    print("   Удалена старая база данных")

print("\n2. Обновляем DatabaseManager (добавляем игровые поля)...")

db_code = '''import sqlite3
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
            rarity TEXT DEFAULT 'Обычное', income_per_day INTEGER DEFAULT 100)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY,
            day INTEGER DEFAULT 1,
            balance REAL DEFAULT 125450,
            energy INTEGER DEFAULT 100,
            max_energy INTEGER DEFAULT 100,
            reputation INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0)""")

        cursor.execute('SELECT COUNT(*) FROM game_state')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO game_state (id, day, balance, energy, max_energy, reputation, level, experience) VALUES (1, 1, 125450, 100, 100, 0, 1, 0)')

        cursor.execute("""CREATE TABLE IF NOT EXISTS events_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER, event_type TEXT, description TEXT, amount REAL)""")

        self.conn.commit()

    def get_game_state(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT day, balance, energy, max_energy, reputation, level, experience FROM game_state WHERE id = 1')
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

    def update_balance(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET balance = balance + ? WHERE id = 1', (amount,))
        self.conn.commit()

    def use_energy(self, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE game_state SET energy = MAX(0, energy - ?) WHERE id = 1', (amount,))
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

    def add_animal(self, animal, price=0):
        cursor = self.conn.cursor()
        genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
        cursor.execute('INSERT INTO animals (name, species, age, genetics, health, hunger, rarity, income_per_day) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger, animal.rarity, animal.income_per_day))
        if price > 0:
            self.update_balance(-price)
        self.conn.commit()
        return cursor.lastrowid

    def get_all_animals(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, species, age, health, hunger, rarity, income_per_day FROM animals')
        return cursor.fetchall()

    def get_animal_genetics(self, animal_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT species, genetics FROM animals WHERE id = ?', (animal_id,))
        result = cursor.fetchone()
        if result:
            return result[0], json.loads(result[1])
        return None, None

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

    def get_events_log(self, limit=20):
        cursor = self.conn.cursor()
        cursor.execute('SELECT day, event_type, description, amount FROM events_log ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()

    def save_game(self):
        self.conn.commit()

    def new_game(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM animals')
        cursor.execute('DELETE FROM events_log')
        cursor.execute('UPDATE game_state SET day=1, balance=125450, energy=100, reputation=0, level=1, experience=0 WHERE id=1')
        self.conn.commit()
'''

with open('database/db_manager.py', 'w', encoding='utf-8') as f:
    f.write(db_code)
print("   DatabaseManager обновлен")

print("\n3. Создаем главное меню (StartScreen)...")

start_screen_code = '''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class StartScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0a0a1a, stop:0.5 #1a1a3e, stop:1 #0f3460);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("ZOO LEGACY")
        title.setStyleSheet("font-size: 72px; font-weight: bold; color: #4CAF50; letter-spacing: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Генетический симулятор зоопарка")
        subtitle.setStyleSheet("font-size: 20px; color: #a0a0a0;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        btn_new = QPushButton("НОВАЯ ИГРА")
        btn_new.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50);
                color: white; padding: 20px 60px; font-size: 22px; font-weight: bold;
                border-radius: 15px; border: none; min-width: 300px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #66BB6A); }
        """)
        btn_new.clicked.connect(self._start_new_game)
        layout.addWidget(btn_new, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_continue = QPushButton("ПРОДОЛЖИТЬ")
        btn_continue.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #42A5F5);
                color: white; padding: 20px 60px; font-size: 22px; font-weight: bold;
                border-radius: 15px; border: none; min-width: 300px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #42A5F5, stop:1 #64B5F6); }
        """)
        btn_continue.clicked.connect(self._continue_game)
        layout.addWidget(btn_continue, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_settings = QPushButton("НАСТРОЙКИ")
        btn_settings.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #757575, stop:1 #9E9E9E);
                color: white; padding: 20px 60px; font-size: 22px; font-weight: bold;
                border-radius: 15px; border: none; min-width: 300px;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9E9E9E, stop:1 #BDBDBD); }
        """)
        btn_settings.clicked.connect(self._show_settings)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        footer = QLabel("v2.0 | 2026")
        footer.setStyleSheet("font-size: 12px; color: #666;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def _start_new_game(self):
        if self.parent:
            self.parent.start_new_game()

    def _continue_game(self):
        if self.parent:
            self.parent.continue_game()

    def _show_settings(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Настройки", "Настройки будут добавлены в следующей версии!")
'''

with open('ui/start_screen.py', 'w', encoding='utf-8') as f:
    f.write(start_screen_code)
print("   StartScreen создан")

print("\n4. Обновляем главное окно игры...")

main_window_code = '''from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
import random
from database.db_manager import DatabaseManager
from models.animal_catalog import ANIMAL_CATALOG
from ui.breeding_dialog import BreedingDialog
from ui.screens.catalog_screen import CatalogScreen

class MainWindow(QMainWindow):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.setWindowTitle("Zoo Legacy")
        self.resize(1400, 900)

        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a2e, stop:1 #16213e); }
            QLabel { color: #e8e8e8; font-family: Segoe UI, Arial, sans-serif; }
            QPushButton { border-radius: 12px; padding: 12px 20px; font-weight: bold; font-size: 14px; color: white; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); border: none; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #66BB6A); }
            QPushButton:disabled { background: #555; color: #888; }
            QListWidget { background-color: #0f3460; border: none; border-radius: 15px; }
            QListWidget::item { color: #e8e8e8; padding: 18px; border-bottom: 1px solid #1a1a2e; font-size: 15px; }
            QListWidget::item:selected { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); border-radius: 10px; }
        """)

        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        sidebar = QListWidget()
        sidebar.setMaximumWidth(220)
        sidebar.setMinimumWidth(220)
        sidebar.addItem("Мой зоопарк")
        sidebar.addItem("Каталог")
        sidebar.addItem("Лаборатория")
        sidebar.addItem("Журнал событий")
        sidebar.currentRowChanged.connect(self._switch_screen)
        sidebar.setStyleSheet("""
            QListWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0f3460, stop:1 #16213e); border: none; border-radius: 20px; }
            QListWidget::item { color: #e8e8e8; padding: 18px 22px; border-bottom: 1px solid #1a1a2e; font-size: 15px; border-radius: 10px; margin: 4px; }
            QListWidget::item:selected { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); font-weight: bold; }
        """)
        main_layout.addWidget(sidebar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")
        main_layout.addWidget(self.stack)

        self.map_screen = self._create_zoo_map()
        self.catalog_screen = CatalogScreen(self.db, self)
        self.breeding_screen = self._create_breeding_screen()
        self.events_screen = self._create_events_screen()

        for screen in [self.map_screen, self.catalog_screen, self.breeding_screen, self.events_screen]:
            self.stack.addWidget(screen)
        sidebar.setCurrentRow(0)

        self._update_header()

    def _update_header(self):
        state = self.db.get_game_state()
        if state:
            day, balance, energy, max_energy, reputation, level, experience = state
            self.balance_label.setText(f"Баланс: {balance:,.0f} RUB")
            self.day_label.setText(f"День: {day}")
            self.energy_label.setText(f"Энергия: {energy}/{max_energy}")
            self.level_label.setText(f"Уровень: {level}")
            income = self.db.get_total_daily_income()
            self.income_label.setText(f"+{income:,} RUB/день")

    def _create_zoo_map(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        header = QFrame()
        header.setStyleSheet("QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); border-radius: 15px; padding: 20px; }")
        header_layout = QHBoxLayout(header)

        title = QLabel("МОЙ ЗООПАРК")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        info_frame = QFrame()
        info_frame.setStyleSheet("background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px 20px;")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(20)

        self.day_label = QLabel("День: 1")
        self.day_label.setStyleSheet("font-size: 14px; color: #90EE90; font-weight: bold;")
        info_layout.addWidget(self.day_label)

        self.balance_label = QLabel("Баланс: 0 RUB")
        self.balance_label.setStyleSheet("font-size: 14px; color: #FFD700; font-weight: bold;")
        info_layout.addWidget(self.balance_label)

        self.energy_label = QLabel("Энергия: 100/100")
        self.energy_label.setStyleSheet("font-size: 14px; color: #42A5F5; font-weight: bold;")
        info_layout.addWidget(self.energy_label)

        self.level_label = QLabel("Уровень: 1")
        self.level_label.setStyleSheet("font-size: 14px; color: #FF9800; font-weight: bold;")
        info_layout.addWidget(self.level_label)

        self.income_label = QLabel("+0 RUB/день")
        self.income_label.setStyleSheet("font-size: 14px; color: #90EE90; font-weight: bold;")
        info_layout.addWidget(self.income_label)

        header_layout.addWidget(info_frame)
        layout.addWidget(header)

        btn_next_day = QPushButton("СЛЕДУЮЩИЙ ДЕНЬ")
        btn_next_day.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF9800, stop:1 #FFB74D);
                color: white; padding: 15px 30px; font-size: 18px; font-weight: bold;
                border-radius: 12px; border: none;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFB74D, stop:1 #FFCC80); }
        """)
        btn_next_day.clicked.connect(self._next_day)
        layout.addWidget(btn_next_day)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.animals_grid = QGridLayout(scroll_content)
        self.animals_grid.setSpacing(20)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        self._refresh_zoo_map()
        return widget

    def _next_day(self):
        day = self.db.get_day()
        income = self.db.get_total_daily_income()
        expenses = len(self.db.get_all_animals()) * 50

        self.db.update_balance(income - expenses)
        self.db.next_day()
        self.db.add_experience(10)

        event_msg = f"День {day} завершен!\n\nДоход от животных: +{income:,} RUB\nРасходы на содержание: -{expenses:,} RUB\nЧистая прибыль: {income - expenses:,} RUB\n\nЭнергия восстановлена!"

        if random.random() < 0.3:
            event = random.choice([
                ("Пожертвование", 5000, "Меценат пожертвовал 5000 RUB!"),
                ("Болезнь", -2000, "Одно животное заболело. Лечение: -2000 RUB"),
                ("Мутация", 0, "У одного животного произошла спонтанная мутация!"),
                ("Звездный гость", 10000, "Известный блогер посетил зоопарк! +10000 RUB"),
            ])
            self.db.update_balance(event[1])
            self.db.log_event(day + 1, event[0], event[2], event[1])
            event_msg += f"\n\nСОБЫТИЕ: {event[2]}"

        self.db.log_event(day + 1, "Конец дня", f"Доход: {income}, Расходы: {expenses}", income - expenses)
        self._update_header()
        self._refresh_zoo_map()
        QMessageBox.information(self, f"День {day} завершен", event_msg)

    def _refresh_zoo_map(self):
        while self.animals_grid.count():
            item = self.animals_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        animals = self.db.get_all_animals()
        if not animals:
            empty = QLabel("У вас пока нет животных. Зайдите в Каталог, чтобы купить первое!")
            empty.setStyleSheet("font-size: 20px; color: #888; padding: 50px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.animals_grid.addWidget(empty, 0, 0)
            return
        for idx, animal_data in enumerate(animals):
            card = self._create_animal_card(animal_data)
            self.animals_grid.addWidget(card, idx // 3, idx % 3)

    def _create_animal_card(self, animal_data):
        species = animal_data[2]
        data = ANIMAL_CATALOG.get(species, {"image": "", "cat": "Неизвестно", "emoji": "?"})
        rarity = animal_data[6] if len(animal_data) > 6 else "Обычное"
        income = animal_data[7] if len(animal_data) > 7 else 100

        rarity_colors = {
            "Обычное": "#808080",
            "Необычное": "#4CAF50",
            "Редкое": "#2196F3",
            "Эпическое": "#9C27B0",
            "Легендарное": "#FFD700"
        }
        rarity_color = rarity_colors.get(rarity, "#808080")

        card = QFrame()
        card.setFixedHeight(380)
        card.setStyleSheet(f"QFrame {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16213e, stop:1 #0f3460); border-radius: 15px; border: 3px solid {rarity_color}; }}")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setFixedSize(400, 220)
        photo_label.setStyleSheet(f"QLabel {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {rarity_color}33, stop:1 #16213e); border-top-left-radius: 15px; border-top-right-radius: 15px; }}")
        img_path = data.get("image", "")
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            scaled = pixmap.scaled(400, 220, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(scaled)
        else:
            photo_label.setText(data.get("emoji", "?"))
            photo_label.setStyleSheet(f"font-size: 100px; color: {rarity_color}; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e); border-top-left-radius: 15px; border-top-right-radius: 15px;")
        layout.addWidget(photo_label)

        info = QWidget()
        info.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(20, 15, 20, 15)
        info_layout.setSpacing(8)

        name = QLabel(animal_data[1])
        name.setStyleSheet("font-size: 20px; font-weight: bold; color: #e8e8e8;")
        info_layout.addWidget(name)

        rarity_label = QLabel(f"Редкость: {rarity}")
        rarity_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {rarity_color};")
        info_layout.addWidget(rarity_label)

        age_label = QLabel(f"{data.get('cat', '')} | {animal_data[3]} лет")
        age_label.setStyleSheet("font-size: 13px; color: #a0a0a0;")
        info_layout.addWidget(age_label)

        health = animal_data[4]
        health_color = "#4CAF50" if health > 70 else "#FFA500" if health > 40 else "#EF4444"
        health_label = QLabel(f"Здоровье: {health}%")
        health_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {health_color};")
        info_layout.addWidget(health_label)

        hunger = animal_data[5]
        hunger_color = "#4CAF50" if hunger < 30 else "#FFA500" if hunger < 60 else "#EF4444"
        hunger_label = QLabel(f"Голод: {hunger}%")
        hunger_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {hunger_color};")
        info_layout.addWidget(hunger_label)

        income_label = QLabel(f"+{income:,} RUB/день")
        income_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #90EE90;")
        info_layout.addWidget(income_label)

        layout.addWidget(info)
        return card

    def _create_breeding_screen(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)

        title = QLabel("ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #9C27B0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Скрещивайте животных для получения редкого потомства!\nТребование: 2 животных одного вида, возраст 2+ года")
        desc.setStyleSheet("font-size: 16px; color: #a0a0a0;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        btn = QPushButton("ОТКРЫТЬ ЛАБОРАТОРИЮ")
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9C27B0, stop:1 #BA68C8);
                color: white; padding: 20px 50px; font-size: 20px; font-weight: bold;
                border-radius: 15px; border: none;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #BA68C8, stop:1 #CE93D8); }
        """)
        btn.clicked.connect(self._open_breeding)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return widget

    def _open_breeding(self):
        energy = self.db.get_energy()
        if energy < 30:
            QMessageBox.warning(self, "Недостаточно энергии", "Для скрещивания нужно 30 энергии. Перейдите к следующему дню!")
            return
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self.db.use_energy(30)
            self.db.add_experience(25)
            self._update_header()
            self._refresh_zoo_map()

    def _create_events_screen(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title = QLabel("ЖУРНАЛ СОБЫТИЙ")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)

        events = self.db.get_events_log(50)
        if not events:
            no_events = QLabel("Пока нет событий. Начните играть!")
            no_events.setStyleSheet("font-size: 16px; color: #888; padding: 30px;")
            content_layout.addWidget(no_events)
        else:
            for day, event_type, description, amount in events:
                event_frame = QFrame()
                color = "#4CAF50" if amount >= 0 else "#EF4444"
                event_frame.setStyleSheet(f"QFrame {{ background: rgba(255,255,255,0.05); border-left: 4px solid {color}; border-radius: 8px; padding: 12px; }}")
                event_layout = QHBoxLayout(event_frame)
                day_label = QLabel(f"День {day}")
                day_label.setStyleSheet("font-size: 13px; color: #888; min-width: 70px;")
                event_layout.addWidget(day_label)
                type_label = QLabel(event_type)
                type_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color}; min-width: 120px;")
                event_layout.addWidget(type_label)
                desc_label = QLabel(description)
                desc_label.setStyleSheet("font-size: 14px; color: #e8e8e8;")
                desc_label.setWordWrap(True)
                event_layout.addWidget(desc_label)
                if amount != 0:
                    amount_label = QLabel(f"{amount:+,.0f} RUB")
                    amount_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color};")
                    event_layout.addWidget(amount_label)
                content_layout.addWidget(event_frame)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        return widget

    def _switch_screen(self, index):
        self.stack.setCurrentIndex(index)

    def refresh_all(self):
        self._update_header()
        self._refresh_zoo_map()
'''

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)
print("   MainWindow обновлен")

print("\n5. Обновляем app.py (точка входа)...")

app_code = '''import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database.db_manager import DatabaseManager
from ui.start_screen import StartScreen
from ui.main_window import MainWindow

class GameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy")
        self.resize(1400, 900)
        self.setStyleSheet("QMainWindow { background: #0a0a1a; }")

        self.db = DatabaseManager()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.start_screen = StartScreen(self)
        self.stack.addWidget(self.start_screen)

        self.game_window = None
        self.stack.setCurrentWidget(self.start_screen)

    def start_new_game(self):
        self.db.new_game()
        self._show_game()

    def continue_game(self):
        state = self.db.get_game_state()
        if not state:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Нет сохранения", "Сохраненная игра не найдена. Начните новую игру!")
            return
        self._show_game()

    def _show_game(self):
        if self.game_window is None:
            self.game_window = MainWindow(self.db)
            self.stack.addWidget(self.game_window)
        else:
            self.game_window.refresh_all()
        self.stack.setCurrentWidget(self.game_window)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    game = GameApp()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("   app.py обновлен")

print("\n=== НАСТРОЙКА ЗАВЕРШЕНА ===")
print("Запустите: py app.py")