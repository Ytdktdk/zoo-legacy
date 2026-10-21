from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class StartScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Фон через QPixmap
        self.bg_label = QLabel(self)
        self.bg_pixmap = QPixmap("C:/Users/User.888888888788/Downloads/beautiful-mountain-forest-landscape.jpg")
        if not self.bg_pixmap.isNull():
            self.bg_pixmap = self.bg_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.bg_label.setPixmap(self.bg_pixmap)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.lower()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("ZOO LEGACY")
        title.setStyleSheet("font-size: 72px; font-weight: bold; color: #00ff88; letter-spacing: 5px; background-color: rgba(0, 0, 0, 0.7); padding: 20px 40px; border-radius: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Генетический симулятор зоопарка")
        subtitle.setStyleSheet("font-size: 20px; color: #ffffff; background-color: rgba(0, 0, 0, 0.7); padding: 10px 20px; border-radius: 10px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        btn_new = QPushButton("НОВАЯ ИГРА")
        btn_new.setStyleSheet("background-color: #00ff88; color: #0b0f19; border: none; border-radius: 15px; padding: 20px 60px; font-size: 22px; font-weight: bold; min-width: 300px;")
        btn_new.clicked.connect(self._start_new_game)
        layout.addWidget(btn_new, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_continue = QPushButton("ПРОДОЛЖИТЬ")
        btn_continue.setStyleSheet("background-color: #00e5ff; color: #0b0f19; border: none; border-radius: 15px; padding: 20px 60px; font-size: 22px; font-weight: bold; min-width: 300px;")
        btn_continue.clicked.connect(self._continue_game)
        layout.addWidget(btn_continue, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_settings = QPushButton("НАСТРОЙКИ")
        btn_settings.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); color: #8da2fb; border: 2px solid #1a2436; border-radius: 15px; padding: 20px 60px; font-size: 22px; font-weight: bold; min-width: 300px;")
        btn_settings.clicked.connect(self._show_settings)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        footer = QLabel("v2.0 | 2026")
        footer.setStyleSheet("font-size: 12px; color: #ffffff; background-color: rgba(0, 0, 0, 0.7); padding: 5px 15px; border-radius: 5px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.bg_pixmap.isNull():
            scaled = self.bg_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.bg_label.setPixmap(scaled)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())

    def _start_new_game(self):
        if self.parent:
            self.parent.start_new_game()

    def _continue_game(self):
        if self.parent:
            self.parent.continue_game()

    def _show_settings(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Настройки", "Настройки будут добавлены в следующей версии!")
