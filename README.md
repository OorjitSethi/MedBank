# Medical Equipment Tracker

The **Medical Equipment Tracker** is a Streamlit-based web application designed to manage and track the availability of medical equipment. The application allows administrators to add and manage equipment categories and items, check out and check in items, and keep a detailed log of all transactions. The application also includes search functionality and the ability to export logs to an Excel file.

## Features

### 1. **Equipment Management by Serial Number**
   - Track equipment using unique serial numbers.
   - Manage and monitor individual items within each category.

### 2. **Admin Section**
   - **Add New Category**: Add new equipment categories. An initial item with a default serial number and description is automatically created.
   - **Add New Item**: Add new items to existing categories, specifying the serial number and description.
   - **Edit Item Description**: Edit the description of existing equipment items.
   - **Update Item Status**: Change the status of items (e.g., Available, Broken, Out For Repair, Useless).

### 3. **Check Out/Check In Equipment**
   - **Check Out**: Fill in the required details (person checking out, contact number, address, advance money, duration, checkout date) to check out available items.
   - **Check In**: Record the check-in date and update the item's status to "Available".
   - **Check Back Out**: Items that have been checked in can be checked back out immediately.

### 4. **Search Functionality**
   - Search for equipment by category, serial number, description, or status.
   - The search results dynamically update the display.

### 5. **Detailed Checkout Logs**
   - View detailed information for each checked-out item, including the person who checked it out, checkout time, contact number, address, advance money, duration, and checkout date.
   - Export checkout and check-in logs to an Excel file.

### 6. **Automatic Status Refresh**
   - The app automatically refreshes after performing actions such as checkout, check-in, or status updates to reflect the latest status.

### 7. **Error Handling**
   - The app includes error handling to catch and display errors related to database operations.

## Installation

To run the Medical Equipment Tracker application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/medical-equipment-tracker.git
   cd medical-equipment-tracker
