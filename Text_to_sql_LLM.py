from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name SUBSCRIPTION and has the following columns - userid, plan_amount, country, start_date, end_date, and coupon_code \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM SUBSCRIPTION ;
    \nExample 2 - Tell me all the subscription plans greater than 500?, 
    the SQL command will be something like this SELECT * FROM SUBSCRIPTION 
    where plan_amount > 500; 
    also the SQL code should not have ``` in beginning or end and SQL word in output
    """
]

# Streamlit App
st.set_page_config(page_title="Generate Answer From SQL Data Operation")
st.header("Generate Answer From SQL Data Operation")

question = st.text_input("Enter your Prompt here: ", key="input")
submit = st.button("Submit")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("The Response is")
    try:
        data = read_sql_query(response, "subscription.db")
        for row in data:
            st.write(row)  # Displaying the contents of each row
    except sqlite3.Error as e:
        st.error(f"Error accessing the database: {e}")
