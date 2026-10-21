from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
import random
from database.db_manager import DatabaseManager
from models.animal_catalog import ANIMAL_CATALOG
from ui.breeding_dialog import BreedingDialog
from ui.screens.catalog_screen import CatalogScreen

class MainWindow(QMainWindow):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.setWindowTitle('Zoo Legacy')
        self.resize(1400, 900)
        self.setStyleSheet('background-color: #0b0f19;')
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: #0b0f19;')
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        sidebar = QListWidget()
        sidebar.setMaximumWidth(220)
        sidebar.setMinimumWidth(220)
        sidebar.addItem('Мой зоопарк')
        sidebar.addItem('Каталог')
        sidebar.addItem('Лаборатория')
        sidebar.addItem('Журнал событий')
        sidebar.addItem('')
        sidebar.addItem('Выход')
        sidebar.currentRowChanged.connect(self._switch_screen)
        sidebar.itemClicked.connect(self._on_item_clicked)
        sidebar.setStyleSheet('QListWidget { background-color: #111827; color: #e5e7eb; border: 1px solid #1a2436; border-radius: 20px; font-size: 15px; } QListWidget::item { padding: 18px 22px; border-bottom: 1px solid #1f2937; margin: 4px; border-radius: 10px; } QListWidget::item:selected { background-color: rgba(0, 255, 136, 0.15); color: #00ff88; border-left: 3px solid #00ff88; font-weight: bold; } QListWidget::item:hover { background-color: rgba(0, 229, 255, 0.1); color: #00e5ff; }')
        main_layout.addWidget(sidebar)
        self.stack = QStackedWidget()
        self.stack.setStyleSheet('background-color: #0b0f19;')
        main_layout.addWidget(self.stack)
        self.map_screen = self._create_zoo_map()
        self.catalog_screen = CatalogScreen(self.db, self)
        self.breeding_screen = self._create_breeding_screen()
        self.events_screen = self._create_events_screen()
        for screen in [self.map_screen, self.catalog_screen, self.breeding_screen, self.events_screen]:
            self.stack.addWidget(screen)
        sidebar.setCurrentRow(0)
        self._update_header()

    def _on_item_clicked(self, item):
        if item.text() == 'Выход':
            self._go_to_menu()
            self.stack.parent().findChild(QListWidget).setCurrentRow(0)

    def _update_header(self):
        state = self.db.get_game_state()
        if state:
            day, balance, energy, max_energy, reputation, level, experience, science = state
            self.day_label.setText(f'День: {day}')
            self.balance_label.setText(f'Баланс: {balance:,.0f} RUB')
            self.energy_label.setText(f'Энергия: {energy}/{max_energy}')
            self.level_label.setText(f'Уровень: {level}')
            self.science_label.setText(f'Наука: {science}')
            income = self.db.get_total_daily_income()
            self.income_label.setText(f'+{income:,} RUB/день')

    def _create_zoo_map(self):
        widget = QWidget()
        widget.setStyleSheet('background-color: #0b0f19;')
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        header = QFrame()
        header.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f9b0f, stop:1 #4CAF50); border-radius: 15px; padding: 20px;')
        header_layout = QHBoxLayout(header)
        title = QLabel('МОЙ ЗООПАРК')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: white;')
        header_layout.addWidget(title)
        header_layout.addStretch()
        info_frame = QFrame()
        info_frame.setStyleSheet('background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px 20px;')
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(15)
        self.day_label = QLabel('День: 1')
        self.day_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #90EE90;')
        info_layout.addWidget(self.day_label)
        self.balance_label = QLabel('Баланс: 0 RUB')
        self.balance_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #FFD700;')
        info_layout.addWidget(self.balance_label)
        self.energy_label = QLabel('Энергия: 100/100')
        self.energy_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #42A5F5;')
        info_layout.addWidget(self.energy_label)
        self.level_label = QLabel('Уровень: 1')
        self.level_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #FF9800;')
        info_layout.addWidget(self.level_label)
        self.science_label = QLabel('Наука: 0')
        self.science_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #9C27B0;')
        info_layout.addWidget(self.science_label)
        self.income_label = QLabel('+0 RUB/день')
        self.income_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #90EE90;')
        info_layout.addWidget(self.income_label)
        header_layout.addWidget(info_frame)
        layout.addWidget(header)
        btn_next_day = QPushButton('СЛЕДУЮЩИЙ ДЕНЬ')
        btn_next_day.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF9800, stop:1 #FFB74D); color: white; padding: 15px 30px; font-size: 18px; font-weight: bold; border-radius: 12px; border: none; min-width: 200px;')
        btn_next_day.clicked.connect(self._next_day)
        layout.addWidget(btn_next_day)
        scroll = QScrollArea()
        scroll.setStyleSheet('QScrollArea { border: none; background-color: transparent; }')
        scroll_content = QWidget()
        scroll_content.setStyleSheet('background-color: transparent;')
        self.animals_grid = QGridLayout(scroll_content)
        self.animals_grid.setSpacing(20)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self._refresh_zoo_map()
        return widget

    def _go_to_menu(self):
        reply = QMessageBox.question(self, 'Выход в меню', 'Сохранить игру и выйти в главное меню?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.save_game()
            app = self.window()
            while app and not isinstance(app, type(self.stack.parent()) if self.stack.parent() else QMainWindow):
                app = app.parent()
            if app and hasattr(app, 'stack') and hasattr(app, 'start_screen'):
                app.stack.setCurrentWidget(app.start_screen)
            return True
        return False

    def _next_day(self):
        day = self.db.get_day()
        income = self.db.get_total_daily_income()
        animals = self.db.get_all_animals()
        expenses = len(animals) * 50
        self.db.update_balance(income - expenses)
        self.db.next_day()
        self.db.add_experience(10)
        msg_lines = []
        msg_lines.append(f'День {day} завершен!')
        msg_lines.append('')
        msg_lines.append(f'Доход от животных: +{income:,} RUB')
        msg_lines.append(f'Расходы на содержание: -{expenses:,} RUB')
        msg_lines.append(f'Чистая прибыль: {income - expenses:,} RUB')
        msg_lines.append('')
        msg_lines.append('Энергия восстановлена!')
        if random.random() < 0.3:
            event = random.choice([
                ('Пожертвование', 5000, 'Меценат пожертвовал 5000 RUB!'),
                ('Болезнь', -2000, 'Одно животное заболело. Лечение: -2000 RUB'),
                ('Мутация', 0, 'У одного животного произошла спонтанная мутация!'),
                ('Звездный гость', 10000, 'Известный блогер посетил зоопарк! +10000 RUB'),
            ])
            self.db.update_balance(event[1])
            self.db.log_event(day + 1, event[0], event[2], event[1])
            msg_lines.append('')
            msg_lines.append(f'СОБЫТИЕ: {event[2]}')
        self.db.log_event(day + 1, 'Конец дня', f'Доход: {income}, Расходы: {expenses}', income - expenses)
        self._update_header()
        self._refresh_zoo_map()
        if hasattr(self, 'events_screen'):
            self._update_events_screen()
        QMessageBox.information(self, f'День {day} завершен', '\n'.join(msg_lines))

    def _refresh_zoo_map(self):
        while self.animals_grid.count():
            item = self.animals_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        animals = self.db.get_all_animals()
        if not animals:
            empty = QLabel('У вас пока нет животных. Зайдите в Каталог, чтобы купить первое!')
            empty.setStyleSheet('font-size: 20px; color: #888; padding: 50px;')
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.animals_grid.addWidget(empty, 0, 0)
            return
        for idx, animal_data in enumerate(animals):
            card = self._create_animal_card(animal_data)
            self.animals_grid.addWidget(card, idx // 3, idx % 3)

    def _create_animal_card(self, animal_data):
        species = animal_data[2]
        data = ANIMAL_CATALOG.get(species, {'image': '', 'cat': 'Неизвестно', 'emoji': '?'})
        rarity = animal_data[6] if len(animal_data) > 6 else 'Обычное'
        income = animal_data[7] if len(animal_data) > 7 else 100
        mutation = animal_data[10] if len(animal_data) > 10 else ''
        rarity_colors = {'Обычное': '#808080', 'Необычное': '#4CAF50', 'Редкое': '#2196F3', 'Эпическое': '#9C27B0', 'Легендарное': '#FFD700'}
        rarity_color = rarity_colors.get(rarity, '#808080')
        card = QFrame()
        card.setFixedHeight(420)
        card.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0a1f0a, stop:1 #051505);
                border-radius: 15px;
                border: none;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a5f1a, stop:1 #0a3f0a);
                border: 2px solid #00ff88;
            }
        ''')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setFixedSize(400, 220)
        photo_label.setStyleSheet('border-top-left-radius: 15px; border-top-right-radius: 15px;')
        img_path = data.get('image', '')
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            scaled = pixmap.scaled(400, 220, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            photo_label.setPixmap(scaled)
        else:
            photo_label.setText(data.get('emoji', '?'))
            photo_label.setStyleSheet('font-size: 100px; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e); border-top-left-radius: 15px; border-top-right-radius: 15px; color: ' + rarity_color + ';')
        layout.addWidget(photo_label)
        info = QWidget()
        info.setStyleSheet('background: rgba(5, 15, 5, 0.85); border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;')
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(15, 12, 15, 12)
        info_layout.setSpacing(5)
        name = QLabel(animal_data[1])
        name.setStyleSheet('font-size: 18px; font-weight: bold; color: #ffffff;')
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(name)
        rarity_label = QLabel('Редкость: ' + rarity)
        rarity_label.setStyleSheet('font-size: 13px; font-weight: bold; color: ' + rarity_color + ';')
        rarity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(rarity_label)
        age_label = QLabel(data.get('cat', '') + ' | ' + str(animal_data[3]) + ' лет')
        age_label.setStyleSheet('font-size: 12px; color: #a0a0a0;')
        age_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(age_label)
        health = animal_data[4]
        health_color = '#4CAF50' if health > 70 else '#FFA500' if health > 40 else '#EF4444'
        health_label = QLabel('Здоровье: ' + str(health) + '%')
        health_label.setStyleSheet('font-size: 13px; font-weight: bold; color: ' + health_color + ';')
        health_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(health_label)
        hunger = animal_data[5]
        hunger_color = '#4CAF50' if hunger < 30 else '#FFA500' if hunger < 60 else '#EF4444'
        hunger_label = QLabel('Голод: ' + str(hunger) + '%')
        hunger_label.setStyleSheet('font-size: 13px; font-weight: bold; color: ' + hunger_color + ';')
        hunger_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(hunger_label)
        income_label = QLabel('+' + f'{income:,}' + ' RUB/день')
        income_label.setStyleSheet('font-size: 13px; font-weight: bold; color: #90EE90;')
        income_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(income_label)
        if mutation:
            mut_label = QLabel('🧬 МУТАЦИЯ: ' + mutation)
            mut_label.setStyleSheet('font-size: 12px; font-weight: bold; color: #FF00FF; background: rgba(255, 0, 255, 0.2); border-radius: 6px; padding: 4px;')
            mut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_layout.addWidget(mut_label)
        layout.addWidget(info)
        return card

    def _create_breeding_screen(self):
        widget = QWidget()
        widget.setStyleSheet('background-color: #0b0f19;')
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)
        title = QLabel('ЛАБОРАТОРИЯ СКРЕЩИВАНИЯ')
        title.setStyleSheet('font-size: 32px; font-weight: bold; color: #9C27B0;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        desc = QLabel('Скрещивайте животных для получения редкого потомства!\nТребование: 2 животных одного вида, возраст 2+ года')
        desc.setStyleSheet('font-size: 16px; color: #a0a0a0;')
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        btn = QPushButton('ОТКРЫТЬ ЛАБОРАТОРИЮ')
        btn.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9C27B0, stop:1 #BA68C8); color: white; padding: 20px 50px; font-size: 20px; font-weight: bold; border-radius: 15px; border: none;')
        btn.clicked.connect(self._open_breeding)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return widget

    def _open_breeding(self):
        energy = self.db.get_energy()
        if energy < 30:
            QMessageBox.warning(self, 'Недостаточно энергии', 'Для скрещивания нужно 30 энергии. Перейдите к следующему дню!')
            return
        dialog = BreedingDialog(self.db, self)
        if dialog.exec():
            self._update_header()
            self._refresh_zoo_map()

    def _create_events_screen(self):
        widget = QWidget()
        widget.setStyleSheet('background-color: #0b0f19;')
        self.events_layout = QVBoxLayout(widget)
        self.events_layout.setContentsMargins(25, 25, 25, 25)
        self.events_layout.setSpacing(20)
        title = QLabel('ЖУРНАЛ СОБЫТИЙ')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #2196F3;')
        self.events_layout.addWidget(title)
        self.events_scroll = QScrollArea()
        self.events_scroll.setStyleSheet('QScrollArea { border: none; background-color: transparent; }')
        self.events_content = QWidget()
        self.events_content.setStyleSheet('background-color: transparent;')
        self.events_content_layout = QVBoxLayout(self.events_content)
        self.events_content_layout.setSpacing(10)
        self.events_scroll.setWidget(self.events_content)
        self.events_scroll.setWidgetResizable(True)
        self.events_layout.addWidget(self.events_scroll)
        self._update_events_screen()
        return widget

    def _update_events_screen(self):
        while self.events_content_layout.count():
            item = self.events_content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        events = self.db.get_events_log(50)
        if not events:
            no_events = QLabel('Пока нет событий. Начните играть!')
            no_events.setStyleSheet('font-size: 20px; color: #888; padding: 50px;')
            self.events_content_layout.addWidget(no_events)
        else:
            for day, event_type, description, amount in events:
                event_frame = QFrame()
                color = '#4CAF50' if amount >= 0 else '#EF4444'
                event_frame.setStyleSheet('background: rgba(255,255,255,0.05); border-left: 4px solid ' + color + '; border-radius: 8px; padding: 12px;')
                event_layout = QHBoxLayout(event_frame)
                day_label = QLabel('День ' + str(day))
                day_label.setStyleSheet('font-size: 13px; color: #888; min-width: 70px;')
                event_layout.addWidget(day_label)
                type_label = QLabel(event_type)
                type_label.setStyleSheet('font-size: 14px; font-weight: bold; color: ' + color + '; min-width: 120px;')
                event_layout.addWidget(type_label)
                desc_label = QLabel(description)
                desc_label.setStyleSheet('font-size: 14px; color: #e8e8e8;')
                desc_label.setWordWrap(True)
                event_layout.addWidget(desc_label)
                if amount != 0:
                    amount_label = QLabel(f'{amount:+,.0f} RUB')
                    amount_label.setStyleSheet('font-size: 14px; font-weight: bold; color: ' + color + ';')
                    event_layout.addWidget(amount_label)
                self.events_content_layout.addWidget(event_frame)
        self.events_content_layout.addStretch()

    def _switch_screen(self, index):
        if index == 5:
            return
        if index == 4:
            return
        self.stack.setCurrentIndex(index)
        if index == 3:
            self._update_events_screen()

    def _update_all(self):
        self._update_header()
        self._refresh_zoo_map()

    def refresh_all(self):
        self._update_header()
        self._refresh_zoo_map()