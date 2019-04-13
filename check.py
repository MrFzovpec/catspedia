import json
cats = [
    {
        "name": "Гуся",
        "photo": "https://memepedia.ru/wp-content/uploads/2019/03/dxdaey6uuaakpup-kopiya.jpg",
        "description": "Любит вкусно поесть гусей.",
        "short_description": "Красивый код",
        "comments": [
            {
                "author": "Александр",
                "text": "*людей...)))",
                "date": "13.37.28"
            }
        ],
        "likes": 60
    }
]

file = open('cats.json', 'w')
file.write(json.dumps(cats))
file.close()
