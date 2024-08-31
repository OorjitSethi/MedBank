# Medical Equipment Tracker

The **Medical Equipment Tracker** is a web application built using Streamlit that allows users to manage and track medical equipment within an organization. The application provides features for checking equipment in and out, adding new equipment and categories, updating equipment status, and exporting logs to Excel for further analysis.

**The app is accessible through the link: [medbankfoundation.streamlit.app](https://medbankfoundation.streamlit.app)**

## Features

- **Equipment Management**: Add, edit, and manage equipment and their categories.
- **Check-out and Check-in**: Track who checks out equipment, manage check-in details, and update statuses accordingly.
- **Search Functionality**: Search for equipment by serial number, category, or other attributes.
- **Export Logs**: Export equipment check-out and check-in logs to Excel format for external use.
- **User Interface**: User-friendly web interface powered by Streamlit for ease of use.

## Usage

### Admin Section

- **Add New Category**: Enter a new category name in the "Add New Category" input field and click "Add Category" to create a new equipment category.
- **Add New Item**: Select a category, enter the serial number and description for the new equipment, and click "Add New Item."
- **Edit Item Description**: Choose an existing item from the list and update its description as needed.
- **Update Item Status**: Select an equipment status (Available, Broken, Out for Repair) and update its current state.

### Equipment Check-out and Check-in

- **Check-Out Equipment**: Select "Check Out" for an available item, fill in the required details (person, contact number, etc.), and submit.
- **Check-In Equipment**: For items that are currently checked out, click "Check In" and provide necessary details to log the check-in event.
- **View Checkout Details**: For checked-out items, click "View Details" to see more information about the checkout.

### Export Logs

To export the equipment logs to an Excel file, click the "Export Logs to Excel" button. The logs will be saved as `equipment_data.xlsx`.

## Database Schema

The application uses an SQLite database with two primary tables:

### `equipment` Table:

- `id`: INTEGER PRIMARY KEY
- `category`: TEXT
- `serial_number`: TEXT (UNIQUE)
- `description`: TEXT
- `status`: TEXT

### `checkout_log` Table:

- `id`: INTEGER PRIMARY KEY
- `serial_number`: TEXT
- `checked_out_by`: TEXT
- `person_taking_equipment`: TEXT
- `contact_number`: TEXT
- `address`: TEXT
- `advance_money`: INTEGER
- `duration_days`: INTEGER
- `checkout_time`: TEXT
- `checkin_time`: TEXT
- `checkout_date`: TEXT
- `checkin_date`: TEXT

## Error Handling

The application includes error handling for database operations and provides user-friendly messages when issues arise, such as database connection failures or input validation errors.

## Contributing

If you would like to contribute to the Medical Equipment Tracker, please follow these guidelines:

1. Fork the repository and create your feature branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

2. Commit your changes:

   ```bash
   git commit -m 'Add new feature'
   ```

3. Push to the branch:

   ```bash
   git push origin feature/YourFeature
   ```

4. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed using Streamlit for the user interface.
- SQLite for managing data persistence.
- OpenPyXL for exporting data to Excel.
