#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget,
    QLineEdit, QCheckBox, QComboBox, QRadioButton, QPushButton, QListWidget, QListWidgetItem, QScrollArea, QLabel,
    QDialog, QTextEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer


class ResultDialog(QDialog):
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle("Результат")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(result)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)


class DraggableRectangle(QWidget):
    def __init__(self, parent=None, color='blue', size=(100, 50)):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(*size)
        self.dragging = False
        self.offset = QPoint(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(self.color))
        painter.drawRect(0, 0, self.width(), self.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()  # Сохраняем смещение курсора относительно прямоугольника
            self.setCursor(Qt.ClosedHandCursor)  # Меняем курсор на "рука"

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Перемещаем прямоугольник
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)  # Возвращаем курсор в исходное состояние


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример с вкладками")
        self.setGeometry(100, 100, 800, 600)

        # Создаем основной вертикальный layout
        main_layout = QVBoxLayout()

        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(self.createTab1(), "Вкладка 1")
        self.tabs.addTab(self.createTab2(), "Вкладка 2")
        self.tabs.addTab(self.createTab3(), "Вкладка 3")  # Обновленная третья вкладка
        self.tabs.addTab(self.createTab4(), "Вкладка 4")
        self.tabs.addTab(self.createTab5(), "Вкладка 5")

        main_layout.addWidget(self.tabs)

        # Кнопка обновления
        self.update_button = QPushButton('Обновить', self)
        self.update_button.clicked.connect(self.reset_fields)
        main_layout.addWidget(self.update_button)

        self.setLayout(main_layout)

    def createTab1(self):
        tab1 = QWidget()
        layout = QVBoxLayout()

        # Поля ввода
        self.entry1 = QLineEdit(self)
        self.entry2 = QLineEdit(self)
        self.entry3 = QLineEdit(self)

        layout.addWidget(self.entry1)
        layout.addWidget(self.entry2)
        layout.addWidget(self.entry3)

        # Чек-боксы
        self.check1 = QCheckBox('Check 1', self)
        self.check2 = QCheckBox('Check 2', self)
        self.check3 = QCheckBox('Check 3', self)

        layout.addWidget(self.check1)
        layout.addWidget(self.check2)
        layout.addWidget(self.check3)

        # Кнопка "Исчезну"
        self.disappear_button = QPushButton('Исчезну', self)
        layout.addWidget(self.disappear_button)

        # Устанавливаем таймер для исчезновения кнопки
        QTimer.singleShot(5000, self.disappear_button.hide)  # Скрыть кнопку через 5 секунд

        # Кнопка "Включен/Выключен"
        self.toggle_button = QPushButton('Включен/Выключен', self)
        self.toggle_button.clicked.connect(self.toggle_button_clicked)
        layout.addWidget(self.toggle_button)

        # Скрытая кнопка
        self.hidden_button = QPushButton('Скрытая кнопка', self)
        self.hidden_button.setVisible(False)  # Изначально скрыта
        layout.addWidget(self.hidden_button)

        tab1.setLayout(layout)
        return tab1

    def toggle_button_clicked(self):
        # Делаем кнопку недоступной
        self.toggle_button.setEnabled(False)

    def createTab2(self):
        tab2 = QWidget()
        layout = QVBoxLayout()
        # Комбо-боксы
        self.combo1 = QComboBox(self)
        self.combo1.addItems(["Option 1", "Option 2", "Option 3"])
        self.combo2 = QComboBox(self)
        self.combo2.addItems(["Option 1", "Option 2", "Option 3"])
        self.combo3 = QComboBox(self)
        self.combo3.addItems(["Option 1", "Option 2", "Option 3"])

        layout.addWidget(self.combo1)
        layout.addWidget(self.combo2)
        layout.addWidget(self.combo3)

        # Радиокнопки
        self.radio1 = QRadioButton('Radio 1', self)
        self.radio2 = QRadioButton('Radio 2', self)
        self.radio3 = QRadioButton('Radio 3', self)

        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)
        layout.addWidget(self.radio3)

        tab2.setLayout(layout)
        return tab2

    def createTab3(self):
        tab3 = QWidget()
        layout = QVBoxLayout()

        # Создаем область для перетаскивания
        self.drag_area = QWidget(self)
        self.drag_area.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: 2px solid black;")
        self.drag_area.setFixedSize(400, 300)  # Размер области
        layout.addWidget(self.drag_area)

        # Создаем два прямоугольника
        self.rectangle1 = DraggableRectangle(self.drag_area, color='blue', size=(150, 75))  # Большой прямоугольник
        self.rectangle1.move(50, 50)  # Начальная позиция первого прямоугольника

        self.rectangle2 = DraggableRectangle(self.drag_area, color='red', size=(100, 50))  # Маленький прямоугольник
        self.rectangle2.move(200, 150)  # Начальная позиция второго прямоугольника

        # Добавляем прямоугольники в область перетаскивания
        self.drag_area_layout = QVBoxLayout(self.drag_area)
        self.drag_area_layout.addWidget(self.rectangle1)
        self.drag_area_layout.addWidget(self.rectangle2)

        self.drag_area.setLayout(self.drag_area_layout)  # Устанавливаем layout для drag_area
        tab3.setLayout(layout)
        return tab3

    def createTab4(self):
        tab4 = QWidget()
        layout = QVBoxLayout()

        # Создаем QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Создаем виджет для размещения в QScrollArea
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Добавляем 300 элементов в список
        for i in range(300):
            item = QLabel(f'Item {i + 1}', self)
            scroll_layout.addWidget(item)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        layout.addWidget(scroll_area)

        tab4.setLayout(layout)
        return tab4

    def createTab5(self):
        tab5 = QWidget()
        layout = QVBoxLayout()

        # Создаем QListWidget с множественным выбором
        self.multi_select_list = QListWidget(self)
        self.multi_select_list.setSelectionMode(QListWidget.MultiSelection)

        # Добавляем элементы в список
        for i in range(1, 11):  # Добавляем 10 элементов
            item = QListWidgetItem(f'Item {i}')
            self.multi_select_list.addItem(item)

        layout.addWidget(self.multi_select_list)

        # Создаем таблицу 3x3
        self.table_widget = QTableWidget(3, 3, self)
        self.table_widget.setHorizontalHeaderLabels(['Col 1', 'Col 2', 'Col 3'])
        self.table_widget.setVerticalHeaderLabels(['Row 1', 'Row 2', 'Row 3'])

        # Заполняем таблицу цифрами от 1 до 9
        count = 1
        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(str(count))
                self.table_widget.setItem(row, col, item)
                count += 1

        layout.addWidget(self.table_widget)

        tab5.setLayout(layout)
        return tab5

    def reset_fields(self):
        # Сбрасываем значения всех полей на значения по умолчанию
        self.entry1.clear()
        self.entry2.clear()
        self.entry3.clear()

        self.check1.setChecked(False)
        self.check2.setChecked(False)
        self.check3.setChecked(False)

        self.combo1.setCurrentIndex(0)  # Сбрасываем на первый элемент
        self.combo2.setCurrentIndex(0)
        self.combo3.setCurrentIndex(0)

        self.radio1.setChecked(False)
        self.radio2.setChecked(False)
        self.radio3.setChecked(False)

        self.multi_select_list.clearSelection()  # Сбрасываем выделение в множественном списке

        # Включаем кнопку "Включен/Выключен"
        self.toggle_button.setEnabled(True)

        # Показать/скрыть скрытую кнопку
        self.hidden_button.setVisible(not self.hidden_button.isVisible())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
