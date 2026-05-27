from fastapi import FastAPI
import mysql.connector

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vasu@2004",
    database="track_curd"
)

cursor = db.cursor(dictionary=True)
cursor.execute("""

CREATE TABLE expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    amount FLOAT,
    category VARCHAR(100),
    expense_date DATE
);
""")
db.commit()
# FastAPI App
app = FastAPI()


# -------------------- ADD EXPENSE --------------------

@app.post("/add_exp")
def add_expense(new_data: dict):
    try:
        name = new_data["n"]
        amount = new_data["a"]
        category = new_data["c"]
        expense_date = new_data["d"]

        query = """
            INSERT INTO expenses(name, amount, category, expense_date)
            VALUES (%s, %s, %s, %s)
        """

        values = (name, amount, category, expense_date)

        cursor.execute(query, values)
        db.commit()

        return {
            "message": "Expense Added Successfully"
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------- VIEW EXPENSES --------------------

@app.get("/view_exp")
def view_expenses():
    try:
        query = "SELECT * FROM expenses"

        cursor.execute(query)

        data = cursor.fetchall()

        return data

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------- UPDATE EXPENSE --------------------

@app.put("/upd_exp/{id}")
def update_expense(updated_data: dict, id: int):

    try:
        name = updated_data["n"]
        amount = updated_data["a"]
        category = updated_data["c"]
        expense_date = updated_data["d"]

        query = """
            UPDATE expenses
            SET name=%s,
                amount=%s,
                category=%s,
                expense_date=%s
            WHERE id=%s
        """

        values = (name, amount, category, expense_date, id)

        cursor.execute(query, values)
        db.commit()

        if cursor.rowcount > 0:
            return {
                "message": "Expense Updated Successfully"
            }

        else:
            return {
                "message": "Expense ID Not Found"
            }

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------- DELETE EXPENSE --------------------

@app.delete("/delete_exp/{id}")
def delete_expense(id: int):

    try:
        query = "DELETE FROM expenses WHERE id=%s"

        values = (id,)

        cursor.execute(query, values)
        db.commit()

        if cursor.rowcount > 0:
            return {
                "message": "Expense Deleted Successfully"
            }

        else:
            return {
                "message": "Expense ID Not Found"
            }

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------- SEARCH EXPENSE --------------------

@app.get("/srh_exp/{id}")
def search_expense(id: int):

    try:
        query = "SELECT * FROM expenses WHERE id=%s"

        values = (id,)

        cursor.execute(query, values)

        data = cursor.fetchone()

        if data:
            return data

        else:
            return {
                "message": "Expense ID Not Found"
            }

    except Exception as e:
        return {
            "error": str(e)
        }


# -------------------- SORT EXPENSES --------------------

@app.get("/sort_exp/{sort_by}/{order}")
def sort_expenses(sort_by: str, order: str):

    try:
        valid_columns = [
            "id",
            "name",
            "amount",
            "category",
            "expense_date"
        ]

        if sort_by not in valid_columns:
            return {
                "message": "Invalid Column Name"
            }

        if order.upper() not in ["ASC", "DESC"]:
            return {
                "message": "Invalid Order"
            }

        query = f"""
            SELECT * FROM expenses
            ORDER BY {sort_by} {order.upper()}
        """

        cursor.execute(query)

        data = cursor.fetchall()

        return data

    except Exception as e:
        return {
            "error": str(e)
        }