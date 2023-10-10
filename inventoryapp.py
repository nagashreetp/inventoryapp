import streamlit as st
import sqlite3
import random
import string

# Create a connection to the SQLite database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, stock_on_hand INTEGER)''')

def generate_random_product_name():
    # Generate a random alphanumeric product name (e.g., Item 1, Item 2, ...)
    return 'Item ' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

def generate_random_stock_on_hand():
    # Generate a random stock on hand value between 20 and 50
    return random.randint(20, 50)

def insert_initial_data():
    # Insert 50 initial records into the database
    for _ in range(50):
        product_name = generate_random_product_name()
        stock_on_hand = generate_random_stock_on_hand()
        c.execute("INSERT INTO inventory (product_name, stock_on_hand) VALUES (?, ?)", (product_name, stock_on_hand))
        conn.commit()

def sort_inventory_by_product_name():
    # Sort the inventory by product_name in ascending order
    return c.execute("SELECT * FROM inventory ORDER BY product_name ASC").fetchall()

def sort_inventory_by_stock_on_hand():
    # Sort the inventory by stock_on_hand in descending order
    return c.execute("SELECT * FROM inventory ORDER BY stock_on_hand DESC").fetchall()

def update_inventory_subtract_2():
    # Update every product's stock_on_hand by subtracting 2
    c.execute("UPDATE inventory SET stock_on_hand = stock_on_hand - 2")
    conn.commit()

def update_inventory_add_2_to_even():
    # Update stock_on_hand of Product_Name ending in even number by adding 2
    c.execute("UPDATE inventory SET stock_on_hand = stock_on_hand + 2 WHERE product_name LIKE '%[02468]'")
    conn.commit()

# Initialize the database with initial data
insert_initial_data()

# Streamlit app
st.title('Inventory Management App')

# Button 1: Sort ascending by Product_Name
if st.button('Sort Ascending by Product Name'):
    sorted_inventory = sort_inventory_by_product_name()
    st.write(sorted_inventory)

# Button 2: Sort descending by Stock_On_Hand
if st.button('Sort Descending by Stock On Hand'):
    sorted_inventory = sort_inventory_by_stock_on_hand()
    st.write(sorted_inventory)

# Button 3: Every Product_Name, Stock_On_Hand should reduce by 2
if st.button('Reduce Stock On Hand by 2'):
    update_inventory_subtract_2()
    st.write("Stock On Hand reduced by 2 for all products.")

# Button 4: Stock_On_Hand of Product_Name ending in even number should increase by 2
if st.button('Increase Stock On Hand for Even-Ending Products by 2'):
    update_inventory_add_2_to_even()
    st.write("Stock On Hand increased by 2 for products with even-ending names.")

# Close the database connection
conn.close()

