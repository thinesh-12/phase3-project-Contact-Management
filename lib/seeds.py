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

# Create contacts with random data
for _ in range(10):
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()
    user = random.choice([user1, user2])
    category = random.choice([category1, category2])
    
    contact = Contact(name=name, phone=phone, email=email, user=user, category=category)
    session.add(contact)

# Add users and categories to the session
session.add_all([user1, user2, category1, category2])
session.commit()

print("Database seeded successfully.")
