from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
from clothes_data import CLOTHES

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


class DragButton(QPushButton):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.item = item
        self.setFixedSize(150, 150)
        self.setStyleSheet("""
            QPushButton {
                background: white;
                border-radius: 15px;
                border: 2px solid rgb(255,200,210);
            }
            QPushButton:hover {
                background: rgb(240,240,240);
            }
        """)
        
        pix = QPixmap(item["image"])
        if not pix.isNull():
            pix = pix.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
            self.setIcon(QIcon(pix))
            self.setIconSize(QSize(120, 120))
        else:
            self.setText(item["name"])
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setData("application/x-clothing", json.dumps(self.item).encode())
            drag.setMimeData(mime)
            
            if self.icon():
                pix = self.icon().pixmap(80, 80)
                drag.setPixmap(pix)
                drag.setHotSpot(QPoint(40, 40))
            
            drag.exec(Qt.DropAction.MoveAction)
        else:
            super().mousePressEvent(event)


class Wardrobe(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedWidth(450)
        self.setStyleSheet("background: white; border-radius: 30px;")
        
        layout = QVBoxLayout()
        
        cat_layout = QHBoxLayout()
        for cat in CLOTHES.keys():
            btn = QPushButton(cat)
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: rgb(255,120,150);
                    font-size: 24px;
                    font-weight: bold;
                    border-radius: 15px;
                    border: 2px solid rgb(255,200,210);
                }
                QPushButton:hover {
                    background: rgb(240,240,240);
                }
            """)
            btn.clicked.connect(lambda checked, c=cat: self.show_category(c))
            cat_layout.addWidget(btn)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: white; border: none;")
        
        self.items_widget = QWidget()
        self.items_grid = QGridLayout(self.items_widget)
        self.items_grid.setSpacing(10)
        
        self.scroll.setWidget(self.items_widget)
        
        layout.addLayout(cat_layout)
        layout.addWidget(self.scroll)
        
        self.setLayout(layout)
        self.show_category("👗")
    
    def show_category(self, cat):
        for i in reversed(range(self.items_grid.count())):
            w = self.items_grid.itemAt(i).widget()
            if w:
                w.deleteLater()
        
        row, col = 0, 0
        for item in CLOTHES[cat]:
            btn = DragButton(item, self)
            self.items_grid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1