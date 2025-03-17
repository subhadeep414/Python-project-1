import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
from datetime import date

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


# #IT do not print the month name only the month number

# def fetch_monthly_expense_summary():
#     logger.info("fetch_monthly_expense_summary called")
#     with get_db_cursor() as cursor:
#         cursor.execute("""
#             SELECT 
#                 DATE_FORMAT(expense_date, '%Y-%m') AS month,
#                 SUM(amount) AS total_amount
#             FROM expenses
#             GROUP BY month
#             ORDER BY month;
#         """)
#         summary = cursor.fetchall()
#         return summary


def fetch_monthly_expense_summary():
    logger.info("fetch_monthly_expense_summary called for all months")
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                MONTHNAME(expense_date) AS month_name,
                SUM(amount) AS total_amount
            FROM expenses
            GROUP BY month_name
            ORDER BY MIN(expense_date);
        """)
        summary = cursor.fetchall()
        return summary





def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
     # Convert dates to string if needed
    start_date_str = start_date.strftime('%Y-%m-%d') if isinstance(start_date, date) else start_date
    end_date_str = end_date.strftime('%Y-%m-%d') if isinstance(end_date, date) else end_date
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-08-28")
    # print(expenses)
    # # delete_expenses_for_date("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for record in summary:
    #     print(record)

    # summary = fetch_expense_summary("2024-08-01", "2024-08-02")
    # print(summary)

  total = fetch_monthly_expense_summary()
  print(total)
