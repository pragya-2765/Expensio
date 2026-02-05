# 💸 Expensio

**Expensio** is a simple and clean **expense tracking web application** built using  
**FastAPI** (backend) and **Streamlit** (frontend).

It allows users to manage daily expenses and view monthly spending summaries with visual insights.

---

## 🚀 Features

- ➕ Add new expenses
- ✏️ Update existing expenses
- ❌ Delete expenses
- 📋 View all expenses in a table
- 📊 Monthly expense summary with chart
- 🗄️ SQLite database (auto-created)

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite
- **Language:** Python

---

## 📁 Project Structure
expensio/
│
├── app.py # Streamlit frontend
├── main.py # FastAPI backend
├── database.py # Database connection & table creation
├── requirements.txt # Project dependencies
└── README.md # Project documentation

---

## ▶️ How to Run Expensio

### Install dependencies
```
pip install -r requirements.txt
```

### Start the FastAPI backend
```
uvicorn main:app --reload
```

### Start the Streamlit frontend
```
streamlit run app.py
```

---

## 🗄️ Database Notes
- SQLite database (expenses.db) is created automatically on startup
- Database file is not committed to GitHub
- Dummy or sample data can be added through the UI

---

## 🔐 Security & Best Practices
- No API keys or secrets are stored in the repository
- Database files are excluded using .gitignore
- Parameterized SQL queries are used to prevent SQL injection

---

## 📌 Future Improvements
- User authentication
- Expense category analytics
- Cloud deployment

