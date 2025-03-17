import streamlit as st
from datetime import datetime
import requests
from add_update_ui import add_update_tab
from  analytics_ui import analytics_tab
from anamonth_ui import show_monthly_expense_chart

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["ADD/Update", "Analytics by category","Analytics by month"])

with tab1:
   add_update_tab()
with tab2:
    analytics_tab()   
with tab3:
   show_monthly_expense_chart()
       
    
