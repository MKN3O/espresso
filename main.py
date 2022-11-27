import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class CoffeeStart(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.change)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        res = self.cur.execute("""SELECT * FROM coffee""")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт кофе', 'Степень прожарки', 'Молотый',
                                                    'Дескриптор', 'Цена', 'Масса, грамм'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def change(self):
        self.changepage = CoffeeChange(self.con)
        self.changepage.show()
        self.hide()


class CoffeeChange(QWidget):
    def __init__(self, con):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.tableWidget.itemChanged.connect(self.chgn)
        self.pushButton.clicked.connect(self.addNew)
        self.clmns = ['id', 'sort', 'grade', 'condition', 'descriptor', 'price', 'mass']
        self.con = con
        self.cur = self.con.cursor()
        res = list(self.cur.execute("""SELECT * FROM coffee"""))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт кофе', 'Степень прожарки', 'Молотый',
                                                    'Дескриптор', 'Цена', 'Масса, грамм'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def addNew(self):
        self.cur.execute(f"""INSERT INTO coffee(sort, grade, condition, descriptor, price, mass)
                             VALUES('{self.sort.text()}','{self.grade.text()}','{self.buttonTrue.isChecked()}','{self.descriptor.text()}',
                             '{self.price.text()}','{self.mass.text()}')""")
        self.con.commit()
        res = list(self.cur.execute("""SELECT * FROM coffee"""))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт кофе', 'Степень прожарки', 'Молотый',
                                                    'Дескриптор', 'Цена', 'Масса, грамм'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def chgn(self, item):
        if int(item.column()) != 0:
            self.cur.execute(f"""UPDATE coffee
                                  SET {self.clmns[item.column()]} = '{str(item.text())}'
                                  WHERE id = '{(item.row() + 1)}'""")
            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeStart()
    ex.show()
    sys.exit(app.exec_())
