from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

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
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        self.label = QLabel("00:00:00")
        self.label.setStyleSheet("color: white; font-size: 300px; font-family: 'Consolas'; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def toggle_blink(self):
        self.is_visible = not self.is_visible
        opacity = "1.0" if self.is_visible else "0.0"
        self.label.setStyleSheet(f"color: {self.current_color}; font-size: 300px; font-family: 'Consolas'; font-weight: bold; opacity: {opacity};")
        # Nota: Como QLabel no tiene opacity real en QSS fácil, alternamos el color con transparente
        if not self.is_visible:
            self.label.setStyleSheet(f"color: white; font-size: 300px; font-family: 'Consolas'; font-weight: bold;")
        else:
            self.label.setStyleSheet(f"color: {self.current_color}; font-size: 300px; font-family: 'Consolas'; font-weight: bold;")

    def update_display(self, text, color, should_blink):
        self.label.setText(text)
        self.current_color = color
        
        if should_blink:
            if not self.blink_timer.isActive():
                self.blink_timer.start(500) # Parpadea cada medio segundo
        else:
            self.blink_timer.stop()
            self.label.setStyleSheet(f"color: {color}; font-size: 300px; font-family: 'Consolas'; font-weight: bold;")

    def stop_presenting(self):
        self.blink_timer.stop()
        self.hide()
        self.label.setStyleSheet(f"color: white; font-size: 300px; font-family: 'Consolas'; font-weight: bold;")
        self.current_color = "white"
        self.is_visible = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.showNormal()