from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QProgressBar, QMessageBox, QGroupBox
from PyQt6.QtCore import Qt, QTimer
from models.animal import ZooAnimal
from models.genetics import Gene, GeneticCode
import random

class BreedingDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.setWindowTitle('Лаборатория скрещивания')
        self.resize(700, 600)
        self.setModal(True)
        self.setStyleSheet('background-color: #0b0f19;')
        layout = QVBoxLayout()
        layout.setSpacing(15)
        title = QLabel('ГЕНЕТИЧЕСКАЯ ЛАБОРАТОРИЯ')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #9C27B0;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        parents_layout = QHBoxLayout()
        self.father_combo = QComboBox()
        self.father_combo.setStyleSheet('background-color: #1a2436; color: #ffffff; border: 1px solid #38bdf8; border-radius: 4px; padding: 8px; font-size: 13px;')
        self.mother_combo = QComboBox()
        self.mother_combo.setStyleSheet('background-color: #1a2436; color: #ffffff; border: 1px solid #38bdf8; border-radius: 4px; padding: 8px; font-size: 13px;')
        self.load_animals_to_combos()
        father_group = QGroupBox('Родитель 1 (Отец)')
        father_group.setStyleSheet('color: #00e5ff; font-size: 14px; font-weight: bold; border: 2px solid #1a2436; border-radius: 8px; margin-top: 10px; padding-top: 10px;')
        father_layout = QVBoxLayout(father_group)
        father_layout.addWidget(self.father_combo)
        self.father_genes_label = QLabel('Гены: -')
        self.father_genes_label.setStyleSheet('font-size: 12px; color: #8da2fb; font-family: Consolas, monospace; padding: 5px;')
        father_layout.addWidget(self.father_genes_label)
        parents_layout.addWidget(father_group)
        mother_group = QGroupBox('Родитель 2 (Мать)')
        mother_group.setStyleSheet('color: #00e5ff; font-size: 14px; font-weight: bold; border: 2px solid #1a2436; border-radius: 8px; margin-top: 10px; padding-top: 10px;')
        mother_layout = QVBoxLayout(mother_group)
        mother_layout.addWidget(self.mother_combo)
        self.mother_genes_label = QLabel('Гены: -')
        self.mother_genes_label.setStyleSheet('font-size: 12px; color: #8da2fb; font-family: Consolas, monospace; padding: 5px;')
        mother_layout.addWidget(self.mother_genes_label)
        parents_layout.addWidget(mother_group)
        layout.addLayout(parents_layout)
        self.father_combo.currentIndexChanged.connect(self.update_genes_display)
        self.mother_combo.currentIndexChanged.connect(self.update_genes_display)
        match_group = QGroupBox('Совместимость')
        match_group.setStyleSheet('color: #00ff88; font-size: 14px; font-weight: bold; border: 2px solid #1a2436; border-radius: 8px; margin-top: 10px; padding-top: 10px;')
        match_layout = QVBoxLayout(match_group)
        self.match_bar = QProgressBar()
        self.match_bar.setStyleSheet('border: 1px solid #1a2436; border-radius: 4px; text-align: center; background-color: #111827; color: #ffffff; min-height: 20px;')
        self.match_bar.setValue(0)
        match_layout.addWidget(self.match_bar)
        self.match_label = QLabel('Выберите родителей')
        self.match_label.setStyleSheet('font-size: 13px; color: #00e5ff; padding: 5px;')
        match_layout.addWidget(self.match_label)
        layout.addWidget(match_group)
        reagents_group = QGroupBox('Химические реагенты')
        reagents_group.setStyleSheet('color: #FF9800; font-size: 14px; font-weight: bold; border: 2px solid #1a2436; border-radius: 8px; margin-top: 10px; padding-top: 10px;')
        reagents_layout = QVBoxLayout(reagents_group)
        self.reagent_combo = QComboBox()
        self.reagent_combo.addItem('Без реагента', None)
        self.reagent_combo.addItem('Радиационный мутаген (+40% мутаций, -30 HP)', 'mutagen')
        self.reagent_combo.addItem('Янтарный стабилизатор (0% мутаций, без дефектов)', 'stabilizer')
        self.reagent_combo.addItem('Питательный субстрат (+20 HP)', 'substrate')
        self.reagent_combo.setStyleSheet('background-color: #1a2436; color: #ffffff; border: 1px solid #FF9800; border-radius: 4px; padding: 8px; font-size: 13px;')
        reagents_layout.addWidget(self.reagent_combo)
        self.reagent_info = QLabel('Выберите реагент для изменения параметров скрещивания')
        self.reagent_info.setStyleSheet('font-size: 12px; color: #a0a0a0; padding: 5px;')
        reagents_layout.addWidget(self.reagent_info)
        layout.addWidget(reagents_group)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('border: 1px solid #1a2436; border-radius: 4px; text-align: center; background-color: #111827; color: #ffffff; min-height: 25px;')
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel('')
        self.status_label.setStyleSheet('font-size: 14px; color: #00e5ff; padding: 10px;')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        btn_layout = QHBoxLayout()
        self.btn_breed = QPushButton('ЗАПУСТИТЬ СКРЕЩИВАНИЕ')
        self.btn_breed.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9C27B0, stop:1 #BA68C8); color: white; padding: 15px 30px; font-size: 16px; font-weight: bold; border-radius: 10px; border: none;')
        self.btn_breed.clicked.connect(self.start_breeding)
        btn_layout.addWidget(self.btn_breed)
        btn_cancel = QPushButton('Отмена')
        btn_cancel.setStyleSheet('background-color: #1a2436; color: #ffffff; border: 1px solid #EF4444; border-radius: 10px; padding: 15px 30px; font-size: 16px; font-weight: bold;')
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def load_animals_to_combos(self):
        animals = self.db.get_all_animals()
        self.father_combo.clear()
        self.mother_combo.clear()
        self.father_combo.addItem('Выберите...', None)
        self.mother_combo.addItem('Выберите...', None)
        for animal in animals:
            display_name = f'#{animal[0]} {animal[1]} ({animal[2]}, {animal[3]} лет)'
            self.father_combo.addItem(display_name, animal[0])
            self.mother_combo.addItem(display_name, animal[0])

    def update_genes_display(self):
        father_id = self.father_combo.currentData()
        mother_id = self.mother_combo.currentData()
        if father_id:
            f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
            genes_str = ', '.join([f'{k}: {v}' for k, v in f_genetics.items()])
            self.father_genes_label.setText(f'Гены: {genes_str}')
        else:
            self.father_genes_label.setText('Гены: -')
        if mother_id:
            m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)
            genes_str = ', '.join([f'{k}: {v}' for k, v in m_genetics.items()])
            self.mother_genes_label.setText(f'Гены: {genes_str}')
        else:
            self.mother_genes_label.setText('Гены: -')
        if father_id and mother_id:
            if father_id == mother_id:
                self.match_bar.setValue(0)
                self.match_label.setText('Нельзя скрестить животное само с собой!')
            else:
                f_species, _, _, _ = self.db.get_animal_genetics(father_id)
                m_species, _, _, _ = self.db.get_animal_genetics(mother_id)
                if f_species == m_species:
                    self.match_bar.setValue(85)
                    self.match_label.setText('Высокая совместимость (один вид)')
                else:
                    self.match_bar.setValue(25)
                    self.match_label.setText('Низкая совместимость (разные виды)')
        else:
            self.match_bar.setValue(0)
            self.match_label.setText('Выберите родителей')

    def start_breeding(self):
        father_id = self.father_combo.currentData()
        mother_id = self.mother_combo.currentData()
        if not father_id or not mother_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите обоих родителей!')
            return
        if father_id == mother_id:
            QMessageBox.warning(self, 'Ошибка', 'Нельзя скрестить животное само с собой!')
            return
        f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
        m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)
        if f_species != m_species:
            QMessageBox.warning(self, 'Несовместимость', f'{f_species} и {m_species} не могут быть скрещены!')
            return
        energy = self.db.get_energy()
        if energy < 30:
            QMessageBox.warning(self, 'Недостаточно энергии', 'Нужно 30 энергии!')
            return
        self.btn_breed.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_value = 0
        self.progress_bar.setValue(0)
        self.status_label.setText('Анализ генетического материала...')
        self.timer.start(50)

    def update_progress(self):
        self.progress_value += 2
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value == 30:
            self.status_label.setText('Комбинирование генов...')
        elif self.progress_value == 60:
            self.status_label.setText('Применение реагентов...')
        elif self.progress_value == 90:
            self.status_label.setText('Инкубация эмбриона...')
        if self.progress_value >= 100:
            self.timer.stop()
            self.finish_breeding()

    def finish_breeding(self):
        father_id = self.father_combo.currentData()
        mother_id = self.mother_combo.currentData()
        f_species, f_genetics, f_gen, f_parent = self.db.get_animal_genetics(father_id)
        m_species, m_genetics, m_gen, m_parent = self.db.get_animal_genetics(mother_id)
        try:
            father_genes = GeneticCode()
            mother_genes = GeneticCode()
            for g_name, g_val in f_genetics.items():
                father_genes.add_gene(Gene(g_name, g_val[0].upper(), g_val[1].lower()))
            for g_name, g_val in m_genetics.items():
                mother_genes.add_gene(Gene(g_name, g_val[0].upper(), g_val[1].lower()))
            reagent = self.reagent_combo.currentData()
            mutation_chance = 0.05
            health_bonus = 0
            has_defect = False
            mutation_name = ''
            if reagent == 'mutagen':
                mutation_chance = 0.4
                health_bonus = -30
                self.db.log_event(self.db.get_day(), 'Мутаген', 'Использован радиационный мутаген', 0)
            elif reagent == 'stabilizer':
                mutation_chance = 0.0
                self.db.log_event(self.db.get_day(), 'Стабилизатор', 'Использован янтарный стабилизатор', 0)
            elif reagent == 'substrate':
                health_bonus = 20
                self.db.log_event(self.db.get_day(), 'Субстрат', 'Использован питательный субстрат', 0)
            offspring_genetics = father_genes.combine(mother_genes)
            offspring_genetics.mutate_all(mutation_chance)
            if f_parent == mother_id or m_parent == father_id:
                if random.random() < 0.3:
                    has_defect = True
                    mutation_name = 'Инбридинг-дефект'
                    self.db.log_event(self.db.get_day(), 'Инбридинг', 'Обнаружен генетический дефект!', 0)
            mutation_types = ['Альбинизм', 'Меланизм', 'Гигантизм', 'Карликовость', 'Полидактилия', 'Гетерохромия']
            if random.random() < mutation_chance and not mutation_name:
                mutation_name = random.choice(mutation_types)
                self.db.log_event(self.db.get_day(), 'Мутация', f'У потомства обнаружена мутация: {mutation_name}', 0)
            offspring = ZooAnimal(f_species, 0, offspring_genetics)
            offspring.feed(20)
            if has_defect:
                offspring._Animal__health = max(10, offspring.health - 30)
            if health_bonus != 0:
                offspring._Animal__health = min(100, max(0, offspring.health + health_bonus))
            self.db.add_animal(offspring, parent_id=father_id, mutation=mutation_name)
            self.db.use_energy(30)
            self.db.add_science_points(15)
            self.db.add_experience(25)
            msg = f'Родился {f_species}!\nРедкость: {offspring.rarity}'
            if mutation_name:
                msg += f'\n МУТАЦИЯ: {mutation_name}'
            self.db.log_event(self.db.get_day(), 'Скрещивание', f'Получен потомок {f_species}' + (f' с мутацией {mutation_name}' if mutation_name else ''), 0)
            self.status_label.setText('Успешно!')
            QMessageBox.information(self, 'Потомство получено!', msg)
            self.accept()
        except Exception as e:
            self.status_label.setText('Ошибка')
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать потомство: {e}')
            self.btn_breed.setEnabled(True)
            self.progress_bar.setVisible(False)