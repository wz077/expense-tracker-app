from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QDate
from etdatabase import fetch_expenses, add_expenses, delete_expenses, sum_expenses

class ExpenseTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUi()
        self.setup_layout()
        self.load_table_data()
        self.apply_styles()
        
    def settings(self):
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        
    def initUi(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Rent", "Food", "Leisure", "Services", "Shopping", "Other"])
        
        self.title = QLineEdit()
        
        self.amount = QLineEdit()
        
        self.description = QLineEdit()
        
        self.btn_add = QPushButton("Add Expense")
        self.btn_add.clicked.connect(self.add_expense)
        
        self.btn_delete = QPushButton("Delete Expense")
        self.btn_delete.clicked.connect(self.delete_expense)
        
        self.btn_sum = QPushButton("Sum Expenses")
        self.btn_sum.clicked.connect(self.show_total_expenses)

        
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Amount", "Date", "Category", "Description"])
        self.table.setColumnWidth(0, 40)
        
    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        
        row1.addWidget(QLabel("Title"))
        row1.addWidget(self.title)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)
        
        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Date"))
        row2.addWidget(self.date_box)
        
        row3.addWidget(QLabel("description"))
        row3.addWidget(self.description)
        row2.addWidget(self.btn_add)
        row2.addWidget(self.btn_delete)
        
        row4.addWidget(self.btn_sum)
        
        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)
        master.addLayout(row4)
        
        self.setLayout(master)
        
    def apply_styles(self):
        self.setStyleSheet("""
                           QWidget {
                                background-color: #f4f6f9;
                                font-family: 'Segoe UI', Arial, sans-serif;
                                font-size: 14px;
                                color: #333333;
                           }
                           
                           QLabel{
                                font-size: 15px;
                                color: #2c3e50;
                                font-weight: 600;
                                padding: 3px;
                               
                           }
                           
                           QLineEdit, QComboBox, QDateEdit{
                               background-color: #ffffff;
                                font-size: 14px;
                                color: #333333;
                                border: 1px solid #cfd8dc;
                                padding: 6px 8px;
                                border-radius: 8px;
                                min-height: 28px;
                               
                           }
                           
                           QLineEdit:hover, QComboBox:hover, QDateEdit:hover{
                               border: 1px solid #3498db;
                               
                           }
                           
                            QLineEdit:focus, QComboBox:focus, QDateEdit:focus{
                               border: 2px solid #2980b9;
                                background-color: #f0f4f8;

                           }
                           
                           QPushButton{
                               background-color: #3498db;
                                color: #ffffff;
                                border: none;
                                border-radius: 8px;
                                padding: 6px 12px;
                                font-weight: 600;
                                min-height: 28px;
                           }
                           
                            QPushButton:hover{
                             background-color: #2980b9;
                            }
                            
                            QPushButton:pressed {
                                background-color: #1c5980;
                            }
                            
                            QTableWidget {
                                background-color: #ffffff;
                                alternate-background-color: #f6f8fa;
                                gridline-color: #dcdcdc;
                                border: 1px solid #cfd8dc;
                                font-size: 14px;
                            }

                            QHeaderView::section {
                                background-color: #3498db;
                                color: white;
                                font-weight: bold;
                                padding: 4px;
                                border: none;
                            }

                            QTableWidget::item {
                                padding: 4px;
                            }
                           
                           """)
    
    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for rowidx, expense in enumerate(expenses):
            self.table.insertRow(rowidx)
            for colidx, data in enumerate(expense):
                item = QTableWidgetItem(str(data))
                
                if colidx != 7:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(rowidx, colidx, item)
                
                
    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.title.clear()
        self.description.clear()
            
    def add_expense(self):
        title = self.title.text().strip()
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text().strip()
        description = self.description.text()
        
        if not title or not amount:
            QMessageBox.warning(self, "Input Error", "Some fields are left empty")
            return
            
        if add_expenses(title, amount, date, category, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")
            
    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"Uh oh","You need to choose a row to delete")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self,
                                       "Confirm",
                                       "Are you sure you want to delete?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()
            
    def show_total_expenses(self):
        total = sum_expenses()
        QMessageBox.information(self, "Total Expenses", f"The total of all expenses is: ${total:.2f}")


    