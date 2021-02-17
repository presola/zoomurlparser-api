from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import urllib.parse
from dateutil import parser

class ZoomURL(BaseModel):
    link: str

class ZoomParser:

    def make_api_call(self, url):
        api_call = requests.get(url)

        return api_call.content
    def get_image(self, url, results):

        parsed_url = urllib.parse.urlparse(url)
        image_url = ""
        images = results.find_all('img', class_='custom_image')
        for image in images:
            image_url = "{0}://{1}{2}".format(parsed_url.scheme, parsed_url.netloc, image['src'])
        return image_url

    def parse_url(self, url):
        content = self.make_api_call(url)
        results = BeautifulSoup(content, 'html.parser')

        form_find = results.find('form')
        details = form_find.find_all('div', class_='controls')

        topic = details[0].get_text()
        description = details[1].get_text()
        split_description = description.split()
        if len(split_description) > 20:
            description = '{0}...'.format(' '.join(split_description[:20]))
        date_time = details[2].get_text()
        date_time_split = date_time.split('in')

        date = ""
        time = ""
        if len(date_time_split) > 0:
            date_time_val = date_time_split[0].strip()
            converted_date_time = parser.parse(date_time_val)

            date = converted_date_time.date()
            time = converted_date_time.time()

        image_url = self.get_image(url, results)
        return {"topic": topic, "description": description, "date": date, "time": time, "image_url": image_url}
