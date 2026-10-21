code = '''from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode
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
        self.balance = 125450
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
        self.finance_screen = FinanceScreen(self.db)
        self.staff_screen = StaffScreen()
        self.visitors_screen = VisitorsScreen(self.db)
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.catalog_screen)
        self.stack.addWidget(self.breeding_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(self.visitors_screen)
        sidebar.setCurrentRow(0)
    
    def _create_zoo_map(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        header = QHBoxLayout()
        title = QLabel("КАРТА ЗООПАРКА")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        stats = QLabel(f"Баланс: {self.balance:,} RUB")
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
'''

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ MainWindow обновлен")
print("\n Все обновления установлены!")
print("Запустите: py app.py")