import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

# st.title("Expense Tracking System")

# tab1, tab2 = st.tabs(["ADD/Update", "Analytics"])

# with tab1:
def add_update_tab():
    selected_date = st.date_input("Enter date", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    
    if response.status_code == 200:
        existing_expense = response.json()
        # st.write(existing_expense)
    else:
        st.error("Failed to fetch expense") 
        existing_expense = [] 
        
    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
    
    with st.form(key="expense_form"):
        col1,col2,col3=st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
                st.text("Category")
        with col3:
                st.text("Notes") 
                
        expenses=[]                   
        for i in range(5):
            if i<len(existing_expense):
                amount=existing_expense[i]['amount']
                category=existing_expense[i]['category']
                notes=existing_expense[i]["notes"]
            else:
                amount=0.0
                category="Shopping"
                notes="Keep shopping"    
                
            col1, col2, col3 = st.columns(3)
            with col1:
               amount_input= st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",label_visibility="collapsed")       
            with col2:
                category_input=st.selectbox(label="Category", options=categories, index=categories.index(category), key=f"category_{i}",label_visibility="collapsed")
            with col3:
                notes_input=notes_input = st.text_input(label="", value=notes, key=f"notes_{i}",label_visibility="collapsed")
        # ✅ Append each expense in the loop
            expenses.append({
            'amount':amount_input,
            'category':category_input,
            'notes':notes_input
            })
        submit = st.form_submit_button()        
        if submit:
            filtered_expenses=[expense for expense in expenses if expense['amount']>0]
            # ✅ Send data to the backend
            response=requests.post(f"{API_URL}/expenses/{selected_date}",json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expense update successfully")
            else:
                st.error("Failed to update expense")    
            pass
