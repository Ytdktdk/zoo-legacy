catalog_code = '''ANIMAL_CATALOG = {
    "Амурский тигр (Panthera tigris altaica)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/tiger.jpg",
        "space": 80.0,
        "sound": "Рёв тигра",
        "price": 75000
    },
    "Белый медведь (Ursus maritimus)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/bear.jpg",
        "space": 100.0,
        "sound": "Рык медведя",
        "price": 85000
    },
    "Кенгуру Беннетта (Macropus rufogriseus)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/kangaroo_bennett.jpg",
        "space": 30.0,
        "sound": "Прыжки",
        "price": 15000
    },
    "Большой серый кенгуру (Macropus giganteus)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/kangaroo_grey.jpg",
        "space": 40.0,
        "sound": "Топот",
        "price": 25000
    },
    "Альпака (Vicugna pacos)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/alpaca.jpg",
        "space": 25.0,
        "sound": "Жевание",
        "price": 22000
    },
    "Гуанако (Lama guanicoe)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/guanaco.jpg",
        "space": 25.0,
        "sound": "Фырканье",
        "price": 22000
    },
    "Европейский лось (Alces alces)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/moose.jpg",
        "space": 60.0,
        "sound": "Рёв лося",
        "price": 35000
    },
    "Северный олень (Rangifer tarandus)": {
        "cat": "Млекопитающие",
        "image": "assets/animals/reindeer.jpg",
        "space": 50.0,
        "sound": "Фырканье оленя",
        "price": 30000
    },
    "Пингвин Гумбольдта (Spheniscus humboldti)": {
        "cat": "Птицы",
        "image": "assets/animals/penguin.jpg",
        "space": 20.0,
        "sound": "Крик пингвина",
        "price": 35000
    },
    "Кудрявый пеликан (Pelecanus crispus)": {
        "cat": "Птицы",
        "image": "assets/animals/pelican_curly.jpg",
        "space": 40.0,
        "sound": "Клокотание",
        "price": 18000
    },
    "Розовый пеликан (Pelecanus onocrotalus)": {
        "cat": "Птицы",
        "image": "assets/animals/pelican_pink.jpg",
        "space": 40.0,
        "sound": "Клокотание",
        "price": 20000
    },
    "Большой тукан (Ramphastos toco)": {
        "cat": "Птицы",
        "image": "assets/animals/toucan.jpg",
        "space": 15.0,
        "sound": "Кракание",
        "price": 22000
    },
    "Нильский крокодил (Crocodylus niloticus)": {
        "cat": "Пресмыкающиеся",
        "image": "assets/animals/crocodile.jpg",
        "space": 80.0,
        "sound": "Рык крокодила",
        "price": 45000
    },
    "Крокодиловый кайман (Caiman crocodilus)": {
        "cat": "Пресмыкающиеся",
        "image": "assets/animals/caiman.jpg",
        "space": 60.0,
        "sound": "Шипение",
        "price": 40000
    },
    "Королевский питон (Python regius)": {
        "cat": "Пресмыкающиеся",
        "image": "assets/animals/python.jpg",
        "space": 20.0,
        "sound": "Шипение змеи",
        "price": 12000
    },
    "Обыкновенная игуана (Iguana iguana)": {
        "cat": "Пресмыкающиеся",
        "image": "assets/animals/iguana.jpg",
        "space": 25.0,
        "sound": "Шипение",
        "price": 10000
    },
    "Гигантский азиатский богомол (Hierodula patellifera)": {
        "cat": "Беспозвоночные",
        "image": "assets/animals/mantis.jpg",
        "space": 5.0,
        "sound": "Шуршание",
        "price": 3000
    },
    "Паук-птицеед (Theraphosa blondi)": {
        "cat": "Беспозвоночные",
        "image": "assets/animals/spider.jpg",
        "space": 5.0,
        "sound": "Тишина",
        "price": 5000
    },
}
'''

with open('models/animal_catalog.py', 'w', encoding='utf-8') as f:
    f.write(catalog_code)

print("✅ animal_catalog.py обновлён с локальными путями")