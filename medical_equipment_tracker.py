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
    except sqlite3.Error as e:
        st.error(f"An error occurred while initializing the database: {e}")
    finally:
        if conn:
            conn.close()

# Load data from the database
def load_data():
    try:
        conn = sqlite3.connect('medical_equipment.db')
        df = pd.read_sql_query("SELECT * FROM equipment", conn)
        return df
    except sqlite3.Error as e:
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
        
        st.write(f"Attempting to check out equipment: {serial_number}")
        print(f"Attempting to check out equipment: {serial_number}")
        st.write(f"Checkout details: {checked_out_by}, {person_taking_equipment}, {contact_number}, {address}, {advance_money}, {duration_days}, {checkout_date}")
        print(f"Checkout details: {checked_out_by}, {person_taking_equipment}, {contact_number}, {address}, {advance_money}, {duration_days}, {checkout_date}")
        
        c.execute("UPDATE equipment SET status='Checked Out' WHERE serial_number=?", (serial_number,))
        c.execute("INSERT INTO checkout_log (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date))
        
        conn.commit()
        st.success(f"Equipment {serial_number} checked out successfully.")
        st.write(f"Equipment {serial_number} checked out successfully.")
        print(f"Equipment {serial_number} checked out successfully.")
        export_logs()
        return True
    except sqlite3.Error as e:
        st.error(f"An error occurred while saving checkout data: {e}")
        st.write(f"Error during checkout: {e}")
        print(f"Error during checkout: {e}")
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
        
        st.write(f"Attempting to check in equipment: {serial_number}")
        print(f"Attempting to check in equipment: {serial_number}")
        
        c.execute("UPDATE equipment SET status='Available' WHERE serial_number=?", (serial_number,))
        c.execute("UPDATE checkout_log SET checkin_time=?, checkin_date=? WHERE serial_number=? AND checkin_time IS NULL",
                  (checkin_time, checkin_date, serial_number))
        
        conn.commit()
        st.success(f"Equipment {serial_number} checked in successfully.")
        st.write(f"Equipment {serial_number} checked in successfully.")
        print(f"Equipment {serial_number} checked in successfully.")
        export_logs()
        return True
    except sqlite3.Error as e:
        st.error(f"An error occurred while saving check-in data: {e}")
        st.write(f"Error during check-in: {e}")
        print(f"Error during check-in: {e}")
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
        st.success("Logs have been exported to equipment_data.xlsx")
    except Exception as e:
        st.error(f"An error occurred while exporting logs: {e}")
    finally:
        if conn:
            conn.close()

# Search functionality
def search_data(df, query):
    if query:
        query = query.lower()
        return df[
            df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        ]
    else:
        return df  # Return the full dataset if no query is provided

# Add new category
def add_new_category(category):
    try:
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                  (category, f"{category[:3].upper()}-001", f"First {category}", 'Available'))
        conn.commit()
        st.success(f"New category '{category}' added successfully.")
        export_logs()
    except sqlite3.Error as e:
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
        st.success(f"New item '{serial_number}' added successfully.")
        export_logs()
    except sqlite3.Error as e:
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
        st.success(f"Description for '{serial_number}' updated successfully.")
        export_logs()
    except sqlite3.Error as e:
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
        st.success(f"Status for '{serial_number}' updated to {new_status}.")
        export_logs()
    except sqlite3.Error as e:
        st.error(f"An error occurred while updating item status: {e}")
    finally:
        if conn:
            conn.close()

