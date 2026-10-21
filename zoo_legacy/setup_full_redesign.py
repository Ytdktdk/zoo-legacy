import os

os.makedirs('assets/animals', exist_ok=True)
os.makedirs('assets/staff', exist_ok=True)

# 1. Обновляем каталог с ценами
catalog_code = """# Каталог животных с ценами и категориями
ANIMAL_CATALOG = {
    # МЛЕКОПИТАЮЩИЕ
    "Кенгуру Беннетта": {"cat": "Млекопитающие", "emoji": "", "space": 30.0, "sound": "Пф-пф!", "price": 15000},
    "Большой серый кенгуру": {"cat": "Млекопитающие", "emoji": "", "space": 40.0, "sound": "Топ-топ!", "price": 25000},
    "Кошачий лемур": {"cat": "Млекопитающие", "emoji": "🐒", "space": 15.0, "sound": "Мяу-мяу!", "price": 12000},
    "Красный вари": {"cat": "Млекопитающие", "emoji": "", "space": 20.0, "sound": "Ууу-ууу!", "price": 18000},
    "Альпака": {"cat": "Млекопитающие", "emoji": "", "space": 25.0, "sound": "Хрум-хрум!", "price": 22000},
    "Таджикский винторогий козёл": {"cat": "Млекопитающие", "emoji": "🐐", "space": 35.0, "sound": "Ме-е-е!", "price": 20000},
    "Европейский лось": {"cat": "Млекопитающие", "emoji": "", "space": 60.0, "sound": "Рёв!", "price": 35000},
    "Северный олень": {"cat": "Млекопитающие", "emoji": "🦌", "space": 50.0, "sound": "Фырканье!", "price": 30000},
    "Амурский тигр": {"cat": "Млекопитающие", "emoji": "🐯", "space": 80.0, "sound": "ГРРР!", "price": 75000},
    "Рысь": {"cat": "Млекопитающие", "emoji": "", "space": 40.0, "sound": "Мур-р-р!", "price": 40000},
    "Пума": {"cat": "Млекопитающие", "emoji": "🐆", "space": 50.0, "sound": "Свист!", "price": 45000},
    "Белый медведь": {"cat": "Млекопитающие", "emoji": "🐻❄️", "space": 100.0, "sound": "Рык!", "price": 85000},
    
    # ПТИЦЫ
    "Кудрявый пеликан": {"cat": "Птицы", "emoji": "🦤", "space": 40.0, "sound": "Клокот!", "price": 18000},
    "Розовый пеликан": {"cat": "Птицы", "emoji": "🦩", "space": 40.0, "sound": "Клокот!", "price": 20000},
    "Чёрный аист": {"cat": "Птицы", "emoji": "", "space": 30.0, "sound": "Клац-клац!", "price": 25000},
    "Каролинская утка": {"cat": "Птицы", "emoji": "🦆", "space": 15.0, "sound": "Кря-кря!", "price": 8000},
    "Пингвин Гумбольдта": {"cat": "Птицы", "emoji": "🐧", "space": 20.0, "sound": "Ар-ар!", "price": 35000},
    "Большой тукан": {"cat": "Птицы", "emoji": "", "space": 15.0, "sound": "Крак-крак!", "price": 22000},
    
    # ПРЕСМЫКАЮЩИЕСЯ
    "Синехвостый варан": {"cat": "Пресмыкающиеся", "emoji": "", "space": 30.0, "sound": "Шшш!", "price": 15000},
    "Королевский питон": {"cat": "Пресмыкающиеся", "emoji": "🐍", "space": 20.0, "sound": "Сссс!", "price": 12000},
    "Обыкновенная игуана": {"cat": "Пресмыкающиеся", "emoji": "🦎", "space": 25.0, "sound": "Шипение!", "price": 10000},
    "Нильский крокодил": {"cat": "Пресмыкающиеся", "emoji": "", "space": 80.0, "sound": "Рёв!", "price": 45000},
    
    # БЕСПОЗВОНОЧНЫЕ
    "Гигантский азиатский богомол": {"cat": "Беспозвоночные", "emoji": "🦗", "space": 5.0, "sound": "Шурш!", "price": 3000},
    "Паук-птицеед": {"cat": "Беспозвоночные", "emoji": "🕷️", "space": 5.0, "sound": "Тишина...", "price": 5000},
}
"""
with open('models/animal_catalog.py', 'w', encoding='utf-8') as f:
    f.write(catalog_code)

