import sqlite3

import pickle
import sys

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from hero import Hero
from save_ui import Ui_MainWindow


class SaveView:
    def __init__(self):
        self.hero = None
        self.level = None

    def start(self):
        app = QApplication(sys.argv)
        sqt = SaveQt(self)
        sqt.show()
        app.exec()


class SaveQt(QMainWindow, Ui_MainWindow):
    def __init__(self, self2):
        super().__init__()
        self.self2 = self2
        self.setupUi(self)
        self.setWindowTitle('Hello')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint)

        self.exit_btn.clicked.connect(self.close)

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

        self.con = sqlite3.connect("saves/saves_sql.db")
        cur = self.con.cursor()
        self.saves_buttons = cur.execute("""SELECT * FROM saves""").fetchall()

        for save in self.saves_buttons:
            btn = QPushButton(f'{save[2]} --- {save[1]}', self)
            btn.setStyleSheet("text-align: left")
            save_f = save[0]
            btn.clicked.connect(
                lambda save_f, save_f0=save_f: self.file_r(save_f0))
            self.btn_lay.addWidget(btn)

    def file_r(self, save_f):
        with open(f'saves/{save_f}/{save_f}/{save_f}.save', "rb") as file:
            hero = pickle.load(file)








