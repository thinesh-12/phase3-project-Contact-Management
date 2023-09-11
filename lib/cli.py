from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Contact, Category
from helpers import ContactManager
from colorama import init, Fore, Style
import re

class CLI:
    def __init__(self):
        engine = create_engine("sqlite:///contacts.db")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.contact_manager = ContactManager(self.session)
        self.user = self.get_user()  # Get the user at the start
    
    def main_menu(self):
        print(Fore.CYAN + "Welcome to the Contact Management!")
        while True:
            print("\nMain Menu:")
            print("1. Add Contact")
            print("2. Search Contacts")
            print("3. Update Contact")
            print("4. Delete Contact")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.search_contacts()
            elif choice == '3':
                self.update_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                self.exit_program()
                print(Fore.YELLOW + "Thank you for using the CLI. Goodbye!")

                break
            else:
                print(Fore.RED + "Invalid choice. Please select a valid option.")
    
    def get_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        user = self.session.query(User).filter_by(username=username, password=password).first()
        if user:
            return user
        else:
            print("Invalid username or password.")
            return None

    def add_contact(self):
        print("\nAdding a New Contact:")
        name = input("Enter Contact Name: ")
        
        while True:
            phone = input("Enter Phone Number (XXX-XXX-XXXX or XXX XXX XXXX): ")
            if re.match(r'^\d{3}[-\s]\d{3}[-\s]\d{4}$', phone):
                break
            else:
                print("Invalid phone number format. Please use XXX-XXX-XXXX or XXX XXX XXXX format.")
        
        while True:
            email = input("Enter E-mail: ")
            if re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                break
            else:
                print("Invalid email format. Please enter a valid email address.")
        
        print("Available Categories: Friends, Family")  
        category_name = input("Enter Category Name: ")

        self.contact_manager.add_contact(name, phone, email, self.user, category_name)
        print("Contact added successfully!")


    def search_contacts(self):
        print("\nSearch Contacts:")
        search_term = input("Enter search term: ")
        print("Available Categories: Friends, Family, Work")
        category_name = input("Enter Category Name (optional): ")

        try:
            contacts = self.contact_manager.search_contacts(self.user, search_term, category_name)

            if contacts:
                print("\nSearch Results:")
                for contact in contacts:
                    print(f"Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}, Category: {contact.category.name}")
            else:
                print("No contacts found.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli = CLI()
    cli.main_menu()
