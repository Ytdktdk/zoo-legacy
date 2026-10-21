import os

# 1. Создаем каталог животных (База данных характеристик)
catalog_code = """# Каталог животных для Zoo Legacy
# Формат: "Название": {"категория": "...", "эмодзи": "...", "площадь": ..., "звук": "..."}

ANIMAL_CATALOG = {
    # МЛЕКОПИТАЮЩИЕ
    "Кенгуру Беннетта": {"cat": "Млекопитающее", "emoji": "🦘", "space": 30.0, "sound": "Пф-пф!"},
    "Большой серый кенгуру": {"cat": "Млекопитающее", "emoji": "🦘", "space": 40.0, "sound": "Топ-топ!"},
    "Кошачий лемур": {"cat": "Млекопитающее", "emoji": "🐒", "space": 15.0, "sound": "Мяу-мяу!"},
    "Толстохвостый галаго": {"cat": "Млекопитающее", "emoji": "🐵", "space": 10.0, "sound": "Уи-уи!"},
    "Красный вари": {"cat": "Млекопитающее", "emoji": "🦧", "space": 20.0, "sound": "Ууу-ууу!"},
    "Черно-белый вари": {"cat": "Млекопитающее", "emoji": "🦧", "space": 20.0, "sound": "Ууу-ууу!"},
    "Альпака": {"cat": "Млекопитающее", "emoji": "🦙", "space": 25.0, "sound": "Хрум-хрум!"},
    "Гуанако": {"cat": "Млекопитающее", "emoji": "🦙", "space": 25.0, "sound": "Фыр-фыр!"},
    "Таджикский винторогий козёл": {"cat": "Млекопитающее", "emoji": "🐐", "space": 35.0, "sound": "Ме-е-е!"},
    "Европейский лось": {"cat": "Млекопитающее", "emoji": "🫎", "space": 60.0, "sound": "Рёв!"},
    "Северный олень": {"cat": "Млекопитающее", "emoji": "🦌", "space": 50.0, "sound": "Фырканье!"},
    "Амурский тигр": {"cat": "Млекопитающее", "emoji": "🐯", "space": 80.0, "sound": "ГРРР!"},
    "Рысь": {"cat": "Млекопитающее", "emoji": "🐈", "space": 40.0, "sound": "Мур-р-р!"},
    "Пума": {"cat": "Млекопитающее", "emoji": "🐆", "space": 50.0, "sound": "Свист!"},
    "Белый медведь": {"cat": "Млекопитающее", "emoji": "🐻‍❄️", "space": 100.0, "sound": "Рык!"},
    
    # ПТИЦЫ
    "Кудрявый пеликан": {"cat": "Птица", "emoji": "🦤", "space": 40.0, "sound": "Клокот!"},
    "Розовый пеликан": {"cat": "Птица", "emoji": "🦩", "space": 40.0, "sound": "Клокот!"},
    "Чёрный аист": {"cat": "Птица", "emoji": "🦢", "space": 30.0, "sound": "Клац-клац!"},
    "Жёлтая цапля": {"cat": "Птица", "emoji": "🦩", "space": 25.0, "sound": "Кряк!"},
    "Красный ибис": {"cat": "Птица", "emoji": "🦩", "space": 20.0, "sound": "Курлык!"},
    "Каролинская утка": {"cat": "Птица", "emoji": "🦆", "space": 15.0, "sound": "Кря-кря!"},
    "Пингвин Гумбольдта": {"cat": "Птица", "emoji": "🐧", "space": 20.0, "sound": "Ар-ар!"},
    "Большой тукан": {"cat": "Птица", "emoji": "🦜", "space": 15.0, "sound": "Крак-крак!"},
    "Венценосный голубь": {"cat": "Птица", "emoji": "🕊️", "space": 15.0, "sound": "Гуль-гуль!"},

    # ПРЕСМЫКАЮЩИЕСЯ И ЗЕМНОВОДНЫЕ
    "Синехвостый варан": {"cat": "Пресмыкающееся", "emoji": "🦎", "space": 30.0, "sound": "Шшш!"},
    "Королевский питон": {"cat": "Пресмыкающееся", "emoji": "🐍", "space": 20.0, "sound": "Сссс!"},
    "Обыкновенная игуана": {"cat": "Пресмыкающееся", "emoji": "🦎", "space": 25.0, "sound": "Шипение!"},
    "Пятнистый эублефар": {"cat": "Пресмыкающееся", "emoji": "🦎", "space": 10.0, "sound": "Писк!"},
    "Бородатая агама": {"cat": "Пресмыкающееся", "emoji": "🦎", "space": 15.0, "sound": "Шшш!"},
    "Нильский крокодил": {"cat": "Пресмыкающееся", "emoji": "🐊", "space": 80.0, "sound": "Рёв!"},
    "Крокодиловый кайман": {"cat": "Пресмыкающееся", "emoji": "🐊", "space": 60.0, "sound": "Хлоп!"},

    # БЕСПОЗВОНОЧНЫЕ
    "Гигантский азиатский богомол": {"cat": "Беспозвоночное", "emoji": "🦗", "space": 5.0, "sound": "Шурш!"},
    "Паук-птицеед": {"cat": "Беспозвоночное", "emoji": "🕷️", "space": 5.0, "sound": "Тишина..."},
    "Мадагаскарский шипящий таракан": {"cat": "Беспозвоночное", "emoji": "🪳", "space": 5.0, "sound": "Шшш-шшш!"},
}
"""
with open('models/animal_catalog.py', 'w', encoding='utf-8') as f:
    f.write(catalog_code)

