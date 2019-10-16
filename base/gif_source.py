import time
import aiohttp
import bs4
import random
import ujson
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


# Source urls
CAATS_BASE_URL = 'https://cataas.com/cat/gif'
RANDOM_CAT_GIFS_BASE_URL = 'https://randomcatgifs.com/'
RAND_CAT_BASE_URL = 'https://rand.cat/gifs/'
GIPHY_BASE_URL = 'https://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=cat'
THE_CATS_API_BASE_URL = 'https://api.thecatapi.com/v1/images/search?limit=1&mime_types=gif&order=Random&size=small&page=0&sub_id=demo-eb6a3'


# Random cat gif source class
class GifSource:
    """Base gifs and mp4 sources class"""

    # List of random methods for get cat document url
    random_list = ('cats_source', 'random_cat_gifs_source', 'random_cat_source', 'random_cat_giphy_source', 'random_cat_thecatapi_source')

    # Select random method and return cat url
    @classmethod
    async def get_random_cat_url(cls) -> str:
        try:
            random_index = random.randint(0, len(cls.random_list) - 1)
            cat_method_to_call = getattr(cls, cls.random_list[random_index])
            result = await cat_method_to_call()

            return result
        except Exception as e:
            logging.info(str(e))

    # asynchronous load content from url
    @staticmethod
    async def get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    # cataas.com source (depend on unix timestamp)
    @staticmethod
    async def cats_source() -> str:
        return CAATS_BASE_URL + '?s=' + str(time.time())

    # randomcatgifs.com source (get mp4 url from page)
    @staticmethod
    async def random_cat_gifs_source() -> str:
        response = await GifSource.get(RANDOM_CAT_GIFS_BASE_URL)
        parse_html = bs4.BeautifulSoup(response, 'html.parser')
        source_node = parse_html.find('source', {'type': 'video/mp4'})

        return source_node.get('src')

    # rand.cat source (depend on random int 1-400)
    @staticmethod
    async def random_cat_source() -> str:
        return RAND_CAT_BASE_URL + 'cat-' + str(random.randint(1, 400)) + '.gif'

    # giphy.com source (get gif url from response)
    @staticmethod
    async def random_cat_giphy_source() -> str:
        response = await GifSource.get(GIPHY_BASE_URL)
        parse_json = ujson.loads(response)

        return parse_json['data']['image_original_url']

    # api.thecatapi.com source (get json from response)
    @staticmethod
    async def random_cat_thecatapi_source() -> str:
        response = await GifSource.get(THE_CATS_API_BASE_URL)
        parse_json = ujson.loads(response)

        return parse_json[0]['url']
