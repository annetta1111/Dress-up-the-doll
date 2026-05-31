from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
from wardrobe import Wardrobe


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
        
        self.doll_area = QWidget()
        self.doll_area.setFixedSize(700, 800)
        self.doll_area.setAcceptDrops(True)
        self.doll_area.setStyleSheet("background: white; border-radius: 30px;")
        
        self.doll = QLabel(self.doll_area)
        pix = QPixmap("images/clothes/doll11.png")
        if not pix.isNull():
            pix = pix.scaled(200, 700, Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
            self.doll.setPixmap(pix)
        else:
            self.doll.setText("🪆")
            self.doll.setStyleSheet("font-size: 40px;")
        
        self.doll.move(250, 50)
        self.doll.setFixedSize(200, 700)
        
    
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
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-clothing"):
            event.acceptProposedAction()
    
    def dropEvent(self, event):
      
        data = event.mimeData().data("application/x-clothing").data()
        item = json.loads(data.decode())
        self.try_wear(item)
    
    def try_wear(self, item):
        cat = item["cat"]
        
        
        if cat in self.worn:
            self.worn[cat].deleteLater()
            del self.worn[cat]
        
       
        pix = QPixmap(item["image"])
        if pix.isNull():
            return
        
        cloth = QLabel(self.doll_area)
        pix = pix.scaled(200,700,
    Qt.AspectRatioMode.IgnoreAspectRatio,
    Qt.TransformationMode.SmoothTransformation
        )

        cloth.setGeometry(
            250,
            50,
            200,
            700
        )
       
        cloth = QLabel(self.doll_area)
        cloth.setPixmap(pix)
        cloth.setGeometry(250,50,200,700)
        cloth.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        cloth.show()
        
        self.worn[cat] = cloth
    
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