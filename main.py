import sys
from PyQt6.QtWidgets import QApplication
from core.timer import StopwatchLogic
from ui.controller_view import ControllerWindow
from ui.presenter_view import PresenterWindow

def main():
    app = QApplication(sys.argv)
    logic = StopwatchLogic()
    presenter = PresenterWindow()
    
    controller = ControllerWindow(logic, presenter)
    controller.show()
    presenter.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()