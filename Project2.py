"""
Goal: Create a command-line contact book that lets users:
Uses ID
Add, search, and delete contacts (name, phone, email).
List all contacts alphabetically.
Save contacts to a file and load them on startup.
Hints:
Use lists/dictionaries for storage.
Use file I/O (with open() as f) for persistence.
"""
import json
import sys
import time
from threading import Thread, Event

#add contact tuples of (name, phone, email)
def add(ID, name, phone, email, gen_dict):
    gen_dict[ID] = (name, phone, email)

#search contact and display name, phone, email, maybe do a try and except if it fails
def search(ID, gen_dict):
    try:
        name, phone, email = gen_dict[ID]
        return f"{name} {phone} {email}"
    except KeyError:
        return -1

#delete contact based on ID
def delete(ID, gen_dict):
    if ID not in gen_dict:
        return -1  
    del gen_dict[ID]
    return 0

#print current dictionary into a text file
def save(filename, gen_dict):
    try:
        with open(filename, 'w') as file:
            json.dump(gen_dict, file, indent=4)
        return 0
    except (IOError, TypeError):
        return -1

#loads json files and uploads the json into the dict
def load(filename, gen_dict):
    try:
        with open(filename) as file:
            data = json.load(file)
        gen_dict.clear()
        for ID, contact in data.items():
            gen_dict[ID] = tuple(contact)
        return 0
    except (IOError, json.JSONDecodeError, ValueError):
        gen_dict.clear()
        return -1

#list the dict in a readable way.
def list_contacts(gen_dict):
    """List all contacts alphabetically by name."""
    if not gen_dict:
        print("No contacts found.")
        return
    
    # Sort by name (element 0 of the tuple)
    sorted_contacts = sorted(gen_dict.items(), key=lambda x: x[1][0].lower())
    
    print("\n--- Contacts ---")
    for ID, (name, phone, email) in sorted_contacts:
        print(f"ID: {ID} | Name: {name} | Phone: {phone} | Email: {email}")
    print("----------------\n")

#autosave after 20 secopnds (set up only in main)
def autosave_worker(filename, gen_dict, stop_event, interval=20):
    """Background thread that auto-saves every 'interval' seconds."""
    while not stop_event.is_set():
        time.sleep(interval)
        if gen_dict:  # Only save if there are contacts
            if save(filename, gen_dict) == 0:
                print(f"\n(Autosaved contacts to {filename})")
            else:
                print("\nError during autosave!")

def main():
    print("\n=== Welcome to Contact Book ===")
    contacts = {}  # Initialize empty dictionary
    
    # Get filename from user
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"Using filename: {filename}")
    else:
        filename = input("Enter filename for contacts (e.g., contacts.json): ").strip()
    
    # Try to load existing file
    if input("Load existing contacts? (y/n): ").lower() == 'y':
        if load(filename, contacts) == -1:
            print("No existing file found, starting with empty contacts.")
        else:
            print(f"Loaded {len(contacts)} contacts from {filename}")
    
    # Start autosave thread
    stop_event = Event()
    autosave_thread = Thread(target=autosave_worker, args=(filename, contacts, stop_event))
    autosave_thread.daemon = True
    autosave_thread.start()
    
    # Main menu loop
    while True:
        print("\nMenu:")
        print("1. Add contact")
        print("2. Search contact")
        print("3. Delete contact")
        print("4. List all contacts")
        print("5. Save and exit")
        print("6. Exit without saving")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == '1':  # Add
            ID = input("Enter ID: ").strip()
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()
            add(ID, name, phone, email, contacts)
            print("Contact added.")
            
        elif choice == '2':  # Search
            ID = input("Enter ID to search: ").strip()
            result = search(ID, contacts)
            if result == -1:
                print("Contact not found.")
            else:
                print("Contact found:", result)
                
        elif choice == '3':  # Delete
            ID = input("Enter ID to delete: ").strip()
            result = delete(ID, contacts)
            if result == -1:
                print("Contact not found.")
            else:
                print("Contact deleted.")
                
        elif choice == '4':  # List
            list_contacts(contacts)
            
        elif choice == '5':  # Save and exit
            if save(filename, contacts) == 0:
                print(f"Contacts saved to {filename}")
            else:
                print("Error saving contacts!")
            stop_event.set()
            break
            
        elif choice == '6':  # Exit without saving
            if input("Are you sure? Unsaved changes will be lost (y/n): ").lower() == 'y':
                stop_event.set()
                break
                
        else:
            print("Invalid choice. Please enter 1-6.")

    autosave_thread.join(timeout=1)
    print("\nGoodbye!\n")

if __name__ == "__main__":
    main()
