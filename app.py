# app.py

import streamlit as st
from query_generator import generate_sql_from_prompt
from utils import get_db_schema, execute_sql_query, plot_chart

DB_PATH = "chinook.db"

st.set_page_config(layout="wide")
st.title("Text to SQL App")

user_prompt = st.text_input("Ask a question about the database:", "")

if user_prompt:
    with st.spinner("Generating SQL and fetching data..."):
        schema = get_db_schema(DB_PATH)
        sql_query = generate_sql_from_prompt(user_prompt, schema)

        if sql_query.startswith("-- ERROR"):
            st.error(sql_query)
        else:
            st.subheader("🔍 Generated SQL")
            st.code(sql_query, language="sql")

            data = execute_sql_query(DB_PATH, sql_query)

            if data is not None and not data.empty:
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.subheader("📋 Retrieved Data")
                    st.dataframe(data)
                with col2:
                    st.subheader("📊 Visualization")
                    plot_chart(data, user_prompt)
            else:
                st.warning("No data returned or query failed.")
