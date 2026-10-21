import os

# Создаем папки, если их нет
os.makedirs('database', exist_ok=True)
os.makedirs('ui', exist_ok=True)

# 1. Файл database/__init__.py
with open('database/__init__.py', 'w', encoding='utf-8') as f:
    f.write("")

# 2. Файл database/db_manager.py (Работа с SQLite)
db_manager_code = """import sqlite3
import json
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                species TEXT,
                age INTEGER,
                genetics TEXT,
                health INTEGER,
                hunger INTEGER
            )
        ''')
        self.conn.commit()

    def add_animal(self, animal):
        try:
            cursor = self.conn.cursor()
            # Сохраняем гены как JSON строку
            genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
            cursor.execute('''
                INSERT INTO animals (name, species, age, genetics, health, hunger)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Не удалось сохранить животное в базу данных. Проверьте права доступа к файлу.")

    def get_all_animals(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT name, species, age, health, hunger FROM animals')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить список животных из базы данных.")
"""
with open('database/db_manager.py', 'w', encoding='utf-8') as f:
    f.write(db_manager_code)

# 3. Файл ui/__init__.py
with open('ui/__init__.py', 'w', encoding='utf-8') as f:
    f.write("")

# 4. Файл ui/main_window.py (Графический интерфейс)
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager
from models.animal import Lion, Tiger
from models.genetics import Gene, GeneticCode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(800, 600)

        # Инициализация базы данных
        try:
            self.db = DatabaseManager()
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", str(e))
            exit()

        # Центральный виджет и компоновка
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Заголовок
        title = QLabel("🦁 Управление зоопарком")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #10B981; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Таблица животных
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Имя", "Вид", "Возраст", "Здоровье (%)", "Голод (%)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Кнопки управления
        btn_layout = QVBoxLayout()
        
        self.btn_add_lion = QPushButton("🦁 Добавить Льва (Симба)")
        self.btn_add_lion.setStyleSheet("background-color: #F59E0B; color: white; padding: 10px; font-weight: bold;")
        self.btn_add_lion.clicked.connect(self.add_test_lion)
        btn_layout.addWidget(self.btn_add_lion)

        self.btn_add_tiger = QPushButton("🐯 Добавить Тигра (Шерхан)")
        self.btn_add_tiger.setStyleSheet("background-color: #3B82F6; color: white; padding: 10px; font-weight: bold;")
        self.btn_add_tiger.clicked.connect(self.add_test_tiger)
        btn_layout.addWidget(self.btn_add_tiger)

        layout.addLayout(btn_layout)

        # Обновляем таблицу при запуске
        self.refresh_table()

    def refresh_table(self):
        try:
            animals = self.db.get_all_animals()
            self.table.setRowCount(len(animals))
            for row, animal_data in enumerate(animals):
                for col, data in enumerate(animal_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)
        except Exception as e:
            QMessageBox.warning(self, "Предупреждение", str(e))

    def add_test_lion(self):
        self._add_animal_safely(Lion, "Симба", 5, "Окрас", "A", "a")

    def add_test_tiger(self):
        self._add_animal_safely(Tiger, "Шерхан", 4, "Размер", "B", "b")

    def _add_animal_safely(self, animal_class, name, age, gene_name, dom, rec):
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene(gene_name, dom, rec))
            animal = animal_class(name, age, genetics)
            animal.feed(30) # Сразу немного покормим
            
            self.db.add_animal(animal)
            self.refresh_table()
            QMessageBox.information(self, "Успех", f"Животное '{animal.name}' успешно добавлено в базу данных и вольер!")
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка валидации", f"Некорректные данные: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Не удалось добавить животное.\\n\\nПодробности: {e}")
"""
with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)

# 5. Файл app.py (Точка входа для GUI)
app_code = """import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Создаем приложение
    app = QApplication(sys.argv)
    
    # Настраиваем стиль приложения (современный вид)
    app.setStyle("Fusion")
    
    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()
    
    # Запускаем цикл обработки событий
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

print("✅ Все файлы для графического интерфейса и базы данных успешно созданы!")
print("Теперь введите в терминале команду: py app.py")