from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Category, Contact
from faker import Faker
import random


engine = create_engine('sqlite:///contacts.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Create users
user1 = User(username='user1', password='password1')
user2 = User(username='user2', password='password2')

# Create categories
category1 = Category(name='Friends')
category2 = Category(name='Family')
category3 = Category(name='Work')  # add "work" category 

# Dictionary to store contacts details
contacts_dict = {}

# Create contacts with random data and store them in the dictionary

for contact_id in range(1, 11): # Random datas 
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()
    user = random.choice([user1, user2])
    category = random.choice([category1, category2, category3])  # Include "Work" category

    contact_details = {
        'id': contact_id,
        'name': name,
        'phone': phone,
        'email': email,
        'user_id': user.id,
        'category_id': category.id,
    }

    contacts_dict[contact_id] = contact_details
    
    for contact_id, details in contacts_dict.items():
     contact = Contact(**details)
    session.add(contact)

# Add users and categories to the session
session.add_all([user1, user2, category1, category2, category3]) 
session.commit()

print("Database seeded successfully.")