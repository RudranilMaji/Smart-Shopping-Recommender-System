import sqlite3
import ollama
import ast

def get_user_recent_search(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT Browsing_History FROM Customers WHERE Customer_ID = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return ast.literal_eval(result[0])
    return None

def get_top_products():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT Category, Subcategory FROM Products LIMIT 5")
    products = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
    conn.close()
    return products

def get_personalized_suggestion(user_name, recent_search):
    prompt = (
        f"Suggest 3 product categories for {user_name} based on their recent interest in {recent_search}. "
        "Be friendly and short."
    )
    response = ollama.chat(
        model='llama2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']