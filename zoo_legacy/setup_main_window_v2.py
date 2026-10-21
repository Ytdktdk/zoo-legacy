main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QEnterEvent
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
        self.setWindowTitle("🦁 Zoo Legacy: Генетический Симулятор")
        self.resize(1400, 900)
        self.balance = 125450
        
        self._apply_theme(self._get_light_theme())

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
        sidebar.addItem("️ Карта зоопарка")
        sidebar.addItem("📚 Каталог животных")
        sidebar.addItem("🧬 Лаборатория")
        sidebar.addItem("💰 Финансы")
        sidebar.addItem("👥 Персонал")
        sidebar.addItem("👥 Посетители")
        sidebar.currentRowChanged.connect(self._switch_screen)
        main_layout.addWidget(sidebar)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        self.map_screen = self._create_zoo_map()
        self.catalog_screen = CatalogScreen(self.db, self)
        self.breeding_screen = self._create_breeding_placeholder()
        self.finance_screen = FinanceScreen()
        self.staff_screen = StaffScreen()
        self.visitors_screen = VisitorsScreen()
        
        self.stack.addWidget(self.map_screen)
        self.stack.addWidget(self.catalog_screen)
        self.stack.addWidget(self.breeding_screen)
        self.stack.addWidget(self.finance_screen)
        self.stack.addWidget(self.staff_screen)
        self.stack.addWidget(self.visitors_screen)
        sidebar.setCurrentRow(0)

    def _get_light_theme(self):
        return '''
            QMainWindow { background-color: #F3F4F6; }
            QLabel { color: #1F2937; }
            QTableWidget { background-color: white; border: 1px solid #D1D5DB; border-radius: 8px; }
            QTableWidget::item { padding: 10px; }
            QHeaderView::section { background-color: #10B981; color: white; font-weight: bold; padding: 10px; border: none; }
            QPushButton { border-radius: 8px; padding: 12px; font-weight: bold; font-size: 14px; color: white; }
            QPushButton:hover { opacity: 0.9; }
            QListWidget { background-color: #1E293B; border: none; font-size: 14px; }
            QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; }
            QListWidget::item:selected { background-color: #3B82F6; }
        '''

    def _apply_theme(self, stylesheet):
        self.setStyleSheet(stylesheet)

    def _create_zoo_map(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QHBoxLayout()
        title = QLabel("️ КАРТА ЗООПАРКА")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        stats = QLabel(f"💰 {self.balance:,} RUB | ⭐ 4.8 |  {len(self.db.get_all_animals())} животных")
        stats.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B5563;")
        header.addWidget(stats)
        layout.addLayout(header)

        # Сетка с животными
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        self.animals_grid = QGridLayout(scroll_content)
        self.animals_grid.setSpacing(25)
        self.animals_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self._refresh_zoo_map()
        return widget

    def _refresh_zoo_map(self):
        # Очищаем сетку
        while self.animals_grid.count():
            item = self.animals_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        animals = self.db.get_all_animals()
        
        for idx, animal_data in enumerate(animals):
            card = self._create_animal_card(animal_data)
            row = idx // 3
            col = idx % 3
            self.animals_grid.addWidget(card, row, col)

    def _create_animal_card(self, animal_data):
        species = animal_data[2]
        data = ANIMAL_CATALOG.get(species, {"emoji": "❓", "cat": "Неизвестно"})
        
        card = QFrame()
        card.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 0px;
            }
            QFrame:hover {
                border: 3px solid #3B82F6;
                background-color: #EFF6FF;
            }
        ''')
        card.setFixedHeight(280)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Фото
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet(f'''
            QLabel {{
                background-color: #10B981;
                font-size: 100px;
                min-height: 180px;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
            }}
        ''')
        layout.addWidget(photo_label)
        
        # Инфо
        info = QWidget()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(15, 10, 15, 10)
        
        name = QLabel(animal_data[1])
        name.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout.addWidget(name)
        
        species_label = QLabel(f"{species} • {animal_data[3]} лет")
        species_label.setStyleSheet("font-size: 13px; color: #6B7280;")
        info_layout.addWidget(species_label)
        
        health_label = QLabel(f"❤️ Здоровье: {animal_data[4]}%")
        health_label.setStyleSheet("font-size: 14px; color: #10B981; font-weight: bold;")
        info_layout.addWidget(health_label)
        
        hunger_label = QLabel(f"🍖 Голод: {animal_data[5]}%")
        hunger_label.setStyleSheet("font-size: 14px; color: #F59E0B; font-weight: bold;")
        info_layout.addWidget(hunger_label)
        
        layout.addWidget(info)
        
        # При клике - показать детальную информацию
        card.mousePressEvent = lambda e, a=animal_data: self._show_animal_details(a)
        
        return card

    def _show_animal_details(self, animal_data):
        QMessageBox.information(self, f"{animal_data[1]} - Детальная информация",
            f"📋 Информация о животном\\n\\n"
            f"🆔 ID: {animal_data[0]}\\n"
            f" Имя: {animal_data[1]}\\n"
            f"🦁 Вид: {animal_data[2]}\\n"
            f"🎂 Возраст: {animal_data[3]} лет\\n"
            f"❤️ Здоровье: {animal_data[4]}%\\n"
            f"🍖 Голод: {animal_data[5]}%\\n\\n"
            f"💡 Нажмите кнопки внизу для действий")

    def _create_breeding_placeholder(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("🧬 ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ")
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
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)

print("✅ Часть 2 готова!")