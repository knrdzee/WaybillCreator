    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QPushButton, QFormLayout, QDialog, \
        QTableWidget, QTableWidgetItem, QDoubleSpinBox, QTextEdit, QMessageBox, QLineEdit
    from PyQt5.QtCore import Qt

    class LoginDialog(QDialog):
        def __init__(self):
            super(LoginDialog, self).__init__()

            self.setWindowTitle('Вход')
            self.setGeometry(300, 300, 300, 150)

            self.init_ui()

        def init_ui(self):
            self.label_username = QLabel('Логин:')
            self.edit_username = QLineEdit(self)

            self.label_password = QLabel('Пароль:')
            self.edit_password = QLineEdit(self)
            self.edit_password.setEchoMode(QLineEdit.Password)

            self.button_login = QPushButton('Войти', self)
            self.button_login.clicked.connect(self.login)

            layout = QVBoxLayout(self)
            layout.addWidget(self.label_username)
            layout.addWidget(self.edit_username)
            layout.addWidget(self.label_password)
            layout.addWidget(self.edit_password)
            layout.addWidget(self.button_login)

        def login(self):
            # Здесь вы можете реализовать проверку логина и пароля
            username = self.edit_username.text()
            password = self.edit_password.text()

            # Пример проверки логина и пароля (замените этот блок на вашу реализацию)
            if username == 'polzovatel' and password == '1':
                self.accept()  # Подтверждаем вход
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль', QMessageBox.Ok)
    class InvoiceApp(QDialog):
        def __init__(self):
            super(InvoiceApp, self).__init__()

            self.setWindowTitle('Создание накладной')
            self.setGeometry(100, 100, 800, 600)

            # Ваши данные о товарах, их ценах, измерениях и адресах магазинов
            self.product_prices = {
                'Молоко': {'price': 50, 'measurement': 'л'},
                'Хлеб': {'price': 25, 'measurement': 'шт'},
                'Яйца': {'price': 90, 'measurement': 'шт'},
                'Картошка': {'price': 30, 'measurement': 'кг'},
                'Масло': {'price': 100, 'measurement': 'шт'},
            }

            self.store_addresses = {
                'Золотой ключик': 'ул.Смирнова',
                'Магазин 2': 'Адрес 2',
                'Магазин 3': 'Адрес 3',
            }

            self.init_ui()

        def init_ui(self):
            self.setStyleSheet("background-color: white;")

            self.store_label = QLabel('Магазин:')
            self.store_edit = QComboBox()
            self.store_edit.addItems(self.store_addresses.keys())
            self.store_edit.currentIndexChanged.connect(self.update_address)

            self.address_label = QLabel('Адрес магазина:')
            self.address_edit = QLabel('')  # Поле для отображения адреса
            self.update_address()  # Установим адрес по умолчанию

            self.warehouse_label = QLabel('Склад:')
            self.warehouse_edit = QComboBox()
            self.warehouse_edit.addItems(['Склад 1', 'Склад 2', 'Склад 3'])

            self.supplier_label = QLabel('Поставщик:')
            self.supplier_edit = QComboBox()
            suppliers = {'Поставщик 1': '123', 'Поставщик 2': '456', 'Поставщик 3': '789'}
            self.supplier_edit.addItems(suppliers.keys())

            self.products_label = QLabel('Товары:')
            self.products_table = QTableWidget()
            self.products_table.setColumnCount(5)
            self.products_table.setHorizontalHeaderLabels(['Товар', 'Цена за единицу', 'Измерение', 'Количество', 'Общая цена'])
            self.add_product_button = QPushButton('Добавить товар')
            self.add_product_button.clicked.connect(self.add_product)

            self.total_label = QLabel('Общая стоимость закупки:')
            self.total_edit = QTextEdit()

            self.save_button = QPushButton('Сохранить накладную')
            self.save_button.clicked.connect(self.save_invoice)

            form_layout = QFormLayout()
            form_layout.addRow(self.store_label, self.store_edit)
            form_layout.addRow(self.address_label, self.address_edit)
            form_layout.addRow(self.warehouse_label, self.warehouse_edit)
            form_layout.addRow(self.supplier_label, self.supplier_edit)

            vbox_layout = QVBoxLayout()
            vbox_layout.addLayout(form_layout)
            vbox_layout.addWidget(self.products_label)
            vbox_layout.addWidget(self.products_table)
            vbox_layout.addWidget(self.add_product_button)
            vbox_layout.addWidget(self.total_label)
            vbox_layout.addWidget(self.total_edit)
            vbox_layout.addWidget(self.save_button)

            self.setLayout(vbox_layout)

        def update_address(self):
            selected_store = self.store_edit.currentText()
            self.address_edit.setText(self.store_addresses.get(selected_store, ''))

        def add_product(self):
            row_position = self.products_table.rowCount()
            self.products_table.insertRow(row_position)

            product_item = QComboBox()
            product_item.addItems(self.product_prices.keys())
            price_item = QLabel('Цена')
            measurement_item = QLabel('Измерение')
            quantity_item = QDoubleSpinBox()
            quantity_item.setSingleStep(1.0)
            quantity_item.setValue(1.0)
            total_item = QLabel('Общая цена')

            product_item.currentIndexChanged.connect(lambda _, r=row_position: self.update_total(r))

            self.products_table.setCellWidget(row_position, 0, product_item)
            self.products_table.setCellWidget(row_position, 1, price_item)
            self.products_table.setCellWidget(row_position, 2, measurement_item)
            self.products_table.setCellWidget(row_position, 3, quantity_item)
            self.products_table.setCellWidget(row_position, 4, total_item)

            self.update_total(row_position)

        def update_total(self, row):
            product_combo = self.products_table.cellWidget(row, 0)
            price_label = self.products_table.cellWidget(row, 1)
            measurement_label = self.products_table.cellWidget(row, 2)
            quantity_spinbox = self.products_table.cellWidget(row, 3)
            total_label = self.products_table.cellWidget(row, 4)

            product_name = product_combo.currentText()
            product_info = self.product_prices.get(product_name, {'price': 0.0, 'measurement': 'ед'})
            price_label.setText(str(product_info['price']))
            measurement_label.setText(product_info['measurement'])
            quantity = quantity_spinbox.value()
            total = quantity * product_info['price']

            total_label.setText(str(total))
            self.calculate_total()

        def calculate_total(self):
            total = 0.0
            items_info = []

            for row in range(self.products_table.rowCount()):
                product_combo = self.products_table.cellWidget(row, 0)
                quantity_spinbox = self.products_table.cellWidget(row, 3)
                price_label = self.products_table.cellWidget(row, 1)
                total_label = self.products_table.cellWidget(row, 4)

                product_name = product_combo.currentText()
                product_info = self.product_prices.get(product_name, {'price': 0.0, 'measurement': 'ед'})
                quantity = quantity_spinbox.value()
                price = float(price_label.text())
                total = quantity * price

                total_label.setText(str(total))
                items_info.append(f"{product_name} - {quantity} {product_info['measurement']} - {total:.2f}")

            total = sum(
                float(self.products_table.cellWidget(row, 4).text()) for row in range(self.products_table.rowCount()))
            self.total_edit.setPlainText(f"Общая стоимость закупки: {total:.2f}\n" + '\n'.join(items_info))

        def save_invoice(self):
            # Здесь вы можете реализовать сохранение накладной в файл или вывод в отдельное окно
            pass


    if __name__ == '__main__':
        app = QApplication(sys.argv)
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            invoice_app = InvoiceApp()
            invoice_app.show()
            sys.exit(app.exec_())
