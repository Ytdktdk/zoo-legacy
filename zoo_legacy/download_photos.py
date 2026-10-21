import os
import urllib.request
from pathlib import Path

print("=== СКАЧИВАНИЕ ФОТОГРАФИЙ ЖИВОТНЫХ ===\n")

# Создаем папку для фото
photos_dir = Path('assets/animals')
photos_dir.mkdir(parents=True, exist_ok=True)

# Ссылки на фотографии
photos = {
    'tiger': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRATNXlnBjV0Unf1mmAHeMc8oRkqAm2IjGg3v_nlxfKTQ&s=10',
    'bear': 'https://i.natgeofe.com/k/d369d971-0360-47ab-bd46-01427f0eb2f7/125-animals-polarbear_square.jpg',
    'kangaroo_bennett': 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/14869476-d7a1-4393-bb9f-87c89a0637fc.jpg',
    'kangaroo_grey': 'https://kldzoo.ru/upload/dev2fun.imagecompress/webp/iblock/e8d/va1xu14ehb4jnrqsme9fzmvwi3uv2s85.webp',
    'alpaca': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRIhJFZezqWKaQ-rK360GuqtGbM_SUribg_tJK5c6zkZskStzawQzfkotC&s=10',
    'guanaco': 'https://i.pinimg.com/736x/02/87/e1/0287e1fa5d95862e1c9679d2f7852041.jpg',
    'moose': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2GeV2ymyzNJNb57GDkK1VTRXm4UUOFLMsgPdmsAVH-w&s=10',
    'reindeer': 'https://qpicture.ru/images/2021/02/20/elch3.jpg',
    'penguin': 'https://poknok.art/uploads/posts/2022-11/1669035961_2-poknok-art-p-pingvin-gumboldta-foto-4.jpg',
    'pelican_curly': 'https://bolzoo.ru/images/cat_imgs/l/2023_06/2dded8b48ac12c34136697a8f0725586.jpg',
    'pelican_pink': 'https://img.pravda.ru/image/preview/article/5/6/4/2380564_amp.jpeg',
    'toucan': 'https://static.wikia.nocookie.net/rio/images/1/17/Toucan_toco.jpg/revision/latest?cb=20140409132547&path-prefix=ru',
    'crocodile': 'https://exotic-animals.ru/wp-content/uploads/2025/12/nilskij-krokodil.jpg',
    'caiman': 'https://zoopodolsk.ru/images/stories/reptilii/Krokodilovyj_kajman2.jpg',
    'python': 'https://pets-start.by/upload/iblock/791/4t161ianbq3sqnjztveiygzmomqd0u2u.jpg',
    'iguana': 'https://upload.wikimedia.org/wikipedia/commons/b/b6/Iguana_iguana_Fern_Forest.JPG?utm_source=ru.wikipedia.org&utm_campaign=index&utm_content=original',
    'mantis': 'https://img.magnific.com/free-photo/giant-shield-mantis-closeup-with-self-defense-position-branch_488145-3168.jpg?semt=ais_hybrid&w=740&q=80',
    'spider': 'https://www.bethowen.ru/upload/medialibrary/cb8/cb8f02d3ae860265421efcb576b0c986.jpg'
}

# Заголовки для запросов (чтобы сайты не блокировали)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

downloaded = 0
failed = 0

for name, url in photos.items():
    filename = photos_dir / f"{name}.jpg"
    try:
        print(f"Скачиваю {name}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filename, 'wb') as out_file:
                out_file.write(response.read())
        print(f"  ✅ {name}.jpg")
        downloaded += 1
    except Exception as e:
        print(f"  ❌ Ошибка загрузки {name}: {e}")
        failed += 1

print(f"\n=== ГОТОВО ===")
print(f"Скачано: {downloaded}")
print(f"Не удалось: {failed}")
print(f"Папка: {photos_dir.absolute()}")