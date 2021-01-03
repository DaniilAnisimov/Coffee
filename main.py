import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sqlite3
from addEditCoffeeForm import Ui_Dialog
from main_form import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.pb_add.clicked.connect(self.add)
        self.pb_edit.clicked.connect(self.edit)
        self.load_table()

    def load_table(self):
        result = self.cur.execute("""SELECT * FROM "coffee" """).fetchall()
        title_list = [i[1] for i in self.cur.execute("pragma table_info(coffee)").fetchall()]
        self.tableWidget.setColumnCount(len(title_list))
        self.tableWidget.setHorizontalHeaderLabels(title_list)
        self.tableWidget.setRowCount(0)
        for i, elem in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            for j, elem1 in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem1)))

    def add(self):
        dialogue = CoffeeDialog(self.con, self.cur, "add", [])
        dialogue.show()
        self.setEnabled(False)
        dialogue.exec()
        self.setEnabled(True)
        self.load_table()

    def edit(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) != 1:
            return 0
        select_row = []
        for i in range(7):
            select_row.append(self.tableWidget.item(rows[0], i).text())
        dialogue = CoffeeDialog(self.con, self.cur, "edit", select_row)
        dialogue.show()
        self.setEnabled(False)
        dialogue.exec()
        self.setEnabled(True)
        self.load_table()


class CoffeeDialog(QDialog, Ui_Dialog):
    def __init__(self, con, cur, type_d, row):
        super(CoffeeDialog, self).__init__()
        self.setupUi(self)
        if type_d == "add":
            self.setWindowTitle("Добавить элемент")
            self.pb_add.setText("Добавить")
        else:
            self.setWindowTitle("Редактирование записи")
            self.pb_add.setText("Сохранить")
        self.con = con
        self.cur = cur
        self.type = type_d
        self.properties = row
        self.initUI()

    def initUI(self):
        self.pb_add.clicked.connect(self.acept_data)
        if self.type == "edit":
            self.le_title.setText(self.properties[1])
            self.le_roasting.setText(self.properties[2])
            self.le_type.setText(self.properties[3])
            self.le_taste.setText(self.properties[4])
            self.le_price.setText(self.properties[5])
            self.le_volume.setText(self.properties[6])

    def acept_data(self):
        try:
            title = self.le_title.text()
            roasting = self.le_roasting.text()
            type = self.le_type.text()
            taste = self.le_taste.text()
            price = self.le_price.text()
            volume = self.le_volume.text()
            if title and roasting and type and taste and price and volume:
                if self.type == "add":
                    self.cur.execute("""INSERT INTO coffee("название сорта", "степень обжарки",
                     "молотый/в зернах", "описание вкуса", "цена", "объем упаковки") VALUES(?, ?, ?, ?, ?, ?)""",
                                     (title, roasting, type, taste, price, volume))
                else:
                    self.cur.execute("""UPDATE coffee SET "название сорта" = ?, "степень обжарки" = ?, 
                    "молотый/в зернах" = ?, "описание вкуса" = ?, "цена" = ?, "объем упаковки" = ?
                                      WHERE id = ?""",
                                     (title, roasting, type, taste, price, volume, self.properties[0]))
                self.con.commit()
                self.close()
            else:
                self.l_error.setText("Некоторые поля не заполнены")
        except ValueError:
            self.l_error.setText("Некорректные значения полей")
        except sqlite3.IntegrityError:
            self.l_error.setText("Название занято")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
