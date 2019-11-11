import sys
import asyncio

sys.path.append('../')

from base.gif_source import GifSource


async def preload_gif_list():

    # list of loaded urls
    url_list = []

    # Clear file
    open('../data/urls_dump.txt', 'w').close()

    # Load 1000 gifs url
    with open("../data/urls_dump.txt", "a") as myfile:
        for i in range(100):
            url = await GifSource.get_random_cat_url()

            if url not in url_list:
                myfile.write(url + '\n')
                url_list.append(url)


if __name__ == '__main__':
    # Run asyncio task
    asyncio.run(preload_gif_list())
