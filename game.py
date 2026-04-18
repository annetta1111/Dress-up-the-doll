from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class GameWindow(QWidget):
    def __init__(self, theme, back_func, complete_func):
        super().__init__()
        
        # Запоминаем параметры
        self.theme = theme
        self.back_func = back_func
        self.complete_func = complete_func
        
        # Настройки окна
        self.setWindowTitle("Одень куклу - Игра")
        self.setStyleSheet("background-color: rgb(255, 182, 193);")
        self.setMinimumSize(800, 600)
        
        # Надпись
        self.label = QLabel("ИГРА ОТКРЫЛАСЬ!")
        self.label.setStyleSheet("font-size: 50px; font-weight: bold; color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Показываем тему
        if theme:
            self.theme_label = QLabel(f"Тема: {theme}")
        else:
            self.theme_label = QLabel("Свободная игра")
        self.theme_label.setStyleSheet("font-size: 30px; color: white;")
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка назад
        self.btn_back = QPushButton("назад")
        self.btn_back.setFixedSize(120, 50) 
        self.btn_back.clicked.connect(back_func)
        self.btn_back.setStyleSheet("""
            QPushButton { background-color: white; color: rgb(255, 120, 150); font-size: 18px; font-weight: bold; border-radius: 15px; padding: 10px;}
            QPushButton:hover { background-color: rgb(240, 240, 240);}
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.theme_label)
        layout.addStretch()
        layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignCenter)  # ВАЖНО: self.btn_back
        layout.addStretch()
        
        self.setLayout(layout)