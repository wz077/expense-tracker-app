import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from etapp import ExpenseTrackerApp
from etdatabase import init_db
from etdatabase import fetch_expenses, add_expenses, delete_expenses, sum_expenses

def main():
    app = QApplication(sys.argv)
    
    if not init_db("db_expenses.db"):
        QMessageBox.critical(None, "Error","Could not load your database!")
        sys.exit(1)
    
    
    window = ExpenseTrackerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    