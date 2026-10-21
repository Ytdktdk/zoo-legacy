import os

# Создаем папку для изображений
os.makedirs('assets', exist_ok=True)
os.makedirs('assets/animals', exist_ok=True)

# 1. Создаем экран каталога с карточками
catalog_screen_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor
from models.animal_catalog import ANIMAL_CATALOG
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode

class CatalogScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.parent = parent
        
        self.setStyleSheet("QWidget { background-color: #F3F4F6; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Заголовок
        title = QLabel(" ЖИВОТНЫЕ ЗООПАРКА")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Категории
        categories_layout = QHBoxLayout()
        categories = ["Все", "Млекопитающие", "Птицы", "Пресмыкающиеся", "Беспозвоночные"]
        for i, cat in enumerate(categories):
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #10B981;
                    color: white;
                    padding: 15px 30px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    min-width: 150px;
                }
                QPushButton:checked {
                    background-color: #059669;
                }
            ''')
            if i == 0:
                btn.setChecked(True)
            categories_layout.addWidget(btn)
        categories_layout.addStretch()
        layout.addLayout(categories_layout)
        
        # Скролл для карточек
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Создаем карточки для всех животных
        self._create_animal_cards()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
    
    def _create_animal_cards(self):
        row, col = 0, 0
        max_cols = 4
        
        for species, data in ANIMAL_CATALOG.items():
            card = self._create_animal_card(species, data)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def _create_animal_card(self, species, data):
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 0px;
            }
            QFrame:hover {
                background-color: #F9FAFB;
                border: 2px solid #10B981;
            }
        ''')
        card.setFixedHeight(280)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Фото (заглушка с цветом и эмодзи)
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet(f'''
            QLabel {{
                background-color: {self._get_category_color(data["cat"])};
                font-size: 80px;
                min-height: 180px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        ''')
        layout.addWidget(photo_label)
        
        # Информация
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(15, 10, 15, 10)
        info_layout.setSpacing(5)
        
        # Название
        name_label = QLabel(species)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F2937;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        
        # Категория
        cat_label = QLabel(data["cat"])
        cat_label.setStyleSheet("font-size: 12px; color: #6B7280;")
        cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(cat_label)
        
        # Площадь
        space_label = QLabel(f" {data['space']} м²")
        space_label.setStyleSheet("font-size: 12px; color: #4B5563;")
        space_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(space_label)
        
        # Кнопка добавить
        add_btn = QPushButton("➕ Добавить")
        add_btn.setStyleSheet('''
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        ''')
        add_btn.clicked.connect(lambda checked, s=species: self._add_animal(s))
        info_layout.addWidget(add_btn)
        
        layout.addWidget(info_widget)
        
        return card
    
    def _get_category_color(self, category):
        colors = {
            "Млекопитающее": "#FDE68A",
            "Птица": "#BFDBFE",
            "Пресмыкающееся": "#BBF7D0",
            "Беспозвоночное": "#FED7AA"
        }
        return colors.get(category, "#E5E7EB")
    
    def _add_animal(self, species):
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene("Окрас", "A", "a"))
            genetics.add_gene(Gene("Размер", "B", "b"))
            
            animal = ZooAnimal(f"Новый {species}", species, 3, genetics)
            animal.feed(30)
            self.db.add_animal(animal)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Успех", f"{ANIMAL_CATALOG[species]['emoji']} {species} добавлен в зоопарк!")
            
            if self.parent:
                self.parent._switch_to_zoo_map()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить животное: {e}")
