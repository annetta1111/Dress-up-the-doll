import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt

#первый экран
class MainWindow(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.initUI(switch_func)

    def initUI(self,switch_func):
        self.setWindowTitle('одень куклу')
        self.setGeometry(300, 300, 150, 150)


        self.label_title = QLabel('ОДЕНЬ КУКЛУ')
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_start = QPushButton('СТАРТ')
        self.btn_start.clicked.connect(switch_func) #Когда кнопка нажата, вызывается функция переключения экрана

        layout = QVBoxLayout()  #размещаем элементы по вертикали 
        layout.addStretch(1) #отступ сверху
        layout.addWidget(self.label_title)
        layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        self.setLayout(layout)

    def resizeEvent(self, event): #изменение кнопки и текста под окно
        new_font_size = max(14, self.width() // 10) 
        self.label_title.setStyleSheet(f"font-size: {new_font_size}px;font-weight: bold;color: white;")

        btn_size = max(60, self.width() // 4) #кнопка-четверть ширины окна
        self.btn_start.setFixedSize(btn_size, btn_size)
        self.btn_start.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: rgb(255, 120, 150);
                font-size: {btn_size // 5}px;
                font-weight: bold;
                border-radius: {btn_size // 2}px;
            }}
            QPushButton:hover {{
                background-color: rgb(240, 240, 240);
            }}
        """)
        super().resizeEvent(event)

class ModeSelectionScreen (QWidget): #второе окно
    def __init__(self,back_func):
        super().__init__()
        self.initUI(back_func)

    def initUI(self,back_func):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(255, 182, 193);")
        main_layout = QVBoxLayout() # Основной вертикальный контейнер

        self.btn_back = QPushButton("назад")
        self.btn_back.setFixedSize(80, 50)
        self.btn_back.clicked.connect(back_func) #функция возврата назад
        main_layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addStretch(2)

        self.label_mode = QLabel("РЕЖИМ ИГРЫ")
        self.label_mode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_mode)
        main_layout.addStretch(1) #промежуток между текстом и кнопками

        buttons_layout = QHBoxLayout() # горизонтальный контейнер для кнопок 
        self.btn_task = QPushButton("ЗАДАНИЕ")
        self.btn_free = QPushButton("СВОБОДНАЯ ИГРА")

        buttons_layout.addStretch(1) #отстут слева 
        buttons_layout.addWidget(self.btn_task)
        buttons_layout.addSpacing(50) # Промежуток между кнопками
        buttons_layout.addWidget(self.btn_free)
        buttons_layout.addStretch(1) #отстут справа

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(2) #отстут снизу
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        title_size = self.width() // 15 #текст заголовка
        self.label_mode.setStyleSheet(f"font-size: {title_size}px; font-weight: bold; color: white; background: transparent;")

        btn_width = self.width() // 3 #ширина каждой кнопки-треть экрана
        btn_font_size = max(12, self.width() // 40)

        btn_style = f"""
            QPushButton {{
                background-color: white;
                color: rgb(255, 120, 150);
                font-size: {btn_font_size}px;
                font-weight: bold;
                border-radius: 10px;
                min-height: 60px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """
        for btn in [self.btn_task, self.btn_free]: #применяем один стиль к обеим кнопкам
            btn.setStyleSheet(btn_style)
            btn.setFixedWidth(btn_width)

        self.btn_back.setStyleSheet("background-color: white; color:rgb(255, 120, 150) ; font-size: 20px;")
        super().resizeEvent(event) #стиль кнопки назад

class GameController(QStackedWidget): #управление переключением экранов
    def __init__(self):
        super().__init__()
        self.screen1 = MainWindow(self.go_to_modes)
        self.screen2 = ModeSelectionScreen(self.go_to_main)
        
        self.addWidget(self.screen1) #добавить их в список
        self.addWidget(self.screen2)
        
        self.setWindowTitle('Одень куклу') 
        self.setStyleSheet("background-color: rgb(255, 182, 193);")
    def go_to_modes(self): #переход на экран выбора режима
        self.setCurrentIndex(1)
    
    def go_to_main(self):
        self.setCurrentIndex(0) # Переход обратно на старт

def main():
    app = QApplication(sys.argv)

    controller = GameController() #запуск контролера для управления всего приложения
    controller.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
