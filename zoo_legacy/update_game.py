import os

print("=== ОБНОВЛЕНИЕ ИГРЫ ===\n")

# 1. Обновляем DatabaseManager - добавляем поля для инбридинга и реагентов
print("1. Обновляем DatabaseManager...")
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
            rarity TEXT DEFAULT 'Обычное', income_per_day INTEGER DEFAULT 100,
            generation INTEGER DEFAULT 1, parent_id INTEGER DEFAULT 0)""")

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

    def add_animal(self, animal, price=0, parent_id=0):
        cursor = self.conn.cursor()
        genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
        cursor.execute('INSERT INTO animals (name, species, age, genetics, health, hunger, rarity, income_per_day, generation, parent_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger, animal.rarity, animal.income_per_day, 1, parent_id))
        if price > 0:
            self.update_balance(-price)
        self.conn.commit()
        return cursor.lastrowid

    def get_all_animals(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, species, age, health, hunger, rarity, income_per_day, generation, parent_id FROM animals')
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
'''

with open('database/db_manager.py', 'w', encoding='utf-8') as f:
    f.write(db_code)
print("   DatabaseManager обновлен")

# 2. Обновляем лабораторию скрещивания
print("\n2. Обновляем лабораторию скрещивания...")
breeding_code = '''from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QProgressBar, QMessageBox, QFrame, QGroupBox, QCheckBox
from PyQt6.QtCore import Qt, QTimer
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode
import random

class BreedingDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.setWindowTitle("Лаборатория скрещивания")
        self.resize(700, 600)
        self.setModal(True)
        self.setObjectName("breedingDialog")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("ГЕНЕТИЧЕСКАЯ ЛАБОРАТОРИЯ")
        title.setProperty("class", "breeding-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        parents_layout = QHBoxLayout()

        self.father_combo = QComboBox()
        self.father_combo.setProperty("class", "parent-select")
        self.mother_combo = QComboBox()
        self.mother_combo.setProperty("class", "parent-select")

        self.load_animals_to_combos()

        father_group = QGroupBox("Родитель 1 (Отец)")
        father_group.setProperty("class", "parent-group")
        father_layout = QVBoxLayout(father_group)
        father_layout.addWidget(self.father_combo)
        self.father_genes_label = QLabel("Гены: -")
        self.father_genes_label.setProperty("class", "genes-display")
        father_layout.addWidget(self.father_genes_label)
        parents_layout.addWidget(father_group)

        mother_group = QGroupBox("Родитель 2 (Мать)")
        mother_group.setProperty("class", "parent-group")
        mother_layout = QVBoxLayout(mother_group)
        mother_layout.addWidget(self.mother_combo)
        self.mother_genes_label = QLabel("Гены: -")
        self.mother_genes_label.setProperty("class", "genes-display")
        mother_layout.addWidget(self.mother_genes_label)
        parents_layout.addWidget(mother_group)

        layout.addLayout(parents_layout)

        self.father_combo.currentIndexChanged.connect(self.update_genes_display)
        self.mother_combo.currentIndexChanged.connect(self.update_genes_display)

        match_group = QGroupBox("Совместимость")
        match_group.setProperty("class", "match-group")
        match_layout = QVBoxLayout(match_group)
        self.match_bar = QProgressBar()
        self.match_bar.setProperty("class", "match-bar")
        self.match_bar.setValue(0)
        match_layout.addWidget(self.match_bar)
        self.match_label = QLabel("Выберите родителей")
        self.match_label.setProperty("class", "match-label")
        match_layout.addWidget(self.match_label)
        layout.addWidget(match_group)

        reagents_group = QGroupBox("Химические реагенты")
        reagents_group.setProperty("class", "reagents-group")
        reagents_layout = QVBoxLayout(reagents_group)

        self.reagent_combo = QComboBox()
        self.reagent_combo.addItem("Без реагента", None)
        self.reagent_combo.addItem("Радиационный мутаген (+40% мутаций, -30 HP)", "mutagen")
        self.reagent_combo.addItem("Янтарный стабилизатор (0% мутаций, без дефектов)", "stabilizer")
        self.reagent_combo.addItem("Питательный субстрат (+20 HP)", "substrate")
        self.reagent_combo.setProperty("class", "reagent-select")
        reagents_layout.addWidget(self.reagent_combo)

        self.reagent_info = QLabel("Выберите реагент для изменения параметров скрещивания")
        self.reagent_info.setProperty("class", "reagent-info")
        reagents_layout.addWidget(self.reagent_info)
        layout.addWidget(reagents_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setProperty("class", "breeding-progress")
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setProperty("class", "breeding-status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        self.btn_breed = QPushButton("ЗАПУСТИТЬ СКРЕЩИВАНИЕ")
        self.btn_breed.setProperty("class", "btn-breed")
        self.btn_breed.clicked.connect(self.start_breeding)
        btn_layout.addWidget(self.btn_breed)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setProperty("class", "btn-cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def load_animals_to_combos(self):
        animals = self.db.get_all_animals()
        self.father_combo.clear()
        self.mother_combo.clear()
        self.father_combo.addItem("Выберите...", None)
        self.mother_combo.addItem("Выберите...", None)
        for animal in animals:
            display_name = f"#{animal[0]} {animal[1]} ({animal[2]}, {animal[3]} лет)"
            self.father_combo.addItem(display_name, animal[0])
            self.mother_combo.addItem(display_name, animal[0])

    def update_genes_display(self):
        father_id = self.father_combo.currentData()
        mother_id = self.mother_combo.currentData()

        if father_id:
            f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
            genes_str = ", ".join([f"{k}: {v}" for k, v in f_genetics.items()])
            self.father_genes_label.setText(f"Гены: {genes_str}")
        else:
            self.father_genes_label.setText("Гены: -")

        if mother_id:
            m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)
            genes_str = ", ".join([f"{k}: {v}" for k, v in m_genetics.items()])
            self.mother_genes_label.setText(f"Гены: {genes_str}")
        else:
            self.mother_genes_label.setText("Гены: -")

        if father_id and mother_id:
            if father_id == mother_id:
                self.match_bar.setValue(0)
                self.match_label.setText("Нельзя скрестить животное само с собой!")
            else:
                f_species, _, _, _ = self.db.get_animal_genetics(father_id)
                m_species, _, _, _ = self.db.get_animal_genetics(mother_id)
                if f_species == m_species:
                    self.match_bar.setValue(85)
                    self.match_label.setText("Высокая совместимость (один вид)")
                else:
                    self.match_bar.setValue(25)
                    self.match_label.setText("Низкая совместимость (разные виды)")
        else:
            self.match_bar.setValue(0)
            self.match_label.setText("Выберите родителей")

    def start_breeding(self):
        father_id = self.father_combo.currentData()
        mother_id = self.mother_combo.currentData()

        if not father_id or not mother_id:
            QMessageBox.warning(self, "Ошибка", "Выберите обоих родителей!")
            return

        if father_id == mother_id:
            QMessageBox.warning(self, "Ошибка", "Нельзя скрестить животное само с собой!")
            return

        f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
        m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)

        if f_species != m_species:
            QMessageBox.warning(self, "Несовместимость", f"{f_species} и {m_species} не могут быть скрещены!")
            return

        energy = self.db.get_energy()
        if energy < 30:
            QMessageBox.warning(self, "Недостаточно энергии", "Нужно 30 энергии!")
            return

        self.btn_breed.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_value = 0
        self.progress_bar.setValue(0)
        self.status_label.setText("Анализ генетического материала...")
        self.timer.start(50)

    def update_progress(self):
        self.progress_value += 2
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value == 30:
            self.status_label.setText("Комбинирование генов...")
        elif self.progress_value == 60:
            self.status_label.setText("Применение реагентов...")
        elif self.progress_value == 90:
            self.status_label.setText("Инкубация эмбриона...")
        if self.progress_value >= 100:
            self.timer.stop()
            self.finish_breeding()

    def finish_breeding(self):
        father_id = self.father_combo.currentData()
        f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
        m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)

        try:
            father_genes = GeneticCode()
            mother_genes = GeneticCode()

            for g_name, g_val in f_genetics.items():
                father_genes.add_gene(Gene(g_name, g_val[0].upper(), g_val[1].lower()))

            for g_name, g_val in m_genetics.items():
                mother_genes.add_gene(Gene(g_name, g_val[0].upper(), g_val[1].lower()))

            reagent = self.reagent_combo.currentData()
            mutation_chance = 0.05
            health_bonus = 0
            has_defect = False

            if reagent == "mutagen":
                mutation_chance = 0.4
                health_bonus = -30
                self.db.log_event(self.db.get_day(), "Мутаген", "Использован радиационный мутаген", 0)
            elif reagent == "stabilizer":
                mutation_chance = 0.0
                self.db.log_event(self.db.get_day(), "Стабилизатор", "Использован янтарный стабилизатор", 0)
            elif reagent == "substrate":
                health_bonus = 20
                self.db.log_event(self.db.get_day(), "Субстрат", "Использован питательный субстрат", 0)

            offspring_genetics = father_genes.combine(mother_genes)
            offspring_genetics.mutate_all(mutation_chance)

            if f_parent == mother_id or m_parent == father_id:
                if random.random() < 0.3:
                    has_defect = True
                    self.db.log_event(self.db.get_day(), "Инбридинг", "Обнаружен генетический дефект!", 0)

            offspring = ZooAnimal(f_species, 0, offspring_genetics)
            offspring.feed(20)

            if has_defect:
                offspring._Animal__health = max(10, offspring.health - 30)

            if health_bonus != 0:
                offspring._Animal__health = min(100, max(0, offspring.health + health_bonus))

            self.db.add_animal(offspring, parent_id=father_id)
            self.db.use_energy(30)
            self.db.add_science_points(15)
            self.db.add_experience(25)
            self.db.log_event(self.db.get_day(), "Скрещивание", f"Получен потомок {f_species}", 0)

            self.status_label.setText("Успешно!")
            QMessageBox.information(self, "Потомство получено!", f"Родился {f_species}!\\nРедкость: {offspring.rarity}")
            self.accept()

        except Exception as e:
            self.status_label.setText("Ошибка")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать потомство: {e}")
            self.btn_breed.setEnabled(True)
            self.progress_bar.setVisible(False)
'''

with open('ui/breeding_dialog.py', 'w', encoding='utf-8') as f:
    f.write(breeding_code)
print("   Лаборатория обновлена")

# 3. Обновляем main_window.py - добавляем кнопку паузы и исправляем журнал
print("\n3. Обновляем главное окно...")
main_window_lines = [
"from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout",
"from PyQt6.QtCore import Qt",
"from PyQt6.QtGui import QPixmap",
"import os",
"import random",
"from database.db_manager import DatabaseManager",
"from models.animal_catalog import ANIMAL_CATALOG",
"from ui.breeding_dialog import BreedingDialog",
"from ui.screens.catalog_screen import CatalogScreen",
"",
"class MainWindow(QMainWindow):",
"    def __init__(self, db: DatabaseManager):",
"        super().__init__()",
"        self.db = db",
"        self.setWindowTitle('Zoo Legacy')",
"        self.resize(1400, 900)",
"        self.setObjectName('gameWindow')",
"        central_widget = QWidget()",
"        central_widget.setObjectName('centralWidget')",
"        self.setCentralWidget(central_widget)",
"        main_layout = QHBoxLayout(central_widget)",
"        main_layout.setContentsMargins(20, 20, 20, 20)",
"        main_layout.setSpacing(20)",
"        sidebar = QListWidget()",
"        sidebar.setObjectName('sidebar')",
"        sidebar.setMaximumWidth(220)",
"        sidebar.setMinimumWidth(220)",
"        sidebar.addItem('Мой зоопарк')",
"        sidebar.addItem('Каталог')",
"        sidebar.addItem('Лаборатория')",
"        sidebar.addItem('Журнал событий')",
"        sidebar.currentRowChanged.connect(self._switch_screen)",
"        main_layout.addWidget(sidebar)",
"        self.stack = QStackedWidget()",
"        self.stack.setObjectName('contentStack')",
"        main_layout.addWidget(self.stack)",
"        self.map_screen = self._create_zoo_map()",
"        self.catalog_screen = CatalogScreen(self.db, self)",
"        self.breeding_screen = self._create_breeding_screen()",
"        self.events_screen = self._create_events_screen()",
"        for screen in [self.map_screen, self.catalog_screen, self.breeding_screen, self.events_screen]:",
"            self.stack.addWidget(screen)",
"        sidebar.setCurrentRow(0)",
"        self._update_header()",
"",
"    def _update_header(self):",
"        state = self.db.get_game_state()",
"        if state:",
"            day, balance, energy, max_energy, reputation, level, experience, science = state",
"            self.day_label.setText(f'День: {day}')",
"            self.balance_label.setText(f'Баланс: {balance:,.0f} RUB')",
"            self.energy_label.setText(f'Энергия: {energy}/{max_energy}')",
"            self.level_label.setText(f'Уровень: {level}')",
"            self.science_label.setText(f'Наука: {science}')",
"            income = self.db.get_total_daily_income()",
"            self.income_label.setText(f'+{income:,} RUB/день')",
"",
"    def _create_zoo_map(self):",
"        widget = QWidget()",
"        widget.setObjectName('zooMapScreen')",
"        layout = QVBoxLayout(widget)",
"        layout.setContentsMargins(25, 25, 25, 25)",
"        layout.setSpacing(20)",
"        header = QFrame()",
"        header.setProperty('class', 'header-frame')",
"        header_layout = QHBoxLayout(header)",
"        title = QLabel('МОЙ ЗООПАРК')",
"        title.setProperty('class', 'section-title')",
"        header_layout.addWidget(title)",
"        header_layout.addStretch()",
"        btn_pause = QPushButton('В МЕНЮ')",
"        btn_pause.setProperty('class', 'btn-pause')",
"        btn_pause.clicked.connect(self._go_to_menu)",
"        header_layout.addWidget(btn_pause)",
"        info_frame = QFrame()",
"        info_frame.setProperty('class', 'info-panel')",
"        info_layout = QHBoxLayout(info_frame)",
"        info_layout.setSpacing(15)",
"        self.day_label = QLabel('День: 1')",
"        self.day_label.setProperty('class', 'stat-label day')",
"        info_layout.addWidget(self.day_label)",
"        self.balance_label = QLabel('Баланс: 0 RUB')",
"        self.balance_label.setProperty('class', 'stat-label balance')",
"        info_layout.addWidget(self.balance_label)",
"        self.energy_label = QLabel('Энергия: 100/100')",
"        self.energy_label.setProperty('class', 'stat-label energy')",
"        info_layout.addWidget(self.energy_label)",
"        self.level_label = QLabel('Уровень: 1')",
"        self.level_label.setProperty('class', 'stat-label level')",
"        info_layout.addWidget(self.level_label)",
"        self.science_label = QLabel('Наука: 0')",
"        self.science_label.setProperty('class', 'stat-label science')",
"        info_layout.addWidget(self.science_label)",
"        self.income_label = QLabel('+0 RUB/день')",
"        self.income_label.setProperty('class', 'stat-label income')",
"        info_layout.addWidget(self.income_label)",
"        header_layout.addWidget(info_frame)",
"        layout.addWidget(header)",
"        btn_next_day = QPushButton('СЛЕДУЮЩИЙ ДЕНЬ')",
"        btn_next_day.setProperty('class', 'btn-next-day')",
"        btn_next_day.clicked.connect(self._next_day)",
"        layout.addWidget(btn_next_day)",
"        scroll = QScrollArea()",
"        scroll.setObjectName('animalsScroll')",
"        scroll_content = QWidget()",
"        scroll_content.setObjectName('animalsContainer')",
"        self.animals_grid = QGridLayout(scroll_content)",
"        self.animals_grid.setSpacing(20)",
"        scroll.setWidget(scroll_content)",
"        scroll.setWidgetResizable(True)",
"        layout.addWidget(scroll)",
"        self._refresh_zoo_map()",
"        return widget",
"",
"    def _go_to_menu(self):",
"        reply = QMessageBox.question(self, 'Выход в меню', 'Сохранить игру и выйти в главное меню?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)",
"        if reply == QMessageBox.StandardButton.Yes:",
"            self.db.save_game()",
"            if self.parent():",
"                self.parent().stack.setCurrentWidget(self.parent().start_screen)",
"",
"    def _next_day(self):",
"        day = self.db.get_day()",
"        income = self.db.get_total_daily_income()",
"        animals = self.db.get_all_animals()",
"        expenses = len(animals) * 50",
"        self.db.update_balance(income - expenses)",
"        self.db.next_day()",
"        self.db.add_experience(10)",
"        msg_lines = []",
"        msg_lines.append(f'День {day} завершен!')",
"        msg_lines.append('')",
"        msg_lines.append(f'Доход от животных: +{income:,} RUB')",
"        msg_lines.append(f'Расходы на содержание: -{expenses:,} RUB')",
"        msg_lines.append(f'Чистая прибыль: {income - expenses:,} RUB')",
"        msg_lines.append('')",
"        msg_lines.append('Энергия восстановлена!')",
"        if random.random() < 0.3:",
"            event = random.choice([",
"                ('Пожертвование', 5000, 'Меценат пожертвовал 5000 RUB!'),",
"                ('Болезнь', -2000, 'Одно животное заболело. Лечение: -2000 RUB'),",
"                ('Мутация', 0, 'У одного животного произошла спонтанная мутация!'),",
"                ('Звездный гость', 10000, 'Известный блогер посетил зоопарк! +10000 RUB'),",
"            ])",
"            self.db.update_balance(event[1])",
"            self.db.log_event(day + 1, event[0], event[2], event[1])",
"            msg_lines.append('')",
"            msg_lines.append(f'СОБЫТИЕ: {event[2]}')",
"        self.db.log_event(day + 1, 'Конец дня', f'Доход: {income}, Расходы: {expenses}', income - expenses)",
"        self._update_header()",
"        self._refresh_zoo_map()",
"        if hasattr(self, 'events_screen'):",
"            self._update_events_screen()",
"        QMessageBox.information(self, f'День {day} завершен', '\\n'.join(msg_lines))",
"",
"    def _refresh_zoo_map(self):",
"        while self.animals_grid.count():",
"            item = self.animals_grid.takeAt(0)",
"            if item.widget():",
"                item.widget().deleteLater()",
"        animals = self.db.get_all_animals()",
"        if not animals:",
"            empty = QLabel('У вас пока нет животных. Зайдите в Каталог, чтобы купить первое!')",
"            empty.setProperty('class', 'empty-message')",
"            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)",
"            self.animals_grid.addWidget(empty, 0, 0)",
"            return",
"        for idx, animal_data in enumerate(animals):",
"            card = self._create_animal_card(animal_data)",
"            self.animals_grid.addWidget(card, idx // 3, idx % 3)",
"",
"    def _create_animal_card(self, animal_data):",
"        species = animal_data[2]",
"        data = ANIMAL_CATALOG.get(species, {'image': '', 'cat': 'Неизвестно', 'emoji': '?'})",
"        rarity = animal_data[6] if len(animal_data) > 6 else 'Обычное'",
"        income = animal_data[7] if len(animal_data) > 7 else 100",
"        rarity_classes = {'Обычное': 'rarity-common', 'Необычное': 'rarity-uncommon', 'Редкое': 'rarity-rare', 'Эпическое': 'rarity-epic', 'Легендарное': 'rarity-legendary'}",
"        rarity_class = rarity_classes.get(rarity, 'rarity-common')",
"        card = QFrame()",
"        card.setProperty('class', f'animal-card {rarity_class}')",
"        card.setFixedHeight(380)",
"        layout = QVBoxLayout(card)",
"        layout.setContentsMargins(0, 0, 0, 0)",
"        layout.setSpacing(0)",
"        photo_label = QLabel()",
"        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)",
"        photo_label.setFixedSize(400, 220)",
"        photo_label.setProperty('class', 'animal-photo')",
"        img_path = data.get('image', '')",
"        if img_path and os.path.exists(img_path):",
"            pixmap = QPixmap(img_path)",
"            scaled = pixmap.scaled(400, 220, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)",
"            photo_label.setPixmap(scaled)",
"        else:",
"            photo_label.setText(data.get('emoji', '?'))",
"        layout.addWidget(photo_label)",
"        info = QWidget()",
"        info.setProperty('class', 'animal-info')",
"        info_layout = QVBoxLayout(info)",
"        info_layout.setContentsMargins(20, 15, 20, 15)",
"        info_layout.setSpacing(8)",
"        name = QLabel(animal_data[1])",
"        name.setProperty('class', 'animal-name')",
"        info_layout.addWidget(name)",
"        rarity_label = QLabel(f'Редкость: {rarity}')",
"        rarity_label.setProperty('class', f'animal-rarity {rarity_class}')",
"        info_layout.addWidget(rarity_label)",
"        age_label = QLabel(f\"{data.get('cat', '')} | {animal_data[3]} лет\")",
"        age_label.setProperty('class', 'animal-species')",
"        info_layout.addWidget(age_label)",
"        health = animal_data[4]",
"        health_label = QLabel(f'Здоровье: {health}%')",
"        health_label.setProperty('class', 'animal-health')",
"        info_layout.addWidget(health_label)",
"        hunger = animal_data[5]",
"        hunger_label = QLabel(f'Голод: {hunger}%')",
"        hunger_label.setProperty('class', 'animal-hunger')",
"        info_layout.addWidget(hunger_label)",
"        income_label = QLabel(f'+{income:,} RUB/день')",
"        income_label.setProperty('class', 'animal-income')",
"        info_layout.addWidget(income_label)",
"        layout.addWidget(info)",
"        return card",
"",
"    def _create_breeding_screen(self):",
"        widget = QWidget()",
"        widget.setObjectName('breedingScreen')",
"        layout = QVBoxLayout(widget)",
"        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)",
"        layout.setSpacing(25)",
"        title = QLabel('ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ')",
"        title.setProperty('class', 'section-title breeding')",
"        title.setAlignment(Qt.AlignmentFlag.AlignCenter)",
"        layout.addWidget(title)",
"        desc = QLabel('Скрещивайте животных для получения редкого потомства!\\nТребование: 2 животных одного вида, возраст 2+ года')",
"        desc.setProperty('class', 'breeding-desc')",
"        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)",
"        layout.addWidget(desc)",
"        btn = QPushButton('ОТКРЫТЬ ЛАБОРАТОРИЮ')",
"        btn.setProperty('class', 'btn-breeding')",
"        btn.clicked.connect(self._open_breeding)",
"        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)",
"        return widget",
"",
"    def _open_breeding(self):",
"        energy = self.db.get_energy()",
"        if energy < 30:",
"            QMessageBox.warning(self, 'Недостаточно энергии', 'Для скрещивания нужно 30 энергии. Перейдите к следующему дню!')",
"            return",
"        dialog = BreedingDialog(self.db, self)",
"        if dialog.exec():",
"            self._update_header()",
"            self._refresh_zoo_map()",
"",
"    def _create_events_screen(self):",
"        widget = QWidget()",
"        widget.setObjectName('eventsScreen')",
"        self.events_layout = QVBoxLayout(widget)",
"        self.events_layout.setContentsMargins(25, 25, 25, 25)",
"        self.events_layout.setSpacing(20)",
"        title = QLabel('ЖУРНАЛ СОБЫТИЙ')",
"        title.setProperty('class', 'section-title events')",
"        self.events_layout.addWidget(title)",
"        self.events_scroll = QScrollArea()",
"        self.events_scroll.setObjectName('eventsScroll')",
"        self.events_content = QWidget()",
"        self.events_content.setObjectName('eventsContainer')",
"        self.events_content_layout = QVBoxLayout(self.events_content)",
"        self.events_content_layout.setSpacing(10)",
"        self.events_scroll.setWidget(self.events_content)",
"        self.events_scroll.setWidgetResizable(True)",
"        self.events_layout.addWidget(self.events_scroll)",
"        self._update_events_screen()",
"        return widget",
"",
"    def _update_events_screen(self):",
"        while self.events_content_layout.count():",
"            item = self.events_content_layout.takeAt(0)",
"            if item.widget():",
"                item.widget().deleteLater()",
"        events = self.db.get_events_log(50)",
"        if not events:",
"            no_events = QLabel('Пока нет событий. Начните играть!')",
"            no_events.setProperty('class', 'empty-message')",
"            self.events_content_layout.addWidget(no_events)",
"        else:",
"            for day, event_type, description, amount in events:",
"                event_frame = QFrame()",
"                event_frame.setProperty('class', 'event-item')",
"                event_layout = QHBoxLayout(event_frame)",
"                day_label = QLabel(f'День {day}')",
"                day_label.setProperty('class', 'event-day')",
"                event_layout.addWidget(day_label)",
"                type_label = QLabel(event_type)",
"                type_label.setProperty('class', 'event-type')",
"                event_layout.addWidget(type_label)",
"                desc_label = QLabel(description)",
"                desc_label.setProperty('class', 'event-desc')",
"                desc_label.setWordWrap(True)",
"                event_layout.addWidget(desc_label)",
"                if amount != 0:",
"                    amount_label = QLabel(f'{amount:+,.0f} RUB')",
"                    amount_label.setProperty('class', 'event-amount')",
"                    event_layout.addWidget(amount_label)",
"                self.events_content_layout.addWidget(event_frame)",
"        self.events_content_layout.addStretch()",
"",
"    def _switch_screen(self, index):",
"        self.stack.setCurrentIndex(index)",
"        if index == 3:",
"            self._update_events_screen()",
"",
"    def refresh_all(self):",
"        self._update_header()",
"        self._refresh_zoo_map()",
]

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(main_window_lines))
print("   MainWindow обновлен")

# 4. Обновляем style.qss
print("\n4. Обновляем стили...")
style_additions = """

/* === ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ === */

QDialog#breedingDialog {
    background-color: #0b0f19;
}

QLabel[class="breeding-title"] {
    font-size: 28px;
    font-weight: bold;
    color: #9C27B0;
}

QGroupBox[class="parent-group"] {
    color: #00e5ff;
    font-size: 14px;
    font-weight: bold;
    border: 2px solid #1a2436;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QComboBox[class="parent-select"] {
    background-color: #1a2436;
    color: #ffffff;
    border: 1px solid #38bdf8;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
}

QLabel[class="genes-display"] {
    font-size: 12px;
    color: #8da2fb;
    font-family: "Consolas", monospace;
    padding: 5px;
}

QGroupBox[class="match-group"] {
    color: #00ff88;
    font-size: 14px;
    font-weight: bold;
    border: 2px solid #1a2436;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QProgressBar[class="match-bar"] {
    border: 1px solid #1a2436;
    border-radius: 4px;
    text-align: center;
    background-color: #111827;
    color: #ffffff;
    min-height: 20px;
}

QProgressBar[class="match-bar"]::chunk {
    background-color: #00ff88;
}

QLabel[class="match-label"] {
    font-size: 13px;
    color: #00e5ff;
    padding: 5px;
}

QGroupBox[class="reagents-group"] {
    color: #FF9800;
    font-size: 14px;
    font-weight: bold;
    border: 2px solid #1a2436;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QComboBox[class="reagent-select"] {
    background-color: #1a2436;
    color: #ffffff;
    border: 1px solid #FF9800;
    border-radius: 4px;
    padding: 8px;
    font-size: 13px;
}

