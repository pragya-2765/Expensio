import streamlit as st
import requests 
from datetime import date
import pandas as pd

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide"
)

def apply_theme(bg_color, sidebar_color, text_color, topbar_color, button_color):
    st.markdown(
        f"""
        <style>
        /* Main background */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_color};
        }}

        section[data-testid="stSidebar"] * {{
            color: {text_color};
        }}

        /* Top bar */
        header[data-testid="stHeader"] {{
            background-color: {topbar_color};
        }}

        /* Buttons */
        .stButton>button {{
            background-color: {button_color};
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }}

        .stButton>button:hover {{
            background-color: #111827;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_theme(
    bg_color="#FFF7FB",
    sidebar_color="#FCE7F3",
    text_color="#374151",
    topbar_color="#FFF7FB",    # pink top bar
    button_color="#FB7185"     # peach buttons
)



st.sidebar.title("💰 Expense Tracker")
st.sidebar.markdown("Track • Analyze • Save")

st.title("💸 Expensio • Expense Analytics")
st.markdown("Manage your expenses smartly and visually 📊")
st.divider()


st.subheader("➕Add a New Expense")
col1, col2= st.columns(2)
with col1:
    amount= st.number_input("💵 Amount", min_value=0.0, step=1.0)
    category= st.text_input("📂 Category (e.g., Food, Travel, Utilities)")
with col2:
    expense_date= st.date_input("📅 Date", value=date.today())
    description= st.text_area("📝 Description (optional)")
if st.button("✅ Add Expense", use_container_width=True):
    payload= {
        "amount": amount,
        "category": category,
        "date": str(expense_date),
        "description": description
    }

    response= requests.post(f"{BACKEND_URL}/add-expense", params=payload, verify=False)
    if response.status_code==200:
        st.success("Expense added successfully! 🎉")
    else:
        st.error("Failed to add expense ❌. Please try again.")
st.divider()
st.subheader("Delete an Expense")
delete_id= st.number_input("Expense ID to delete", min_value=1, step=1)

if st.button("Delete Expense"):
    response= requests.delete(f"{BACKEND_URL}/delete-expense/{delete_id}", verify=False)
    if response.status_code==204:
        st.success("Expense deleted successfully!")
    elif response.status_code==404:
        st.error("Expense not found. Please check the ID and try again.")
    else:
        st.error("Failed to delete expense. Please try again.")
st.divider()
st.subheader("✏️ Update an Expense")
update_id= st.number_input("Expense ID to update", min_value=1, step=1)
new_amount= st.number_input("New Amount", min_value=0.0)
new_category= st.text_input("New Category")
new_date= st.date_input("New Date")
new_description= st.text_area("New Description (optional)")
if st.button("Update Expense"):
    payload= {
        "amount": new_amount,
        "category": new_category,
        "date": str(new_date),
        "description": new_description
    }

    response= requests.put(f"{BACKEND_URL}/update-expense/{update_id}", params=payload, verify=False)
    if response.status_code==200:
        st.success("Expense updated successfully!")
    elif response.status_code==404:
        st.error("Expense not found. Please check the ID and try again.")
    else:
        st.error("Failed to update expense. Please try again.")
st.divider()
st.subheader("📋 All Expenses")

response= requests.get(f"{BACKEND_URL}/expenses", verify=False)
if response.status_code==200:
    expenses= response.json()
    if expenses:
        df= pd.DataFrame(expenses)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expenses found. Start adding some! 📝")
else:
    st.error("Failed to fetch expenses from the backend.")

st.divider()
st.subheader("🗓️ Monthly Expense Summary")
df_summary= pd.DataFrame()
response= requests.get(f"{BACKEND_URL}/monthly-summary")
if response.status_code==200:
    summary= response.json()
    if summary:
        df_summary= pd.DataFrame(summary)
        st.table(df_summary)
    else:
        st.info("No data available for monthly summary.")
    
    st.divider()
    if not df_summary.empty:
        st.bar_chart(df_summary.set_index("month"))
    else:
        st.info("No data available.")
else:

    st.error("Failed to fetch monthly summary from the backend.")

