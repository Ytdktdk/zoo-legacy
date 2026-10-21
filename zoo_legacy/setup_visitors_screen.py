visitors_code = """from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
from PyQt6.QtCore import Qt

class VisitorsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: white; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Заголовок
        title = QLabel(" ИНФОРМАЦИЯ ДЛЯ ПОСЕТИТЕЛЕЙ")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        # Контактная информация и режим работы
        info_layout = QHBoxLayout()
        
        # Контакты
        contacts_frame = QFrame()
        contacts_frame.setStyleSheet("QFrame { background-color: #FDE68A; border-radius: 12px; padding: 20px; }")
        contacts_layout = QVBoxLayout(contacts_frame)
        
        contacts_title = QLabel("📞 КОНТАКТНАЯ ИНФОРМАЦИЯ")
        contacts_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        contacts_layout.addWidget(contacts_title)
        
        contacts_layout.addWidget(QLabel("📱 Приемная: +7 (383) 388-72-58"))
        contacts_layout.addWidget(QLabel("📧 E-mail: info@zoonovosib.ru"))
        contacts_layout.addWidget(QLabel("📍 Адрес: г. Новосибирск, ул. Тимирязева, д.71/1"))
        contacts_layout.addWidget(QLabel("\\n Мы в соцсетях:"))
        contacts_layout.addWidget(QLabel("  • Telegram канал"))
        contacts_layout.addWidget(QLabel("  • Группа ВКонтакте"))
        
        info_layout.addWidget(contacts_frame)
        
        # Режим работы
        hours_frame = QFrame()
        hours_frame.setStyleSheet("QFrame { background-color: #BBF7D0; border-radius: 12px; padding: 20px; }")
        hours_layout = QVBoxLayout(hours_frame)
        
        hours_title = QLabel("🕐 РЕЖИМ РАБОТЫ")
        hours_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2937;")
        hours_layout.addWidget(hours_title)
        
        hours_layout.addWidget(QLabel(" Будние дни: 8:00 - 21:00"))
        hours_layout.addWidget(QLabel("📅 Выходные: 8:00 - 22:00"))
        hours_layout.addWidget(QLabel("\\n Кассы закрываются:\\n   Будни: 20:00\\n   Выходные: 20:30"))
        hours_layout.addWidget(QLabel("\\n🅿️ Парковка: 100 руб/авто"))
        
        info_layout.addWidget(hours_frame)
        
        layout.addLayout(info_layout)
        
        # Кнопки разделов
        sections_layout = QHBoxLayout()
        sections = [
            ("💰 Стоимость и оплата", "#10B981"),
            ("🎫 Абонемент на месяц", "#3B82F6"),
            ("📜 Правила зоопарка", "#F59E0B"),
            ("⚖️ Правовая информация", "#8B5CF6"),
            ("♿ Доступность для инвалидов", "#EF4444"),
        ]
        
        for text, color in sections:
            btn = QPushButton(text)
            btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 30px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 12px;
                    min-width: 200px;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            ''')
            sections_layout.addWidget(btn)
        
        layout.addLayout(sections_layout)
        layout.addStretch()
"""

with open('ui/screens/visitors_screen.py', 'w', encoding='utf-8') as f:
    f.write(visitors_code)

print("✅ Часть 3 готова!")
print("\\n🎉 Все обновления установлены!")
print("Теперь запустите: py app.py")