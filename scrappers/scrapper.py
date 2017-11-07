import logging
import requests
from parsers.html_parser import HtmlParser


logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects
        self.htmlParser = HtmlParser(['beatmap', 'id'])

    def scrap_process(self, storage):
        # You can iterate over ids, or get list of objects
        # from any API, or iterate throught pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you
        searchUrl = 'https://osu.ppy.sh/p/beatmaplist?l=1&r=0&q=&g=0&la=0&ra=&s=4&o=1&m=0&page='
        data = []

        for page in range(1,40):
            response = requests.get(searchUrl + str(page))

            if not response.ok:
                logger.error(response.text)
                # then continue process, or retry, or fix your code
            else:
                print('\nSearch page ' + str(page) + '\n')
                # Note: here json can be used as response.json
                html = response.text
                IDs = self.htmlParser.getIDs(html)

                for id in IDs:
                    try:
                        data.append(self.getData(id))
                        print('ID ' + str(id))
                    except AttributeError:
                        print('ID ' + str(id) + ' was skipped')

        print('Number of items ' + str(len(data)))
        storage.write_data(str(data))


    def getData(self, id):
        beatmapsUrl = 'https://osu.ppy.sh/s/'
        data = {}
        response = requests.get(beatmapsUrl + str(id))

        if not response.ok:
            logger.error(response.text)
        else:
            html = response.text
            data = (self.htmlParser.parse(html))
        return data
