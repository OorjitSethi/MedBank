import sqlite3

def initialize_db():
    conn = sqlite3.connect('medical_equipment.db')
    c = conn.cursor()

    # Create the equipment table
    c.execute('''CREATE TABLE IF NOT EXISTS equipment (
                 id INTEGER PRIMARY KEY,
                 category TEXT,
                 serial_number TEXT UNIQUE,
                 description TEXT,
                 status TEXT
                 )''')

    # Create the checkout_log table with the person_taking_equipment column
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
    conn.close()

def populate_sample_data():
    conn = sqlite3.connect('medical_equipment.db')
    c = conn.cursor()

    # Define the categories and their respective equipment
    categories = {
        "X-Ray Machine": ["XRM-001", "XRM-002", "XRM-003"],
        "Ultrasound Machine": ["USM-001", "USM-002", "USM-003", "USM-004"],
        "MRI Machine": ["MRIM-001", "MRIM-002", "MRIM-003", "MRIM-004", "MRIM-005"],
        "CT Scanner": ["CTS-001", "CTS-002", "CTS-003", "CTS-004"],
        "Defibrillator": ["DEF-001", "DEF-002", "DEF-003"],
        "Ventilator": ["VNT-001", "VNT-002", "VNT-003", "VNT-004"],
        "Patient Monitor": ["PM-001", "PM-002", "PM-003", "PM-004", "PM-005"],
        "Infusion Pump": ["IP-001", "IP-002", "IP-003", "IP-004", "IP-005", "IP-006"],
        "Surgical Light": ["SL-001", "SL-002", "SL-003"],
        "ECG Machine": ["ECG-001", "ECG-002", "ECG-003"],
        "Anesthesia Machine": ["AM-001", "AM-002", "AM-003"],
        "Blood Pressure Monitor": ["BPM-001", "BPM-002", "BPM-003"],
        "Dialysis Machine": ["DM-001", "DM-002", "DM-003"],
        "Endoscopy System": ["ES-001", "ES-002", "ES-003"],
        "Oxygen Concentrator": ["OC-001", "OC-002", "OC-003"],
        "Pulse Oximeter": ["PO-001", "PO-002", "PO-003"],
        "Nebulizer": ["NEB-001", "NEB-002", "NEB-003"],
        "Syringe Pump": ["SP-001", "SP-002", "SP-003"],
        "Electrosurgical Unit": ["ESU-001", "ESU-002", "ESU-003"],
        "Ophthalmoscope": ["OPH-001", "OPH-002", "OPH-003"],
        "Otoscope": ["OTO-001", "OTO-002", "OTO-003"],
        "Spirometer": ["SPR-001", "SPR-002", "SPR-003"],
        "Suction Machine": ["SM-001", "SM-002", "SM-003"],
        "Laryngoscope": ["LRY-001", "LRY-002", "LRY-003"],
        "Autoclave": ["AUT-001", "AUT-002", "AUT-003"],
        "Dental Chair": ["DC-001", "DC-002", "DC-003"],
        "Microscope": ["MIC-001", "MIC-002", "MIC-003"],
    }

    # Insert each category and its equipment into the database
    for category, serial_numbers in categories.items():
        for serial_number in serial_numbers:
            description = f"{category} with serial number {serial_number}"
            c.execute("INSERT OR IGNORE INTO equipment (category, serial_number, description, status) VALUES (?, ?, ?, ?)",
                      (category, serial_number, description, 'Available'))

    conn.commit()
    conn.close()

# Run the functions to initialize the database and populate it with sample data
initialize_db()
populate_sample_data()
