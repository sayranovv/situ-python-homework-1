import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from goods_window import GoodsWindow
from stores_window import StoresWindow
from movements_window import MovementsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления базой данных")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        btn_goods = QPushButton("Управление товарами")
        btn_goods.clicked.connect(self.open_goods_window)
        layout.addWidget(btn_goods)

        btn_stores = QPushButton("Управление магазинами")
        btn_stores.clicked.connect(self.open_stores_window)
        layout.addWidget(btn_stores)

        btn_movements = QPushButton("Управление движением товаров")
        btn_movements.clicked.connect(self.open_movements_window)
        layout.addWidget(btn_movements)

    def open_goods_window(self):
        self.goods_window = GoodsWindow()
        self.goods_window.show()

    def open_stores_window(self):
        self.stores_window = StoresWindow()
        self.stores_window.show()

    def open_movements_window(self):
        self.movements_window = MovementsWindow()
        self.movements_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())