import sqlite3

import time

import pickle
import sys
import traceback

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from save_ui import Ui_MainWindow
from textures import Textures
from views.game_levels.Middle_Ages.ma_level_1 import GameView_ma_level_1
from views.game_levels.Middle_Ages.ma_level_2 import GameView_ma_level_2
from views.game_levels.Middle_Ages.ma_level_3 import GameView_ma_level_3
from views.game_levels.Middle_Ages.ma_level_4 import GameView_ma_level_4
from views.game_levels.Middle_Ages.ma_level_5 import GameView_ma_level_5
from views.game_levels.Middle_Ages.ma_level_6 import GameView_ma_level_6
from views.game_levels.Middle_Ages.ma_level_7 import GameView_ma_level_7

from views.game_levels.Future.Future_level_1 import GameView_fut_level_1
from views.game_levels.Future.Future_level_2 import GameView_fut_level_2
from views.load_view import LoadView

LEVELS = [GameView_ma_level_1, GameView_ma_level_2, GameView_ma_level_3, GameView_ma_level_4, GameView_ma_level_5,
          GameView_ma_level_6, GameView_ma_level_7, GameView_fut_level_1, GameView_fut_level_2]
LEVELS_DICT = {}
for level in LEVELS:
    LEVELS_DICT[level.__name__] = level

class SaveView:
    def __init__(self):
        self.hero = None
        self.level = None

    def start(self, window):
        self.window = window
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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.exit_btn.clicked.connect(self.close_w)

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
            btn = QPushButton(f'{save[2]} --- {format_time(int(save[1]))}', self)
            btn.setStyleSheet("text-align: left")
            btn.clicked.connect(
                lambda save, save0=save: self.file_r(save0))
            self.btn_lay.addWidget(btn)

    def file_r(self, save):
        with open(f'saves/saves_files/{save[0]}.save', "rb") as file:
            hero = pickle.load(file)
            level = LEVELS_DICT[save[3]]
            Textures.texture_hero_1()
            self.self2.window.show_view(LoadView(hero, 993, level))
            self.close()

    def close_w(self):
        self.con.close()
        self.close()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


def format_time(seconds):
    time_f = time.gmtime(seconds)
    return time.strftime("%H:%M:%S", time_f)


sys.excepthook = excepthook
