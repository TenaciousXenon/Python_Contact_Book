# Python_Contact_Book

A simple command-line contact book application written in Python.  
Manage your personal or professional contacts by adding, searching, deleting, and listing them. Contacts are persisted to a JSON file and automatically saved at regular intervals.

## Features

- Add contacts with a unique ID, name, phone number, and email.
- Search for a contact by its ID.
- Delete a contact by its ID.
- List all contacts alphabetically by name.
- Save contacts to a JSON file.
- Load contacts from an existing JSON file on startup.
- Automatic background auto-save every 20 seconds.

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/TenaciousXenon/Python_Contact_Book.git
   cd Python_Contact_Book
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies (none required beyond the Python standard library).

## Usage

Run the script with an optional filename argument. If no filename is provided, you will be prompted to enter one.

```bash
python Project2.py contacts.json
```

### Menu Options

When the application starts, you will see a menu:

```
1. Add contact
2. Search contact
3. Delete contact
4. List all contacts
5. Save and exit
6. Exit without saving
```

- **Add contact**  
  Enter a unique ID, name, phone, and email to add a new contact.
  
- **Search contact**  
  Provide an ID to look up the stored contact details.
  
- **Delete contact**  
  Provide an ID to remove the contact from the address book.
  
- **List all contacts**  
  Displays all contacts sorted alphabetically by name.
  
- **Save and exit**  
  Writes current contacts to the specified JSON file and exits.
  
- **Exit without saving**  
  Quits the application without writing changes to disk.

### Loading Existing Contacts

On startup, you will be asked:
```
Load existing contacts? (y/n):
```
- Enter `y` to load from the provided JSON file (fails gracefully if the file is missing or corrupted).
- Enter `n` to start with an empty contact book.

## Auto-Save

A background thread auto-saves the contact list every 20 seconds if there are any contacts in memory. You will see a message in the console when an autosave occurs.

## Data Storage

Contacts are stored as a JSON object mapping IDs to contact tuples. Example `contacts.json` structure:

```json
{
    "001": ["Alice Smith", "555-1234", "alice@example.com"],
    "002": ["Bob Johnson", "555-5678", "bob@example.com"]
}
```

## Hints & Implementation

- Contacts are kept in a Python dictionary for fast lookup.
- File I/O uses:
  ```python
  with open(filename, 'w') as f:
      json.dump(contacts, f, indent=4)
  ```
- Auto-save is implemented using a daemon `Thread` and `Event` for graceful shutdown.

## Future Improvements

- Add validation for phone numbers and email formats.
- Support updating existing contacts.
- Implement search by name or phone (not just by ID).
- Encrypt the JSON file for privacy.
- Package as a standalone CLI tool with `argparse`.

## License

This project is licensed under the MIT License.  
Feel free to use, modify, and distribute!
