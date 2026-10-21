from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QDialog, QScrollArea, QTextEdit, QLineEdit, QCheckBox, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt

class VisitorsScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__()
        self.db = db_manager
        self.parent = parent
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
        buy_ticket_btn.setStyleSheet("QPushButton { background-color: #FCD34D; color: #1F2937; padding: 20px 40px; font-size: 20px; font-weight: bold; border-radius: 12px; border: 3px solid #F59E0B; } QPushButton:hover { background-color: #F59E0B; color: white; }")
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
        sections = [("Стоимость и оплата", "#10B981", self._show_prices),
                    ("Абонемент на месяц", "#3B82F6", self._show_subscription),
                    ("Правила зоопарка", "#F59E0B", self._show_rules)]
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
        buy_btn.clicked.connect(lambda: self._process_ticket_purchase(name_input.text(), phone_input.text(), email_input.text(), adult_counter.value(), льготный_counter.value(), checkbox1.isChecked(), checkbox2.isChecked(), checkbox3.isChecked(), dialog))
        layout.addWidget(buy_btn)
        dialog.exec()
    
    def _process_ticket_purchase(self, name, phone, email, adult_count, льготный_count, cb1, cb2, cb3, dialog):
        if not name or not phone or not email:
            QMessageBox.warning(dialog, "Ошибка", "Пожалуйста, заполните все поля")
            return
        if adult_count == 0 and льготный_count == 0:
            QMessageBox.warning(dialog, "Ошибка", "Выберите хотя бы один билет")
            return
        if not (cb1 and cb2 and cb3):
            QMessageBox.warning(dialog, "Ошибка", "Примите все условия соглашения")
            return
        total = adult_count * 700 + льготный_count * 350
        try:
            self.db.add_ticket_sale(name, adult_count, льготный_count, total)
            QMessageBox.information(dialog, "Билет куплен!", f"Спасибо, {name}!\n\nВзрослых: {adult_count}\nЛьготных: {льготный_count}\nИтого: {total} руб.\n\nДоход добавлен в бюджет!")
            dialog.close()
            if self.parent and hasattr(self.parent, '_update_all'):
                self.parent._update_all()
        except Exception as e:
            QMessageBox.critical(dialog, "Ошибка", f"Ошибка: {e}")
    
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
        content = "<h2>Стоимость посещения</h2><table border='1' cellpadding='8'><tr style='background-color:#10B981;color:white'><th>Категория</th><th>Цена</th></tr><tr><td>Взрослые</td><td><b>700 руб</b></td></tr><tr><td>Дети 7-16 лет</td><td><b>350 руб</b></td></tr><tr style='background-color:#BBF7D0'><td>Дети до 7 лет</td><td><b>Бесплатно</b></td></tr><tr style='background-color:#BBF7D0'><td>Инвалиды I группы</td><td><b>Бесплатно</b></td></tr></table>"
        self._show_modal("Стоимость", content)
    
    def _show_subscription(self):
        content = "<h2>Абонемент на месяц</h2><p>Действителен 1 месяц. Именной.</p><table border='1' cellpadding='8'><tr style='background-color:#3B82F6;color:white'><th>Категория</th><th>Цена</th></tr><tr><td>Взрослый</td><td><b>3000 руб</b></td></tr><tr><td>Льготный</td><td><b>1750 руб</b></td></tr><tr style='background-color:#BBF7D0'><td>Дети до 7 лет</td><td><b>Бесплатно</b></td></tr></table>"
        self._show_modal("Абонемент", content)
    
    def _show_rules(self):
        content = "<h2>Правила зоопарка</h2><ul><li>Соблюдайте тишину</li><li>НЕ кормите животных</li><li>НЕ заходите за ограждения</li><li>НЕ трогайте животных</li><li>Соблюдайте чистоту</li><li>Дети до 14 лет только с взрослыми</li></ul>"
        self._show_modal("Правила", content)
