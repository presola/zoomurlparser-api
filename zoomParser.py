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

    def get_main_url(self, url, alternate_url):
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme:
            parsed_url = urllib.parse.urlparse(alternate_url)
            url = "{0}://{1}{2}".format(parsed_url.scheme, parsed_url.netloc, url)
        return url


    def get_single_image(self, url, images):

        parsed_url = urllib.parse.urlparse(url)
        image_url = None
        if len(images) > 0:
            for image in images:
                image_url = self.get_main_url(image['src'], url)

        return image_url

    def get_image(self, url, results):

        images = results.find_all('img', class_='custom_image')
        image_url = self.get_single_image(url, images)
        if not image_url:
            images_div = results.find('div', class_='top-logo')
            if images_div:
                images = images_div.find_all('img')
                image_url = self.get_single_image(url, images)

        return image_url

    def get_time(self, date_val, time_val=None):
        date = ""
        time = ""
        try:
            converted_date_time = parser.parse(date_val)

            date = converted_date_time.date()
            if time_val:
                converted_time = parser.parse(time_val)
                time = converted_time.time()
            else:

                time = converted_date_time.time()
        except:
            pass
        return date, time

    def parse_url(self, url):
        try:
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

                details_3 = results.find('div', class_='cms-title1').parent
                if details_3:
                    details_desc = details_3.find_all('p')
                    if len(details_desc) > 0:
                        details.append(details_desc[0])

            topic = details[0].get_text()
            description = ""
            date = ""
            time = ""
            if len(details) > 1:
                description = details[1].get_text()
                split_description = description.split()
                if len(split_description) > 20:
                    description = '{0}...'.format(' '.join(split_description[:20]))
                if len(details) > 2:
                    date_time = details[2].get_text()
                    date_time_split = date_time.split('in')

                    if len(date_time_split) > 0:
                        date_time_val = date_time_split[0].strip()
                        date, time = self.get_time(date_time_val)
                else:
                    details_time = results.find('div', class_="meeting-dur")
                    details_time_p = details_time.find_all('p')
                    if len(details_time_p) > 0:
                        time = details_time_p[0].get_text()
                    details_date = results.find('div', class_="meeting-date")
                    details_date_p = details_date.find_all('p')
                    if len(details_date_p) > 0:
                        date = details_date_p[0].get_text()


            image_url = self.get_image(url, results)
            return {"topic": topic.strip(), "description": description.strip(), "date": date, "time": time, "image_url": image_url}, True
        except:
            return {"error": "Unable to retrieve information"}, False
