from fastapi import FastAPI, status, HTTPException
from database import create_table, get_db_connection

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_table()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}

@app.post("/add-expense")
def add_expense(amount:float, category:str, date:str, description:str=None):
    conn= get_db_connection()
    cursor=conn.cursor()
    cursor.execute('''
                   INSERT INTO EXPENSES (amount, category, date, description)
                   VALUES (?,?,?,?)
                   ''', 
                   (amount, category, date, description)
                   )
    conn.commit()
    conn.close()
    return {"status_code": 201, "message": "Expense added successfully."}

@app.get("/expenses")
def get_expenses():
    conn= get_db_connection()
    cursor= conn.cursor()
    cursor.execute('SELECT*FROM expenses')
    rows= cursor.fetchall()
    expenses= []
    for row in rows:
        expenses.append({
            "id": row["id"],
            "amount": row["amount"],
            "category": row["category"],
            "date": row["date"],
            "description": row["description"]
        })
    
    return {"status_code":200, "expenses": expenses}

@app.delete("/delete-expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id:int):
    conn= get_db_connection()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id= ?", (expense_id,))
    conn.commit()

    if cursor.rowcount==0:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found.")
    
    conn.close()

@app.put("/update-expense/{expense_id}")
def update_expense(
    expense_id:int,
    amount: float,
    category: str,
    date: str,
    description:str=None
):
    conn= get_db_connection()
    cursor= conn.cursor()
    cursor.execute('''
                   UPDATE expenses
                   SET amount=?, category=?, date=?, description=?
                   WHERE id=?
                   ''',
                   (amount, category, date, description, expense_id)
                   )
    conn.commit()

    if cursor.rowcount==0:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found.")
    
    conn.close()
    return {"status_code": 200, "message": "Expense updated successfully."}

@app.get("/monthly-summary")
def monthly_summary():
    conn= get_db_connection()
    cursor= conn.cursor()
    cursor.execute("""
                   SELECT substr(date, 1, 7) AS month, SUM(amount) as total
                   FROM expenses
                   GROUP BY month
                   """)
    data= cursor.fetchall()
    conn.close()
    return [
        {"month": row["month"], "total": row["total"]} 
        for row in data
    ]