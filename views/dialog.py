import arcade
import traceback
import sys

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox
from arcade import get_display_size

from consts import *

from dialog_fr_ui import Ui_MainWindow


class Dialog:
    def __init__(self, text_npc, hero_answers, npc, hero):
        self.text_npc  = text_npc
        self.hero_answers = hero_answers
        self.npc = npc
        self.hero = hero

    def start(self):
        app = QApplication(sys.argv)
        dqt = DialogQt(self.npc, self.hero, self.text_npc, self.hero_answers, self)
        dqt.show()
        app.exec()
        print(self.hero_answers)


class DialogQt(QMainWindow, Ui_MainWindow):
    def __init__(self, npc, hero, text_npc, hero_answers, self2):
        super().__init__()
        self.setupUi(self)
        self.hero_answers = hero_answers
        self.self2 = self2
        screen_width, screen_height = get_display_size()
        self.setGeometry(int(screen_width // 2 - int(800 * SCALE) / 2), int(screen_height // 2 - int(428 * SCALE) / 2 - 200 * SCALE), 0, 0)
        self.setFixedWidth(int(800 * SCALE))
        self.setFixedHeight(int(428 * SCALE))

        self.setWindowTitle('Hello')

        self.npc_av.setStyleSheet(f"border-image: url(assets/textures/NPC/{npc}) space")
        self.npc_av.setMinimumSize(int(200 * SCALE), int(200 * SCALE))

        self.hero_av.setStyleSheet(f"border-image: url({hero}) space")
        self.hero_av.setMinimumSize(int(200 * SCALE), int(200 * SCALE))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowStaysOnTopHint)

        self.npc_tb.setText(text_npc)

        self.answers_buttons = {}
        for answer in self.hero_answers:
            self.answers_buttons[answer] = QPushButton(answer, self)
            self.answers_buttons[answer].setStyleSheet("text-align: right")
            self.answers_buttons[answer].clicked.connect(lambda answer, answer0=answer: self.to_answer(self.hero_answers[answer0], answer0, answer0))
            self.answers_lay.addWidget(self.answers_buttons[answer])

    def to_answer(self, answer, answer_p, answer_0):
        self.answers_buttons = {}
        while self.answers_lay.count():
            self.answers_lay.removeWidget(self.answers_lay.itemAt(0).widget())

        print(answer_p)
        if answer_p:
            self.npc_tb.setText(self.npc_tb.toPlainText() + '\n' + 'hero: ' + answer_p)

        if answer.__class__.__name__ == 'dict':
            for answer_new in answer[list(answer)[0]]:
                self.answers_buttons[answer_new] = QPushButton(answer_new, self)
                self.answers_buttons[answer_new].setStyleSheet("text-align: right")
                self.answers_buttons[answer_new].clicked.connect(lambda answer_new, answer_new0=answer_new: self.to_answer(answer[list(answer)[0]][answer_new0], answer_new0, answer_0))
                self.answers_lay.addWidget(self.answers_buttons[answer_new])
            self.npc_tb.setText(self.npc_tb.toPlainText() + '\n' + 'king: ' + list(answer)[0])

        if answer.__class__.__name__ == 'int':
            self.self2.hero_answers = self.hero_answers
            self.close()

        if answer.__class__.__name__ == 'str':
            del  self.hero_answers[answer_0]
            for answer_new in self.hero_answers:
                self.answers_buttons[answer_new] = QPushButton(answer_new, self)
                self.answers_buttons[answer_new].setStyleSheet("text-align: right")
                self.answers_buttons[answer_new].clicked.connect(lambda answer_new, answer_new0=answer_new: self.to_answer(self.hero_answers[answer_new0], None, answer_new0))
                self.answers_lay.addWidget(self.answers_buttons[answer_new])

            self.npc_tb.setText(self.npc_tb.toPlainText() + '\n' + 'king: ' + answer)






