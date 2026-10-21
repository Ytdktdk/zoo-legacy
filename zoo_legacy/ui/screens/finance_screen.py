from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt6.QtCore import Qt

class FinanceScreen(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__()
        self.db = db_manager
        self.parent = parent
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Финансы и аналитика")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        # Общий баланс
        balance = self.db.get_balance()
        balance_card = QFrame()
        balance_card.setStyleSheet("QFrame { background-color: #10B981; border-radius: 12px; padding: 25px; }")
        balance_layout = QVBoxLayout(balance_card)
        balance_title = QLabel("ОБЩИЙ БЮДЖЕТ ЗООПАРКА")
        balance_title.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        balance_layout.addWidget(balance_title)
        balance_value = QLabel(f"{balance:,.0f} RUB")
        balance_value.setStyleSheet("font-size: 36px; color: white; font-weight: bold;")
        balance_layout.addWidget(balance_value)
        layout.addWidget(balance_card)
        
        # Карточки статистики
        cards_layout = QHBoxLayout()
        stats = self.db.get_sales_statistics()
        total_revenue = stats[3] if stats[3] else 0
        total_tickets = (stats[1] if stats[1] else 0) + (stats[2] if stats[2] else 0)
        
        cards_layout.addWidget(self._create_stat_card("Доход от билетов", f"{total_revenue:,.0f} RUB", "#3B82F6"))
        cards_layout.addWidget(self._create_stat_card("Продано билетов", str(total_tickets), "#8B5CF6"))
        cards_layout.addWidget(self._create_stat_card("Взрослых", str(stats[1] if stats[1] else 0), "#F59E0B"))
        cards_layout.addWidget(self._create_stat_card("Льготных", str(stats[2] if stats[2] else 0), "#EF4444"))
        layout.addLayout(cards_layout)
        
        # Таблица доходов
        income_title = QLabel("📈 История доходов (продажа билетов)")
        income_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(income_title)
        
        self.income_table = QTableWidget()
        self.income_table.setColumnCount(5)
        self.income_table.setHorizontalHeaderLabels(["Дата", "Посетитель", "Взрослых", "Льготных", "Сумма"])
        self.income_table.horizontalHeader().setStretchLastSection(True)
        self.income_table.setAlternatingRowColors(True)
        layout.addWidget(self.income_table)
        
        # Таблица расходов
        expense_title = QLabel("📉 История расходов (покупка животных)")
        expense_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(expense_title)
        
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Дата", "Описание", "Сумма", "Время"])
        self.expense_table.horizontalHeader().setStretchLastSection(True)
        self.expense_table.setAlternatingRowColors(True)
        layout.addWidget(self.expense_table)
        
        self._refresh_tables()
    
    def _create_stat_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: white; border-radius: 8px; padding: 15px; border-left: 4px solid {color}; }}")
        layout = QVBoxLayout(frame)
        layout.addWidget(QLabel(title))
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
        return frame
    
    def _refresh_tables(self):
        sales = self.db.get_ticket_sales_by_date()
        self.income_table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            for col, data in enumerate([sale[1], sale[2], sale[3], sale[4], sale[5]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 4:
                    item.setForeground(Qt.GlobalColor.darkGreen)
                self.income_table.setItem(row, col, item)
        
        expenses = self.db.get_expenses()
        self.expense_table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            for col, data in enumerate([expense[1], expense[2], expense[3], expense[4]]):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 2:
                    item.setForeground(Qt.GlobalColor.red)
                self.expense_table.setItem(row, col, item)
    
    def refresh(self):
        self._refresh_tables()
