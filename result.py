import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QMessageBox,QApplication)
from PyQt6.QtCore import Qt
from datetime import datetime

class ResultScreen(QWidget):
    def __init__(self, restart_func, exit_func, back_to_menu_func, doll_area):
        super().__init__()

        self.doll_area = doll_area  

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
        QWidget{
            background-image: url('images/фон.jpg');
            background-repeat: no-repeat;
            background-position: center;
            background-color: rgb(255,200,210);
        }
        """)

        panel = QWidget()
        panel.setFixedSize(420, 350)
        panel.setStyleSheet("""
            QWidget{
                background:white;
                border-radius:25px;}
        """)

        title = QLabel("ОБРАЗ ГОТОВ 💗")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:38px;
            font-weight:bold;
            color:rgb(255,120,150);
        """)

        self.save_btn = QPushButton("СОХРАНИТЬ ОБРАЗ")
        self.restart_btn = QPushButton("НАЧАТЬ ЗАНОВО")
        self.exit_btn = QPushButton("ВЫХОД")

        for b in (self.save_btn, self.restart_btn, self.exit_btn):
            b.setFixedHeight(55)
            b.setStyleSheet("""
                QPushButton{
                    background:rgb(255,120,150);
                    color:white;
                    font-size:18px;
                    font-weight:bold;
                    border-radius:15px;}
                QPushButton:hover{
                    background:rgb(255,150,170);}
            """)

        self.restart_btn.clicked.connect(restart_func)
        self.exit_btn.clicked.connect(exit_func)
        self.save_btn.clicked.connect(self.save_image)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.save_btn)
        layout.addSpacing(10)
        layout.addWidget(self.restart_btn)
        layout.addSpacing(10)
        layout.addWidget(self.exit_btn)
        layout.addSpacing(10)

        panel.setLayout(layout)

        main = QVBoxLayout()
        main.addStretch()
        main.addWidget(panel, alignment=Qt.AlignmentFlag.AlignCenter)
        main.addStretch()

        self.setLayout(main)



    def save_image(self):
        desktop = r"C:\Users\osunc\OneDrive\Рабочий стол"
        folder = os.path.join(desktop, "Мои_образы")
        
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Создана папка: {folder}")
        
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"образ_{now}.png"
        filepath = os.path.join(folder, filename)
        
        pixmap = self.doll_area.grab()
        pixmap.save(filepath)
        
        if os.path.exists(filepath):
            QMessageBox.information(
                self, 
                "Сохранено! 💗", 
                f"Образ сохранён!\n\n📁 Папка: {folder}\n📄 Файл: {filename}")
        else:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Не удалось сохранить файл!")