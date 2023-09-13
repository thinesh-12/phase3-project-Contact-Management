from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import re
from colorama import Fore, init

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    contacts = relationship('Contact', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    contacts = relationship('Contact', back_populates='category')

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='contacts')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='contacts')
    
MENU_COLOR = Fore.BLUE
TITLE_COLOR = Fore.YELLOW  # Color for titles
CONTACT_COLOR = Fore.CYAN  # Color for contact details  

class CLI:
    def __init__(self):
        engine = create_engine("sqlite:///contacts.db")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.user = self.get_user()  # Get the user at the start
        self.data_dict = self.load_data()  # Load data into a dictionary

    def load_data(self):
        data_dict = {
            'users': {},
            'categories': {},
            'contacts': {},
        }

        users = self.session.query(User).all()
        for user in users:
            data_dict['users'][user.id] = {
                'id': user.id,
                'username': user.username,
                'password': user.password,
            }

        categories = self.session.query(Category).all()
        for category in categories:
            data_dict['categories'][category.id] = {
                'id': category.id,
                'name': category.name,
            }

        contacts = self.session.query(Contact).all()
        for contact in contacts:
            data_dict['contacts'][contact.id] = {
                'id': contact.id,
                'name': contact.name,
                'phone': contact.phone,
                'email': contact.email,
                'user_id': contact.user_id,
                'category_id': contact.category_id,
            }

        return data_dict

    def save_data(self):
        self.session.commit()
        self.data_dict = self.load_data()

    def main_menu(self):
        print(Fore.YELLOW + "Welcome to the Contact Management!")
        while True:
            print(Fore.CYAN +"\nMain Menu:")
            print(Fore.BLUE +"1. Add Contact")
            print(Fore.GREEN +"2. Search Contacts")
            print(Fore.YELLOW +"3. Edit Contact")
            print(Fore.MAGENTA +"4. Delete Contact")
            print(Fore.RED +"5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.search_contacts()
            elif choice == '3':
                self.edit_contact()
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

        print("Available Categories: Friends, Family, Work")
        category_name = input("Enter Category Name: ")

        category = self.get_or_create_category(category_name)

        new_contact = Contact(name=name, phone=phone, email=email, user=self.user, category=category)
        self.session.add(new_contact)
        self.save_data()
        print("Contact added successfully!")

    def search_contacts(self):
        print("\nSearch Contacts:")
        search_term = input("Enter search term(at least three characters): ")
        if len(search_term) < 3:
            print("Search term should contain atleast three charectors.")
            return 
        
        print("Available Categories: Friends, Family, Work")
        category_name = input("Enter Category Name (optional): ")

        contacts = self.filter_contacts(search_term, category_name)

        if contacts:
            print(TITLE_COLOR + "\nSearch Results:")
            for contact in contacts:
                contact_id = contact.get('id', 'N/A')
                name = contact.get('name', 'N/A')
                phone = contact.get('phone', 'N/A')
                email = contact.get('email', 'N/A')
                category_id = contact.get('category_id')
                category = self.data_dict['categories'].get(category_id, {})
                category_name = category.get('name', 'N/A')
                print(TITLE_COLOR + f"ID: {CONTACT_COLOR}{contact_id}, "
                      + TITLE_COLOR + f"Name: {CONTACT_COLOR}{name}, "
                      + TITLE_COLOR + f"Phone: {CONTACT_COLOR}{phone}, "
                      + TITLE_COLOR + f"Email: {CONTACT_COLOR}{email}, "
                      + TITLE_COLOR + f"Category: {CONTACT_COLOR}{category_name}")
        else:
            print("No contacts found.")

    def filter_contacts(self, search_term, category_name=None):
        filtered_contacts = []
        for contact_id, contact in self.data_dict['contacts'].items():
            if (contact['user_id'] == self.user.id) and (search_term.lower() in contact['name'].lower() or
                                                        search_term.lower() in contact['phone'].lower() or
                                                        search_term.lower() in contact['email'].lower()):
                if category_name:
                    category = self.data_dict['categories'].get(contact['category_id'], {})
                    if category_name.lower() == category.get('name', '').lower():
                        filtered_contacts.append(contact)
                else:
                    filtered_contacts.append(contact)
        return filtered_contacts

    def get_or_create_category(self, category_name):
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.commit()
        return category

    def edit_contact(self):
        print("\nEdit Contact:")
        contact_id = input("Enter Contact ID to edit: ")
        contact = self.data_dict['contacts'].get(int(contact_id))

        if contact and contact['user_id'] == self.user.id:
            print("Contact Details:")
            print(f"Name: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            category = self.data_dict['categories'].get(contact['category_id'], {})
            print(f"Category: {category.get('name', 'N/A')}")

            new_name = input("Enter new name (or press Enter to keep the current name): ")
            new_phone = input("Enter new phone (or press Enter to keep the current phone): ")
            new_email = input("Enter new email (or press Enter to keep the current email): ")
            new_category_name = input("Enter new category name (or press Enter to keep the current category): ")

            if new_name:
                contact['name'] = new_name
            if new_phone:
                contact['phone'] = new_phone
            if new_email:
                contact['email'] = new_email
            if new_category_name:
                category = self.get_or_create_category(new_category_name)
                contact['category_id'] = category.id

            self.save_data()
            print("Contact updated successfully!")
        else:
            print("Invalid Contact ID or you don't have permission to edit this contact.")

    def delete_contact(self):
        print("\nDelete Contact:")
        contact_id = input("Enter Contact ID to delete: ")
        contact = self.data_dict['contacts'].get(int(contact_id))

        if contact and contact['user_id'] == self.user.id:
            print(f"Are you sure you want to delete the contact: {contact['name']} (ID: {contact_id})?")
            confirmation = input("Type 'yes' to confirm: ")

            if confirmation.lower() == 'yes':
                contact_orm = self.session.query(Contact).filter_by(id=int(contact_id)).first()
                if contact_orm:
                    self.session.delete(contact_orm)
                    self.save_data()
                    print("Contact deleted successfully!")
                else:
                    print("Contact not found in the database.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid Contact ID or you don't have permission to delete this contact.")
            
    def exit_program(self):
        print(Fore.YELLOW + "Thank you for using the CLI. Goodbye!")
        import sys
        sys.exit(0)

if __name__ == "__main__":
    init()
    cli = CLI()
    cli.main_menu()