# Display the main app interface
def main():
    st.title("Medical Equipment Tracker")

    init_db()
    df = load_data()

    # Admin section
    with st.expander("Admin Section"):
        # Add new category
        new_category = st.text_input("Add New Category")
        if st.button("Add Category"):
            if new_category:
                add_new_category(new_category)
                st.rerun()
            else:
                st.error("Please enter a category name.")

        # Add new item
        categories = df['category'].unique()
        selected_category = st.selectbox("Select Category", categories)
        new_serial_number = st.text_input("New Serial Number")
        new_description = st.text_input("New Description")
        if st.button("Add New Item"):
            if selected_category and new_serial_number and new_description:
                add_new_item(selected_category, new_serial_number, new_description)
                st.rerun()
            else:
                st.error("Please fill in all fields.")

        # Edit item description
        edit_serial_number = st.selectbox("Select Item to Edit", df['serial_number'])
        edit_description = st.text_input("Edit Description", value=df[df['serial_number'] == edit_serial_number]['description'].values[0])
        if st.button("Update Description"):
            edit_item_description(edit_serial_number, edit_description)
            st.rerun()

    search_query = st.text_input("Search Equipment")
    df_filtered = search_data(df, search_query)

    if df_filtered.empty:
        st.warning("No equipment matches your search.")
    else:
        grouped = df_filtered.groupby('category')

        # Display the table with all categories and their respective equipment
        for category, items in grouped:
            available_count = items['status'].value_counts().get('Available', 0)
            with st.expander(f"{category} ({available_count}/{len(items)})", expanded=False):
                for _, row in items.iterrows():
                    st.write(f"**Serial Number:** {row['serial_number']}")
                    st.write(f"**Description:** {row['description']}")
                    
                    if row['status'] != 'Checked Out':
                        status_options = ["Available", "Broken", "Out For Repair", "Useless"]
                        new_status = st.selectbox(f"Status for {row['serial_number']}", status_options, index=status_options.index(row['status']))
                        if new_status != row['status']:
                            update_item_status(row['serial_number'], new_status)
                            st.rerun()
                    else:
                        st.write(f"**Status:** {row['status']}")

                    if row['status'] == 'Available':
                        checkout_form_key = f"checkout_form_{row['serial_number']}"
                        with st.form(checkout_form_key):
                            st.subheader(f"Check Out {row['serial_number']}")
                            checked_out_by = st.selectbox("Checked Out By", ["Vinod Singh"])
                            person_taking_equipment = st.text_input("Person taking equipment")
                            contact_number = st.text_input("Contact Number (10 digits)")
                            address = st.text_area("Address")
                            advance_money = st.number_input("Advance Money", min_value=0)
                            duration_days = st.number_input("Duration (days)", min_value=1)
                            checkout_date = st.date_input("Checkout Date")
                            submit_now = st.form_submit_button("Now")
                            submit = st.form_submit_button("Submit Form")
                            
                            if submit_now:
                                checkout_date = datetime.now().date()
                                submit = True
                            
                            if submit or submit_now:
                                st.write(f"Submit button clicked for {row['serial_number']}")
                                print(f"Submit button clicked for {row['serial_number']}")
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
                                elif advance_money is None or advance_money < 0:
                                    st.error("Please enter a valid advance money amount (0 or greater).")
                                elif duration_days is None or duration_days < 1:
                                    st.error("Please enter a valid duration (1 day or more).")
                                else:
                                    st.write(f"Attempting to save checkout for {row['serial_number']}")
                                    print(f"Attempting to save checkout for {row['serial_number']}")
                                    if save_checkout(row['serial_number'], checked_out_by, person_taking_equipment, contact_number, address, int(advance_money), int(duration_days), checkout_date.strftime("%Y-%m-%d")):
                                        st.write(f"Checkout saved successfully for {row['serial_number']}")
                                        print(f"Checkout saved successfully for {row['serial_number']}")
                                        st.rerun()  # Refresh the page to update status
                                    else:
                                        st.write(f"Failed to save checkout for {row['serial_number']}")
                                        print(f"Failed to save checkout for {row['serial_number']}")

                    elif row['status'] == 'Checked Out':
                        conn = sqlite3.connect('medical_equipment.db')
                        checkout_info = pd.read_sql_query(f"SELECT * FROM checkout_log WHERE serial_number='{row['serial_number']}' AND checkin_time IS NULL", conn)
                        conn.close()
                        
                        if not checkout_info.empty:
                            checkout_row = checkout_info.iloc[0]
                            st.write(f"**Checked Out By:** {checkout_row['checked_out_by']}")
                            st.write(f"**Person Taking Equipment:** {checkout_row.get('person_taking_equipment', 'N/A')}")
                            st.write(f"**Checkout Time:** {checkout_row['checkout_time']}")
                            st.write(f"**Contact Number:** {checkout_row['contact_number']}")
                            st.write(f"**Address:** {checkout_row['address']}")
                            st.write(f"**Advance Money:** {checkout_row['advance_money']}")
                            st.write(f"**Duration (days):** {checkout_row['duration_days']}")
                            st.write(f"**Checkout Date:** {checkout_row['checkout_date']}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Check In {row['serial_number']}", key=f"checkin_{row['serial_number']}"):
                                st.write(f"Check In button clicked for {row['serial_number']}")
                                print(f"Check In button clicked for {row['serial_number']}")
                                checkin_date = datetime.now().date()
                                if save_checkin(row['serial_number'], checkin_date.strftime("%Y-%m-%d")):
                                    st.write(f"Check In successful for {row['serial_number']}")
                                    print(f"Check In successful for {row['serial_number']}")
                                    st.rerun()  # Refresh the page to update status
                                else:
                                    st.write(f"Check In failed for {row['serial_number']}")
                                    print(f"Check In failed for {row['serial_number']}")
                        with col2:
                            if st.button(f"Check Back Out {row['serial_number']}", key=f"checkbackout_{row['serial_number']}"):
                                st.write(f"Check Back Out button clicked for {row['serial_number']}")
                                print(f"Check Back Out button clicked for {row['serial_number']}")
                                with st.form(f"checkbackout_form_{row['serial_number']}"):
                                    checked_out_by = st.selectbox("Checked Out By", ["Vinod Singh"])
                                    contact_number = st.text_input("Contact Number (10 digits)")
                                    address = st.text_area("Address")
                                    advance_money = st.number_input("Advance Money", min_value=0)
                                    duration_days = st.number_input("Duration (days)", min_value=1)
                                    checkout_date = st.date_input("Check-back-out Date")
                                    submit_now = st.form_submit_button("Now")
                                    submit_form = st.form_submit_button("Submit Form")
                                    
                                    if submit_now or submit_form:
                                        st.write(f"Check Back Out form submitted for {row['serial_number']}")
                                        if submit_now:
                                            checkout_date = datetime.now().date()
                                        if not checked_out_by:
                                            st.error("Please select who is checking out the equipment.")
                                        elif not contact_number:
                                            st.error("Please enter a contact number.")
                                        elif not contact_number.isdigit() or len(contact_number) != 10:
                                            st.error("Contact number must be 10 digits long and contain only numbers.")
                                        elif not address:
                                            st.error("Please enter an address.")
                                        elif advance_money is None or advance_money < 0:
                                            st.error("Please enter a valid advance money amount (0 or greater).")
                                        elif duration_days is None or duration_days < 1:
                                            st.error("Please enter a valid duration (1 day or more).")
                                        elif not submit_now and checkout_date == datetime.now().date():
                                            st.error("Please select a check-back-out date.")
                                        elif not any([checked_out_by, contact_number, address, advance_money is not None, duration_days is not None, checkout_date != datetime.now().date()]):
                                            st.error("Please fill out at least one field before submitting.")
                                        else:
                                            if save_checkin(row['serial_number'], datetime.now().strftime("%Y-%m-%d")):  # First check in the equipment
                                                if save_checkout(row['serial_number'], checked_out_by, contact_number, address, int(advance_money), int(duration_days), checkout_date.strftime("%Y-%m-%d")):
                                                    st.rerun()  # Refresh the page to update status

    if st.button("Export Logs to Excel"):
        export_logs()

# Initialize the database and run the app
if __name__ == "__main__":
    main()