"""

with open('ui/screens/catalog_screen.py', 'w', encoding='utf-8') as f:
    f.write(catalog_screen_code)

# 2. Обновляем main_window.py - добавляем кнопку каталога и переключение
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QFormLayout, QLineEdit, QComboBox, QSpinBox, QGroupBox
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode
from models.animal_catalog import ANIMAL_CATALOG
from ui.breeding_dialog import BreedingDialog
from ui.screens.finance_screen import FinanceScreen
from ui.screens.staff_screen import StaffScreen
from ui.screens.catalog_screen import CatalogScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(1400, 900)
        
        self.themes = {
            0: self._get_light_theme(),
            1: self._get_dark_theme(),
            2: self._get_blue_theme()
        }
        self._apply_theme(0)

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
        sidebar.setMaximumWidth(220)
        sidebar.addItem("🗺️ Карта зоопарка")
        sidebar.addItem(" Каталог животных")
        sidebar.addItem("💰 Финансы")
        sidebar.addItem("👥 Персонал")
        sidebar.addItem("⚙️ Настройки")
        sidebar.currentRowChanged.connect(self._switch_screen)
        main_layout.addWidget(sidebar)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        self.map_screen = self._create_map_screen()
        self.catalog_screen = CatalogScreen(self.db, self)
        self.finance_screen = FinanceScreen()
        self.staff_screen = StaffScreen()
        self.settings_screen = self._create_settings_screen()
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.catalog_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(self.settings_screen)
        sidebar.setCurrentRow(0)

    def _switch_to_zoo_map(self):
        self.stack.setCurrentIndex(0)

    def _get_light_theme(self):
        return '''QMainWindow { background-color: #F3F4F6; } QLabel { color: #1F2937; } QTableWidget { background-color: white; border: 1px solid #D1D5DB; border-radius: 8px; gridline-color: #E5E7EB; font-size: 14px; } QTableWidget::item { padding: 8px; } QHeaderView::section { background-color: #10B981; color: white; font-weight: bold; padding: 8px; border: none; } QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #1E293B; border: none; font-size: 14px; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; } QListWidget::item:selected { background-color: #3B82F6; } QGroupBox { background-color: white; border: 2px solid #10B981; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; } QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #D1D5DB; border-radius: 4px; background-color: white; }'''

    def _get_dark_theme(self):
        return '''QMainWindow { background-color: #1E293B; } QLabel { color: #F1F5F9; } QTableWidget { background-color: #334155; border: 1px solid #475569; border-radius: 8px; gridline-color: #475569; font-size: 14px; color: #F1F5F9; } QTableWidget::item { padding: 8px; } QHeaderView::section { background-color: #059669; color: white; font-weight: bold; padding: 8px; border: none; } QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; background-color: #3B82F6; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #0F172A; border: none; font-size: 14px; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #1E293B; } QListWidget::item:selected { background-color: #3B82F6; } QGroupBox { background-color: #334155; border: 2px solid #3B82F6; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; color: #F1F5F9; } QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #475569; border-radius: 4px; background-color: #475569; color: #F1F5F9; }'''

    def _get_blue_theme(self):
        return '''QMainWindow { background-color: #EFF6FF; } QLabel { color: #1E3A8A; } QTableWidget { background-color: white; border: 1px solid #3B82F6; border-radius: 8px; gridline-color: #BFDBFE; font-size: 14px; } QTableWidget::item { padding: 8px; } QHeaderView::section { background-color: #2563EB; color: white; font-weight: bold; padding: 8px; border: none; } QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; background-color: #2563EB; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #1E3A8A; border: none; font-size: 14px; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #1E40AF; } QListWidget::item:selected { background-color: #3B82F6; } QGroupBox { background-color: white; border: 2px solid #2563EB; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; color: #1E3A8A; } QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #93C5FD; border-radius: 4px; background-color: white; color: #1E3A8A; }'''

    def _apply_theme(self, theme_index):
        self.setStyleSheet(self.themes[theme_index])

    def _create_settings_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        title = QLabel("Настройки приложения")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        general_group = QGroupBox("Основные настройки")
        general_layout = QFormLayout(general_group)
        self.name_input = QLineEdit("Zoo Legacy")
        general_layout.addRow("Название зоопарка:", self.name_input)
        layout.addWidget(general_group)
        
        visual_group = QGroupBox("Визуальные настройки")
        visual_layout = QFormLayout(visual_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая тема", "Тёмная тема", "Синяя тема"])
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        visual_layout.addRow("Тема оформления:", self.theme_combo)
        layout.addWidget(visual_group)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton(" Сохранить настройки")
        btn_save.setStyleSheet("background-color: #10B981; padding: 15px; font-size: 16px;")
        btn_save.clicked.connect(lambda: QMessageBox.information(self, "Успех", "Настройки сохранены!"))
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
        layout.addStretch()
        return widget

    def _on_theme_changed(self, index):
        self._apply_theme(index)

    def _create_map_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("🗺️ Карта зоопарка")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        stats = QLabel("💰 125 450 RUB | ⭐ 4.8")
        stats.setStyleSheet("font-size: 16px; font-weight: bold;")
        header.addWidget(stats)
        layout.addLayout(header)

        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["Фото", "ID", "Имя", "Вид", "Возраст", "Здоровье", "Голод"])
        table.setColumnWidth(0, 80)
        table.setColumnWidth(1, 50)
        table.setColumnWidth(2, 180)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 80)
        table.setColumnWidth(5, 100)
        table.setColumnWidth(6, 100)
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        btn_breed = QPushButton("🧬 Лаборатория скрещивания")
        btn_breed.setStyleSheet("background-color: #8B5CF6; min-width: 250px; padding: 12px; font-size: 16px;")
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
                species = animal_data[2]
                emoji = ANIMAL_CATALOG.get(species, {"emoji": "❓"})["emoji"]
                
                photo_label = QLabel(emoji)
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                photo_label.setStyleSheet("font-size: 40px;")
                table.setCellWidget(row, 0, photo_label)
                
                for col in range(6):
                    item = QTableWidgetItem(str(animal_data[col]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if col == 4:
                        if animal_data[col] < 50:
                            item.setBackground(Qt.GlobalColor.red)
                            item.setForeground(Qt.GlobalColor.white)
                        elif animal_data[col] < 80:
                            item.setBackground(Qt.GlobalColor.yellow)
                    table.setItem(row, col + 1, item)
        except Exception as e:
            QMessageBox.warning(self, "Предупреждение", str(e))

    def _open_breeding_lab(self, table):
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._refresh_table(table)
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)

print("✅ Каталог с карточками создан!")
print("✅ Добавлена кнопка '📚 Каталог животных' в меню!")
print("✅ Карточки расположены сеткой, как на сайте зоопарка!")
print("Запустите: py app.py")