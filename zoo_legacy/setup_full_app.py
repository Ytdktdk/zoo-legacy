import os

os.makedirs('ui/screens', exist_ok=True)
with open('ui/screens/__init__.py', 'w', encoding='utf-8') as f:
    f.write('')

# 1. animal_card.py
animal_card_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt

class AnimalCard(QWidget):
    def __init__(self, animal_data, db_manager, parent=None):
        super().__init__(parent)
        self.animal_id = animal_data[0]
        self.name = animal_data[1]
        self.species = animal_data[2]
        self.age = animal_data[3]
        self.health = animal_data[4]
        self.hunger = animal_data[5]
        self.db = db_manager
        
        self.setStyleSheet("QWidget { background-color: #1E293B; border-radius: 12px; padding: 20px; } QLabel { color: white; } QPushButton { border-radius: 8px; padding: 12px; font-weight: bold; color: white; }")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        header = QHBoxLayout()
        title = QLabel(f"{self.name} ({self.species})")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        age_label = QLabel(f"Возраст: {self.age} лет")
        age_label.setStyleSheet("font-size: 16px; color: #94A3B8;")
        header.addWidget(age_label)
        layout.addLayout(header)
        
        self.health_bar = self._create_progress_bar("Здоровье", self.health, "#10B981")
        self.hunger_bar = self._create_progress_bar("Голод", self.hunger, "#F59E0B")
        self.happiness_bar = self._create_progress_bar("Счастье", 85, "#3B82F6")
        self.stress_bar = self._create_progress_bar("Стресс", 15, "#EF4444")
        
        layout.addWidget(self.health_bar)
        layout.addWidget(self.hunger_bar)
        layout.addWidget(self.happiness_bar)
        layout.addWidget(self.stress_bar)
        
        genetics_label = QLabel("Генетический код:")
        genetics_label.setStyleSheet("font-size: 14px; color: #94A3B8; margin-top: 10px;")
        layout.addWidget(genetics_label)
        
        genetics_layout = QHBoxLayout()
        species, genetics = self.db.get_animal_genetics(self.animal_id)
        if genetics:
            for gene_name, gene_value in genetics.items():
                gene_btn = QPushButton(f"[{gene_value}]")
                if gene_value[0].isupper():
                    gene_btn.setStyleSheet("QPushButton { background-color: #10B981; border: 2px solid #059669; padding: 8px; font-size: 14px; font-weight: bold; color: white; }")
                else:
                    gene_btn.setStyleSheet("QPushButton { background-color: #334155; border: 2px solid #475569; padding: 8px; font-size: 14px; font-weight: bold; color: white; }")
                genetics_layout.addWidget(gene_btn)
        layout.addLayout(genetics_layout)
        
        btn_layout = QHBoxLayout()
        btn_feed = QPushButton("Покормить")
        btn_feed.setStyleSheet("background-color: #10B981;")
        btn_feed.clicked.connect(self._feed_animal)
        
        btn_treat = QPushButton("Вылечить")
        btn_treat.setStyleSheet("background-color: #3B82F6;")
        btn_treat.clicked.connect(self._treat_animal)
        
        btn_breed = QPushButton("На скрещивание")
        btn_breed.setStyleSheet("background-color: #8B5CF6;")
        btn_breed.clicked.connect(self._send_to_breeding)
        
        btn_layout.addWidget(btn_feed)
        btn_layout.addWidget(btn_treat)
        btn_layout.addWidget(btn_breed)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _create_progress_bar(self, label, value, color):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 14px; min-width: 80px; color: white;")
        layout.addWidget(label_widget)
        
        bar = QProgressBar()
        bar.setValue(value)
        bar.setStyleSheet(f"QProgressBar {{ border: 2px solid #475569; border-radius: 5px; text-align: center; background-color: #334155; }} QProgressBar::chunk {{ background-color: {color}; }}")
        layout.addWidget(bar)
        
        value_label = QLabel(f"{value}%")
        value_label.setStyleSheet("font-size: 14px; min-width: 50px; color: white;")
        layout.addWidget(value_label)
        
        return widget
    
    def _feed_animal(self):
        QMessageBox.information(self, "Успех", f"{self.name} покормлен!")
    
    def _treat_animal(self):
        QMessageBox.information(self, "Успех", f"{self.name} вылечен!")
    
    def _send_to_breeding(self):
        QMessageBox.information(self, "Информация", f"{self.name} отправлен в лабораторию скрещивания")
