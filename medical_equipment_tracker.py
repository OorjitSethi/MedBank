# Import necessary libraries
import streamlit as st  # For creating the web application interface
import sqlite3  # For database operations
import pandas as pd  # For data manipulation and analysis
from datetime import datetime  # For handling date and time
import openpyxl  # For exporting data to Excel

st.set_page_config(layout="wide")

# Function to initialize the SQLite database
def init_db():
    try:
        # Establish a connection to the database (creates it if it doesn't exist)
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()

        # Create 'equipment' table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS equipment (
                     id INTEGER PRIMARY KEY,
                     category TEXT,
                     serial_number TEXT UNIQUE,
                     description TEXT,
                     status TEXT
                     )''')

        # Create 'checkout_log' table if it doesn't exist
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
        
        # Commit the changes to the database
        conn.commit()
        print("Database initialized successfully")
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur during initialization
        print(f"An error occurred while initializing the database: {e}")
        st.error(f"An error occurred while initializing the database: {e}")
    finally:
        # Ensure the database connection is closed, even if an error occurred
        if conn:
            conn.close()

# Function to load data from the database
def load_data():
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        # Read all data from the 'equipment' table into a pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM equipment", conn)
        print(f"Data loaded successfully. {len(df)} rows retrieved.")
        return df
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur during data loading
        print(f"An error occurred while loading data: {e}")
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to save checkout information to the database
def save_checkout(serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_date):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Get the current date and time for the checkout
        checkout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log the checkout attempt
        print(f"Attempting to check out equipment: {serial_number}")
        print(f"Checkout details: {checked_out_by}, {person_taking_equipment}, {contact_number}, {address}, {advance_money}, {duration_days}, {checkout_date}")
        
        # Update the equipment status to 'Checked Out'
        c.execute("UPDATE equipment SET status='Checked Out' WHERE serial_number=?", (serial_number,))
        # Insert a new record into the checkout_log table
        c.execute("INSERT INTO checkout_log (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (serial_number, checked_out_by, person_taking_equipment, contact_number, address, advance_money, duration_days, checkout_time, checkout_date))
        
        # Commit the changes to the database
        conn.commit()
        print(f"Equipment {serial_number} checked out successfully.")
        st.success(f"Equipment {serial_number} checked out successfully.")
        # Export the updated logs to Excel
        export_logs()
        return True
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur during the checkout process
        print(f"An error occurred while saving checkout data: {e}")
        st.error(f"An error occurred while saving checkout data: {e}")
        return False
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to save check-in information to the database
def save_checkin(serial_number, checkin_date):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Get the current date and time for the check-in
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log the check-in attempt
        print(f"Attempting to check in equipment: {serial_number}")
        print(f"Check-in date: {checkin_date}")
        
        # Update the equipment status to 'Available'
        c.execute("UPDATE equipment SET status='Available' WHERE serial_number=?", (serial_number,))
        # Update the checkout_log with the check-in information
        c.execute("UPDATE checkout_log SET checkin_time=?, checkin_date=? WHERE serial_number=? AND checkin_time IS NULL",
                  (checkin_time, checkin_date, serial_number))
        
        # Commit the changes to the database
        conn.commit()
        print(f"Equipment {serial_number} checked in successfully.")
        st.success(f"Equipment {serial_number} checked in successfully.")
        # Export the updated logs to Excel
        export_logs()
        return True
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur during the check-in process
        print(f"An error occurred while saving check-in data: {e}")
        st.error(f"An error occurred while saving check-in data: {e}")
        return False
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to export logs to an Excel file
def export_logs():
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        # Read all data from the 'checkout_log' table into a pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM checkout_log", conn)
        # Export the DataFrame to an Excel file
        df.to_excel('equipment_data.xlsx', index=False)
        print("Logs have been exported to equipment_data.xlsx")
        st.success("Logs have been exported to equipment_data.xlsx")
    except Exception as e:
        # Handle any errors that occur during the export process
        print(f"An error occurred while exporting logs: {e}")
        st.error(f"An error occurred while exporting logs: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to search for equipment based on a query
def search_data(df, query):
    if query:
        # Convert the query to lowercase for case-insensitive search
        query = query.lower()
        # Filter the DataFrame based on the search query
        filtered_df = df[
            df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        ]
        print(f"Search query: '{query}'. {len(filtered_df)} results found.")
        return filtered_df
    else:
        # If no query is provided, return the full dataset
        print("No search query. Returning full dataset.")
        return df

# Function to add a new category to the database
def add_new_category(category):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Insert a new category with a default item
        c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                  (category, f"{category[:3].upper()}-001", f"First {category}", 'Available'))
        # Commit the changes to the database
        conn.commit()
        print(f"New category '{category}' added successfully.")
        st.success(f"New category '{category}' added successfully.")
        # Export the updated logs to Excel
        export_logs()
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur while adding a new category
        print(f"An error occurred while adding new category: {e}")
        st.error(f"An error occurred while adding new category: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to add a new item to the database
def add_new_item(category, serial_number, description):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Insert a new item into the equipment table
        c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                  (category, serial_number, description, 'Available'))
        # Commit the changes to the database
        conn.commit()
        print(f"New item '{serial_number}' added successfully.")
        st.success(f"New item '{serial_number}' added successfully.")
        # Export the updated logs to Excel
        export_logs()
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur while adding a new item
        print(f"An error occurred while adding new item: {e}")
        st.error(f"An error occurred while adding new item: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to edit the description of an existing item
def edit_item_description(serial_number, new_description):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Update the description of the specified item
        c.execute("UPDATE equipment SET description=? WHERE serial_number=?", (new_description, serial_number))
        # Commit the changes to the database
        conn.commit()
        print(f"Description for '{serial_number}' updated successfully.")
        st.success(f"Description for '{serial_number}' updated successfully.")
        # Export the updated logs to Excel
        export_logs()
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur while editing the item description
        print(f"An error occurred while editing item description: {e}")
        st.error(f"An error occurred while editing item description: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Function to update the status of an existing item
def update_item_status(serial_number, new_status):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Update the status of the specified item
        c.execute("UPDATE equipment SET status=? WHERE serial_number=?", (new_status, serial_number))
        # Commit the changes to the database
        conn.commit()
        print(f"Status for '{serial_number}' updated to {new_status}.")
        st.success(f"Status for '{serial_number}' updated to {new_status}.")
        # Export the updated logs to Excel
        export_logs()
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur while updating the item status
        print(f"An error occurred while updating item status: {e}")
        st.error(f"An error occurred while updating item status: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Streamlit dialog for checking out equipment
@st.dialog("Check Out Equipment")
def checkout_dialog(serial_number):
    # Create input fields for checkout information
    checked_out_by = st.selectbox("Checked Out By", ["Vinod Singh"])
    person_taking_equipment = st.text_input("Person taking equipment")
    contact_number = st.text_input("Contact Number (10 digits)")
    address = st.text_area("Address")
    advance_money = st.number_input("Advance Money", min_value=0)
    duration_days = st.number_input("Duration (days)", min_value=1)
    checkout_date = st.date_input("Checkout Date")
    
    # Handle form submission
    if st.button("Submit"):
        # Validate input fields
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
            # If all validations pass, save the checkout information
            if save_checkout(serial_number, checked_out_by, person_taking_equipment, contact_number, address, int(advance_money), int(duration_days), checkout_date.strftime("%Y-%m-%d")):
                st.success(f"Equipment {serial_number} checked out successfully.", icon="✅")
                st.rerun()

# Streamlit dialog for viewing checkout details
@st.dialog("View Checkout Details")
def view_details_dialog(serial_number):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('medical_equipment.db')
        c = conn.cursor()
        # Fetch the checkout details for the specified serial number
        c.execute("SELECT * FROM checkout_log WHERE serial_number=? AND checkin_time IS NULL", (serial_number,))
        details = c.fetchone()
        if details:
            # Display the checkout details if found
            st.write(f"**Serial Number:** {details[1]}")
            st.write(f"**Checked Out By:** {details[2]}")
            st.write(f"**Person Taking Equipment:** {details[3]}")
            st.write(f"**Contact Number:** {details[4]}")
            st.write(f"**Address:** {details[5]}")
            st.write(f"**Advance Money:** {details[6]}")
            st.write(f"**Duration (days):** {details[7]}")
            st.write(f"**Checkout Time:** {details[8]}")
            st.write(f"**Checkout Date:** {details[10]}")
        else:
            # Display an error if no active checkout is found
            st.error("No active checkout found for this equipment.")
    except sqlite3.Error as e:
        # Handle any SQLite errors that occur while fetching checkout details
        print(f"An error occurred while fetching checkout details: {e}")
        st.error(f"An error occurred while fetching checkout details: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            conn.close()

# Main function to display the Streamlit app interface
def main():
    # Set the title of the Streamlit app
    st.title("Medical Equipment Tracker")

    # Initialize the database
    init_db()
    # Load data from the database
    df = load_data()

    # Admin section (expandable)
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
                # Add actual description for each category
                category_descriptions = {
                    "ventilator": "Machines that provide mechanical ventilation by moving breathable air into and out of the lungs.",
                    "defibrillator": "Devices that deliver a dose of electric current to the heart to treat life-threatening cardiac dysrhythmias.",
                    "ecg machine": "Devices that record the electrical activity of the heart over a period of time.",
                    "infusion pump": "Devices that deliver fluids, such as nutrients and medications, into a patient's body in controlled amounts.",
                    "patient monitor": "Devices that continuously measure and display vital signs such as heart rate, blood pressure, and oxygen saturation.",
                    "syringe pump": "Devices that deliver small amounts of fluids at a controlled rate, often used for medications.",
                    "oxygen concentrator": "Devices that concentrate oxygen from ambient air and deliver it to patients requiring oxygen therapy.",
                    "suction machine": "Devices that remove substances such as blood, saliva, mucus, and vomit from a person's airway.",
                    "nebulizer": "Devices that convert liquid medication into a mist to be inhaled into the lungs.",
                    "ultrasound machine": "Devices that use high-frequency sound waves to create images of the inside of the body.",
                    "x-ray machine": "Devices that use X-rays to create images of the inside of the body, primarily for diagnostic purposes.",
                    "ct scanner": "Devices that use computer-processed combinations of X-ray measurements to produce cross-sectional images of specific areas of the body.",
                    "mri machine": "Devices that use strong magnetic fields and radio waves to generate detailed images of the organs and tissues in the body.",
                    "anesthesia machine": "Devices that deliver a precisely known but variable gas mixture, including anesthetizing and life-sustaining gases.",
                    "surgical light": "Devices that provide illumination in the operating room during surgical procedures.",
                    "autoclave": "Devices that use steam to sterilize equipment and other objects, ensuring that all bacteria, viruses, fungi, and spores are inactivated.",
                    "sterilizer": "Devices that eliminate all forms of life, including transmissible agents such as fungi, bacteria, viruses, spore forms, etc., from a surface, equipment, or medium.",
                    "dialysis machine": "Devices that remove waste products and excess fluid from the blood when the kidneys stop working properly.",
                    "incubator": "Devices that provide a controlled environment for the care and protection of premature or sick newborns.",
                    "ventilator accessory": "Various components and attachments used in conjunction with ventilators to ensure proper functioning and patient care.",
                    "defibrillator accessory": "Various components and attachments used in conjunction with defibrillators to ensure proper functioning and patient care.",
                    "ecg accessory": "Various components and attachments used in conjunction with ECG machines to ensure proper functioning and patient care.",
                    "infusion pump accessory": "Various components and attachments used in conjunction with infusion pumps to ensure proper functioning and patient care.",
                    "patient monitor accessory": "Various components and attachments used in conjunction with patient monitors to ensure proper functioning and patient care.",
                    "blood pressure monitor": "Devices that measure blood pressure, typically consisting of an inflatable cuff to collapse and then release the artery under the cuff in a controlled manner."
                }
                
                # Display the category description once
                normalized_category = category.strip().lower()
                category_description = next((desc for key, desc in category_descriptions.items() if key.lower() == normalized_category), f"Description for {category}")
                st.markdown(f"**Description:** <span style='font-size: 1.05em;'>{category_description}</span>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
                with col1:
                    st.write("**Serial No.**")
                with col2:
                    st.write("**Status**")
                with col3:
                    st.write("**Check Out/In**")
                with col4:
                    st.write("**View Details**")
                
                for _, row in items.iterrows():
                    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
                    with col1:
                        st.write(f"{row['serial_number']}")
                    with col2:
                        if row['status'] != 'Checked Out':
                            status_options = ['Available', 'Broken', 'Out for Repair']
                            new_status = st.selectbox(
                                "Status",
                                options=status_options,
                                index=status_options.index(row['status']) if row['status'] in status_options else 0,
                                key=f"status_{row['serial_number']}",
                                label_visibility="collapsed"
                            )
                            if new_status != row['status']:
                                if update_item_status(row['serial_number'], new_status):
                                    row['status'] = new_status  # Update the status in the current row
                                    st.rerun()  # Reload the website
                        else:
                            st.write(f"{row['status']}")
                    with col3:
                        if row['status'] == 'Available':
                            if st.button(f"Check Out", key=f"btn_checkout_{row['serial_number']}"):
                                checkout_dialog(row['serial_number'])
                                st.rerun()
                        elif row['status'] == 'Checked Out':
                            if st.button(f"Check In", key=f"btn_checkin_{row['serial_number']}"):
                                print(f"Check-in button clicked for {row['serial_number']}")
                                checkin_date = datetime.now().date()
                                if save_checkin(row['serial_number'], checkin_date.strftime("%Y-%m-%d")):
                                    print(f"Check-in successful for {row['serial_number']}")
                                    st.success(f"Equipment {row['serial_number']} checked in successfully.")
                                    st.rerun()
                        else:
                            st.write("-")
                    with col4:
                        if row['status'] == 'Checked Out':
                            if st.button(f"View Details", key=f"btn_view_details_{row['serial_number']}"):
                                view_details_dialog(row['serial_number'])
                        else:
                            st.write("-")

    if st.button("Export Logs to Excel", key="export_logs_button"):
        print("Export Logs button clicked")
        export_logs()
        st.rerun()

# Initialize the database and run the app
if __name__ == "__main__":
    print("Starting the Medical Equipment Tracker app")
    main()
