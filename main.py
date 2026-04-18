import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from game import GameWindow

# первый экран
class MainWindow(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.initUI(switch_func)


        self.create_sparkles()  # создаём блёстки
        self.start_sparkle_animation()  # запускаем мерцание

    def initUI(self,switch_func):
        self.setWindowTitle('одень куклу')
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(""" background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 rgb(255, 200, 210),
                                        stop:0.5 rgb(255, 170, 190),
                                        stop:1 rgb(255, 140, 170));
        """)

        self.label = QLabel("ОДЕНЬ КУКЛУ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
    font-size: 120px;
    font-weight: bold;
    letter-spacing: 12px;
    color: #ffffff;
    background: linear-gradient(145deg, #ffffff, #ffe4e9);
   
""")

        self.btn_start = QPushButton("СТАРТ")
        self.btn_start.setFixedSize(300, 300)
        self.btn_start.clicked.connect(switch_func)

        self.btn_start.setStyleSheet("""
            QPushButton { background-color: white; color: rgb(255, 120, 150); font-size: 50px; font-weight: bold; border-radius: 150px;}
            QPushButton:hover { background-color: rgb(240, 240, 240);}""")
        
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)


    def create_sparkles(self): #мерцающие блестки на фоне
        self.sparkles = []
        sparkle_symbols = ["✦", "✧", "✩", "✪", "★", "☆", "*"]
        
        for i in range(60):  # 50 блёсток
            sparkle = QLabel(self)  # Звёздочка
            sparkle.setText(random.choice(sparkle_symbols))
            
            #фон прозрачным
            sparkle.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            
            # Случайный цвет и размер
            r = random.randint(200, 255)
            g = random.randint(200, 255)
            b = random.randint(150, 255)
            size = random.randint(15, 35)
            
            sparkle.setStyleSheet(f"""
                background-color: transparent;
                color: rgb({r}, {g}, {b});
                font-size: {size}px;
            """)
            # Случайное место на экране
            x = random.randint(0, 1900)
            y = random.randint(0, 1000)
            sparkle.move(x, y)
            sparkle.resize(40, 40)
            sparkle.show()
            
            self.sparkles.append(sparkle)
    
    def start_sparkle_animation(self): #мерцание звезд
        self.timer = QTimer()
        self.timer.timeout.connect(self.blink_sparkles)
        self.timer.start(300)  # каждые 0.3 секунды
    
    def blink_sparkles(self):
        symbols = ["✦", "✧", "✩", "✪", "★", "☆"]
        
        for sparkle in self.sparkles:
            if random.randint(1, 3) == 1:  # 33% звёзд меняются
                new_symbol = random.choice(symbols)
                new_r = random.randint(200, 255)
                new_g = random.randint(200, 255)
                new_b = random.randint(150, 255)
                new_size = random.randint(15, 35)
                
                sparkle.setText(new_symbol)
                sparkle.setStyleSheet(f"""
                    background-color: transparent;
                    color: rgb({new_r}, {new_g}, {new_b});
                    font-size: {new_size}px;
                """)


# второй экран
class ModeSelectionScreen(QWidget):
    def __init__(self, back_func,task_func,free_func):
        super().__init__()
        self.initUI(back_func,task_func,free_func)

    def initUI(self,back_func,task_func,free_func):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(255, 182, 193);")

        self.btn_back = QPushButton("назад")
        self.btn_back.setFixedSize(120, 50) 
        self.btn_back.clicked.connect(back_func)
        self.btn_back.setStyleSheet("""
            QPushButton { background-color: white; color: rgb(255, 120, 150); font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;}
            QPushButton:hover { background-color: rgb(240, 240, 240);}""")

        self.label = QLabel("РЕЖИМ ИГРЫ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(""" font-size: 110px; font-weight: bold; color: white; """)

        self.btn_task = QPushButton("ЗАДАНИЕ")
        self.btn_free = QPushButton("СВОБОДНАЯ ИГРА")
        self.btn_task.setFixedSize(300, 120)
        self.btn_free.setFixedSize(300, 120)

        self.btn_task.clicked.connect(task_func) #кнопка задание октрывает 3 окно
        self.btn_free.clicked.connect(free_func)

        btn_style = """
            QPushButton {background-color: white; color: rgb(255, 120, 150); font-size: 20px; font-weight: bold; border-radius: 20px;}
            QPushButton:hover {background-color: rgb(240, 240, 240);}
        """

        self.btn_task.setStyleSheet(btn_style)
        self.btn_free.setStyleSheet(btn_style)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.btn_task)
        h_layout.addSpacing(30)
        h_layout.addWidget(self.btn_free)
        h_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addStretch()
        main_layout.addWidget(self.label)
        main_layout.addSpacing(40)
        main_layout.addLayout(h_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)



#третий экран
class ThemeScrenn (QWidget):
        def __init__(self, back_func, next_func):
            super().__init__()
            self.themes = [
                "Пляжный стиль 🏖️",
                "Деловой образ 💼",
                "Спортивный образ 🏃",
                "Вечерний наряд 🌙",
                "Повседневный стиль 👕",
                "Романтический образ 💕",
                "Рок-стиль 🎸",
        ]
            self.current_theme = ""
            self.initUI(back_func, next_func)

        def initUI(self, back_func, next_func):
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
            self.setStyleSheet("background-color: rgb(255, 182, 193);")


            #кнопка назад
            self.btn_back = QPushButton("назад")
            self.btn_back.setFixedSize(120, 50)
            self.btn_back.clicked.connect(back_func)
            self.btn_back.setStyleSheet( """
            QPushButton {background-color: white; color: rgb(255, 120, 150); font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;}
            QPushButton:hover {background-color: rgb(240, 240, 240);}""")


            self.label = QLabel("RANDOM THEME")
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setStyleSheet ("""font-size:90px; font-weight: bold; color: white;""")
            self.theme_display = QLabel("Нажмите 'Генерировать'")
            self.theme_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.theme_display.setStyleSheet("""background-color: white; color: rgb(255, 120, 150); font-size: 35px; font-weight: bold; border-radius: 20px; padding: 40px; min-width: 500px; min-height: 150px;""")

            self.btn_generate = QPushButton("ГЕНЕРИРОВАТЬ")
            self.btn_generate.setFixedSize(250,80)
            self.btn_generate.clicked.connect(self.generate_theme)
            self.btn_generate.setStyleSheet ("""
                                             QPushButton { background-color: white; color: rgb(255, 120, 150); font-size: 22px; font-weight: bold; border-radius: 15px;}
                                             QPushButton:hover { background-color: rgb(240, 240, 240);}
                                             """)        
            # Кнопка "Дальше"
            self.btn_next = QPushButton("ДАЛЬШЕ")
            self.btn_next.setFixedSize(250, 80)
            self.btn_next.clicked.connect(next_func)
            self.btn_next.setEnabled(False)
            self.btn_next.setStyleSheet("""
                                        QPushButton {background-color: white; color: rgb(255, 120, 150); font-size: 22px; font-weight: bold; border-radius: 15px;}
                                        QPushButton:hover { background-color: rgb(240, 240, 240); }
                                        QPushButton:disabled { background-color: rgb(200, 200, 200); color: rgb(150, 150, 150);}
                                         """)
            # Layout для кнопок
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()
            btn_layout.addWidget(self.btn_generate)
            btn_layout.addSpacing(30)
            btn_layout.addWidget(self.btn_next)
            btn_layout.addStretch()  

            # Основной layout
            main_layout = QVBoxLayout()
            main_layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
            main_layout.addStretch()
            main_layout.addWidget(self.label)
            main_layout.addSpacing(30)
            main_layout.addWidget(self.theme_display, alignment=Qt.AlignmentFlag.AlignCenter)
            main_layout.addSpacing(40)
            main_layout.addLayout(btn_layout)
            main_layout.addStretch()

            self.setLayout(main_layout)
        def generate_theme(self):
            self.current_theme = random.choice(self.themes)
            self.theme_display.setText(self.current_theme)
            self.btn_next.setEnabled(True)

        def get_current_theme(self):
            return self.current_theme


# управление
class GameController(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.screen1 = MainWindow(self.open_modes)
        self.screen2 = ModeSelectionScreen(self.go_back,self.open_theme_screen,self.open_free_game)
        self.screen3 = ThemeScrenn(self.go_back_to_modes, self.start_game_with_theme)
        self.screen4 = None

        self.addWidget(self.screen1)
        self.addWidget(self.screen2)
        self.addWidget(self.screen3)

    def open_modes(self):
        self.setCurrentIndex(1)

    def go_back(self):
        self.setCurrentIndex(0)

    def open_theme_screen(self):
        print("Открываем третий экран")  # Проверка
        self.setCurrentIndex(2)
    
    def go_back_to_modes(self):
        print("Возврат на второй экран")  # Проверка
        self.setCurrentIndex(1)

    def open_free_game(self):
        print("открываем свободную игру")
        self.screen4 = GameWindow (None, self.go_back_to_modes,self.game_complete) 
        self.addWidget(self.screen4)
        self.setCurrentIndex(3)

    def start_game_with_theme(self):
        theme = self.screen3.get_current_theme()
        if theme:
            print(f"ИГРА НАЧАЛАСЬ! Тема задания: {theme}")
            self.screen4 = GameWindow(theme, self.go_back_to_modes, self.game_complete)
            self.addWidget(self.screen4)
            self.setCurrentIndex(3)
        else:
            print("Сначала сгенерируйте тему!")
    
    def game_complete(self):
        print('игра завершена')
        self.go_back_to_modes()
# запуск
def main():
    app = QApplication(sys.argv)
    window = GameController()
    window.showMaximized()  # ОТКРЫВАЕТ НА ВЕСЬ ЭКРАН
    sys.exit(app.exec())

if __name__ == "__main__":
    main()