from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, \
    QMessageBox, QTableWidgetItem
import sqlite3
from database import add_store, update_store, get_all_stores, delete_store

class StoresWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление магазинами")
        self.setGeometry(200, 200, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        form_layout = QHBoxLayout()
        self.district_input = QLineEdit()
        self.district_input.setPlaceholderText("Район")
        form_layout.addWidget(self.district_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Адрес")
        form_layout.addWidget(self.address_input)

        main_layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_store)
        buttons_layout.addWidget(btn_add)

        btn_edit = QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_store)
        buttons_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_store)
        buttons_layout.addWidget(btn_delete)

        main_layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Район", "Адрес"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self.fill_inputs_from_selection)
        main_layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        try:
            stores = get_all_stores()
            self.table.setRowCount(len(stores))
            for row, store in enumerate(stores):
                for col, value in enumerate(store):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def fill_inputs_from_selection(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            self.district_input.setText(self.table.item(row, 1).text())
            self.address_input.setText(self.table.item(row, 2).text())


    def add_store(self):
        district = self.district_input.text().strip()
        address = self.address_input.text().strip()

        if not district or not address:
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        try:
            add_store(district, address)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Товар добавлен")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {e}")


    def edit_store(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для редактирования")

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())
        district = self.district_input.text().strip()
        address = self.address_input.text().strip()

        if not district or not address:
            QMessageBox.warning(self, "Внимание", "Все поля обязательны!")
            return

        try:
            update_store(id, district, address)
            self.load_data()
            self.clear_inputs()
            QMessageBox.information(self, "Успех", "Магазин обновлен")
        except ValueError as ve:
            QMessageBox.warning(self, "Внимание", f"Неверные данные: {ve}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {e}")

    def delete_store(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления")
            return

        row = selected_rows[0].row()
        id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "Подтверждение", "Удалить эту запись?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_store(id)
                self.load_data()
                self.clear_inputs()
                QMessageBox.information(self, "Успех", "Товар удален")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def clear_inputs(self):
        self.district_input.clear()
        self.address_input.clear()

