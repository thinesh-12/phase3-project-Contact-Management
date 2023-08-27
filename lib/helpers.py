from sqlalchemy.orm import Session
from models import User, Category, Contact

class ContactManager:
    def __init__(self, session):
        self.session = session
    
    def get_or_create_category(self, category_name):
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.commit()
        return category
    
    def add_contact(self, name, phone, email, user, category_name):
        category = self.get_or_create_category(category_name)
        new_contact = Contact(name=name, phone=phone, email=email, user=user, category=category)
        self.session.add(new_contact)
        self.session.commit()
     
    
    def search_contacts(self, user, search_term, category_name):
        query = self.session.query(Contact).filter(
            Contact.user == user,
            (Contact.name.ilike(f"%{search_term}%")) |
            (Contact.phone.ilike(f"%{search_term}%")) |
            (Contact.email.ilike(f"%{search_term}%"))
        )
        
        if category_name:
            category = self.session.query(Category).filter_by(name=category_name).first()
            if category:
                query = query.join(Contact.category).filter(Category.name == category_name)
            else:
                print(f"Category '{category_name}' not found. Searching without category filter.")
                 
        contacts = query.all()
        return contacts