QLabel[class="reagent-info"] {
    font-size: 12px;
    color: #a0a0a0;
    padding: 5px;
}

QProgressBar[class="breeding-progress"] {
    border: 1px solid #1a2436;
    border-radius: 4px;
    text-align: center;
    background-color: #111827;
    color: #ffffff;
    min-height: 25px;
}

QProgressBar[class="breeding-progress"]::chunk {
    background-color: #9C27B0;
}

QLabel[class="breeding-status"] {
    font-size: 14px;
    color: #00e5ff;
    padding: 10px;
}

QPushButton[class="btn-breed"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9C27B0, stop:1 #BA68C8);
    color: white;
    padding: 15px 30px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

QPushButton[class="btn-breed"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #BA68C8, stop:1 #CE93D8);
}

QPushButton[class="btn-cancel"] {
    background-color: #1a2436;
    color: #ffffff;
    border: 1px solid #EF4444;
    border-radius: 10px;
    padding: 15px 30px;
    font-size: 16px;
    font-weight: bold;
}

QPushButton[class="btn-cancel"]:hover {
    background-color: #EF4444;
    color: white;
}

/* === КНОПКА ПАУЗЫ === */

QPushButton[class="btn-pause"] {
    background-color: #EF4444;
    color: white;
    border: 2px solid #DC2626;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton[class="btn-pause"]:hover {
    background-color: #DC2626;
    border-color: #EF4444;
}

QLabel[class="stat-label.science"] {
    color: #9C27B0;
}
"""

with open('ui/style.qss', 'a', encoding='utf-8') as f:
    f.write(style_additions)
print("   Стили обновлены")

print("\n=== ОБНОВЛЕНИЕ ЗАВЕРШЕНО ===")
print("Запустите: py app.py")