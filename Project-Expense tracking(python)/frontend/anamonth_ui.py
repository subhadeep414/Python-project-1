import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000/expenses/"

def show_monthly_expense_chart():
    st.title("Monthly Expense Summary")

    try:
        response = requests.get(API_URL)
        # st.write(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # Extract the 'data' field
            data = result.get("data", [])

            if data:
                # Convert to DataFrame
                df = pd.DataFrame(data)

                # Rename columns for clarity
                df = df.rename(columns={"month_name": "Month Name", "total_amount": "Total Amount"})

                # Display DataFrame
                st.dataframe(df)

                # Plotting using Pandas
                fig, ax = plt.subplots(figsize=(8, 5))
                df.plot(kind='bar', x='Month Name', y='Total Amount', ax=ax, color='skyblue', legend=False)

                # Customize the plot
                plt.title("Monthly Expense Summary")
                plt.xlabel("Month Name")
                plt.ylabel("Total Amount")
                plt.xticks(rotation=45)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Display the chart in Streamlit
                st.pyplot(fig)

            else:
                st.error("No data found in the API response.")
        else:
            st.error(f"Failed to fetch data: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Run the function to display the chart
show_monthly_expense_chart()
