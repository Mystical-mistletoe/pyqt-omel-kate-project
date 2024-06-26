from math import sqrt
import sqlite3
from PyQt5 import QtCore, QtWidgets
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleFactory, QWidget, QSpinBox, QTableView, QPushButton, \
    QVBoxLayout, QComboBox, QLabel, QStatusBar, QMenuBar, QTableWidget, QTableWidgetItem, QPlainTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class AddWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('Документация')
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.move(5, 5)
        self.text_edit.resize(390, 390)
        self.setStyle(QStyleFactory.create('Fusion'))  # стиль
        self.setStyleSheet('background-color: #F5F5DC; color: black; font-size: 20px;')  # цвет фона и цвет текста
        self.open_file()

    def open_file(self):
        self.text_edit.clear()
        with open("document.txt", mode="r", encoding="utf-8") as file:
            data = file.readlines()
            for line in data:
                if "\n" in line:
                    self.text_edit.appendPlainText(line[:-1])
                else:
                    self.text_edit.appendPlainText(line)


class TheMainWorkingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.initUI()
        self.con = sqlite3.connect('name1.sqlite')
        self.creating_table()
        plt.grid(True)
        self.setStyle(QStyleFactory.create('Fusion'))  # стиль
        self.setStyleSheet('background-color: #F5F5DC; color: black; font-size: 20px;')  # цвет фона и цвет текста

    def initUI(self):
        self.setGeometry(400, 400, 800, 800)
        self.setWindowTitle('Функции и их графики')
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Решение уравнения при у == 0:')
        self.koeff_a = QSpinBox(self)
        self.koeff_a.setGeometry(410, 110, 100, 30)
        self.koeff_a.setButtonSymbols(2)
        self.koeff_a.setRange(-9999, 9999)
        self.label_a = QLabel(self)
        self.label_a.setText("Коэффициент а")
        self.koeff_b = QSpinBox(self)
        self.koeff_b.setGeometry(410, 140, 100, 30)
        self.koeff_b.setButtonSymbols(2)
        self.koeff_b.setRange(-9999, 9999)
        self.label_b = QLabel(self)
        self.label_b.setText("Коэффициент b")
        self.koeff_c = QSpinBox(self)
        self.koeff_c.setGeometry(410, 170, 100, 30)
        self.koeff_c.setButtonSymbols(2)
        self.koeff_c.setRange(-9999, 9999)
        self.label_c = QLabel(self)
        self.label_c.setText("Коэффициент c")
        self.btn = QPushButton('Выполнить', self)
        #self.btn.setGeometry(410, 200, 93, 28)
        self.btn.clicked.connect(self.plot)
        self.btn.clicked.connect(self.add_elem)
        self.btn1 = QPushButton('очистить историю', self)
        #self.btn1.setGeometry(410, 250, 93, 28)
        self.btn1.clicked.connect(self.delete_history)
        self.label = QLabel(self)
        self.label.setText("Индекс")
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("у = aх^3")
        self.comboBox.addItem("y = a / x")
        self.comboBox.addItem("y = ax^2 + bx + c")
        self.comboBox.addItem("y = √x")
        self.view = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        self.view.setDatabaseName('name1.sqlite')
        # И откроем подключение
        self.view.open()
        # QTableView - виджет для отображения данных из базы
        self.tableWidget = QTableView(self)
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, self.view)
        model.setTable('name1')
        model.select()
        # Для отображения данных на виджете свяжем его и нашу модель данных
        self.tableWidget.setModel(model)

        self.btn_doc = QPushButton('документация', self)
        self.btn_doc.setGeometry(410, 250, 93, 28)
        self.btn_doc.clicked.connect(self.adding)
        layout = QVBoxLayout()
        layout.addWidget(self.btn_doc)
        layout.addWidget(self.label)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.label_a)
        layout.addWidget(self.koeff_a)
        layout.addWidget(self.label_b)
        layout.addWidget(self.koeff_b)
        layout.addWidget(self.label_c)
        layout.addWidget(self.koeff_c)
        layout.addWidget(self.canvas)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.btn)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.btn1)
        layout.addWidget(self.status_bar)
        self.setLayout(layout)

    def creating_table(self):
            cur = self.con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS name1 (
                    fc TEXT,
                    a INTEGER,
                    b INTEGER,
                    c INTEGER
                )
                ''')

    def diskrimonant(self, a, b, c):
        d = b ** 2 - 4 * a * c
        if a == 0 and b == 0 and c == 0:
            return 'При любом x'
        elif (b == 0 and c == 0) or (a == 0 and c == 0) or (a == 0 and b == 0):
            return 'x1,2 = 0'
        elif a == 0:
            x = -c / b
            return f'x = {x:.2f}'
        elif b == 0:
            x = -c / a
            if x > 0:
                return f'x = {sqrt(x):.2f}'
            else:
                return 'Нет решений'
        elif c == 0:
            x = -b / a
            return f'x1 = 0; x2 = {x:.2f}'
        else:
            if d > 0:
                x1 = (-b + sqrt(d) / (2 * a))
                x2 = (-b - sqrt(d) / (2 * a))
                return f'x1 = {x1:.2f}; x2 = {x2:.2f}'
            elif d == 0:
                x1 = -b / (2 * a)
                return f'x1 = {x1:.2f}'
            else:
                return 'Нет решений'

    def plot(self):
        i = self.comboBox.currentIndex()
        self.label.setText("Индекс:" + str(i))
        a = int(self.koeff_a.text())
        b = int(self.koeff_b.text())
        c = int(self.koeff_c.text())
        if i == 2:
            x = np.linspace(-1000, 1000, 10000)
            # для генерации последовательности чисел в линейном пространстве с одинаковым размером шага
            y = a * x ** 2 + b * x + c
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            plt.grid(True)
            self.canvas.draw()
            self.status_bar.showMessage(f'Решение уравнения при у == 0: {self.diskrimonant(a, b, c)}')
        if i == 0:
            x = np.linspace(-1000, 1000, 10000)
            y = a * x ** 3
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            plt.grid(True)
            self.canvas.draw()
        if i == 1:
            x = np.linspace(-1000, 1000, 10000)
            y = a / x
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            plt.grid(True)
            self.canvas.draw()
        if i == 3:
            x = np.linspace(0, 10, 10000)
            y = np.sqrt(x)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            plt.grid(True)
            self.canvas.draw()

    def add_elem(self):
        cur = self.con.cursor()
        fc = self.comboBox.currentText()
        a = int(self.koeff_a.text())
        b = int(self.koeff_b.text())
        c = int(self.koeff_c.text())
        new_data = (fc, a, b, c)
        cur.execute("INSERT INTO name1 (fc, a, b, c) VALUES (?,?,?,?)", new_data)
        self.con.commit()
        model = QSqlTableModel(self, self.view)
        model.setTable('name1')
        model.select()
        self.tableWidget.setModel(model)

    def delete_history(self):
        cur = self.con.cursor()
        cur.execute('DELETE FROM name1')
        self.con.commit()
        model = QSqlTableModel(self, self.view)
        model.setTable('name1')
        model.select()
        self.tableWidget.setModel(model)

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TheMainWorkingWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
