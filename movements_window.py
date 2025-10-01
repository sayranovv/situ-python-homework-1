from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, \
    QMessageBox, QTableWidgetItem
import sqlite3
import datetime
from database import add_movement, update_movement, delete_movement, get_all_movements


class MovementsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление движением товаров")
        self.setGeometry(200, 200, 800, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        form_layout = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Дата (YYYY-MM-DD)")
        form_layout.addWidget(self.date_input)

        self.good_id_input = QLineEdit()
        self.good_id_input.setPlaceholderText("ID Товара")
        form_layout.addWidget(self.good_id_input)

        self.store_id_input = QLineEdit()
        self.store_id_input.setPlaceholderText("ID Магазина")
        form_layout.addWidget(self.store_id_input)

        self.operation_type_input = QLineEdit()
        self.operation_type_input.setPlaceholderText("Тип операции")
        form_layout.addWidget(self.operation_type_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Кол-во упаковок")
        form_layout.addWidget(self.quantity_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")
        form_layout.addWidget(self.price_input)

        main_layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_movement)
        buttons_layout.addWidget(btn_add)

        btn_edit = QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_movement)
        buttons_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_movement)
        buttons_layout.addWidget(btn_delete)

        main_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "ID Товара", "ID Магазина", "Тип операции", "Кол-во упаковок", "Цена"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.fill_inputs_from_selection)
        main_layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        try:
            movements = get_all_movements()
            self.table.setRowCount(len(movements))
            for row, movement in enumerate(movements):
                for col, value in enumerate(movement):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def fill_inputs_from_selection(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.date_input.setText(self.table.item(row, 1).text())
            self.good_id_input.setText(self.table.item(row, 2).text())
            self.store_id_input.setText(self.table.item(row, 3).text())
            self.operation_type_input.setText(self.table.item(row, 4).text())
            self.quantity_input.setText(self.table.item(row, 5).text())
            self.price_input.setText(self.table.item(row, 6).text())

    def validate_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_movement(self):
        date = self.date_input.text().strip()
        good_id_str = self.good_id_input.text().strip()
        store_id_str = self.store_id_input.text().strip()
        op_type = self.operation_type_input.text().strip()
        quantity_str = self.quantity_input.text().strip()
        price_str = self.price_input.text().strip()

        if not all([date, good_id_str, store_id_str, op_type, quantity_str, price_str]):
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        if not self.validate_date(date):
            QMessageBox.warning(self, "Внимание", "Дата должна быть в формате YYYY-MM-DD!")
            return

        try:
            good_id = int(good_id_str)
            store_id = int(store_id_str)
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity <= 0 or price < 0:
                raise ValueError("Количество >0, цена >=0")
            add_movement(date, good_id, store_id, op_type, quantity, price)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Операция добавлена")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {e} (Проверьте ID товара/магазина)")


    def edit_movement(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для редактирования!")
            return

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())
        date = self.date_input.text().strip()
        good_id_str = self.good_id_input.text().strip()
        store_id_str = self.store_id_input.text().strip()
        op_type = self.operation_type_input.text().strip()
        quantity_str = self.quantity_input.text().strip()
        price_str = self.price_input.text().strip()

        if not all([date, good_id_str, store_id_str, op_type, quantity_str, price_str]):
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        if not self.validate_date(date):
            QMessageBox.warning(self, "Внимание", "Дата должна быть в формате YYYY-MM-DD!")
            return

        try:
            good_id = int(good_id_str)
            store_id = int(store_id_str)
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity <= 0 or price < 0:
                raise ValueError("Количество >0, цена >=0")
            update_movement(id, date, good_id, store_id, op_type, quantity, price)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Операция обновлена")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {e} (Проверьте ID)")

    def delete_movement(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления!")
            return

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Подтверждение", "Удалить эту запись?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_movement(id)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Успех", "Операция удалена")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def clear_inputs(self):
        self.date_input.clear()
        self.good_id_input.clear()
        self.store_id_input.clear()
        self.operation_type_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()