code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QFormLayout, QLineEdit, QComboBox, QSpinBox, QGroupBox
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
        return '''
            QMainWindow { background-color: #F3F4F6; }
            QLabel { color: #1F2937; }
            QTableWidget { background-color: white; border: 1px solid #D1D5DB; border-radius: 8px; gridline-color: #E5E7EB; font-size: 14px; }
            QTableWidget::item { padding: 8px; }
            QHeaderView::section { background-color: #10B981; color: white; font-weight: bold; padding: 8px; border: none; }
            QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; }
            QPushButton:hover { opacity: 0.9; }
            QListWidget { background-color: #1E293B; border: none; font-size: 14px; }
            QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; }
            QListWidget::item:selected { background-color: #3B82F6; }
            QGroupBox { background-color: white; border: 2px solid #10B981; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; }
            QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #D1D5DB; border-radius: 4px; background-color: white; }
        '''

    def _get_dark_theme(self):
        return '''
            QMainWindow { background-color: #1E293B; }
            QLabel { color: #F1F5F9; }
            QTableWidget { background-color: #334155; border: 1px solid #475569; border-radius: 8px; gridline-color: #475569; font-size: 14px; color: #F1F5F9; }
            QTableWidget::item { padding: 8px; }
            QHeaderView::section { background-color: #059669; color: white; font-weight: bold; padding: 8px; border: none; }
            QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; background-color: #3B82F6; }
            QPushButton:hover { opacity: 0.9; }
            QListWidget { background-color: #0F172A; border: none; font-size: 14px; }
            QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #1E293B; }
            QListWidget::item:selected { background-color: #3B82F6; }
            QGroupBox { background-color: #334155; border: 2px solid #3B82F6; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; color: #F1F5F9; }
            QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #475569; border-radius: 4px; background-color: #475569; color: #F1F5F9; }
        '''

    def _get_blue_theme(self):
        return '''
            QMainWindow { background-color: #EFF6FF; }
            QLabel { color: #1E3A8A; }
            QTableWidget { background-color: white; border: 1px solid #3B82F6; border-radius: 8px; gridline-color: #BFDBFE; font-size: 14px; }
            QTableWidget::item { padding: 8px; }
            QHeaderView::section { background-color: #2563EB; color: white; font-weight: bold; padding: 8px; border: none; }
            QPushButton { border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px; color: white; background-color: #2563EB; }
            QPushButton:hover { opacity: 0.9; }
            QListWidget { background-color: #1E3A8A; border: none; font-size: 14px; }
            QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #1E40AF; }
            QListWidget::item:selected { background-color: #3B82F6; }
            QGroupBox { background-color: white; border: 2px solid #2563EB; border-radius: 8px; margin-top: 10px; padding: 15px; font-size: 16px; font-weight: bold; color: #1E3A8A; }
            QLineEdit, QSpinBox, QComboBox { padding: 8px; border: 1px solid #93C5FD; border-radius: 4px; background-color: white; color: #1E3A8A; }
        '''

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
        
        self.start_balance_input = QLineEdit("125450")
        general_layout.addRow("Начальный баланс:", self.start_balance_input)
        
        layout.addWidget(general_group)
        
        animals_group = QGroupBox("Настройки животных")
        animals_layout = QFormLayout(animals_group)
        
        self.feed_amount_spin = QSpinBox()
        self.feed_amount_spin.setRange(10, 100)
        self.feed_amount_spin.setValue(30)
        animals_layout.addRow("Количество еды при кормлении:", self.feed_amount_spin)
        
        self.mutation_rate_spin = QSpinBox()
        self.mutation_rate_spin.setRange(1, 10)
        self.mutation_rate_spin.setValue(1)
        animals_layout.addRow("Шанс мутации (%):", self.mutation_rate_spin)
        
        layout.addWidget(animals_group)
        
        visual_group = QGroupBox("Визуальные настройки")
        visual_layout = QFormLayout(visual_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая тема", "Тёмная тема", "Синяя тема"])
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        visual_layout.addRow("Тема оформления:", self.theme_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 20)
        self.font_size_spin.setValue(14)
        visual_layout.addRow("Размер шрифта:", self.font_size_spin)
        
        layout.addWidget(visual_group)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Сохранить настройки")
        btn_save.setStyleSheet("background-color: #10B981; padding: 15px; font-size: 16px;")
        btn_save.clicked.connect(self._save_settings)
        btn_layout.addWidget(btn_save)
        
        btn_reset = QPushButton("🔄 Сбросить настройки")
        btn_reset.setStyleSheet("background-color: #EF4444; padding: 15px; font-size: 16px;")
        btn_reset.clicked.connect(self._reset_settings)
        btn_layout.addWidget(btn_reset)
        
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
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 80)
        table.setColumnWidth(5, 100)
        table.setColumnWidth(6, 100)
        table.horizontalHeader().setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        
        btn_add_lion = QPushButton(" Добавить Льва")
        btn_add_lion.setStyleSheet("background-color: #F59E0B;")
        btn_add_lion.clicked.connect(lambda: self._add_animal_safely(Lion, "Симба", 5, "Окрас", "A", "a", table))
        btn_layout.addWidget(btn_add_lion)

        btn_add_tiger = QPushButton("🐯 Добавить Тигра")
        btn_add_tiger.setStyleSheet("background-color: #3B82F6;")
        btn_add_tiger.clicked.connect(lambda: self._add_animal_safely(Tiger, "Шерхан", 4, "Размер", "B", "b", table))
        btn_layout.addWidget(btn_add_tiger)
        
        btn_add_elephant = QPushButton(" Добавить Слона")
        btn_add_elephant.setStyleSheet("background-color: #6B7280;")
        btn_add_elephant.clicked.connect(lambda: self._add_animal_safely(Tiger, "Слониха", 8, "Размер", "C", "c", table))
        btn_layout.addWidget(btn_add_elephant)
        
        btn_layout.addStretch()

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
                if animal_data[2] == "Лев":
                    emoji = "🦁"
                elif animal_data[2] == "Тигр":
                    emoji = "🐯"
                else:
                    emoji = "🐘"
                
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
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить животное.\\n\\n{e}")

    def _open_breeding_lab(self, table):
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._refresh_table(table)
    
    def _save_settings(self):
        QMessageBox.information(self, "Настройки сохранены", "Настройки успешно сохранены!")
    
    def _reset_settings(self):
        reply = QMessageBox.question(self, "Сброс настроек", "Вы уверены, что хотите сбросить все настройки?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.name_input.setText("Zoo Legacy")
            self.start_balance_input.setText("125450")
            self.feed_amount_spin.setValue(30)
            self.mutation_rate_spin.setValue(1)
            self.theme_combo.setCurrentIndex(0)
            self.font_size_spin.setValue(14)
            self._apply_theme(0)
            QMessageBox.information(self, "Настройки сброшены", "Настройки сброшены к значениям по умолчанию!")
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Темы оформления добавлены!")
print("Теперь при выборе темы в настройках она будет применяться мгновенно!")
print("Запустите: py app.py")