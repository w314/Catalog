from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = [
    'Animals',
    'Colors',
    'Furniture',
    'Languages',
    'Computer Languages',
    'Countries',
    ]

for category in categories:
    newCategory = Category(name=category)
    session.add(newCategory)
    session.commit()
