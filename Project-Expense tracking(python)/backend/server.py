from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app=FastAPI()
#Pydantic class
class Expense(BaseModel):
    amount:float
    category:str
    notes:str
    
class Daterange(BaseModel):
    start_date:date
    end_date:date



@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expenses(expense_date:date):
    expenses=db_helper.fetch_expenses_for_date(expense_date)
    if expenses is  None:
        raise HTTPException(status_code=500, detail="Failed to retrive expense from database")
    
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date,expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
      db_helper.insert_expense(expense_date,expense.amount,expense.category,expense.notes)
    return {"message:expanse update successfully"}


@app.post("/analytics/")
def get_analytics(date_range: Daterange):
    print(f"Received start_date: {date_range.start_date}, end_date: {date_range.end_date}")
    
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    
    if not data:
        print("No data found for the given date range.")
        raise HTTPException(status_code=500, detail="No expenses found for the given date range.")
    
    total=sum([row['total']for row in data])
    breakdown = {}
    for row in data:
        percentage=(row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']]={
            "total":row['total'],
            "percentage":percentage
        }    
    
    # print(f"Fetched Data: {data}")
    # return data
    return breakdown


@app.get("/expenses/")
def get_monthly_summary():
    try:
        # Fetch monthly summary from the database
        data = db_helper.fetch_monthly_expense_summary()
        
        # If no data is found, return a 404 error
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        
        # Return the data
        return {"data": data}
    
    except Exception as e:
        # Handle and return any errors as a 500 error
        raise HTTPException(status_code=500, detail=str(e))
