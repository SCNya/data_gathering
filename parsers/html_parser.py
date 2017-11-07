import re
import datetime
from parsers.parser import Parser

from bs4 import BeautifulSoup  # You can use any other library


class HtmlParser(Parser):
    def parse(self, html):
        data = {}
        soup = BeautifulSoup(html, 'html5lib')

        fields = soup.table.find_all('td')

        iterator = iter(fields)

        for field in iterator:
            if field.strong:
                if field.strong.contents[0] == 'Star Difficulty':
                    next_field = next(iterator)
                    difficulty = next_field.div.div
                    data['Difficulty'] = 10 / 140 * float(re.findall(r'\d+\.\d*|\d+', difficulty['style'])[0])
            elif field.contents:
                if field.contents[0] == 'Title:':
                    next_field = next(iterator)
                    title = next_field.a.contents[0]
                    data['Title'] = title
                elif field.contents[0] == 'Accuracy:':
                    next_field = next(iterator)
                    accuracy = next_field.div.div
                    data['Accuracy'] = 10 / 140 * float(re.findall(r'\d+\.\d*|\d+', accuracy['style'])[0])
                elif field.contents[0] == 'Length:':
                    next_field = next(iterator)
                    time = datetime.datetime.strptime(re.findall(r'\d+:\d*|\d+', next_field.contents[0])[1], '%M:%S')
                    length = (3600 * time.hour) + (60 * time.minute) + time.second
                    data['Length'] = length
                elif field.contents[0] == 'BPM:':
                    next_field = next(iterator)
                    bpm = next_field.contents[0]
                    data['BPM'] = float(bpm)

        return data

    def getIDs(self, html):
        IDs = []
        soup = BeautifulSoup(html, "html5lib")
        beatmaps = soup.find_all('div', {'class': 'beatmap'})
        for beatmap in beatmaps:
            IDs.append(beatmap.get("id"))
        return IDs
