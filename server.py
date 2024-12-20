import aiohttp
from aiohttp import web
import json
from datetime import datetime

# Хранилище для объявлений
ads = {}
ad_id_counter = 1

async def create_ad(request):
    global ad_id_counter
    data = await request.json()
    ad = {
        'id': ad_id_counter,
        'title': data['title'],
        'description': data['description'],
        'created_at': datetime.now().isoformat(),
        'owner': data['owner']
    }
    ads[ad_id_counter] = ad
    ad_id_counter += 1
    return web.json_response(ad, status=201)

async def get_all_ads(request):
    return web.json_response(list(ads.values()))

async def get_ad(request):
    ad_id = int(request.match_info['id'])
    ad = ads.get(ad_id)
    if ad is None:
        return web.json_response({'error': 'Ad not found'}, status=404)
    return web.json_response(ad)

async def delete_ad(request):
    ad_id = int(request.match_info['id'])
    if ad_id in ads:
        del ads[ad_id]
        return web.json_response({'message': 'Ad deleted'}, status=200)
    return web.json_response({'error': 'Ad not found'}, status=404)

app = web.Application()
app.router.add_post('/ads', create_ad)
app.router.add_get('/ads', get_all_ads)  # Добавлен обработчик для получения всех объявлений
app.router.add_get('/ads/{id}', get_ad)
app.router.add_delete('/ads/{id}', delete_ad)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)