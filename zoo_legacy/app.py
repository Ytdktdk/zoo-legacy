import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database.db_manager import DatabaseManager
from ui.start_screen import StartScreen
from ui.main_window import MainWindow

class GameApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoo Legacy: Генетический Симулятор")
        self.resize(1400, 900)
        self.setStyleSheet("QMainWindow { background-color: #0b0f19; }")

        self.db = DatabaseManager()
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #0b0f19;")
        self.setCentralWidget(self.stack)

        self.start_screen = StartScreen(self)
        self.stack.addWidget(self.start_screen)

        self.game_window = None
        self.stack.setCurrentWidget(self.start_screen)

    def start_new_game(self):
        self.db.new_game()
        self._show_game()

    def continue_game(self):
        state = self.db.get_game_state()
        if not state:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Нет сохранения", "Сохраненная игра не найдена. Начните новую игру!")
            return
        self._show_game()

    def _show_game(self):
        if self.game_window is None:
            self.game_window = MainWindow(self.db)
            self.game_window._game_app = self
            self.stack.addWidget(self.game_window)
        else:
            self.game_window.refresh_all()
        self.stack.setCurrentWidget(self.game_window)

    def go_to_menu(self):
        self.stack.setCurrentWidget(self.start_screen)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow { background-color: #0b0f19; }
        QDialog { background-color: #0b0f19; }
        QWidget { background-color: transparent; color: #e5e7eb; font-family: "Segoe UI", sans-serif; }
        QPushButton { background-color: #1a2436; color: #ffffff; border: 1px solid #38bdf8; border-radius: 5px; padding: 8px 15px; font-size: 14px; font-weight: bold; }
        QPushButton:hover { background-color: #00e5ff; color: #0b0f19; border: 1px solid #00e5ff; }
        QPushButton:pressed { background-color: #00ff88; color: #0b0f19; }
        QListWidget { background-color: #111827; color: #e5e7eb; border: 1px solid #1a2436; border-radius: 6px; font-size: 15px; }
        QListWidget::item { padding: 18px 22px; border-bottom: 1px solid #1f2937; margin: 2px; }
        QListWidget::item:selected { background-color: rgba(0, 255, 136, 0.15); color: #00ff88; border-left: 3px solid #00ff88; }
        QListWidget::item:hover { background-color: rgba(0, 229, 255, 0.1); color: #00e5ff; }
        QLabel { color: #e5e7eb; font-family: "Segoe UI", sans-serif; }
        QFrame { border-radius: 15px; }
        QScrollArea { border: none; background-color: transparent; }
        QScrollBar:vertical { background: #111827; width: 8px; border-radius: 4px; }
        QScrollBar::handle:vertical { background: #1a2436; border-radius: 4px; min-height: 30px; }
        QScrollBar::handle:vertical:hover { background: #00e5ff; }
        QTableWidget { background-color: #111827; color: #e5e7eb; gridline-color: #1f2937; border: 1px solid #1a2436; border-radius: 6px; font-size: 12px; }
        QHeaderView::section { background-color: #1f2937; color: #00e5ff; padding: 6px; border: 1px solid #111827; font-weight: bold; }
        QMessageBox QLabel { color: #e5e7eb; }
        QComboBox { background-color: #1a2436; color: #ffffff; border: 1px solid #38bdf8; border-radius: 4px; padding: 8px; font-size: 13px; }
        QComboBox QAbstractItemView { background-color: #111827; color: #ffffff; selection-background-color: #00ff88; selection-color: #0b0f19; }
        QProgressBar { border: 1px solid #1a2436; border-radius: 4px; text-align: center; background-color: #111827; color: #ffffff; min-height: 20px; }
        QProgressBar::chunk { background-color: #00ff88; }
        QGroupBox { color: #00e5ff; font-size: 14px; font-weight: bold; border: 2px solid #1a2436; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
    """)
    game = GameApp()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
