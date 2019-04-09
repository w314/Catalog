from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# # DELETE ALL USERS
# users = session.query(User).all()
# print('Deleting following users:')
# for user in users:
#     print(user.id)
#     print(user.email)
#     session.delete(user)
#     session.commit()


# PRINT TABLES & TABLE COLUMN
inspector = inspect(engine)
print(inspector.get_table_names())
print('user table columns:')
print(inspector.get_columns('user'))

# PRINT ALL USERS IN DB:
users = session.query(User).all()
print(users)
for user in users:
    print(user)
    print(user.id)
    print(user.name)
    print(user.email)

# PRINT ALL ITEMS IN DB:
items = session.query(Item).all()
print(users)
for item in items:
    print(item.name)
    print(item.category.name)
    print(item.user_id)
    print(item.user.name)
