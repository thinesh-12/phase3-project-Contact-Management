
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine
)

Base = declarative_base()
engine = create_engine('sqlite:///contacts.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    contacts = relationship('Contact', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, )
    
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
    
if __name__ == "__main__":  
    Base.metadata.create_all(engine)
    
   