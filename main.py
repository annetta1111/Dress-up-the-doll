
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from game import GameWindow
from result import ResultScreen

import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def button_style(size=20):
    return f"""
        QPushButton {{
            background:white;
            color:rgb(255,120,150);
            font-size:{size}px;
            font-weight:bold;
            border-radius:15px;
            padding:10px;}}
        QPushButton:hover {{
            background:rgb(240,240,240);}}"""



class MainWindow(QWidget):

    def __init__(self, open_modes):
        super().__init__()
        self.setWindowTitle("Одень куклу")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
    QWidget{
        background:qlineargradient(
            x1:0, y1:0, x2:1, y2:1,
            stop:0 rgb(255,200,210),
            stop:0.5 rgb(255,170,190),
            stop:1 rgb(255,140,170));}
    QLabel{
        background:transparent;}""")

        self.label = QLabel("ОДЕНЬ КУКЛУ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size:100px;
            font-weight:bold;
            color:white;
            letter-spacing:8px;""")

        self.btn = QPushButton("СТАРТ")
        self.btn.setFixedSize(300,300)
        self.btn.setStyleSheet("""
    QPushButton{
        background:white;
        color:rgb(255,120,150);
        font-size:40px;
        font-weight:bold;
        border-radius:150px;}
                               
    QPushButton:hover{
        background:rgb(240,240,240);}""")
        self.btn.clicked.connect(open_modes)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(
            self.btn,
            alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
        self.create_sparkles()



    def create_sparkles(self):
        self.sparkles = []
        symbols = ["✦", "✧", "✩", "✪", "★", "☆"]

        for i in range(60):
            star = QLabel(random.choice(symbols), self)
            size = random.randint(15,35)
            r = random.randint(200,255)
            g = random.randint(200,255)
            b = random.randint(150,255)

            star.setStyleSheet(f"""
                color:rgb({r},{g},{b});
                font-size:{size}px;
                background:transparent; """)

            x = random.randint(0,1900)
            y = random.randint(0,1000)

            star.move(x,y) 
            self.sparkles.append(star)

        self.timer = QTimer() #анимация
        self.timer.timeout.connect(self.blink)
        self.timer.start(300)

    def blink(self): 
        symbols = ["✦", "✧", "✩", "✪", "★", "☆"]
        for star in self.sparkles:
            if random.randint(1,3) == 1:
                star.setText(random.choice(symbols))


class ModeScreen(QWidget):
    def __init__(self, back, task, free):
        super().__init__()
        self.setWindowTitle("Одень куклу")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color:rgb(255,182,193);")
        self.back_btn = QPushButton("НАЗАД")
        self.back_btn.setFixedSize(120,50)
        self.back_btn.setStyleSheet(button_style())
        self.back_btn.clicked.connect(back)
        self.label = QLabel("РЕЖИМ ИГРЫ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet("""
            font-size:90px;
            font-weight:bold;
            color:white;""")

        self.task_btn = QPushButton("ЗАДАНИЕ")
        self.free_btn = QPushButton("СВОБОДНАЯ ИГРА")

        self.task_btn.setFixedSize(300,120)
        self.free_btn.setFixedSize(300,120)

        self.task_btn.setStyleSheet(button_style())
        self.free_btn.setStyleSheet(button_style())

        self.task_btn.clicked.connect(task)
        self.free_btn.clicked.connect(free)

        h = QHBoxLayout()

        h.addStretch()
        h.addWidget(self.task_btn)
        h.addSpacing(30)
        h.addWidget(self.free_btn)
        h.addStretch()

        layout = QVBoxLayout()

        layout.addWidget(
            self.back_btn,
            alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(40)
        layout.addLayout(h)
        layout.addStretch()
        self.setLayout(layout)



class ThemeScreen(QWidget):

    def __init__(self, back, start_game):
        super().__init__()
        self.setWindowTitle("Одень куклу")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.themes = [
            "Пляжный стиль 🏖️",
            "Деловой образ 💼",
            "Спортивный образ 🏃",
            "Вечерний наряд 🌙",
            "Повседневный стиль 👕",
            "Романтический образ 💕",
            "Рок стиль 🎸"]

        self.current_theme = ""

        self.setStyleSheet("background-color:rgb(255,182,193);")
        
        self.back_btn = QPushButton("НАЗАД")
        self.back_btn.setFixedSize(120,50)
        self.back_btn.setStyleSheet(button_style())
        self.back_btn.clicked.connect(back)

        self.label = QLabel("RANDOM THEME")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            font-size:80px;
            font-weight:bold;
            color:white;""")

        self.theme_label = QLabel('Нажмите кнопку "генерировать"')
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.theme_label.setStyleSheet("""
            background:white;
            color:rgb(255,120,150);
            font-size:35px;
            font-weight:bold;
            border-radius:20px;
            padding:40px;""")

        self.gen_btn = QPushButton("ГЕНЕРИРОВАТЬ")
        self.gen_btn.setFixedSize(250,80)
        self.gen_btn.setStyleSheet(button_style())
        self.gen_btn.clicked.connect(self.generate_theme)

        self.next_btn = QPushButton("ДАЛЬШЕ")
        self.next_btn.setFixedSize(250,80)
        self.next_btn.setStyleSheet(button_style())

       
        self.next_btn.setEnabled(False)

       
        self.next_btn.clicked.connect(start_game)

        h = QHBoxLayout()

        h.addStretch()
        h.addWidget(self.gen_btn)
        h.addSpacing(30)
        h.addWidget(self.next_btn)
        h.addStretch()

        layout = QVBoxLayout()

        layout.addWidget(
            self.back_btn,
            alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(30)
        layout.addWidget(self.theme_label)
        layout.addSpacing(40)
        layout.addLayout(h)
        layout.addStretch()
        self.setLayout(layout)

    def generate_theme(self):
        self.current_theme = random.choice(self.themes)
        self.theme_label.setText(self.current_theme)
        self.next_btn.setEnabled(True)

    def reset_theme(self):

        self.current_theme = ""
        self.theme_label.setText('Нажмите кнопку "генерировать"')
        self.next_btn.setEnabled(False)
    def get_theme(self):
        return self.current_theme



class Controller(QStackedWidget):

    def __init__(self):
        super().__init__()
        self.current_theme = None  
        self.game = None

        self.main = MainWindow(self.open_modes)

        self.modes = ModeScreen(
            self.back_main,
            self.open_theme,
            self.open_free_game)

        self.theme = ThemeScreen(
            self.back_modes,
            self.start_game)

        self.addWidget(self.main)
        self.addWidget(self.modes)
        self.addWidget(self.theme)

        self.setCurrentWidget(self.main)

    def reset_theme(self):
    
        self.theme.reset_theme()
        self.current_theme = None 

    def back_to_theme(self):
        self.setCurrentWidget(self.theme)

    def open_modes(self):
        self.setCurrentWidget(self.modes)

    def back_main(self):
        self.reset_theme()  
        self.setCurrentWidget(self.main)

    def open_theme(self):
        self.setCurrentWidget(self.theme)

    def back_modes(self):
        self.reset_theme()  
        self.setCurrentWidget(self.modes)

    def open_free_game(self):
        self.game = GameWindow(
            None,
            self.back_modes,
            self.open_result)

        self.addWidget(self.game)
        self.setCurrentWidget(self.game)

    def start_game(self):
        self.current_theme = self.theme.get_theme()

        if not self.current_theme:
            return  

        self.game = GameWindow(
            self.current_theme,
            self.back_to_theme,  
            self.open_result)
        
        self.addWidget(self.game)
        self.setCurrentWidget(self.game)

    def open_result(self):
        self.result = ResultScreen(
            self.restart_game,
            self.exit_app,
            self.game.doll_area)
        self.addWidget(self.result)
        self.setCurrentWidget(self.result)

    def restart_game(self):
        self.reset_theme()
        self.setCurrentWidget(self.main)

    def exit_app(self):
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = Controller()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()