from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
import sys
import os
from wardrobe import Wardrobe


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def button_style(color="rgb(255,120,150)", size=20):
    return f"""
    QPushButton{{
        background: white;
        color: {color};
        font-size: {size}px;
        font-weight: bold;
        border-radius: 15px;
        padding: 10px;
    }}
    QPushButton:hover{{
        background: rgb(240,240,240);
    }}
    """


class WornCloth(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.deleteLater()


class DollArea(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.doll = None
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-clothing"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if not self.doll:
            event.ignore()
            return
        
        pos = event.position().toPoint()

        if not self.doll.geometry().contains(pos):
            event.ignore()
            return

        data = event.mimeData().data("application/x-clothing").data()
        item = json.loads(data.decode())

        self.game.try_wear(item) 
        event.acceptProposedAction()


class GameWindow(QWidget):
    def __init__(self, theme, back_func, complete_func):
        super().__init__()
        self.complete_func = complete_func
        self.worn = {}  
        self.setAcceptDrops(True)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(255,200,210),
                    stop:1 rgb(255,140,170));}
        """)
        
        self.back_btn = QPushButton("НАЗАД")
        self.back_btn.setFixedSize(120, 50)
        self.back_btn.setStyleSheet(button_style())
        self.back_btn.clicked.connect(back_func)
        
        self.wardrobe = Wardrobe(self)
        
        self.doll_area = DollArea(self)
        self.doll_area.setFixedSize(700, 800)
        self.doll_area.setAcceptDrops(True)
        self.doll_area.setStyleSheet("background: white; border-radius: 30px;")
        
        # Загрузка куклы с resource_path
        doll_path = resource_path("images/clothes/doll11.png")
        self.doll = QLabel(self.doll_area)
        pix = QPixmap(doll_path)
        if not pix.isNull():
            pix = pix.scaled(200, 700, Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
            self.doll.setPixmap(pix)
        else:
            self.doll.setText("🪆")
            self.doll.setStyleSheet("font-size: 40px;")
            print(f"[ОШИБКА] Не найдена кукла: {doll_path}")
        
        self.doll.move(250, 50)
        self.doll.setFixedSize(200, 700)
        self.doll_area.doll = self.doll
    
        self.reset_btn = QPushButton("СБРОСИТЬ")
        self.done_btn = QPushButton("ГОТОВО")
        self.reset_btn.setFixedSize(180, 60)
        self.done_btn.setFixedSize(180, 60)
        self.reset_btn.setStyleSheet(button_style("rgb(255,160,170)"))
        self.done_btn.setStyleSheet(button_style("rgb(255,120,140)"))
        self.reset_btn.clicked.connect(self.reset_all)
        self.done_btn.clicked.connect(complete_func)
        
      
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.reset_btn)
        btn_row.addSpacing(20)
        btn_row.addWidget(self.done_btn)
        
        left_col = QVBoxLayout()
        left_col.addWidget(self.back_btn)
        left_col.addWidget(self.wardrobe)
        left_col.addLayout(btn_row)
        
        main_row = QHBoxLayout()
        main_row.addLayout(left_col)
        main_row.addSpacing(50)
        main_row.addWidget(self.doll_area)
        
        self.setLayout(main_row)
    
    def try_wear(self, item):
        cat = item["cat"]
        
        if cat in self.worn:
            self.worn[cat].deleteLater()
            del self.worn[cat]
        
    
        image_path = resource_path(item["image"])
        print(f"[DEBUG] Загружаем: {image_path}")
        
        pix = QPixmap(image_path)
        if pix.isNull():
            print(f"[ОШИБКА] Не загружено изображение: {image_path}")
            return
        
        pix = pix.scaled(200, 700,
                         Qt.AspectRatioMode.IgnoreAspectRatio,
                         Qt.TransformationMode.SmoothTransformation)
       
        cloth = WornCloth(self.doll_area)
        cloth.setPixmap(pix)
        cloth.setGeometry(250, 50, 200, 700)
        cloth.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        cloth.show()
        
        self.worn[cat] = cloth
        print(f"[DEBUG] Успешно надето: {cat}")
    
    def reset_all(self):
        box = QMessageBox()
        box.setWindowTitle("СБРОС")
        box.setText("Точно хотите сбросить образ?")
        box.setStyleSheet("""
            QMessageBox { background: rgb(255,180,210); }
            QLabel { font-size: 25px; color: white; font-weight: bold; }
            QPushButton { background: white; min-width: 120px; min-height: 45px; border-radius: 15px; color: rgb(255,120,150); font-size: 18px; }
        """)
        
        yes = box.addButton("ДА", QMessageBox.ButtonRole.YesRole)
        no = box.addButton("НЕТ", QMessageBox.ButtonRole.NoRole)
        box.exec()
        
        if box.clickedButton() == yes:
            for cloth in self.worn.values():
                cloth.deleteLater()
            self.worn.clear()