"""
with open('ui/screens/animal_card.py', 'w', encoding='utf-8') as f:
    f.write(animal_card_code)

# 2. finance_screen.py
finance_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class FinanceScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Финансы и аналитика")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        cards_layout = QHBoxLayout()
        cards_layout.addWidget(self._create_stat_card("Доход за месяц", "45 250 RUB", "#10B981"))
        cards_layout.addWidget(self._create_stat_card("Расходы", "28 100 RUB", "#EF4444"))
        cards_layout.addWidget(self._create_stat_card("Прибыль", "17 150 RUB", "#3B82F6"))
        cards_layout.addWidget(self._create_stat_card("Довольство посетителей", "87%", "#F59E0B"))
        layout.addLayout(cards_layout)
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px;")
        chart_layout = QVBoxLayout(chart_frame)
        chart_title = QLabel("Доходы и расходы (Июль-Декабрь 2026)")
        chart_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        chart_layout.addWidget(chart_title)
        chart_placeholder = QLabel("[Здесь будет график]")
        chart_placeholder.setStyleSheet("color: #9CA3AF; font-size: 14px; padding: 40px;")
        chart_layout.addWidget(chart_placeholder)
        layout.addWidget(chart_frame)
        
        bottom_layout = QHBoxLayout()
        
        popular_frame = QFrame()
        popular_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px;")
        popular_layout = QVBoxLayout(popular_frame)
        popular_layout.addWidget(QLabel("Самые популярные животные"))
        popular_layout.addWidget(QLabel("Лев: 45%"))
        popular_layout.addWidget(QLabel("Тигр: 32%"))
        popular_layout.addWidget(QLabel("Слон: 28%"))
        bottom_layout.addWidget(popular_frame)
        
        expenses_frame = QFrame()
        expenses_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px;")
        expenses_layout = QVBoxLayout(expenses_frame)
        expenses_layout.addWidget(QLabel("Структура расходов"))
        expenses_layout.addWidget(QLabel("Корм: 40%"))
        expenses_layout.addWidget(QLabel("Персонал: 30%"))
        expenses_layout.addWidget(QLabel("Обслуживание: 20%"))
        expenses_layout.addWidget(QLabel("Ветеринария: 10%"))
        bottom_layout.addWidget(expenses_frame)
        
        layout.addLayout(bottom_layout)
        self.setLayout(layout)
    
    def _create_stat_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: white; border-radius: 8px; padding: 15px; border-left: 4px solid {color}; }}")
        layout = QVBoxLayout(frame)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #6B7280;")
        layout.addWidget(title_label)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
        return frame
"""
with open('ui/screens/finance_screen.py', 'w', encoding='utf-8') as f:
    f.write(finance_code)

