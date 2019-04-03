items = [
    {
        'name': 'dog',
        'description': 'barks',
        'category_id': 0
    },
    {
        'name': 'cat',
        'description': 'says miau',
        'category_id': 0,
    }
    
]

for item in items:
    new_item = Item(
        name = item['name'],
        description = item['description'],
        category_id = item['category_id']
        )
    session.add(new_item)
    session.commit()
    
