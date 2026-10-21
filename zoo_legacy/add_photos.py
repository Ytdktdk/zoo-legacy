import os

print("=== ДОБАВЛЕНИЕ ФОТОГРАФИЙ ЖИВОТНЫХ ===\n")

# Обновляем animal_catalog.py с ссылками на фотографии
catalog_code = '''ANIMAL_CATALOG = {
    "Амурский тигр (Panthera tigris altaica)": {
        "cat": "Млекопитающие",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRATNXlnBjV0Unf1mmAHeMc8oRkqAm2IjGg3v_nlxfKTQ&s=10",
        "space": 80.0,
        "sound": "Рёв тигра",
        "price": 75000
    },
    "Белый медведь (Ursus maritimus)": {
        "cat": "Млекопитающие",
        "image": "https://i.natgeofe.com/k/d369d971-0360-47ab-bd46-01427f0eb2f7/125-animals-polarbear_square.jpg",
        "space": 100.0,
        "sound": "Рык медведя",
        "price": 85000
    },
    "Кенгуру Беннетта (Macropus rufogriseus)": {
        "cat": "Млекопитающие",
        "image": "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/14869476-d7a1-4393-bb9f-87c89a0637fc.jpg",
        "space": 30.0,
        "sound": "Прыжки",
        "price": 15000
    },
    "Большой серый кенгуру (Macropus giganteus)": {
        "cat": "Млекопитающие",
        "image": "https://kldzoo.ru/upload/dev2fun.imagecompress/webp/iblock/e8d/va1xu14ehb4jnrqsme9fzmvwi3uv2s85.webp",
        "space": 40.0,
        "sound": "Топот",
        "price": 25000
    },
    "Альпака (Vicugna pacos)": {
        "cat": "Млекопитающие",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRIhJFZezqWKaQ-rK360GuqtGbM_SUribg_tJK5c6zkZskStzawQzfkotC&s=10",
        "space": 25.0,
        "sound": "Жевание",
        "price": 22000
    },
    "Гуанако (Lama guanicoe)": {
        "cat": "Млекопитающие",
        "image": "https://i.pinimg.com/736x/02/87/e1/0287e1fa5d95862e1c9679d2f7852041.jpg",
        "space": 25.0,
        "sound": "Фырканье",
        "price": 22000
    },
    "Европейский лось (Alces alces)": {
        "cat": "Млекопитающие",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2GeV2ymyzNJNb57GDkK1VTRXm4UUOFLMsgPdmsAVH-w&s=10",
        "space": 60.0,
        "sound": "Рёв лося",
        "price": 35000
    },
    "Северный олень (Rangifer tarandus)": {
        "cat": "Млекопитающие",
        "image": "https://qpicture.ru/images/2021/02/20/elch3.jpg",
        "space": 50.0,
        "sound": "Фырканье оленя",
        "price": 30000
    },
    "Пингвин Гумбольдта (Spheniscus humboldti)": {
        "cat": "Птицы",
        "image": "https://poknok.art/uploads/posts/2022-11/1669035961_2-poknok-art-p-pingvin-gumboldta-foto-4.jpg",
        "space": 20.0,
        "sound": "Крик пингвина",
        "price": 35000
    },
    "Кудрявый пеликан (Pelecanus crispus)": {
        "cat": "Птицы",
        "image": "https://bolzoo.ru/images/cat_imgs/l/2023_06/2dded8b48ac12c34136697a8f0725586.jpg",
        "space": 40.0,
        "sound": "Клокотание",
        "price": 18000
    },
    "Розовый пеликан (Pelecanus onocrotalus)": {
        "cat": "Птицы",
        "image": "https://img.pravda.ru/image/preview/article/5/6/4/2380564_amp.jpeg",
        "space": 40.0,
        "sound": "Клокотание",
        "price": 20000
    },
    "Большой тукан (Ramphastos toco)": {
        "cat": "Птицы",
        "image": "https://static.wikia.nocookie.net/rio/images/1/17/Toucan_toco.jpg/revision/latest?cb=20140409132547&path-prefix=ru",
        "space": 15.0,
        "sound": "Кракание",
        "price": 22000
    },
    "Нильский крокодил (Crocodylus niloticus)": {
        "cat": "Пресмыкающиеся",
        "image": "https://sun9-66.vkuserphoto.ru/impg/BTJs4-3Y6s6gSiDb3ArESqPTe6nqj1VSmUPrsg/UfrsGYMDibY.jpg?size=1920x1280&quality=95&sign=d3fdde9281cf02c085d2f7b100c41a98&type=album",
        "space": 80.0,
        "sound": "Рык крокодила",
        "price": 45000
    },
    "Крокодиловый кайман (Caiman crocodilus)": {
        "cat": "Пресмыкающиеся",
        "image": "https://zoopodolsk.ru/images/stories/reptilii/Krokodilovyj_kajman2.jpg",
        "space": 60.0,
        "sound": "Шипение",
        "price": 40000
    },
    "Королевский питон (Python regius)": {
        "cat": "Пресмыкающиеся",
        "image": "https://pets-start.by/upload/iblock/791/4t161ianbq3sqnjztveiygzmomqd0u2u.jpg",
        "space": 20.0,
        "sound": "Шипение змеи",
        "price": 12000
    },
    "Обыкновенная игуана (Iguana iguana)": {
        "cat": "Пресмыкающиеся",
        "image": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Iguana_iguana_Fern_Forest.JPG?utm_source=ru.wikipedia.org&utm_campaign=index&utm_content=original",
        "space": 25.0,
        "sound": "Шипение",
        "price": 10000
    },
    "Гигантский азиатский богомол (Hierodula patellifera)": {
        "cat": "Беспозвоночные",
        "image": "https://img.magnific.com/free-photo/giant-shield-mantis-closeup-with-self-defense-position-branch_488145-3168.jpg?semt=ais_hybrid&w=740&q=80",
        "space": 5.0,
        "sound": "Шуршание",
        "price": 3000
    },
    "Паук-птицеед (Theraphosa blondi)": {
        "cat": "Беспозвоночные",
        "image": "https://www.bethowen.ru/upload/medialibrary/cb8/cb8f02d3ae860265421efcb576b0c986.jpg",
        "space": 5.0,
        "sound": "Тишина",
        "price": 5000
    },
}
'''

with open('models/animal_catalog.py', 'w', encoding='utf-8') as f:
    f.write(catalog_code)

print("✅ animal_catalog.py обновлён с фотографиями!")
print("\nТеперь все животные будут отображаться с реальными фотографиями!")
print("Запустите игру: py app.py")