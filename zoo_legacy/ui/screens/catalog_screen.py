from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from models.animal_catalog import ANIMAL_CATALOG
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode

class CatalogScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.parent_window = parent
        self.current_category = 'Все'
        self.setStyleSheet('background-color: #0b0f19;')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        title = QLabel('КАТАЛОГ ЖИВОТНЫХ')
        title.setStyleSheet('font-size: 32px; font-weight: bold; color: #00ff88;')
        layout.addWidget(title)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('Категория:'))
        categories = ['Все', 'Млекопитающие', 'Птицы', 'Пресмыкающиеся', 'Беспозвоночные']
        self.category_buttons = {}
        for cat in categories:
            btn = QPushButton(cat)
            btn.setCheckable(True)
            btn.setStyleSheet('QPushButton { background-color: #1a2436; color: white; padding: 12px 25px; font-size: 14px; font-weight: bold; border-radius: 8px; border: 1px solid #38bdf8; } QPushButton:checked { background-color: #00ff88; color: #0b0f19; border-color: #00ff88; } QPushButton:hover { background-color: #00e5ff; color: #0b0f19; }')
            btn.clicked.connect(lambda checked, c=cat: self._filter_by_category(c))
            self.category_buttons[cat] = btn
            filter_layout.addWidget(btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        self.category_buttons['Все'].setChecked(True)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea { border: none; background-color: transparent; }')
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet('background-color: transparent;')
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
        for species, data in ANIMAL_CATALOG.items():
            if self.current_category != 'Все' and data['cat'] != self.current_category:
                continue
            self.grid_layout.addWidget(self._create_animal_card(species, data), row, col)
            col += 1
            if col >= 3:
                col, row = 0, row + 1

    def _create_animal_card(self, species, data):
        card = QFrame()
        card.setFixedHeight(380)
        card.setStyleSheet('QFrame { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16213e, stop:1 #0f3460); border-radius: 12px; border: 1px solid #1a2436; } QFrame:hover { border: 2px solid #00e5ff; }')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setFixedSize(300, 200)
        photo_label.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e); border-top-left-radius: 12px; border-top-right-radius: 12px;')
        img_path = data.get('image', '')
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            scaled = pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(scaled)
        else:
            photo_label.setText('🦁')
            photo_label.setStyleSheet('font-size: 100px; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e); border-top-left-radius: 12px; border-top-right-radius: 12px;')
        layout.addWidget(photo_label)
        info_widget = QWidget()
        info_widget.setStyleSheet('background: transparent;')
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(20, 15, 20, 15)
        info_layout.setSpacing(8)
        name_label = QLabel(species)
        name_label.setStyleSheet('font-size: 16px; font-weight: bold; color: #e8e8e8;')
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        cat_label = QLabel(f"{data['cat']} • {data['space']} м²")
        cat_label.setStyleSheet('font-size: 13px; color: #a0a0a0;')
        cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(cat_label)
        price_label = QLabel(f"{data['price']:,} RUB")
        price_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #FFD700;')
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(price_label)
        add_btn = QPushButton('Добавить в зоопарк')
        add_btn.setStyleSheet('QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); color: white; padding: 12px; border-radius: 8px; font-weight: bold; border: none; } QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #66BB6A); }')
        add_btn.clicked.connect(lambda checked, s=species: self._add_animal(s))
        info_layout.addWidget(add_btn)
        layout.addWidget(info_widget)
        return card

    def _add_animal(self, species):
        data = ANIMAL_CATALOG[species]
        price = data['price']
        current_balance = self.db.get_balance()
        if current_balance < price:
            QMessageBox.warning(self, 'Недостаточно средств', f"Нужно {price:,} RUB\nВаш баланс: {current_balance:,.0f} RUB")
            return
        try:
            genetics = GeneticCode()
            genetics.add_gene(Gene('Окрас', 'A', 'a'))
            genetics.add_gene(Gene('Размер', 'B', 'b'))
            animal = ZooAnimal(species, 3, genetics)
            animal.feed(30)
            self.db.add_animal(animal, price)
            QMessageBox.information(self, 'Успех!', f"{species} добавлен в зоопарк!\nСписано: {price:,} RUB")
            if self.parent_window and hasattr(self.parent_window, '_update_all'):
                self.parent_window._update_all()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))