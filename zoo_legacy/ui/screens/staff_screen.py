from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class StaffScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #F3F4F6; } QLabel { color: #1F2937; }")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Управление персоналом")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #059669;")
        layout.addWidget(title)
        
        staff_list = [
            ("Др. Смит", "Ветеринар", 87, "#10B981", "👨‍⚕️"),
            ("Иванов", "Смотритель", 92, "#3B82F6", "👨‍"),
            ("Петрова", "Смотритель", 78, "#3B82F6", "👩‍"),
            ("Сидоров", "Смотритель", 95, "#3B82F6", "👨‍🌾"),
        ]
        
        for name, position, skill, color, emoji in staff_list:
            layout.addWidget(self._create_staff_card(name, position, skill, color, emoji))
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_staff_card(self, name, position, skill, color, emoji):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; padding: 15px; }")
        layout = QHBoxLayout(frame)
        
        # Фото (эмодзи как заглушка)
        photo_label = QLabel(emoji)
        photo_label.setStyleSheet("font-size: 48px; min-width: 60px;")
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(photo_label)
        
        info_layout = QVBoxLayout()
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        position_label = QLabel(position)
        position_label.setStyleSheet("font-size: 12px; color: #6B7280;")
        info_layout.addWidget(position_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        skill_label = QLabel(f"Навык: {skill}%")
        skill_label.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: bold;")
        layout.addWidget(skill_label)
        
        return frame
