# Python-project-1

# Expense Management System


This project is an expense management system that consist of a Streamlit frontend application and FastAPI backend server.


## Project Structure

**frontend**:Contains the streamlit application code.
**backend**:Contains the FastAPI backend server code.
**tests**:Contains the test cases for both frontend and backend.
**requirement.txt**:Lists that required python packages.
**README.md**:Provides an instruction for the project.

**Setup Instructions

1. **Clone the repositry**:
   ```bash
   git clone https://github.com/subhadeep414/expense-management-system
   cd expense-management-system
   ```

1. **Install dependencies**:
   ```commandline
   pip install -r requirement.txt
   ```

1.**Run the FastAPI server**:
 
```bash
uvicorn server:app --reload
```
1. **Run the streamlit app**:
    ```commandline
    streamlit run frontend/app.py
    ```
