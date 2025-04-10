import streamlit as st
import sqlite3
import ollama
import ast
import time

def connect_db():
    return sqlite3.connect('db.sqlite')

def get_user_recent_search(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Browsing_History FROM Customers WHERE Customer_ID = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return ast.literal_eval(result[0]) if result else None

def get_top_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Category, Subcategory FROM Products LIMIT 5")
    products = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    conn.close()
    return products

def get_personalized_suggestion(user_name, recent_search):
    prompt = f"Suggest 3 product categories for {user_name} based on their interest in {recent_search}. Be brief."
    response = ollama.chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': "Short response(max 1 sentences): " + prompt}],
        options={'num_predict': 180}  # Limits long responses
    )
    return response['message']['content']

st.title("🛍️ Smart Shopping Recommender")
st.write("Get product suggestions based on your recent interests!")

user_id = st.text_input("Enter Customer ID:")
user_name = st.text_input("Enter Your Name:")

if st.button("Get Suggestions"):
    if user_id and user_name:
        start_time = time.time()  # Start timing
        recent_search = get_user_recent_search(user_id)
        if recent_search:
            with st.spinner("Fetching your recommendations..."):
                suggestion = get_personalized_suggestion(user_name, recent_search)
            duration = round(time.time() - start_time, 2)  # Stop timing
            st.success(f"Hello {user_name}, based on your interest in {recent_search}, here are some suggestions:")
            st.write(suggestion)
            st.info(f"⏱️ Query completed in {duration} seconds")
        else:
            duration = round(time.time() - start_time, 2)
            st.warning("No recent search data found. Showing top products:")
            top_products = get_top_products()
            st.write(top_products)
            st.info(f"⏱️ Query completed in {duration} seconds")
    else:
        st.error("Please enter both Customer ID and Name.")
