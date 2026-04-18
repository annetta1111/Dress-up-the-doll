import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout

# ========== ПЕРВЫЙ ЭКРАН (СТАРТОВЫЙ) ==========
class MainWindow(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        
        # Делаем фон розовым
        self.setStyleSheet("background-color: pink;")
        
        # Заголовок
        label = QLabel("ОДЕНЬ КУКЛУ")
        label.setStyleSheet("font-size: 80px; font-weight: bold; color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка старт
        btn = QPushButton("СТАРТ")
        btn.setStyleSheet("font-size: 40px; background-color: white; color: pink; padding: 30px;")
        btn.clicked.connect(switch_func)
        
        # Располагаем всё вертикально
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

# ========== ВТОРОЙ ЭКРАН (ВЫБОР РЕЖИМА) ==========
class ModeSelectionScreen(QWidget):
    def __init__(self, back_func, task_func):
        super().__init__()
        
        # Делаем фон розовым
        self.setStyleSheet("background-color: pink;")
        
        # Кнопка назад
        btn_back = QPushButton("Назад")
        btn_back.setStyleSheet("font-size: 20px; background-color: white; color: pink; padding: 10px;")
        btn_back.clicked.connect(back_func)
        
        # Заголовок
        label = QLabel("РЕЖИМ ИГРЫ")
        label.setStyleSheet("font-size: 70px; font-weight: bold; color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка ЗАДАНИЕ (открывает третий экран)
        btn_task = QPushButton("ЗАДАНИЕ")
        btn_task.setStyleSheet("font-size: 30px; background-color: white; color: pink; padding: 30px;")
        btn_task.clicked.connect(task_func)
        
        # Кнопка СВОБОДНАЯ ИГРА (пока не работает)
        btn_free = QPushButton("СВОБОДНАЯ ИГРА")
        btn_free.setStyleSheet("font-size: 30px; background-color: white; color: pink; padding: 30px;")
        
        # Располагаем кнопки в ряд
        buttons_row = QHBoxLayout()
        buttons_row.addStretch()
        buttons_row.addWidget(btn_task)
        buttons_row.addSpacing(30)
        buttons_row.addWidget(btn_free)
        buttons_row.addStretch()
        
        # Основной вертикальный layout
        layout = QVBoxLayout()
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()
        layout.addWidget(label)
        layout.addSpacing(50)
        layout.addLayout(buttons_row)
        layout.addStretch()
        
        self.setLayout(layout)

# ========== ТРЕТИЙ ЭКРАН (ЗАДАНИЕ - ТЕМА) ==========
class ThemeScreen(QWidget):
    def __init__(self, back_func, start_game_func):
        super().__init__()
        
        # Сохраняем функцию для начала игры
        self.start_game_func = start_game_func
        
        # Список тем
        self.themes = ["Пляжный", "Деловой", "Спортивный", "Вечерний", "Повседневный"]
        
        # Выбранная тема (пока пустая)
        self.selected_theme = ""
        
        # Фон розовый
        self.setStyleSheet("background-color: pink;")
        
        # Кнопка назад
        self.btn_back = QPushButton("Назад")
        self.btn_back.setStyleSheet("font-size: 20px; background-color: white; color: pink; padding: 10px;")
        self.btn_back.clicked.connect(back_func)
        
        # Заголовок
        self.title = QLabel("Твоё задание")
        self.title.setStyleSheet("font-size: 60px; font-weight: bold; color: white;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Окошко для темы
        self.theme_box = QLabel("Нажми кнопку ниже")
        self.theme_box.setStyleSheet("font-size: 40px; background-color: white; color: pink; padding: 40px;")
        self.theme_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка "Получить тему"
        self.btn_get = QPushButton("Получить тему")
        self.btn_get.setStyleSheet("font-size: 25px; background-color: white; color: pink; padding: 20px;")
        self.btn_get.clicked.connect(self.get_random_theme)
        
        # Кнопка "Начать игру" (сначала неактивна)
        self.btn_start = QPushButton("Начать игру")
        self.btn_start.setStyleSheet("font-size: 25px; background-color: white; color: pink; padding: 20px;")
        self.btn_start.clicked.connect(self.start_game)
        self.btn_start.setEnabled(False)  # Пока неактивна
        
        # Ряд с кнопками
        buttons_row = QHBoxLayout()
        buttons_row.addStretch()
        buttons_row.addWidget(self.btn_get)
        buttons_row.addSpacing(30)
        buttons_row.addWidget(self.btn_start)
        buttons_row.addStretch()
        
        # Основной layout
        layout = QVBoxLayout()
        layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addSpacing(30)
        layout.addWidget(self.theme_box)
        layout.addSpacing(40)
        layout.addLayout(buttons_row)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def get_random_theme(self):
        """Выбирает случайную тему"""
        self.selected_theme = random.choice(self.themes)
        self.theme_box.setText(self.selected_theme)
        self.btn_start.setEnabled(True)  # Делаем кнопку активной
    
    def start_game(self):
        """Начинает игру с выбранной темой"""
        self.start_game_func()

# ========== ГЛАВНЫЙ КОНТРОЛЛЕР (ПЕРЕКЛЮЧАЕТ ЭКРАНЫ) ==========
class GameController(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        # Создаём три экрана
        self.screen1 = MainWindow(self.go_to_screen2)
        self.screen2 = ModeSelectionScreen(self.go_to_screen1, self.go_to_screen3)
        self.screen3 = ThemeScreen(self.go_to_screen2, self.start_game_mode)
        
        # Добавляем экраны (индексы: 0, 1, 2)
        self.addWidget(self.screen1)
        self.addWidget(self.screen2)
        self.addWidget(self.screen3)
    
    def go_to_screen1(self):
        """Показывает первый экран"""
        self.setCurrentIndex(0)
    
    def go_to_screen2(self):
        """Показывает второй экран"""
        self.setCurrentIndex(1)
    
    def go_to_screen3(self):
        """Показывает третий экран"""
        self.setCurrentIndex(2)
    
    def start_game_mode(self):
        """Начинает игру (пока просто выводим тему в консоль)"""
        theme = self.screen3.selected_theme
        print(f"Начинаем игру! Тема задания: {theme}")
        # TODO: здесь будет экран с одеванием куклы

# ========== ЗАПУСК ==========
def main():
    app = QApplication(sys.argv)
    window = GameController()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()