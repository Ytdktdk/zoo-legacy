from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt

class AnimalCard(QWidget):
    def __init__(self, animal_data, db_manager, parent=None):
        super().__init__(parent)
        self.animal_id = animal_data[0]
        self.name = animal_data[1]
        self.species = animal_data[2]
        self.age = animal_data[3]
        self.health = animal_data[4]
        self.hunger = animal_data[5]
        self.db = db_manager
        
        self.setStyleSheet("QWidget { background-color: #1E293B; border-radius: 12px; padding: 20px; } QLabel { color: white; } QPushButton { border-radius: 8px; padding: 12px; font-weight: bold; color: white; }")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        header = QHBoxLayout()
        title = QLabel(f"{self.name} ({self.species})")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        age_label = QLabel(f"Возраст: {self.age} лет")
        age_label.setStyleSheet("font-size: 16px; color: #94A3B8;")
        header.addWidget(age_label)
        layout.addLayout(header)
        
        self.health_bar = self._create_progress_bar("Здоровье", self.health, "#10B981")
        self.hunger_bar = self._create_progress_bar("Голод", self.hunger, "#F59E0B")
        self.happiness_bar = self._create_progress_bar("Счастье", 85, "#3B82F6")
        self.stress_bar = self._create_progress_bar("Стресс", 15, "#EF4444")
        
        layout.addWidget(self.health_bar)
        layout.addWidget(self.hunger_bar)
        layout.addWidget(self.happiness_bar)
        layout.addWidget(self.stress_bar)
        
        genetics_label = QLabel("Генетический код:")
        genetics_label.setStyleSheet("font-size: 14px; color: #94A3B8; margin-top: 10px;")
        layout.addWidget(genetics_label)
        
        genetics_layout = QHBoxLayout()
        species, genetics = self.db.get_animal_genetics(self.animal_id)
        if genetics:
            for gene_name, gene_value in genetics.items():
                gene_btn = QPushButton(f"[{gene_value}]")
                if gene_value[0].isupper():
                    gene_btn.setStyleSheet("QPushButton { background-color: #10B981; border: 2px solid #059669; padding: 8px; font-size: 14px; font-weight: bold; color: white; }")
                else:
                    gene_btn.setStyleSheet("QPushButton { background-color: #334155; border: 2px solid #475569; padding: 8px; font-size: 14px; font-weight: bold; color: white; }")
                genetics_layout.addWidget(gene_btn)
        layout.addLayout(genetics_layout)
        
        btn_layout = QHBoxLayout()
        btn_feed = QPushButton("Покормить")
        btn_feed.setStyleSheet("background-color: #10B981;")
        btn_feed.clicked.connect(self._feed_animal)
        
        btn_treat = QPushButton("Вылечить")
        btn_treat.setStyleSheet("background-color: #3B82F6;")
        btn_treat.clicked.connect(self._treat_animal)
        
        btn_breed = QPushButton("На скрещивание")
        btn_breed.setStyleSheet("background-color: #8B5CF6;")
        btn_breed.clicked.connect(self._send_to_breeding)
        
        btn_layout.addWidget(btn_feed)
        btn_layout.addWidget(btn_treat)
        btn_layout.addWidget(btn_breed)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _create_progress_bar(self, label, value, color):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 14px; min-width: 80px; color: white;")
        layout.addWidget(label_widget)
        
        bar = QProgressBar()
        bar.setValue(value)
        bar.setStyleSheet(f"QProgressBar {{ border: 2px solid #475569; border-radius: 5px; text-align: center; background-color: #334155; }} QProgressBar::chunk {{ background-color: {color}; }}")
        layout.addWidget(bar)
        
        value_label = QLabel(f"{value}%")
        value_label.setStyleSheet("font-size: 14px; min-width: 50px; color: white;")
        layout.addWidget(value_label)
        
        return widget
    
    def _feed_animal(self):
        QMessageBox.information(self, "Успех", f"{self.name} покормлен!")
    
    def _treat_animal(self):
        QMessageBox.information(self, "Успех", f"{self.name} вылечен!")
    
    def _send_to_breeding(self):
        QMessageBox.information(self, "Информация", f"{self.name} отправлен в лабораторию скрещивания")
