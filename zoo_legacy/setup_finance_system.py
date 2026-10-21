import os

# 1. Обновляем DatabaseManager - добавляем таблицу доходов
db_manager_code = """import sqlite3
import json
from datetime import datetime
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                visitor_name TEXT,
                adult_tickets INTEGER,
                discount_tickets INTEGER,
                total_amount REAL,
                timestamp TEXT
            )
        ''')
        
        self.conn.commit()

    def add_animal(self, animal):
        try:
            cursor = self.conn.cursor()
            genetics_str = json.dumps({k: v.genotype for k, v in animal.genetic_code.get_all_genes().items()})
            cursor.execute('''
                INSERT INTO animals (name, species, age, genetics, health, hunger)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (animal.name, animal.get_species(), animal.age, genetics_str, animal.health, animal.hunger))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise RuntimeError(f"Не удалось сохранить животное в базу данных.")

    def get_all_animals(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, species, age, health, hunger FROM animals')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить список животных.")

    def get_animal_genetics(self, animal_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT species, genetics FROM animals WHERE id = ?', (animal_id,))
            result = cursor.fetchone()
            if result:
                return result[0], json.loads(result[1])
            return None, None
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить генетику.")

    def add_ticket_sale(self, visitor_name, adult_tickets, discount_tickets, total_amount):
        try:
            cursor = self.conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO ticket_sales (date, visitor_name, adult_tickets, discount_tickets, total_amount, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (today, visitor_name, adult_tickets, discount_tickets, total_amount, timestamp))
            self.conn.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Не удалось записать продажу билета: {e}")

    def get_ticket_sales_by_date(self, date=None):
        try:
            cursor = self.conn.cursor()
            if date:
                cursor.execute('SELECT * FROM ticket_sales WHERE date = ?', (date,))
            else:
                cursor.execute('SELECT * FROM ticket_sales ORDER BY timestamp DESC')
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить продажи билетов.")

    def get_total_revenue(self, date=None):
        try:
            cursor = self.conn.cursor()
            if date:
                cursor.execute('SELECT SUM(total_amount) FROM ticket_sales WHERE date = ?', (date,))
            else:
                cursor.execute('SELECT SUM(total_amount) FROM ticket_sales')
            result = cursor.fetchone()
            return result[0] if result[0] else 0
        except Exception as e:
            raise RuntimeError(f"Не удалось подсчитать доход.")

    def get_sales_statistics(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_sales,
                    SUM(adult_tickets) as total_adult,
                    SUM(discount_tickets) as total_discount,
                    SUM(total_amount) as total_revenue
                FROM ticket_sales
            ''')
            return cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Не удалось получить статистику.")
"""

with open('database/db_manager.py', 'w', encoding='utf-8') as f:
    f.write(db_manager_code)
print("1. DatabaseManager обновлен")

# 2. Обновляем FinanceScreen - добавляем доходы от билетов
finance_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager

class FinanceScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Финансы и аналитика")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        # Карточки статистики
        cards_layout = QHBoxLayout()
        
        stats = self.db.get_sales_statistics()
        total_sales = stats[0] if stats[0] else 0
        total_adult = stats[1] if stats[1] else 0
        total_discount = stats[2] if stats[2] else 0
        total_revenue = stats[3] if stats[3] else 0
        
        income_card = self._create_stat_card("Доход от билетов", f"{total_revenue:,.0f} RUB", "#10B981")
        tickets_card = self._create_stat_card("Продано билетов", f"{total_adult + total_discount}", "#3B82F6")
        adult_card = self._create_stat_card("Взрослых", f"{total_adult}", "#F59E0B")
        discount_card = self._create_stat_card("Льготных", f"{total_discount}", "#8B5CF6")
        
        cards_layout.addWidget(income_card)
        cards_layout.addWidget(tickets_card)
        cards_layout.addWidget(adult_card)
        cards_layout.addWidget(discount_card)
        layout.addLayout(cards_layout)
        
        # Кнопка симуляции
        simulate_btn = QPushButton("🎲 Симулировать день (15 посетителей)")
        simulate_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        simulate_btn.clicked.connect(self._simulate_day)
        layout.addWidget(simulate_btn)
        
        # Таблица продаж
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        table_title = QLabel("История продаж билетов")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        table_layout.addWidget(table_title)
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(["Дата", "Посетитель", "Взрослых", "Льготных", "Сумма"])
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.sales_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.sales_table)
        
        scroll.setWidget(table_widget)
        layout.addWidget(scroll)
        
        self._refresh_sales_table()
    
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
    
    def _refresh_sales_table(self):
        sales = self.db.get_ticket_sales_by_date()
        self.sales_table.setRowCount(len(sales))
        
        for row, sale in enumerate(sales):
            # sale: (id, date, visitor_name, adult_tickets, discount_tickets, total_amount, timestamp)
            for col, data in enumerate([sale[1], sale[2], sale[3], sale[4], sale[5]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 4:  # Сумма
                    item.setForeground(Qt.GlobalColor.darkGreen)
                self.sales_table.setItem(row, col, item)
    
    def _simulate_day(self):
        import random
        from PyQt6.QtWidgets import QMessageBox
        
        names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Попов", "Васильев", "Зайцев", "Павлов", "Семенов"]
        
        total_revenue = 0
        total_visitors = 0
        
        for i in range(15):
            name = random.choice(names) + " " + chr(ord('А') + random.randint(0, 32)) + "."
            adult_tickets = random.randint(1, 3)
            discount_tickets = random.randint(0, 2)
            total_amount = adult_tickets * 700 + discount_tickets * 350
            
            self.db.add_ticket_sale(name, adult_tickets, discount_tickets, total_amount)
            total_revenue += total_amount
            total_visitors += adult_tickets + discount_tickets
        
        QMessageBox.information(self, "День смоделирован!", 
            f" Симуляция завершена!\\n\\n"
            f"👥 Посетителей: {total_visitors}\\n"
            f"💰 Доход: {total_revenue:,} RUB\\n\\n"
            f"Данные добавлены в таблицу продаж.")
        
        self._refresh_sales_table()
"""

with open('ui/screens/finance_screen.py', 'w', encoding='utf-8') as f:
    f.write(finance_code)
print("2. FinanceScreen обновлен")

# 3. Обновляем VisitorsScreen - добавляем запись в БД при покупке
visitors_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QDialog, QScrollArea, QTextEdit, QLineEdit, QCheckBox, QSpinBox
from PyQt6.QtCore import Qt

class VisitorsScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setStyleSheet("QWidget { background-color: white; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("ИНФОРМАЦИЯ ДЛЯ ПОСЕТИТЕЛЕЙ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        buy_ticket_btn = QPushButton("КУПИТЬ БИЛЕТ")
        buy_ticket_btn.setStyleSheet("""
            QPushButton {
                background-color: #FCD34D;
                color: #1F2937;
                padding: 20px 40px;
                font-size: 20px;
                font-weight: bold;
                border-radius: 12px;
                border: 3px solid #F59E0B;
            }
            QPushButton:hover {
                background-color: #F59E0B;
                color: white;
            }
        """)
        buy_ticket_btn.clicked.connect(self._show_ticket_form)
        header_layout.addWidget(buy_ticket_btn)
        
        layout.addLayout(header_layout)
        
        info_layout = QHBoxLayout()
        
        contacts_frame = QFrame()
        contacts_frame.setStyleSheet("QFrame { background-color: #FDE68A; border-radius: 12px; padding: 20px; }")
        contacts_layout = QVBoxLayout(contacts_frame)
        
        contacts_title = QLabel("КОНТАКТНАЯ ИНФОРМАЦИЯ")
        contacts_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        contacts_layout.addWidget(contacts_title)
        
        contacts_layout.addWidget(QLabel("Телефон: +7 (383) 388-72-58"))
        contacts_layout.addWidget(QLabel("E-mail: info@zoonovosib.ru"))
        contacts_layout.addWidget(QLabel("Адрес: г. Новосибирск, ул. Российская, д. 3"))
        contacts_layout.addWidget(QLabel(""))
        contacts_layout.addWidget(QLabel("Мы в социальных сетях:"))
        contacts_layout.addWidget(QLabel("  Telegram: @Zoo_Legacy"))
        contacts_layout.addWidget(QLabel("  ВКонтакте: ZooLegacy"))
        
        info_layout.addWidget(contacts_frame)
        
        hours_frame = QFrame()
        hours_frame.setStyleSheet("QFrame { background-color: #BBF7D0; border-radius: 12px; padding: 20px; }")
        hours_layout = QVBoxLayout(hours_frame)
        
        hours_title = QLabel("РЕЖИМ РАБОТЫ")
        hours_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        hours_layout.addWidget(hours_title)
        
        hours_layout.addWidget(QLabel("Будние дни: 8:00 - 21:00"))
        hours_layout.addWidget(QLabel("Выходные: 8:00 - 22:00"))
        hours_layout.addWidget(QLabel(""))
        hours_layout.addWidget(QLabel("Кассы закрываются:"))
        hours_layout.addWidget(QLabel("  Будни: 20:00"))
        hours_layout.addWidget(QLabel("  Выходные: 20:30"))
        hours_layout.addWidget(QLabel(""))
        hours_layout.addWidget(QLabel("Парковка: 100 руб/авто"))
        
        info_layout.addWidget(hours_frame)
        
        layout.addLayout(info_layout)
        
        sections_layout = QHBoxLayout()
        sections = [
            ("Стоимость и оплата", "#10B981", self._show_prices),
            ("Абонемент на месяц", "#3B82F6", self._show_subscription),
            ("Правила зоопарка", "#F59E0B", self._show_rules),
        ]
        
        for text, color, handler in sections:
            btn = QPushButton(text)
            btn.setStyleSheet(f"QPushButton {{ background-color: {color}; color: white; padding: 30px; font-size: 16px; font-weight: bold; border-radius: 12px; min-width: 200px; }} QPushButton:hover {{ opacity: 0.9; }}")
            btn.clicked.connect(handler)
            sections_layout.addWidget(btn)
        
        layout.addLayout(sections_layout)
        layout.addStretch()
    
    def _show_ticket_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Покупка билета")
        dialog.resize(500, 700)
        dialog.setStyleSheet("QDialog { background-color: #1E3A5F; }")
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Фамилия, Имя")
        name_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        layout.addWidget(name_input)
        
        contact_layout = QHBoxLayout()
        
        phone_input = QLineEdit()
        phone_input.setPlaceholderText("+7 (   )   -   -")
        phone_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        contact_layout.addWidget(phone_input)
        
        email_input = QLineEdit()
        email_input.setPlaceholderText("E-mail")
        email_input.setStyleSheet("QLineEdit { background-color: white; border: none; border-radius: 25px; padding: 15px 20px; font-size: 16px; }")
        contact_layout.addWidget(email_input)
        
        layout.addLayout(contact_layout)
        
        adult_frame = QFrame()
        adult_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; padding: 20px; }")
        adult_layout = QVBoxLayout(adult_frame)
        
        adult_header = QHBoxLayout()
        adult_title = QLabel("Входной билет Взрослый")
        adult_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        adult_header.addWidget(adult_title)
        adult_header.addStretch()
        
        adult_counter = QSpinBox()
        adult_counter.setRange(0, 20)
        adult_counter.setValue(0)
        adult_counter.setStyleSheet("QSpinBox { background-color: #1E3A5F; color: white; border: none; border-radius: 15px; padding: 8px 15px; font-size: 16px; font-weight: bold; min-width: 50px; }")
        adult_header.addWidget(adult_counter)
        adult_layout.addLayout(adult_header)
        
        adult_price = QLabel("Цена билета: 700 рублей.")
        adult_price.setStyleSheet("font-size: 14px; color: #6B7280;")
        adult_layout.addWidget(adult_price)
        
        layout.addWidget(adult_frame)
        
        льготный_frame = QFrame()
        льготный_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; padding: 20px; }")
        льготный_layout = QVBoxLayout(льготный_frame)
        
        льготный_header = QHBoxLayout()
        льготный_title = QLabel("Входной билет Льготный")
        льготный_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        льготный_header.addWidget(льготный_title)
        льготный_header.addStretch()
        
        льготный_counter = QSpinBox()
        льготный_counter.setRange(0, 20)
        льготный_counter.setValue(0)
        льготный_counter.setStyleSheet("QSpinBox { background-color: #1E3A5F; color: white; border: none; border-radius: 15px; padding: 8px 15px; font-size: 16px; font-weight: bold; min-width: 50px; }")
        льготный_header.addWidget(льготный_counter)
        льготный_layout.addLayout(льготный_header)
        
        льготный_price = QLabel("Цена билета: 350 рублей.")
        льготный_price.setStyleSheet("font-size: 14px; color: #6B7280;")
        льготный_layout.addWidget(льготный_price)
        
        layout.addWidget(льготный_frame)
        
        consent_frame = QFrame()
        consent_frame.setStyleSheet("QFrame { background-color: #9CA3AF; border-radius: 12px; padding: 15px; }")
        consent_layout = QVBoxLayout(consent_frame)
        
        checkbox1 = QCheckBox("Согласие на обработку персональных данных")
        checkbox1.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox1)
        
        checkbox2 = QCheckBox("Согласие с правилами поведения в зоопарке")
        checkbox2.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox2)
        
        checkbox3 = QCheckBox("Согласие с правилами покупки электронных билетов")
        checkbox3.setStyleSheet("QCheckBox { color: #1F2937; font-size: 13px; }")
        consent_layout.addWidget(checkbox3)
        
        layout.addWidget(consent_frame)
        
        buy_btn = QPushButton("КУПИТЬ")
        buy_btn.setStyleSheet("QPushButton { background-color: #D1D5DB; color: #1F2937; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 25px; } QPushButton:hover { background-color: #9CA3AF; }")
        buy_btn.clicked.connect(lambda: self._process_ticket_purchase(
            name_input.text(), phone_input.text(), email_input.text(),
            adult_counter.value(), льготный_counter.value(),
            checkbox1.isChecked(), checkbox2.isChecked(), checkbox3.isChecked(),
            dialog
        ))
        layout.addWidget(buy_btn)
        
        dialog.exec()
    
    def _process_ticket_purchase(self, name, phone, email, adult_count, льготный_count, cb1, cb2, cb3, dialog):
        from PyQt6.QtWidgets import QMessageBox
        
        if not name or not phone or not email:
            QMessageBox.warning(dialog, "Ошибка", "Пожалуйста, заполните все поля: Имя, Телефон и E-mail")
            return
        
        if adult_count == 0 and льготный_count == 0:
            QMessageBox.warning(dialog, "Ошибка", "Выберите хотя бы один билет")
            return
        
        if not (cb1 and cb2 and cb3):
            QMessageBox.warning(dialog, "Ошибка", "Необходимо принять все условия соглашения")
            return
        
        total = adult_count * 700 + льготный_count * 350
        
        # Записываем продажу в базу данных
        try:
            self.db.add_ticket_sale(name, adult_count, льготный_count, total)
            
            QMessageBox.information(dialog, "Билет куплен!", 
                f"Спасибо, {name}!\\n\\n"
                f"Взрослых билетов: {adult_count}\\n"
                f"Льготных билетов: {льготный_count}\\n"
                f"Итого к оплате: {total} рублей\\n\\n"
                f"Билет отправлен на {email}\\n\\n"
                f" Доход добавлен в бюджет зоопарка!")
            
            dialog.close()
        except Exception as e:
            QMessageBox.critical(dialog, "Ошибка", f"Не удалось записать покупку: {e}")
    
    def _show_modal(self, title, content):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(content)
        text_edit.setStyleSheet("QTextEdit { font-size: 14px; padding: 15px; border: none; }")
        
        scroll.setWidget(text_edit)
        layout.addWidget(scroll)
        
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("QPushButton { background-color: #10B981; color: white; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 8px; }")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def _show_prices(self):
        content = """
        <h2>Стоимость посещения зоопарка</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #10B981; color: white;">
                <th>Категории лиц</th>
                <th>Стоимость</th>
            </tr>
            <tr>
                <td>Для взрослых</td>
                <td><b>700 рублей</b></td>
            </tr>
            <tr>
                <td>Для детей (от 7 до 16 лет включительно)<br>Для школьников группой 15 человек руководитель бесплатно!</td>
                <td><b>350 рублей</b></td>
            </tr>
            <tr>
                <td>Для студентов очной формы обучения (средних и высших образовательных учреждений РФ очных отделений) до 24 лет</td>
                <td><b>350 рублей</b></td>
            </tr>
            <tr>
                <td>Для курсантов военных образовательных учреждений Министерства обороны Российской Федерации до 24 лет</td>
                <td><b>350 рублей</b></td>
            </tr>
            <tr>
                <td>Для лиц достигших возраста - женщины 55, мужчины 60 лет, инвалидов 2 группы, солдат срочной службы, участников ликвидации последствий катастрофы на Чернобыльской АЭС, ветеранов боевых действий</td>
                <td><b>350 рублей</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети до 7 лет (требуется: свидетельство о рождении или паспорт родителей)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети из многодетных семей до 16 лет включительно либо до окончания среднего общеобразовательного учреждения (с сопровождающим - один из родителей)<br>(требуется: паспорт родителя, справка или удостоверение о праве на льготы, свидетельства о рождении детей)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети - инвалиды (до 18 лет) с сопровождающим - один из родителей<br>(требуется: соответствующее удостоверение, справка МСЭ)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети и воспитанники интернатов, детских домов и приютов с одним сопровождающим<br>(требуется: официальное письмо - заявка на посещение от имени руководителя учреждения)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети-сироты и дети, оставшиеся без попечения родителей (до 18 лет)<br>(соответствующее удостоверение)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Инвалиды I группы с сопровождающим<br>(соответствующее удостоверение или справка МСЭ и паспорт)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Герои Советского союза, Герои Российской Федерации, полные кавалеры ордена Славы, Герои Социалистического труда<br>(соответствующее удостоверение)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Участники и ветераны Великой Отечественной Войны (удостоверение ветерана Великой Отечественной войны), бывшие несовершеннолетние узники концлагерей</td>
                <td><b>Бесплатно!</b></td>
            </tr>
        </table>
        """
        self._show_modal("Стоимость и оплата", content)
    
    def _show_subscription(self):
        content = """
        <h2>Абонемент на месяц</h2>
        <p><b>Абонемент действителен в течение одного месяца со дня приобретения.</b></p>
        <p>Абонемент является именным, без права передачи другому лицу. Абонемент действителен только при предъявлении паспорта или документа, удостоверяющего личность.</p>
        
        <h3>Стоимость абонемента:</h3>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #3B82F6; color: white;">
                <th>Категории лиц</th>
                <th>Стоимость</th>
            </tr>
            <tr>
                <td>Взрослый</td>
                <td><b>3000 рублей</b></td>
            </tr>
            <tr>
                <td>Льготный</td>
                <td><b>1750 рублей</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети до 7 лет (требуется: свидетельство о рождении или паспорт родителей)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети из многодетных семей до 16 лет включительно либо до окончания среднего общеобразовательного учреждения (с сопровождающим - один из родителей)<br>(требуется: паспорт родителя, справка или удостоверение о праве на льготы, свидетельства о рождении детей)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети - инвалиды (до 18 лет) с сопровождающим - один из родителей<br>(требуется: соответствующее удостоверение, справка МСЭ)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети и воспитанники интернатов, детских домов и приютов с одним сопровождающим<br>(требуется: официальное письмо - заявка на посещение от имени руководителя учреждения)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Дети-сироты и дети, оставшиеся без попечения родителей (до 18 лет)<br>(соответствующее удостоверение)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Инвалиды I группы с сопровождающим<br>(соответствующее удостоверение или справка МСЭ и паспорт)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Герои Советского союза, Герои Российской Федерации, полные кавалеры ордена Славы, Герои Социалистического труда<br>(соответствующее удостоверение)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
            <tr style="background-color: #BBF7D0;">
                <td>Участники и ветераны Великой Отечественной Войны<br>(удостоверение ветерана Великой Отечественной войны)</td>
                <td><b>Бесплатно!</b></td>
            </tr>
        </table>
        """
        self._show_modal("Абонемент на месяц", content)
    
    def _show_rules(self):
        content = """
        <h2>Правила поведения в Зоопарке</h2>
        <p>Коллекция животных зоопарка представляет большую научную и государственную ценность. Многие виды животных опасны для посетителей. Для сохранения животных и вашей безопасности соблюдайте следующие основные правила:</p>
        
        <ul>
            <li>Соблюдайте тишину;</li>
            <li><b>НЕ кормите, НЕ дразните и НЕ пугайте животных</b>, они нуждаются в спокойствии и отдыхе;</li>
            <li><b>НЕ заходите за барьеры и ограждения</b>, НЕ ставьте и НЕ сажайте на них детей - это опасно;</li>
            <li>НЕ прислоняйтесь к сеткам и решеткам помещений с животными, НЕ протягивайте через решетки руки и ноги;</li>
            <li>НЕ трогайте и НЕ пытайтесь погладить доступных для контактов животных, это может повлечь за собой несчастные случаи;</li>
            <li>НЕ приближайте посторонние предметы (телефоны, фотоаппараты, штативы, селфи палки и пр.) к сеткам и решеткам вольер с животными;</li>
            <li>НЕ бросайте в помещения с животными посторонние предметы. Соблюдайте чистоту;</li>
            <li>Фотографируйте животных без штативов и без применения вспышек;</li>
            <li>НЕ ходите по газонам, НЕ ломайте ветки зеленых насаждений для кормления животных, оберегайте цветочные насаждения;</li>
            <li>НЕ отпускайте от себя детей, следите за соблюдением ими правил поведения в зоопарке;</li>
            <li>НЕ перемещайте по своему усмотрению садово-парковый инвентарь: скамейки, диваны, шезлонги, стулья и т.п.;</li>
            <li>НЕ заходите в служебные помещения, а также в зоны строительства и ремонта;</li>
            <li>НЕ приводите и НЕ приносите с собой домашних животных;</li>
            <li>НЕ вступайте в разговоры с дежурными у вольер и клеток, НЕ отвлекайте их от службы по охране животных;</li>
            <li>Запрещено проводить экскурсии посетителям на территории зоопарка, без письменного согласования с директором зоопарка.</li>
        </ul>
        
        <p><b>Вход и передвижение по территории зоопарка на любых механических или электрических средствах передвижения (самокат, велосипед, роликовые коньки, скейтборд, сегвей, гироскутер, моноколесо и т.п.) ЗАПРЕЩЕН.</b></p>
        <p>Исключение: детская коляска; средства передвижения, предназначенные для инвалидов; беговел и трехколесный самокат для детей.</p>
        
        <ul>
            <li>Лица в нетрезвом виде на территорию зоопарка НЕ допускаются;</li>
            <li>Проносить на территорию зоопарка пиво и напитки, изготавливаемые на его основе, алкогольную и спиртосодержащую продукцию, а также продукцию, содержащую запрещенные вещества в соответствии с законодательством Российской Федерации запрещено;</li>
            <li>Курение на территории зоопарка запрещено;</li>
        </ul>
        
        <p>По всем интересующим вас вопросам и в случаях возникающих недоразумений обращайтесь к дежурному администратору (дирекция зоопарка).</p>
        
        <p><b>Билет сохранять до конца посещения.</b></p>
        <p><b>Дети до 14 лет могут проходить на территорию зоопарка только в сопровождении взрослого.</b></p>
        
        <p>Нарушение правил поведения является основанием для лишения права дальнейшего пребывания на территории зоопарка.</p>
        <p>Лица, допускающие нарушения правил поведения, могут быть удалены с территории зоопарка службой охраны.</p>
        <p>Также могут быть применены другие административные меры, соответствующие действующему законодательству.</p>
        """
        self._show_modal("Правила зоопарка", content)
"""

with open('ui/screens/visitors_screen.py', 'w', encoding='utf-8') as f:
    f.write(visitors_code)
print("3. VisitorsScreen обновлен")

# 4. Обновляем main_window.py - передаем db_manager в экраны
main_window_code = """from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QStackedWidget, QListWidget, QScrollArea, QFrame, QGridLayout
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
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(1400, 900)
        self.balance = 125450
        
        self.setStyleSheet("QMainWindow { background-color: #F3F4F6; } QLabel { color: #1F2937; } QTableWidget { background-color: white; border: 1px solid #D1D5DB; border-radius: 8px; } QTableWidget::item { padding: 10px; } QHeaderView::section { background-color: #10B981; color: white; font-weight: bold; padding: 10px; border: none; } QPushButton { border-radius: 8px; padding: 12px; font-weight: bold; font-size: 14px; color: white; } QPushButton:hover { opacity: 0.9; } QListWidget { background-color: #1E293B; border: none; font-size: 14px; } QListWidget::item { color: white; padding: 15px; border-bottom: 1px solid #334155; } QListWidget::item:selected { background-color: #3B82F6; }")

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
        layout.setSpacing(20)

        header = QHBoxLayout()
        title = QLabel("КАРТА ЗООПАРКА")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        header.addWidget(title)
        header.addStretch()
        animals_count = len(self.db.get_all_animals())
        stats = QLabel(f"Баланс: {self.balance:,} RUB | Животных: {animals_count}")
        stats.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B5563;")
        header.addWidget(stats)
        layout.addLayout(header)

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
        data = ANIMAL_CATALOG.get(species, {"emoji": "", "cat": "Неизвестно"})
        
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; padding: 0px; } QFrame:hover { border: 3px solid #3B82F6; background-color: #EFF6FF; }")
        card.setFixedHeight(280)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        
        photo_label = QLabel(data["emoji"])
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet("QLabel { background-color: #10B981; font-size: 100px; min-height: 180px; border-top-left-radius: 15px; border-top-right-radius: 15px; }")
        layout.addWidget(photo_label)
        
        info = QWidget()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(15, 10, 15, 10)
        
        name = QLabel(animal_data[1])
        name.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout.addWidget(name)
        
        species_label = QLabel(f"{species} - {animal_data[3]} лет")
        species_label.setStyleSheet("font-size: 13px; color: #6B7280;")
        info_layout.addWidget(species_label)
        
        health_label = QLabel(f"Здоровье: {animal_data[4]}%")
        health_label.setStyleSheet("font-size: 14px; color: #10B981; font-weight: bold;")
        info_layout.addWidget(health_label)
        
        hunger_label = QLabel(f"Голод: {animal_data[5]}%")
        hunger_label.setStyleSheet("font-size: 14px; color: #F59E0B; font-weight: bold;")
        info_layout.addWidget(hunger_label)
        
        layout.addWidget(info)
        
        card.mousePressEvent = lambda e, a=animal_data: self._show_animal_details(a)
        
        return card

    def _show_animal_details(self, animal_data):
        QMessageBox.information(self, f"{animal_data[1]} - Детальная информация",
            f"Информация о животном\\n\\n"
            f"ID: {animal_data[0]}\\n"
            f"Имя: {animal_data[1]}\\n"
            f"Вид: {animal_data[2]}\\n"
            f"Возраст: {animal_data[3]} лет\\n"
            f"Здоровье: {animal_data[4]}%\\n"
            f"Голод: {animal_data[5]}%")

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
"""

with open('ui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(main_window_code)
print("4. MainWindow обновлен")

print("\n✅ Все обновления установлены!")
print("Теперь запустите: py app.py")