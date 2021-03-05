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
        if not form_find:
            return {"error": "Unable to retrieve information"}, False
        details = form_find.find_all('div', class_='controls')
        details_2 = results.find_all('div', class_='cms-title1')
        if len(details) < 1 and len(details_2) < 1:
            return {"error": "Unable to retrieve information"}, False
        if len(details_2) > 0:
            details = details_2

            details_3 = details_2.find_parent()
            if details_3:
                details_desc = details_3.find_all('p')

        topic = details[0].get_text()
        description = ""
        date = ""
        time = ""
        if len(description) > 0:
            description = details[1].get_text()
            split_description = description.split()
            if len(split_description) > 20:
                description = '{0}...'.format(' '.join(split_description[:20]))
            date_time = details[2].get_text()
            date_time_split = date_time.split('in')


            if len(date_time_split) > 0:
                date_time_val = date_time_split[0].strip()
                try:
                    converted_date_time = parser.parse(date_time_val)

                    date = converted_date_time.date()
                    time = converted_date_time.time()
                except:
                    pass

        image_url = self.get_image(url, results)
        return {"topic": topic.strip(), "description": description.strip(), "date": date, "time": time, "image_url": image_url}, True
