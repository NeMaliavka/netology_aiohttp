import aiohttp
import asyncio

# URL Вашего API
base_url = 'http://127.0.0.1:8080/ads'

# Список объявлений для создания
ads_to_create = [
    {
        'title': 'Объявление 1',
        'description': 'Описание 1',
        'owner': 'Владелец 1'
    },
    {
        'title': 'Объявление 2',
        'description': 'Описание 2',
        'owner': 'Владелец 2'
    },
    {
        'title': 'Объявление 3',
        'description': 'Описание 3',
        'owner': 'Владелец 3'
    }
]

async def create_ads():
    async with aiohttp.ClientSession() as session:
        # 1. Создание нескольких объявлений (POST)
        for ad in ads_to_create:
            async with session.post(base_url, json=ad) as response_post:
                print('POST статус-код:', response_post.status)
                print()
                print('POST ответ:', await response_post.json())
                print()

        # 2. Получение всех объявлений (GET)
        async with session.get(base_url) as response_get:
            print('GET статус-код:', response_get.status)
            print()
            print('GET ответ:', await response_get.json())
            print()

        # 3. Получение конкретного объявления (GET)
        ad_id = 1  # Замените на ID объявления, которое хотите получить
        async with session.get(f'{base_url}/{ad_id}') as response_get_single:
            print('GET (одиночное) статус-код:', response_get_single.status)
            try:
                response_data = await response_get_single.json()
                print('GET (одиночное) ответ:', response_data)
            except aiohttp.ContentTypeError:
                print('Ошибка декодирования JSON:', await response_get_single.text())
            print()

        # 4. Удаление объявления (DELETE)
        async with session.delete(f'{base_url}/{ad_id}') as response_delete:
            print('DELETE статус-код:', response_delete.status)
            if response_delete.status == 200:
                response_data = await response_delete.json()
                print('DELETE ответ:', response_data.get('message', 'Нет сообщения'))
            else:
                print('Ошибка при удалении:', await response_delete.text())

# Запуск асинхронной функции
if __name__ == '__main__':
    asyncio.run(create_ads())