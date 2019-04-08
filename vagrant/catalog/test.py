from sqlalchemy import create_engine, inspector
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# DELETE ALL USERS
users = session.query(User).all()
print('Deleting following users:')
for user in users:
    print(user.id)
    print(user.email)
    session.delete(user)
    session.commit()


# PRINT TABLES & TABLE COLUMN
inspector = inspect(engine)
print(inspector.get_table_names())
print('user table columns:')
print(inspector.get_columns('user'))
print(login_session['username'])


