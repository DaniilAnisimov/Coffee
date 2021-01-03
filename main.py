import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        result = self.cur.execute("""SELECT * FROM "coffee" """).fetchall()
        title_list = [i[1] for i in self.cur.execute("pragma table_info(coffee)").fetchall()]
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            for j, elem1 in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
