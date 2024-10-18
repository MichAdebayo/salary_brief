import streamlit as st
import pandas as pd


df = pd.read_csv("salary_statistics_streamlit.csv")

# Sidebar for user interaction
st.sidebar.title("Salary Viewer")

# Select company to view salaries
company = st.sidebar.selectbox("Select a company", ["ProjectLead", "DesignWorks", "TechCorp"])
filtered_df = df[df['Company'] == company]

# Display employees of the selected company
st.write(f"Employees in {company}:")
st.table(filtered_df[['Employee', 'Job', 'Salary']])

# Search for an employee
st.sidebar.write("Search for an Employee")
employee_name = st.sidebar.text_input("Enter employee name:")
if employee_name:
    search_results = df[df['Employee'].str.contains(employee_name, case=False)]
    st.write(f"Search Results for {employee_name}:")
    if search_results.empty:
        st.write("No employees found.")
    else:
        st.table(search_results[['Employee', 'Job', 'Salary', 'Company']])

# Show statistics
if st.sidebar.button("Show Salary Statistics"):
    st.write("Salary Statistics:")
    st.write(f"Average Salary: {df['Salary'].mean():.2f}€")
    st.write(f"Highest Salary: {df['Salary'].max():.2f}€")
    st.write(f"Lowest Salary: {df['Salary'].min():.2f}€")