# 3. staff_screen.py
staff_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class StaffScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Управление персоналом")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        staff_list = [
            ("Др. Смит", "Ветеринар", 87, "#10B981"),
            ("Иванов", "Смотритель", 92, "#3B82F6"),
            ("Петрова", "Смотритель", 78, "#3B82F6"),
            ("Сидоров", "Смотритель", 95, "#3B82F6"),
        ]
        
        for name, position, skill, color in staff_list:
            layout.addWidget(self._create_staff_card(name, position, skill, color))
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_staff_card(self, name, position, skill, color):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; padding: 15px; }")
        layout = QHBoxLayout(frame)
        
        info_layout = QVBoxLayout()
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        position_label = QLabel(position)
        position_label.setStyleSheet("font-size: 12px; color: #6B7280;")
        info_layout.addWidget(position_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        skill_label = QLabel(f"Навык: {skill}%")
        skill_label.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: bold;")
        layout.addWidget(skill_label)
        
        return frame
"""
with open('ui/screens/staff_screen.py', 'w', encoding='utf-8') as f:
    f.write(staff_code)

# 4. main_window.py
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal import Lion, Tiger
from models.genetics import Gene, GeneticCode
from ui.breeding_dialog import BreedingDialog
from ui.screens.finance_screen import FinanceScreen
from ui.screens.staff_screen import StaffScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(1200, 800)
        
        self.setStyleSheet("QMainWindow { background-color: #F3F4F6; } QLabel { color: #1F2937; } QTableWidget { background-color: white; border: 1px solid #D1D5DB; border-radius: 8px; gridline-color: #E5E7EB; font-size: 14px; } QTableWidget::item { padding: 8px; } QHeaderView::section { background-color: #10B981; color: white; font-weight: bold; padding: 8px; border: none; } QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #1E293B; border: none; font-size: 14px; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; } QListWidget::item:selected { background-color: #3B82F6; }")

        try:
            self.db = DatabaseManager()
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", str(e))
            exit()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        sidebar = QListWidget()
        sidebar.setMaximumWidth(200)
        sidebar.addItem("Карта зоопарка")
        sidebar.addItem("Финансы")
        sidebar.addItem("Персонал")
        sidebar.addItem("Настройки")
        sidebar.currentRowChanged.connect(self._switch_screen)
        main_layout.addWidget(sidebar)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        self.map_screen = self._create_map_screen()
        self.finance_screen = FinanceScreen()
        self.staff_screen = StaffScreen()
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(QWidget())
        
        sidebar.setCurrentRow(0)

    def _create_map_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("Zoo Legacy: Управление зоопарком")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        
        stats = QLabel("Баланс: 125 450 RUB | Репутация: 4.8")
        stats.setStyleSheet("font-size: 16px; color: #4B5563; font-weight: bold;")
        header.addWidget(stats)
        layout.addLayout(header)

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Имя", "Вид", "Возраст", "Здоровье", "Голод"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        
        btn_add_lion = QPushButton("Добавить Льва")
        btn_add_lion.setStyleSheet("background-color: #F59E0B;")
        btn_add_lion.clicked.connect(lambda: self._add_animal_safely(Lion, "Симба", 5, "Окрас", "A", "a", table))
        btn_layout.addWidget(btn_add_lion)

        btn_add_tiger = QPushButton("Добавить Тигра")
        btn_add_tiger.setStyleSheet("background-color: #3B82F6;")
        btn_add_tiger.clicked.connect(lambda: self._add_animal_safely(Tiger, "Шерхан", 4, "Размер", "B", "b", table))
        btn_layout.addWidget(btn_add_tiger)
        
        btn_layout.addStretch()

        btn_breed = QPushButton("Лаборатория скрещивания")
        btn_breed.setStyleSheet("background-color: #8B5CF6; min-width: 250px;")
        btn_breed.clicked.connect(lambda: self._open_breeding_lab(table))
        btn_layout.addWidget(btn_breed)

        layout.addLayout(btn_layout)
        
        self.map_table = table
        self._refresh_table(table)
        
        return widget

    def _switch_screen(self, index):
        self.stack.setCurrentIndex(index)

    def _refresh_table(self, table):
        try:
            animals = self.db.get_all_animals()
            table.setRowCount(len(animals))
            for row, animal_data in enumerate(animals):
                for col, data in enumerate(animal_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if col == 4:
                        if data < 50:
                            item.setBackground(Qt.GlobalColor.red)
                            item.setForeground(Qt.GlobalColor.white)
                        elif data < 80:
                            item.setBackground(Qt.GlobalColor.yellow)
                    table.setItem(row, col, item)
        except Exception as e:
            QMessageBox.warning(self, "Предупреждение", str(e))

    def _add_animal_safely(self, animal_class, name, age, gene_name, dom, rec, table):
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene(gene_name, dom, rec))
            animal = animal_class(name, age, genetics)
            animal.feed(30)
            self.db.add_animal(animal)
            self._refresh_table(table)
            QMessageBox.information(self, "Успех", f"Животное '{animal.name}' успешно добавлено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить животное. {e}")

    def _open_breeding_lab(self, table):
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._refresh_table(table)
"""
with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)

print("Все новые экраны успешно созданы!")
print("Теперь запустите: py app.py")