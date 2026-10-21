code = '''from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt
import random

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
        
        cards_layout = QHBoxLayout()
        stats = self.db.get_sales_statistics()
        total_revenue = stats[3] if stats[3] else 0
        total_tickets = (stats[1] if stats[1] else 0) + (stats[2] if stats[2] else 0)
        
        cards_layout.addWidget(self._create_stat_card("Доход от билетов", f"{total_revenue:,.0f} RUB", "#10B981"))
        cards_layout.addWidget(self._create_stat_card("Продано билетов", str(total_tickets), "#3B82F6"))
        cards_layout.addWidget(self._create_stat_card("Взрослых", str(stats[1] if stats[1] else 0), "#F59E0B"))
        cards_layout.addWidget(self._create_stat_card("Льготных", str(stats[2] if stats[2] else 0), "#8B5CF6"))
        layout.addLayout(cards_layout)
        
        simulate_btn = QPushButton("🎲 Симулировать день (15 посетителей)")
        simulate_btn.setStyleSheet("QPushButton { background-color: #8B5CF6; color: white; padding: 15px; font-size: 16px; font-weight: bold; border-radius: 8px; } QPushButton:hover { background-color: #7C3AED; }")
        simulate_btn.clicked.connect(self._simulate_day)
        layout.addWidget(simulate_btn)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_title = QLabel("История продаж")
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
        self._refresh_table()
    
    def _create_stat_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: white; border-radius: 8px; padding: 15px; border-left: 4px solid {color}; }}")
        layout = QVBoxLayout(frame)
        layout.addWidget(QLabel(title))
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
        return frame
    
    def _refresh_table(self):
        sales = self.db.get_ticket_sales_by_date()
        self.sales_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            for col, data in enumerate([sale[1], sale[2], sale[3], sale[4], sale[5]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 4:
                    item.setForeground(Qt.GlobalColor.darkGreen)
                self.sales_table.setItem(row, col, item)
    
    def _simulate_day(self):
        names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Попов"]
        total_revenue = 0
        total_visitors = 0
        for i in range(15):
            name = random.choice(names) + " А."
            adult = random.randint(1, 3)
            discount = random.randint(0, 2)
            total = adult * 700 + discount * 350
            self.db.add_ticket_sale(name, adult, discount, total)
            total_revenue += total
            total_visitors += adult + discount
        QMessageBox.information(self, "День смоделирован!", f"👥 Посетителей: {total_visitors}\\n💰 Доход: {total_revenue:,} руб.")
        self._refresh_table()
'''

with open('ui/screens/finance_screen.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ FinanceScreen создан")