# 2. Обновляем animal.py с методом to_dict для сериализации
animal_update = """

    def to_dict(self):
        return {
            "name": self._Animal__name,
            "age": self._Animal__age,
            "health": self._Animal__health,
            "hunger": self._Animal__hunger,
            "species": self.get_species(),
            "sound": self.make_sound(),
            "space": self.get_space_required()
        }
"""
with open('models/animal.py', 'a', encoding='utf-8') as f:
    f.write(animal_update)

# 3. Создаем улучшенный каталог с фильтрацией и ценами
catalog_screen_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QGridLayout, QMessageBox
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
        
        title = QLabel("📚 КАТАЛОГ ЖИВОТНЫХ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        # Фильтр по категориям
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("📂 Категория:"))
        
        categories = ["Все", "Млекопитающие", "Птицы", "Пресмыкающиеся", "Беспозвоночные"]
        self.category_buttons = {}
        for cat in categories:
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #10B981;
                    color: white;
                    padding: 12px 25px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                }
                QPushButton:checked {
                    background-color: #059669;
                    border: 2px solid #047857;
                }
            ''')
            btn.clicked.connect(lambda checked, c=cat: self._filter_by_category(c))
            self.category_buttons[cat] = btn
            filter_layout.addWidget(btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        self.category_buttons["Все"].setChecked(True)
        
        # Скролл для карточек
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
        # Очищаем текущие виджеты
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Создаем карточки
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
        card.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 0px;
            }
            QFrame:hover {
                border: 3px solid #10B981;
            }
        ''')
        card.setFixedHeight(320)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Фото/эмодзи
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet(f'''
            QLabel {{
                background-color: {self._get_category_color(data["cat"])};
                font-size: 100px;
                min-height: 200px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        ''')
        layout.addWidget(photo_label)
        
        # Информация
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(20, 15, 20, 15)
        info_layout.setSpacing(8)
        
        name_label = QLabel(species)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        
        cat_label = QLabel(f"{data['cat']} • {data['space']} м²")
        cat_label.setStyleSheet("font-size: 13px; color: #6B7280;")
        cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(cat_label)
        
        price_label = QLabel(f" {data['price']:,} RUB")
        price_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #F59E0B;")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(price_label)
        
        add_btn = QPushButton("➕ Добавить в зоопарк")
        add_btn.setStyleSheet('''
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #9CA3AF;
            }
        ''')
        add_btn.clicked.connect(lambda checked, s=species: self._add_animal(s))
        info_layout.addWidget(add_btn)
        
        layout.addWidget(info_widget)
        return card
    
    def _get_category_color(self, category):
        colors = {
            "Млекопитающие": "#FDE68A",
            "Птицы": "#BFDBFE",
            "Пресмыкающиеся": "#BBF7D0",
            "Беспозвоночные": "#FED7AA"
        }
        return colors.get(category, "#E5E7EB")
    
    def _add_animal(self, species):
        data = ANIMAL_CATALOG[species]
        price = data["price"]
        
        # Проверяем баланс (заглушка - в реальности брать из настроек)
        balance = 125450  # Нужно получать из реальной системы
        
        if balance < price:
            QMessageBox.warning(self, "Недостаточно средств", 
                f"💸 Для покупки {species} нужно {price:,} RUB\\n"
                f"Ваш баланс: {balance:,} RUB\\n\\n"
                f"Не хватает {price - balance:,} RUB")
            return
        
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene("Окрас", "A", "a"))
            genetics.add_gene(Gene("Размер", "B", "b"))
            
            animal = ZooAnimal(f"Новый {species}", species, 3, genetics)
            animal.feed(30)
            self.db.add_animal(animal)
            
            QMessageBox.information(self, "✅ Успешная покупка!", 
                f"{data['emoji']} {species} добавлен в ваш зоопарк!\\n\\n"
                f"💰 Списано: {price:,} RUB")
            
            if self.parent and hasattr(self.parent, '_refresh_table'):
                self.parent._refresh_table(self.parent.map_table)
                
        except Exception as e:
            QMessageBox.critical(self, " Ошибка", f"Не удалось добавить животное:\\n{e}")
"""
with open('ui/screens/catalog_screen.py', 'w', encoding='utf-8') as f:
    f.write(catalog_screen_code)

print("✅ Часть 1 готова! Создайте следующий файл...")