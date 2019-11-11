import aiohttp
import config
import ujson

GIPHY_RANDOM_URL = 'http://api.giphy.com/v1/gifs/random?tag=cat&limit=5&api_key='

# Random cat gif from giphy.com
class GiphyConnector:
    """Base gifs and mp4 sources class"""

    # asynchronous load content from url
    @staticmethod
    async def get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    @staticmethod
    async def get_random_gif() -> str:
        response = await GiphyConnector.get(GIPHY_RANDOM_URL + config.GIPHY_API_KEY)
        parse_json = ujson.loads(response)

        return parse_json['image_original_url']