# 2. Обновляем animal.py, добавляя универсальный класс ZooAnimal
animal_update = """
from models.animal_catalog import ANIMAL_CATALOG

class ZooAnimal(Animal):
    \"\"\"Универсальный класс для любого животного из каталога\"\"\"
    def __init__(self, name: str, species_key: str, age: int, genetic_code):
        super().__init__(name, age, genetic_code)
        self.__species_key = species_key
        self.__data = ANIMAL_CATALOG.get(species_key, ANIMAL_CATALOG["Амурский тигр"]) # Fallback
        
    def make_sound(self) -> str:
        return self.__data["sound"]
    
    def get_species(self) -> str:
        return self.__species_key
    
    def get_space_required(self) -> float:
        return self.__data["space"]
    
    def get_emoji(self) -> str:
        return self.__data["emoji"]
    
    def _create_offspring(self, genetics):
        return ZooAnimal(f"Детёныш ({self.__species_key})", self.__species_key, 0, genetics)
"""

# Читаем текущий animal.py и добавляем в конец новый класс
with open('models/animal.py', 'a', encoding='utf-8') as f:
    f.write(animal_update)

# 3. Обновляем main_window.py, чтобы использовать выпадающий список вместо кнопок
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QFormLayout, QLineEdit, QComboBox, QSpinBox, QGroupBox
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode
from models.animal_catalog import ANIMAL_CATALOG
from ui.breeding_dialog import BreedingDialog
from ui.screens.finance_screen import FinanceScreen
from ui.screens.staff_screen import StaffScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(1200, 800)
        
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
        self.settings_screen = self._create_settings_screen()
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(self.settings_screen)
        sidebar.setCurrentRow(0)

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
        btn_save = QPushButton("💾 Сохранить настройки")
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
        title = QLabel("Zoo Legacy: Управление зоопарком")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        stats = QLabel("Баланс: 125 450 RUB | Репутация: 4.8")
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

        # Панель добавления животных
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Выберите животное:"))
        
        self.animal_selector = QComboBox()
        self.animal_selector.setStyleSheet("padding: 8px; border: 1px solid #D1D5DB; border-radius: 4px; min-width: 250px;")
        for species in ANIMAL_CATALOG.keys():
            emoji = ANIMAL_CATALOG[species]["emoji"]
            self.animal_selector.addItem(f"{emoji} {species}", species)
        add_layout.addWidget(self.animal_selector)
        
        btn_add = QPushButton("➕ Добавить в зоопарк")
        btn_add.setStyleSheet("background-color: #10B981; padding: 10px; font-weight: bold;")
        btn_add.clicked.connect(lambda: self._add_selected_animal(table))
        add_layout.addWidget(btn_add)
        add_layout.addStretch()
        layout.addLayout(add_layout)

        btn_layout = QHBoxLayout()
        btn_breed = QPushButton("🧬 Лаборатория скрещивания")
        btn_breed.setStyleSheet("background-color: #8B5CF6; min-width: 250px; padding: 12px;")
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

    def _add_selected_animal(self, table):
        species_key = self.animal_selector.currentData()
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene("Окрас", "A", "a"))
            genetics.add_gene(Gene("Размер", "B", "b"))
            
            # Создаем универсальное животное
            animal = ZooAnimal(f"Новый {species_key}", species_key, 3, genetics)
            animal.feed(30)
            self.db.add_animal(animal)
            self._refresh_table(table)
            QMessageBox.information(self, "Успех", f"{animal.get_emoji()} {species_key} успешно добавлен в зоопарк!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить животное.\\n\\n{e}")

    def _open_breeding_lab(self, table):
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._refresh_table(table)
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)

print("✅ Каталог из 30+ животных успешно добавлен!")
print("✅ Интерфейс обновлен: теперь есть удобный выпадающий список.")
print("Запустите: py app.py")