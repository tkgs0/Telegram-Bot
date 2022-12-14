from sys import exc_info
import httpx, random
from httpx import AsyncClient

from telegram import InputMediaPhoto

from utils.log import logger
from src.config import ACGGOV


headers = {                                                                         'token': ACGGOV.token if ACGGOV.token else 'apikey', 
    'referer': 'https://www.acgmx.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'                                 }


def generate_image_struct():
    return {
        'id': 0,
        'url': '',
        'title': '',
        'author': '',
        'tags': [],
        'data': None,
        'native': False,
    }

async def get_pix(keyword=['R-18',], img=1) -> list:
    logger.info('loading...')

    img = img if img < 11 else 1
    image_list = []
    image = generate_image_struct()
    
    async with AsyncClient() as client:
        url = 'https://api.acgmx.com/public/search'
        params = {
            'q': '%20'.join(keyword) if keyword else ['R-18',],
            'offset': 0
        }
        try:
            res = await client.get(
                url,
                params=params,
                headers=headers,
                timeout=120
            )
        except httpx.HTTPError as e:
            logger.warning(e)
            return [f'API异常{e}', False]
        data = res.json()

        if not data['illusts']:
            logger.info(e := f'图库中没有搜到关于{keyword}的图。')
            return [e, False]

        try:
            for _ in range(img if len(data['illusts']) > img else len(data['illusts'])):
                item = random.choice(data['illusts'])
                data['illusts'].remove(item)
                image = generate_image_struct()
                image['id'] = item['id']
                image['title'] = item['title']
                image['author'] = item['user']['name']
                for tag in item['tags']:
                    image['tags'].append(tag['name'])
                try:
                    if item['page_count'] == 1:
                        image['url'] = item['meta_single_page']['original_image_url']
                    else:
                        num = random.randint(0, item['page_count'] - 1)
                        image['url'] = item['meta_pages'][num]['image_urls']['original']
                except:
                    pass
                if image['url']:
                    image_list.append(image)

            content = [{
                'pid': i['id'],
                'url': i['url'].replace('https://i.pximg.net', ACGGOV.pixproxy if ACGGOV.pixproxy else 'https://i.pixiv.re'),
                'caption': (
                    f'标题: {i["title"]}\n'
                    f'pid: {i["id"]}\n'
                    f'画师: {i["author"]}\n'
                    f'标签: {", ".join(i["tags"])}'
                )
            } for i in image_list]

            logger.success('complete.')

            if len(content) == 1:
                return [content[0]['url'], 1, content[0]['caption']]

            media = [
                InputMediaPhoto(media=i['url'], caption=i['caption'])
                for i in content
            ]
            return [media, 2]

        except httpx.ProxyError as e:
            logger.warning(e)
            return [f'代理错误: {e}', False]
        except IndexError as e:
            logger.warning(e)
            return [f'图库中没有搜到关于{keyword}的图。', False]
        except:
            logger.warning(f'{exc_info()[0]}, {exc_info()[1]}')
            return [f'{exc_info()[0]} {exc_info()[1]}。', False]

