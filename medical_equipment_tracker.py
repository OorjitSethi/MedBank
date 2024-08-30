import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import openpyxl

# Initialize the SQLite database
def init_db():
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS equipment (
                     id INTEGER PRIMARY KEY,
                     category TEXT,
                     serial_number TEXT UNIQUE,
                     description TEXT,
                     status TEXT
                     )''')

        c.execute('''CREATE TABLE IF NOT EXISTS checkout_log (
                     id INTEGER PRIMARY KEY,
                     serial_number TEXT,
                     checked_out_by TEXT,
                     person_taking_equipment TEXT,
                     contact_number TEXT,
                     address TEXT,
                     advance_money INTEGER,
                     duration_days INTEGER,
                     checkout_time TEXT,
                     checkin_time TEXT,
                     checkout_date TEXT,
                     checkin_date TEXT
                     )''')
        
        conn.commit()
        print("Database initialized successfully")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
        st.error(f"An error occurred while initializing the database: {e}")
    finally:
        if conn:
            conn.close()

# Load data from the database
def load_data():
    try:
        conn = sqlite3.connect('medical_equipment.db')
        df = pd.read_sql_query("SELECT * FROM equipment", conn)
        print(f"Data loaded successfully. {len(df)} rows retrieved.")
        return df
    except sqlite3.Error as e:
        print(f"An error occurred while loading data: {e}")
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Save data to the database
def save_checkout(serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_date):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        checkout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Attempting to check out equipment: {serial_number}")
        print(f"Checkout details: {checked_out_by}, {person_taking_equipment}, {contact_number}, {address}, {advance_money}, {duration_days}, {checkout_date}")
        
        c.execute("UPDATE equipment SET status='Checked Out' WHERE serial_number=?", (serial_number,))
        c.execute("INSERT INTO checkout_log (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date))
        
        conn.commit()
        print(f"Equipment {serial_number} checked out successfully.")
        st.success(f"Equipment {serial_number} checked out successfully.")
        export_logs()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while saving checkout data: {e}")
        st.error(f"An error occurred while saving checkout data: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Save check-in to the database
def save_checkin(serial_number, checkin_date):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Attempting to check in equipment: {serial_number}")
        print(f"Check-in date: {checkin_date}")
        
        c.execute("UPDATE equipment SET status='Available' WHERE serial_number=?", (serial_number,))
        c.execute("UPDATE checkout_log SET checkin_time=?, checkin_date=? WHERE serial_number=? AND checkin_time IS NULL",
                  (checkin_time, checkin_date, serial_number))
        
        conn.commit()
        print(f"Equipment {serial_number} checked in successfully.")
        st.success(f"Equipment {serial_number} checked in successfully.")
        export_logs()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while saving check-in data: {e}")
        st.error(f"An error occurred while saving check-in data: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Export logs to Excel
def export_logs():
    try:
        conn = sqlite3.connect('medical_equipment.db')
        df = pd.read_sql_query("SELECT * FROM checkout_log", conn)
        df.to_excel('equipment_data.xlsx', index=False)
        print("Logs have been exported to equipment_data.xlsx")
        st.success("Logs have been exported to equipment_data.xlsx")
    except Exception as e:
        print(f"An error occurred while exporting logs: {e}")
        st.error(f"An error occurred while exporting logs: {e}")
    finally:
        if conn:
            conn.close()

# Search functionality
def search_data(df, query):
    if query:
        query = query.lower()
        filtered_df = df[
            df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        ]
        print(f"Search query: '{query}'. {len(filtered_df)} results found.")
        return filtered_df
    else:
        print("No search query. Returning full dataset.")
        return df  # Return the full dataset if no query is provided

# Add new category
def add_new_category(category):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                  (category, f"{category[:3].upper()}-001", f"First {category}", 'Available'))
        conn.commit()
        print(f"New category '{category}' added successfully.")
        st.success(f"New category '{category}' added successfully.")
        export_logs()
    except sqlite3.Error as e:
        print(f"An error occurred while adding new category: {e}")
        st.error(f"An error occurred while adding new category: {e}")
    finally:
        if conn:
            conn.close()

# Add new item
def add_new_item(category, serial_number, description):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                  (category, serial_number, description, 'Available'))
        conn.commit()
        print(f"New item '{serial_number}' added successfully.")
        st.success(f"New item '{serial_number}' added successfully.")
        export_logs()
    except sqlite3.Error as e:
        print(f"An error occurred while adding new item: {e}")
        st.error(f"An error occurred while adding new item: {e}")
    finally:
        if conn:
            conn.close()

# Edit item description
def edit_item_description(serial_number, new_description):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        c.execute("UPDATE equipment SET description=? WHERE serial_number=?", (new_description, serial_number))
        conn.commit()
        print(f"Description for '{serial_number}' updated successfully.")
        st.success(f"Description for '{serial_number}' updated successfully.")
        export_logs()
    except sqlite3.Error as e:
        print(f"An error occurred while editing item description: {e}")
        st.error(f"An error occurred while editing item description: {e}")
    finally:
        if conn:
            conn.close()

# Update item status
def update_item_status(serial_number, new_status):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        c.execute("UPDATE equipment SET status=? WHERE serial_number=?", (new_status, serial_number))
        conn.commit()
        print(f"Status for '{serial_number}' updated to {new_status}.")
        st.success(f"Status for '{serial_number}' updated to {new_status}.")
        export_logs()
    except sqlite3.Error as e:
        print(f"An error occurred while updating item status: {e}")
        st.error(f"An error occurred while updating item status: {e}")
    finally:
        if conn:
            conn.close()

# Checkout dialog
@st.dialog("Check Out Equipment")
def checkout_dialog(serial_number):
    checked_out_by = st.selectbox("Checked Out By", ["Vinod Singh"])
    person_taking_equipment = st.text_input("Person taking equipment")
    contact_number = st.text_input("Contact Number (10 digits)")
    address = st.text_area("Address")
    advance_money = st.number_input("Advance Money", min_value=0)
    duration_days = st.number_input("Duration (days)", min_value=1)
    checkout_date = st.date_input("Checkout Date")
    
    if st.button("Submit"):
        if not checked_out_by:
            st.error("Please select who is checking out the equipment.")
        elif not person_taking_equipment:
            st.error("Please enter the name of the person taking the equipment.")
        elif not contact_number:
            st.error("Please enter a contact number.")
        elif not contact_number.isdigit() or len(contact_number) != 10:
            st.error("Contact number must be 10 digits long and contain only numbers.")
        elif not address:
            st.error("Please enter an address.")
        elif advance_money < 0:
            st.error("Please enter a valid advance money amount (0 or greater).")
        elif duration_days < 1:
            st.error("Please enter a valid duration (1 day or more).")
        else:
            if save_checkout(serial_number, checked_out_by, person_taking_equipment, contact_number, address, int(advance_money), int(duration_days), checkout_date.strftime("%Y-%m-%d")):
                st.success(f"Equipment {serial_number} checked out successfully.")
                st.rerun()

# Display the main app interface
def main():
    st.title("Medical Equipment Tracker")

    init_db()
    df = load_data()

    # Admin section
    with st.expander("Admin Section"):
        # Add new category
        new_category = st.text_input("Add New Category", key="new_category_input")
        if st.button("Add Category", key="add_category_button"):
            if new_category:
                add_new_category(new_category)
                st.rerun()
            else:
                st.error("Please enter a category name.")

        # Add new item
        categories = df['category'].unique()
        selected_category = st.selectbox("Select Category", categories, key="category_select")
        new_serial_number = st.text_input("New Serial Number", key="new_serial_input")
        new_description = st.text_input("New Description", key="new_description_input")
        if st.button("Add New Item", key="add_item_button"):
            if selected_category and new_serial_number and new_description:
                add_new_item(selected_category, new_serial_number, new_description)
                st.rerun()
            else:
                st.error("Please fill in all fields.")

        # Edit item description
        edit_serial_number = st.selectbox("Select Item to Edit", df['serial_number'], key="edit_item_select")
        edit_description = st.text_input("Edit Description", value=df[df['serial_number'] == edit_serial_number]['description'].values[0], key="edit_description_input")
        if st.button("Update Description", key="update_description_button"):
            edit_item_description(edit_serial_number, edit_description)
            st.rerun()

    search_query = st.text_input("Search Equipment", key="search_input")
    df_filtered = search_data(df, search_query)

    if df_filtered.empty:
        st.warning("No equipment matches your search.")
    else:
        grouped = df_filtered.groupby('category')

        for category, items in grouped:
            available_count = items['status'].value_counts().get('Available', 0)
            with st.expander(f"{category} ({available_count}/{len(items)})", expanded=False):
                for _, row in items.iterrows():
                    st.write(f"**Serial Number:** {row['serial_number']}")
                    st.write(f"**Description:** {row['description']}")

                    if row['status'] == 'Available':
                        if st.button(f"Check Out {row['serial_number']}", key=f"btn_checkout_{row['serial_number']}"):
                            checkout_dialog(row['serial_number'])

                    elif row['status'] == 'Checked Out':
                        if st.button(f"Check In {row['serial_number']}", key=f"btn_checkin_{row['serial_number']}"):
                            print(f"Check-in button clicked for {row['serial_number']}")
                            checkin_date = datetime.now().date()
                            if save_checkin(row['serial_number'], checkin_date.strftime("%Y-%m-%d")):
                                print(f"Check-in successful for {row['serial_number']}")
                                st.success(f"Equipment {row['serial_number']} checked in successfully.")
                                st.rerun()

    if st.button("Export Logs to Excel", key="export_logs_button"):
        print("Export Logs button clicked")
        export_logs()

# Initialize the database and run the app
if __name__ == "__main__":
    print("Starting the Medical Equipment Tracker app")
    main()
