import os

# 1. Обновляем DatabaseManager - добавляем баланс и расходы
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
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, description TEXT,
            amount REAL, timestamp TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS zoo_balance (
            id INTEGER PRIMARY KEY,
            balance REAL)''')
        
        cursor.execute('SELECT COUNT(*) FROM zoo_balance')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO zoo_balance (id, balance) VALUES (1, 125450)')
        
        self.conn.commit()

    def get_balance(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT balance FROM zoo_balance WHERE id = 1')
            result = cursor.fetchone()
            return result[0] if result else 125450
        except Exception as e:
            raise RuntimeError(f"Не удалось получить баланс: {e}")

    def update_balance(self, amount):
        try:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE zoo_balance SET balance = balance + ? WHERE id = 1', (amount,))
            self.conn.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Не удалось обновить баланс: {e}")

    def add_animal(self, animal, price=0):
        try:
            cursor = self.conn.cursor()
            genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
            cursor.execute('INSERT INTO animals (name, species, age, genetics, health, hunger) VALUES (?, ?, ?, ?, ?, ?)',
                (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger))
            
            if price > 0:
                today = datetime.now().strftime('%Y-%m-%d')
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('INSERT INTO expenses (date, description, amount, timestamp) VALUES (?, ?, ?, ?)',
                    (today, f"Покупка животного: {animal.get_species()}", price, timestamp))
                cursor.execute('UPDATE zoo_balance SET balance = balance - ? WHERE id = 1', (price,))
            
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
            cursor.execute('UPDATE zoo_balance SET balance = balance + ? WHERE id = 1', (total_amount,))
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

    def get_expenses(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM expenses ORDER BY timestamp DESC')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить расходы: {e}")

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
print("1. DatabaseManager обновлен")

# 2. Обновляем FinanceScreen - показываем баланс, доходы, расходы
finance_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt6.QtCore import Qt

class FinanceScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__()
        self.db = db_manager
        self.parent = parent
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Финансы и аналитика")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        # Общий баланс
        balance = self.db.get_balance()
        balance_card = QFrame()
        balance_card.setStyleSheet("QFrame { background-color: #10B981; border-radius: 12px; padding: 25px; }")
        balance_layout = QVBoxLayout(balance_card)
        balance_title = QLabel("ОБЩИЙ БЮДЖЕТ ЗООПАРКА")
        balance_title.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        balance_layout.addWidget(balance_title)
        balance_value = QLabel(f"{balance:,.0f} RUB")
        balance_value.setStyleSheet("font-size: 36px; color: white; font-weight: bold;")
        balance_layout.addWidget(balance_value)
        layout.addWidget(balance_card)
        
        # Карточки статистики
        cards_layout = QHBoxLayout()
        stats = self.db.get_sales_statistics()
        total_revenue = stats[3] if stats[3] else 0
        total_tickets = (stats[1] if stats[1] else 0) + (stats[2] if stats[2] else 0)
        
        cards_layout.addWidget(self._create_stat_card("Доход от билетов", f"{total_revenue:,.0f} RUB", "#3B82F6"))
        cards_layout.addWidget(self._create_stat_card("Продано билетов", str(total_tickets), "#8B5CF6"))
        cards_layout.addWidget(self._create_stat_card("Взрослых", str(stats[1] if stats[1] else 0), "#F59E0B"))
        cards_layout.addWidget(self._create_stat_card("Льготных", str(stats[2] if stats[2] else 0), "#EF4444"))
        layout.addLayout(cards_layout)
        
        # Таблица доходов
        income_title = QLabel("📈 История доходов (продажа билетов)")
        income_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(income_title)
        
        self.income_table = QTableWidget()
        self.income_table.setColumnCount(5)
        self.income_table.setHorizontalHeaderLabels(["Дата", "Посетитель", "Взрослых", "Льготных", "Сумма"])
        self.income_table.horizontalHeader().setStretchLastSection(True)
        self.income_table.setAlternatingRowColors(True)
        layout.addWidget(self.income_table)
        
        # Таблица расходов
        expense_title = QLabel("📉 История расходов (покупка животных)")
        expense_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(expense_title)
        
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Дата", "Описание", "Сумма", "Время"])
        self.expense_table.horizontalHeader().setStretchLastSection(True)
        self.expense_table.setAlternatingRowColors(True)
        layout.addWidget(self.expense_table)
        
        self._refresh_tables()
    
    def _create_stat_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: white; border-radius: 8px; padding: 15px; border-left: 4px solid {color}; }}")
        layout = QVBoxLayout(frame)
        layout.addWidget(QLabel(title))
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
        return frame
    
    def _refresh_tables(self):
        sales = self.db.get_ticket_sales_by_date()
        self.income_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            for col, data in enumerate([sale[1], sale[2], sale[3], sale[4], sale[5]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 4:
                    item.setForeground(Qt.GlobalColor.darkGreen)
                self.income_table.setItem(row, col, item)
        
        expenses = self.db.get_expenses()
        self.expense_table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            for col, data in enumerate([expense[1], expense[2], expense[3], expense[4]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 2:
                    item.setForeground(Qt.GlobalColor.red)
                self.expense_table.setItem(row, col, item)
    
    def refresh(self):
        self._refresh_tables()
"""

with open('ui/screens/finance_screen.py', 'w', encoding='utf-8') as f:
    f.write(finance_code)
print("2. FinanceScreen обновлен")

# 3. Обновляем CatalogScreen - вычитаем деньги при покупке
catalog_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from models.animal_catalog import ANIMAL_CATALOG
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode

class CatalogScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.parent = parent
        self.current_category = "Все"
        
        self.setStyleSheet("QWidget { background-color: #F3F4F6; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("КАТАЛОГ ЖИВОТНЫХ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Категория:"))
        
        categories = ["Все", "Млекопитающие", "Птицы", "Пресмыкающиеся", "Беспозвоночные"]
        self.category_buttons = {}
        for cat in categories:
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setStyleSheet("QPushButton { background-color: #10B981; color: white; padding: 12px 25px; font-size: 14px; font-weight: bold; border-radius: 8px; } QPushButton:checked { background-color: #059669; border: 2px solid #047857; }")
            btn.clicked.connect(lambda checked, c=cat: self._filter_by_category(c))
            self.category_buttons[cat] = btn
            filter_layout.addWidget(btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        self.category_buttons["Все"].setChecked(True)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll)
        
        self._refresh_catalog()
    
    def _filter_by_category(self, category):
        self.current_category = category
        for cat, btn in self.category_buttons.items():
            btn.setChecked(cat == category)
        self._refresh_catalog()
    
    def _refresh_catalog(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        row, col = 0, 0
        max_cols = 3
        
        for species, data in ANIMAL_CATALOG.items():
            if self.current_category != "Все" and data["cat"] != self.current_category:
                continue
                
            card = self._create_animal_card(species, data)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def _create_animal_card(self, species, data):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 12px; padding: 0px; } QFrame:hover { border: 3px solid #10B981; }")
        card.setFixedHeight(320)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet(f"QLabel {{ background-color: #FDE68A; font-size: 100px; min-height: 200px; border-top-left-radius: 12px; border-top-right-radius: 12px; }}")
        layout.addWidget(photo_label)
        
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(20, 15, 20, 15)
        info_layout.setSpacing(8)
        
        name_label = QLabel(species)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        
        cat_label = QLabel(f"{data['cat']} - {data['space']} м2")
        cat_label.setStyleSheet("font-size: 13px; color: #6B7280;")
        cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(cat_label)
        
        price_label = QLabel(f"{data['price']:,} RUB")
        price_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #F59E0B;")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(price_label)
        
        add_btn = QPushButton("Добавить в зоопарк")
        add_btn.setStyleSheet("QPushButton { background-color: #10B981; color: white; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 14px; } QPushButton:hover { background-color: #059669; }")
        add_btn.clicked.connect(lambda checked, s=species: self._add_animal(s))
        info_layout.addWidget(add_btn)
        
        layout.addWidget(info_widget)
        return card
    
    def _add_animal(self, species):
        data = ANIMAL_CATALOG[species]
        price = data["price"]
        
        current_balance = self.db.get_balance()
        if current_balance < price:
            QMessageBox.warning(self, "Недостаточно средств", f"Для покупки {species} нужно {price:,} RUB\\nВаш баланс: {current_balance:,.0f} RUB")
            return
        
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene("Окрас", "A", "a"))
            genetics.add_gene(Gene("Размер", "B", "b"))
            
            animal = ZooAnimal(f"Новый {species}", species, 3, genetics)
            animal.feed(30)
            self.db.add_animal(animal, price)
            
            QMessageBox.information(self, "Успешная покупка!", f"{data['emoji']} {species} добавлен в зоопарк!\\nСписано: {price:,} RUB")
            
            if self.parent and hasattr(self.parent, '_update_all'):
                self.parent._update_all()
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить животное: {e}")
"""

with open('ui/screens/catalog_screen.py', 'w', encoding='utf-8') as f:
    f.write(catalog_code)
print("3. CatalogScreen обновлен")

# 4. Обновляем MainWindow - передаем db и обновляем баланс
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal_catalog import ANIMAL_CATALOG
from ui.breeding_dialog import BreedingDialog
from ui.screens.finance_screen import FinanceScreen
from ui.screens.staff_screen import StaffScreen
from ui.screens.catalog_screen import CatalogScreen
from ui.screens.visitors_screen import VisitorsScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy")
        self.resize(1400, 900)
        self.setStyleSheet("QMainWindow { background-color: #F3F4F6; } QLabel { color: #1F2937; } QPushButton { border-radius: 8px; padding: 12px; font-weight: bold; color: white; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #1E293B; border: none; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; } QListWidget::item:selected { background-color: #3B82F6; }")
        
        try:
            self.db = DatabaseManager()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            exit()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        sidebar = QListWidget()
        sidebar.setMaximumWidth(220)
        sidebar.addItem("Карта зоопарка")
        sidebar.addItem("Каталог животных")
        sidebar.addItem("Лаборатория")
        sidebar.addItem("Финансы")
        sidebar.addItem("Персонал")
        sidebar.addItem("Посетители")
        sidebar.currentRowChanged.connect(self._switch_screen)
        main_layout.addWidget(sidebar)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        self.map_screen = self._create_zoo_map()
        self.catalog_screen = CatalogScreen(self.db, self)
        self.breeding_screen = self._create_breeding_placeholder()
        self.finance_screen = FinanceScreen(self.db, self)
        self.staff_screen = StaffScreen()
        self.visitors_screen = VisitorsScreen(self.db, self)
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.catalog_screen)
        self.stack.addWidget(self.breeding_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(self.visitors_screen)
        sidebar.setCurrentRow(0)
    
    def _update_all(self):
        self._refresh_zoo_map()
        self.finance_screen.refresh()
        header = self.map_screen.findChild(QHBoxLayout)
        if header:
            for i in range(header.count()):
                item = header.itemAt(i)
                if item.widget() and isinstance(item.widget(), QLabel) and "Баланс" in item.widget().text():
                    balance = self.db.get_balance()
                    item.widget().setText(f"Баланс: {balance:,.0f} RUB")
                    break
    
    def _create_zoo_map(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        header = QHBoxLayout()
        title = QLabel("КАРТА ЗООПАРКА")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        balance = self.db.get_balance()
        stats = QLabel(f"Баланс: {balance:,.0f} RUB")
        stats.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(stats)
        layout.addLayout(header)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll_content = QWidget()
        self.animals_grid = QGridLayout(scroll_content)
        self.animals_grid.setSpacing(25)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        self._refresh_zoo_map()
        return widget
    
    def _refresh_zoo_map(self):
        while self.animals_grid.count():
            item = self.animals_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        animals = self.db.get_all_animals()
        for idx, animal_data in enumerate(animals):
            card = self._create_animal_card(animal_data)
            self.animals_grid.addWidget(card, idx // 3, idx % 3)
    
    def _create_animal_card(self, animal_data):
        species = animal_data[2]
        data = ANIMAL_CATALOG.get(species, {"emoji": "", "cat": "Неизвестно"})
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; } QFrame:hover { border: 3px solid #3B82F6; }")
        card.setFixedHeight(280)
        layout = QVBoxLayout(card)
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet("QLabel { background-color: #10B981; font-size: 100px; min-height: 180px; border-top-left-radius: 15px; border-top-right-radius: 15px; }")
        layout.addWidget(photo_label)
        info = QWidget()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(15, 10, 15, 10)
        info_layout.addWidget(QLabel(animal_data[1]))
        info_layout.addWidget(QLabel(f"{species} - {animal_data[3]} лет"))
        info_layout.addWidget(QLabel(f"Здоровье: {animal_data[4]}%"))
        info_layout.addWidget(QLabel(f"Голод: {animal_data[5]}%"))
        layout.addWidget(info)
        return card
    
    def _create_breeding_placeholder(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #8B5CF6;")
        layout.addWidget(title)
        btn = QPushButton("Открыть лабораторию")
        btn.setStyleSheet("background-color: #8B5CF6; padding: 20px; font-size: 18px;")
        btn.clicked.connect(lambda: self._open_breeding_dialog())
        layout.addWidget(btn)
        return widget
    
    def _open_breeding_dialog(self):
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._refresh_zoo_map()
    
    def _switch_screen(self, index):
        self.stack.setCurrentIndex(index)
        if index == 3:
            self.finance_screen.refresh()
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)
print("4. MainWindow обновлен")

# 5. Обновляем VisitorsScreen - передаем parent для обновления баланса
visitors_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QDialog, QScrollArea, QTextEdit, QLineEdit, QCheckBox, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt

class VisitorsScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__()
        self.db = db_manager
        self.parent = parent
        self.setStyleSheet("QWidget { background-color: white; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        title = QLabel("ИНФОРМАЦИЯ ДЛЯ ПОСЕТИТЕЛЕЙ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        buy_ticket_btn = QPushButton("КУПИТЬ БИЛЕТ")
        buy_ticket_btn.setStyleSheet("QPushButton { background-color: #FCD34D; color: #1F2937; padding: 20px 40px; font-size: 20px; font-weight: bold; border-radius: 12px; border: 3px solid #F59E0B; } QPushButton:hover { background-color: #F59E0B; color: white; }")
        buy_ticket_btn.clicked.connect(self._show_ticket_form)
        header_layout.addWidget(buy_ticket_btn)
        layout.addLayout(header_layout)
        
        info_layout = QHBoxLayout()
        contacts_frame = QFrame()
        contacts_frame.setStyleSheet("QFrame { background-color: #FDE68A; border-radius: 12px; padding: 20px; }")
        contacts_layout = QVBoxLayout(contacts_frame)
        contacts_title = QLabel("КОНТАКТНАЯ ИНФОРМАЦИЯ")
        contacts_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        contacts_layout.addWidget(contacts_title)
        contacts_layout.addWidget(QLabel("Телефон: +7 (383) 388-72-58"))
        contacts_layout.addWidget(QLabel("E-mail: info@zoonovosib.ru"))
        contacts_layout.addWidget(QLabel("Адрес: г. Новосибирск, ул. Российская, д. 3"))
        contacts_layout.addWidget(QLabel(""))
        contacts_layout.addWidget(QLabel("Мы в социальных сетях:"))
        contacts_layout.addWidget(QLabel("  Telegram: @Zoo_Legacy"))
        contacts_layout.addWidget(QLabel("  ВКонтакте: ZooLegacy"))
        info_layout.addWidget(contacts_frame)
        
        hours_frame = QFrame()
        hours_frame.setStyleSheet("QFrame { background-color: #BBF7D0; border-radius: 12px; padding: 20px; }")
        hours_layout = QVBoxLayout(hours_frame)
        hours_title = QLabel("РЕЖИМ РАБОТЫ")
        hours_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        hours_layout.addWidget(hours_title)
        hours_layout.addWidget(QLabel("Будние дни: 8:00 - 21:00"))
        hours_layout.addWidget(QLabel("Выходные: 8:00 - 22:00"))
        hours_layout.addWidget(QLabel(""))
        hours_layout.addWidget(QLabel("Кассы закрываются:"))
        hours_layout.addWidget(QLabel("  Будни: 20:00"))
        hours_layout.addWidget(QLabel("  Выходные: 20:30"))
        hours_layout.addWidget(QLabel(""))
        hours_layout.addWidget(QLabel("Парковка: 100 руб/авто"))
        info_layout.addWidget(hours_frame)
        layout.addLayout(info_layout)
        
        sections_layout = QHBoxLayout()
        sections = [("Стоимость и оплата", "#10B981", self._show_prices),
                    ("Абонемент на месяц", "#3B82F6", self._show_subscription),
                    ("Правила зоопарка", "#F59E0B", self._show_rules)]
        for text, color, handler in sections:
            btn = QPushButton(text)
            btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; padding: 30px; font-size: 16px; font-weight: bold; border-radius: 12px; min-width: 200px; }} QPushButton:hover {{ opacity: 0.9; }}")
            btn.clicked.connect(handler)
            sections_layout.addWidget(btn)
        layout.addLayout(sections_layout)
        layout.addStretch()
    
    def _show_ticket_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Покупка билета")
        dialog.resize(500, 700)
        dialog.setStyleSheet("QDialog { background-color: #1E3A5F; }")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Фамилия, Имя")
        name_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        layout.addWidget(name_input)
        
        contact_layout = QHBoxLayout()
        phone_input = QLineEdit()
        phone_input.setPlaceholderText("+7 (   )   -   -")
        phone_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        contact_layout.addWidget(phone_input)
        email_input = QLineEdit()
        email_input.setPlaceholderText("E-mail")
        email_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        contact_layout.addWidget(email_input)
        layout.addLayout(contact_layout)
        
        adult_frame = QFrame()
        adult_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; padding: 20px; }")
        adult_layout = QVBoxLayout(adult_frame)
        adult_header = QHBoxLayout()
        adult_title = QLabel("Входной билет Взрослый")
        adult_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        adult_header.addWidget(adult_title)
        adult_header.addStretch()
        adult_counter = QSpinBox()
        adult_counter.setRange(0, 20)
        adult_counter.setValue(0)
        adult_counter.setStyleSheet("QSpinBox { background-color: #1E3A5F; color: white; border: none; border-radius: 15px; padding: 8px 15px; font-size: 16px; font-weight: bold; min-width: 50px; }")
        adult_header.addWidget(adult_counter)
        adult_layout.addLayout(adult_header)
        adult_price = QLabel("Цена билета: 700 рублей.")
        adult_price.setStyleSheet("font-size: 14px; color: #6B7280;")
        adult_layout.addWidget(adult_price)
        layout.addWidget(adult_frame)
        
        льготный_frame = QFrame()
        льготный_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; padding: 20px; }")
        льготный_layout = QVBoxLayout(льготный_frame)
        льготный_header = QHBoxLayout()
        льготный_title = QLabel("Входной билет Льготный")
        льготный_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        льготный_header.addWidget(льготный_title)
        льготный_header.addStretch()
        льготный_counter = QSpinBox()
        льготный_counter.setRange(0, 20)
        льготный_counter.setValue(0)
        льготный_counter.setStyleSheet("QSpinBox { background-color: #1E3A5F; color: white; border: none; border-radius: 15px; padding: 8px 15px; font-size: 16px; font-weight: bold; min-width: 50px; }")
        льготный_header.addWidget(льготный_counter)
        льготный_layout.addLayout(льготный_header)
        льготный_price = QLabel("Цена билета: 350 рублей.")
        льготный_price.setStyleSheet("font-size: 14px; color: #6B7280;")
        льготный_layout.addWidget(льготный_price)
        layout.addWidget(льготный_frame)
        
        consent_frame = QFrame()
        consent_frame.setStyleSheet("QFrame { background-color: #9CA3AF; border-radius: 12px; padding: 15px; }")
        consent_layout = QVBoxLayout(consent_frame)
        checkbox1 = QCheckBox("Согласие на обработку персональных данных")
        checkbox1.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox1)
        checkbox2 = QCheckBox("Согласие с правилами поведения в зоопарке")
        checkbox2.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox2)
        checkbox3 = QCheckBox("Согласие с правилами покупки электронных билетов")
        checkbox3.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox3)
        layout.addWidget(consent_frame)
        
        buy_btn = QPushButton("КУПИТЬ")
        buy_btn.setStyleSheet("QPushButton { background-color: #D1D5DB; color: #1F2937; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 25px; } QPushButton:hover { background-color: #9CA3AF; }")
        buy_btn.clicked.connect(lambda: self._process_ticket_purchase(name_input.text(), phone_input.text(), email_input.text(), adult_counter.value(), льготный_counter.value(), checkbox1.isChecked(), checkbox2.isChecked(), checkbox3.isChecked(), dialog))
        layout.addWidget(buy_btn)
        dialog.exec()
    
    def _process_ticket_purchase(self, name, phone, email, adult_count, льготный_count, cb1, cb2, cb3, dialog):
        if not name or not phone or not email:
            QMessageBox.warning(dialog, "Ошибка", "Пожалуйста, заполните все поля")
            return
        if adult_count == 0 and льготный_count == 0:
            QMessageBox.warning(dialog, "Ошибка", "Выберите хотя бы один билет")
            return
        if not (cb1 and cb2 and cb3):
            QMessageBox.warning(dialog, "Ошибка", "Примите все условия соглашения")
            return
        total = adult_count * 700 + льготный_count * 350
        try:
            self.db.add_ticket_sale(name, adult_count, льготный_count, total)
            QMessageBox.information(dialog, "Билет куплен!", f"Спасибо, {name}!\\n\\nВзрослых: {adult_count}\\nЛьготных: {льготный_count}\\nИтого: {total} руб.\\n\\nДоход добавлен в бюджет!")
            dialog.close()
            if self.parent and hasattr(self.parent, '_update_all'):
                self.parent._update_all()
        except Exception as e:
            QMessageBox.critical(dialog, "Ошибка", f"Ошибка: {e}")
    
    def _show_modal(self, title, content):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(800, 600)
        layout = QVBoxLayout(dialog)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(content)
        text_edit.setStyleSheet("QTextEdit { font-size: 14px; padding: 15px; border: none; }")
        scroll.setWidget(text_edit)
        layout.addWidget(scroll)
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("QPushButton { background-color: #10B981; color: white; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px; }")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        dialog.exec()
    
    def _show_prices(self):
        content = "<h2>Стоимость посещения</h2><table border='1' cellpadding='8'><tr style='background-color:#10B981;color:white'><th>Категория</th><th>Цена</th></tr><tr><td>Взрослые</td><td><b>700 руб</b></td></tr><tr><td>Дети 7-16 лет</td><td><b>350 руб</b></td></tr><tr style='background-color:#BBF7D0'><td>Дети до 7 лет</td><td><b>Бесплатно</b></td></tr><tr style='background-color:#BBF7D0'><td>Инвалиды I группы</td><td><b>Бесплатно</b></td></tr></table>"
        self._show_modal("Стоимость", content)
    
    def _show_subscription(self):
        content = "<h2>Абонемент на месяц</h2><p>Действителен 1 месяц. Именной.</p><table border='1' cellpadding='8'><tr style='background-color:#3B82F6;color:white'><th>Категория</th><th>Цена</th></tr><tr><td>Взрослый</td><td><b>3000 руб</b></td></tr><tr><td>Льготный</td><td><b>1750 руб</b></td></tr><tr style='background-color:#BBF7D0'><td>Дети до 7 лет</td><td><b>Бесплатно</b></td></tr></table>"
        self._show_modal("Абонемент", content)
    
    def _show_rules(self):
        content = "<h2>Правила зоопарка</h2><ul><li>Соблюдайте тишину</li><li>НЕ кормите животных</li><li>НЕ заходите за ограждения</li><li>НЕ трогайте животных</li><li>Соблюдайте чистоту</li><li>Дети до 14 лет только с взрослыми</li></ul>"
        self._show_modal("Правила", content)
"""

with open('ui/screens/visitors_screen.py', 'w', encoding='utf-8') as f:
    f.write(visitors_code)
print("5. VisitorsScreen обновлен")

print("\n✅ Все обновления установлены!")
print("Теперь запустите: py app.py")