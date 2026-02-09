import sys
import traceback

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow


from time_ui import Ui_MainWindow


class TimeView:
    def __init__(self):
        self.hero = None
        self.level = None

    def start(self, window):
        self.window = window
        app = QApplication(sys.argv)
        sqt = TimeQt(self)
        sqt.show()
        app.exec()


class TimeQt(QMainWindow, Ui_MainWindow):
    def __init__(self, self2):
        super().__init__()
        self.self2 = self2
        self.setupUi(self)
        self.setWindowTitle('Hello')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.exit_btn.clicked.connect(self.close)
        self.act_btn.clicked.connect(self.end)

        stylesheet = """
                        QMainWindow {
                            background-color: #15203b;
                        }

                        QTextBrowser {
                            font-size: 18px;
                            font-family: "Courier New"
                        }

                        QWidget {
                            background-color: #15203b;
                            color: #b69a7a;
                            border: 2px solid #555;
                        }

                        QPushButton {
                            background-color: #15203b;
                            color: #b69a7a;
                            border: 1px solid #555;
                            border-radius: 5px;
                            padding: 5px 10px;
                            font-size: 18px;
                            font-family: "Courier New";
                        }

                        QPushButton:hover {
                            border: 2px solid #3498db;
                            border-radius: 10px;
                        }

                        QPushButton:pressed {
                            border: 2px solid #2980b9;
                            border-radius: 10px;
                        }
                    """
        self.setStyleSheet(stylesheet)

    def end(self):
        self.self2.window.show_view(self.window)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


sys.excepthook = excepthook
