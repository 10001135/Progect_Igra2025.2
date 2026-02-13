import sys
from texts import text_d

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from consts import *

from dialog_fr_ui import Ui_MainWindow


class Dialog:
    def __init__(self, text_npc, hero_answers, npc, hero, npc_name):
        self.text_npc = text_npc
        self.hero_answers = hero_answers
        self.npc = npc
        self.npc_name = npc_name
        self.hero = hero

    def start(self):
        app = QApplication(sys.argv)
        dqt = DialogQt(self.npc, self.hero, self.text_npc, self.hero_answers, self, self.npc_name)
        dqt.show()
        app.exec()


class DialogQt(QMainWindow, Ui_MainWindow):
    def __init__(self, npc, hero, text_npc, hero_answers, self2, npc_name):
        super().__init__()
        self.setupUi(self)
        self.hero_answers = hero_answers
        self.self2 = self2
        self.npc_name = npc_name
        screen_width, screen_height = get_display_size()
        self.setGeometry(int(screen_width // 2 - int(1620 * SCALE) / 2),
                         int(screen_height // 2 - int(600 * SCALE) / 2 - 200 * SCALE), 0, 0)
        self.setFixedWidth(int(SCREEN_WIDTH - (300 * SCALE)))
        self.setFixedHeight(int(SCREEN_HEIGHT - (480 * SCALE)))

        self.setWindowTitle('Hello')

        self.npc_av.setStyleSheet(f"border-image: url(assets/textures/NPC/{npc}) space")
        self.npc_av.setFixedSize(int(200 * SCALE), int(200 * SCALE))
        if self.npc_name == text_d['fara_name']:
            self.npc_av.setFixedSize(int(200 * SCALE), int(313 * SCALE))

        if self.npc_name == text_d['captain_name']:
            self.npc_av.setFixedSize(int(125 * SCALE), int(264 * SCALE))

        self.hero_av.setStyleSheet(f"border-image: url({hero}) space")
        self.hero_av.setFixedSize(int(200 * SCALE), int(200 * SCALE))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        self.npc_tb.setText(f'<b>{self.npc_name}: </b>{text_npc}')

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

        self.answers_buttons = {}
        for answer in self.hero_answers:
            self.answers_buttons[answer] = QPushButton(answer, self)
            self.answers_buttons[answer].setStyleSheet("text-align: left")
            self.answers_buttons[answer].clicked.connect(
                lambda answer, answer0=answer: self.to_answer(self.hero_answers[answer0], answer0, answer0))
            self.answers_lay.addWidget(self.answers_buttons[answer])

    def to_answer(self, answer, answer_p, answer_0):
        self.answers_buttons = {}
        while self.answers_lay.count():
            self.answers_lay.removeWidget(self.answers_lay.itemAt(0).widget())

        if answer_p:
            self.npc_tb.setText(self.npc_tb.toHtml() + '\n' + '<b>Вы: </b>' + answer_p)

        if answer.__class__.__name__ == 'dict':
            for answer_new in answer[list(answer)[0]]:
                self.answers_buttons[answer_new] = QPushButton(answer_new, self)
                self.answers_buttons[answer_new].setStyleSheet("text-align: left")
                self.answers_buttons[answer_new].clicked.connect(
                    lambda answer_new, answer_new0=answer_new: self.to_answer(answer[list(answer)[0]][answer_new0],
                                                                              answer_new0, answer_0))
                self.answers_lay.addWidget(self.answers_buttons[answer_new])
            self.npc_tb.setText(self.npc_tb.toHtml() + '\n' + f'<b>{self.npc_name}: </b>' + list(answer)[0])

        if answer == 0:
            self.self2.hero_answers = self.hero_answers
            self.close()

        if answer == 1:
            del self.hero_answers[answer_0]
            self.self2.hero_answers = self.hero_answers
            self.close()

        if answer.__class__.__name__ == 'str':
            del self.hero_answers[answer_0]
            for answer_new in self.hero_answers:
                self.answers_buttons[answer_new] = QPushButton(answer_new, self)
                self.answers_buttons[answer_new].setStyleSheet("text-align: left")
                self.answers_buttons[answer_new].clicked.connect(
                    lambda answer_new, answer_new0=answer_new: self.to_answer(self.hero_answers[answer_new0],
                                                                              answer_new0, answer_new0))
                self.answers_lay.addWidget(self.answers_buttons[answer_new])

            self.npc_tb.setText(self.npc_tb.toHtml() + '\n' + f'<b>{self.npc_name}: </b>' + answer)
