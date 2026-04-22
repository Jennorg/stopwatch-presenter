import os
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PresenterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_color = "white"
        self.is_visible = True
        
        # Timer para el parpadeo
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_blink)

    def init_ui(self):
        self.setWindowTitle("Proyección de Cronómetro")
        self.setWindowIcon(QIcon(resource_path("assets/icon.png")))
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.label = QLabel("00:00:00")
        # Reducimos un poco el tamaño de fuente para evitar desbordamiento horizontal
        # y aseguramos que el texto esté centrado tanto vertical como horizontalmente.
        self.label.setStyleSheet("color: white; font-size: 250px; font-family: 'Consolas'; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

    def toggle_blink(self):
        self.is_visible = not self.is_visible
        color = self.current_color if self.is_visible else "transparent"
        self.label.setStyleSheet(f"color: {color}; font-size: 250px; font-family: 'Consolas'; font-weight: bold;")

    def update_display(self, text, color, should_blink):
        self.label.setText(text)
        self.current_color = color
        
        if should_blink:
            if not self.blink_timer.isActive():
                self.blink_timer.start(500) # Parpadea cada medio segundo
        else:
            self.blink_timer.stop()
            self.label.setStyleSheet(f"color: {color}; font-size: 250px; font-family: 'Consolas'; font-weight: bold;")

    def stop_presenting(self):
        self.blink_timer.stop()
        self.hide()
        self.label.setStyleSheet(f"color: white; font-size: 250px; font-family: 'Consolas'; font-weight: bold;")
        self.current_color = "white"
        self.is_visible = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.showNormal()