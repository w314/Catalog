from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Category, Item

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
        'category_id': 1,
        'user_id': 1,
    },
    {
        'name': 'Cat',
        'description': 'says miau',
        'category_id': 1,
        'user_id': 2,
    },
    {
        'name': 'Red',
        'description': 'sunset color',
        'category_id': 2,
        'user_id': 2,
    },
    {
        'name': 'Yellow',
        'description': 'sun color',
        'category_id': 2,
        'user_id': 2,
    },
    {
        'name': 'Black',
        'description': 'a very dark color',
        'category_id': 2,
        'user_id': 1,
    },
    {
        'name': 'Chair',
        'description': 'to stand on',
        'category_id': 3,
        'user_id': 1,
    },
    {
        'name': 'Bed',
        'description': 'to hide under',
        'category_id': 3,
        'user_id': 1,
    },
    {
        'name': 'Table',
        'description': 'to crawl under in case of earthquake',
        'category_id': 3,
        'user_id': 2,
    },
    {
        'name': 'German',
        'description': 'to speak in Germany',
        'category_id': 4,
        'user_id': 2,
    },
    {
        'name': 'French',
        'description': 'to listen to',
        'category_id': 4,
        'user_id': 2,
    },
    {
        'name': 'Russian',
        'description': 'to speak in Russia',
        'category_id': 4,
        'user_id': 1,
    },
    {
        'name': 'Python',
        'description': 'to use when talking to snakes',
        'category_id': 5,
        'user_id': 1,
    },
    {
        'name': 'JavaScript',
        'description': 'to use when making coffee',
        'category_id': 5,
        'user_id': 1,
    },
    {
        'name': 'C++',
        'description': 'to use to get extra points',
        'category_id': 5,
        'user_id': 2,
    },
    {
        'name': 'Germany',
        'description': 'best place to speak German',
        'category_id': 6,
        'user_id': 2,
    },
    {
        'name': 'Ireland',
        'description': 'best place for little green men',
        'category_id': 6,
        'user_id': 2,
    },
    {
        'name': 'Finnland',
        'description': 'to go to lakes and build snowmen',
        'category_id': 6,
        'user_id': 1,
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

print('Categories and items created in catalog database.')
