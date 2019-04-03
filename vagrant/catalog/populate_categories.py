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
    new_category = Category(name=category)
    session.add(new_category)
    session.commit()


items = [
    {
        'name': 'Dog',
        'description': 'barks',
        'category_id': 1
    },
    {
        'name': 'Cat',
        'description': 'says miau',
        'category_id': 1,
    },
    {
        'name': 'Red',
        'description': 'sunset color',
        'category_id': 2,
    },
    {
        'name': 'Yellow',
        'description': 'sun color',
        'category_id': 2,
    },
    {
        'name': 'Chair',
        'description': 'to stand on',
        'category_id': 3,
    },
    {
        'name': 'Bed',
        'description': 'to hide under',
        'category_id': 3,
    },
    {
        'name': 'German',
        'description': 'to speak in Germany',
        'category_id': 4,
    },
    {
        'name': 'French',
        'description': 'to listen to',
        'category_id': 4,
    },
    {
        'name': 'Python',
        'description': 'to use when talking to snakes',
        'category_id': 5,
    },
    {
        'name': 'JavaScript',
        'description': 'to use when making coffee',
        'category_id': 5,
    },
    {
        'name': 'Germany',
        'description': 'best place to speak German',
        'category_id': 6,
    },
    {
        'name': 'Ireland',
        'description': 'best place for little green men',
        'category_id': 6,
    },
]

for item in items:
    new_item = Item(
        name=item['name'],
        description=item['description'],
        category_id=item['category_id']
        )
    session.add(new_item)
    session.commit()
