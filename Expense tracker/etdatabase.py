from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_expenses):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_expenses)
    
    if not database.open():
        return False
    
    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS expenses (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Title TEXT,
                   Amount REAL,
                   Category TEXT,
                   Date DATE,
                   Description TEXT
                ) 
               """)
    
    return True

def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        expenses.append([query.value(i) for i in range (6)])
    return expenses

def add_expenses(title, amount, date, category, description):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (Title, Amount, Date, Category, Description)
        VALUES (?, ?, ?, ?, ?)
    """)
    query.addBindValue(title)
    query.addBindValue(amount)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(description)
    return query.exec()


def delete_expenses(id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    
    query.addBindValue(id)
    return query.exec()


def sum_expenses():
    query = QSqlQuery("SELECT SUM(Amount) FROM expenses")
    if query.next():
        total = query.value(0)
        return total if total is not None else 0
    return 0