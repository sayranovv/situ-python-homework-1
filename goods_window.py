from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3
from database import add_good, get_all_goods, update_good, delete_good

class GoodsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление товарами")
        self.setGeometry(200, 200, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        form_layout = QHBoxLayout()
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Категория")
        form_layout.addWidget(self.category_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Наименование")
        form_layout.addWidget(self.name_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Количество в упаковке")
        form_layout.addWidget(self.quantity_input)

        main_layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_good)
        buttons_layout.addWidget(btn_add)

        btn_edit = QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_good)
        buttons_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_good)
        buttons_layout.addWidget(btn_delete)

        main_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Категория", "Наименование", "Кол-во в упаковке"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.fill_inputs_from_selection)
        main_layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        try:
            goods = get_all_goods()
            self.table.setRowCount(len(goods))
            for row, good in enumerate(goods):
                for col, value in enumerate(good):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def fill_inputs_from_selection(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.category_input.setText(self.table.item(row, 1).text())
            self.name_input.setText(self.table.item(row, 2).text())
            self.quantity_input.setText(self.table.item(row, 3).text())

    def add_good(self):
        category = self.category_input.text().strip()
        name = self.name_input.text().strip()
        quantity_str = self.quantity_input.text().strip()

        if not category or not name or not quantity_str:
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным")
            add_good(category, name, quantity)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Товар добавлен")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {e}")

    def edit_good(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для редактирования!")
            return

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())
        category = self.category_input.text().strip()
        name = self.name_input.text().strip()
        quantity_str = self.quantity_input.text().strip()

        if not category or not name or not quantity_str:
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным")
            update_good(id, category, name, quantity)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Товар обновлен")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {e}")

    def delete_good(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления!")
            return

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Подтверждение", "Удалить эту запись?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_good(id)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Успех", "Товар удален")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def clear_inputs(self):
        self.category_input.clear()
        self.name_input.clear()
        self.quantity_input.clear()


