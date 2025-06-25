# utils.py

import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def get_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = ""
    for table_name in tables:
        table = table_name[0]
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        schema += f"Table: {table} Columns: {[col[1] for col in columns]}\n"

    conn.close()
    return schema

def execute_sql_query(db_path, query):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"SQL Execution Error: {e}")
        df = pd.DataFrame()
    conn.close()
    return df

def plot_chart(df, prompt):
    chart_type = None
    prompt_lower = prompt.lower()

    if any(x in prompt_lower for x in ["trend", "over time", "line chart", "daily", "monthly"]):
        chart_type = "line"
    elif any(x in prompt_lower for x in ["distribution", "breakdown", "pie"]):
        chart_type = "pie"
    elif any(x in prompt_lower for x in ["compare", "comparison", "bar"]):
        chart_type = "bar"

    if not chart_type or df.empty or df.shape[1] < 2:
        return None

    fig, ax = plt.subplots()

    try:
        if chart_type == "line":
            df.plot(x=df.columns[0], y=df.columns[1], kind='line', ax=ax)
        elif chart_type == "bar":
            df.plot(x=df.columns[0], y=df.columns[1], kind='bar', ax=ax)
        elif chart_type == "pie":
            df.set_index(df.columns[0])[df.columns[1]].plot.pie(autopct='%1.1f%%', ax=ax)
            ax.set_ylabel("")

        st.pyplot(fig)
    except Exception as e:
        st.warning(f"Chart generation failed: {e}")
