import scrapy
from scrapy import Request
from datetime import datetime
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from car_data_extraction.items import CarItem 
from car_data_extraction.polovniautomobili_extraction import extract_car_details
from car_data_extraction.utils import url_constructor, get_brand_models


class PolovniAutomobiliSpider(scrapy.Spider):
    name = "polovniautomobili"
    allowed_domains = ["polovniautomobili.com"] 
    
    def __init__(self, bm=1, *args, **kwargs):
        super(PolovniAutomobiliSpider, self).__init__(*args, **kwargs)
        self.brand_models = int(bm)
    
    def start_requests(self):
        # Iterate through brands and models to initiate requests
        brand_models = get_brand_models(self.brand_models) 
        separator = '-' * 35 # Separator lines for a print
        print(f"{separator}\nRunning spider for brand: {next(iter(brand_models))}\n{separator}") # Print current brand 
        for brand, models in brand_models.items():
            for model in models:
                url = url_constructor(brand, model, 1)
                yield Request(url=url, callback=self.parse, meta={'brand': brand, 'model': model, 'page': 1})

    def parse(self, response):

        # Log the current proxy being used for this request
        current_proxy = response.meta.get('proxy', 'No proxy used')
        self.logger.info(f"Processing request with proxy: {current_proxy}")

        brand = response.meta['brand']
        model = response.meta['model']
        page = response.meta['page']

        soup = BeautifulSoup(response.text, 'html.parser')
        car_listings = soup.find_all('article', class_='classified')
        
        if not car_listings:
            self.logger.info(f"No more listings for brand {brand}, model {model} on page {page}.")
            print(f"No more listings for brand {brand}, model {model} on page {page}.")
            return
        
        for listing in car_listings:
            # Get the current date and time for scraped
            now = datetime.now()
            car = extract_car_details(listing)
            present_time = now.strftime('%d/%m/%Y %H:%M:%S')
            if car:
                item = CarItem()
                item['id'] = car[0]
                item['brand'] = brand
                item['model'] = model
                item['title'] = car[1]
                item['current_price'] = car[2]
                item['old_price'] = 0  # Initial old value
                item['currency'] = car[4]
                item['mileage'] = car[5]
                item['location'] = car[6]
                item['year_produced'] = car[7]
                item['car_type'] = car[8]
                item['posted_date'] = car[9]
                item['fuel'] = car[10]
                item['ccm'] = car[11]
                item['kw'] = car[12]
                item['hp'] = car[13]
                item['url'] = car[14]
                item['scraped'] = present_time
                                
                yield item

        # Find the next page link if it exists
        next_page = soup.find('a', {'class': 'js-pagination-next', 'rel': 'next'})
        if next_page:
            next_url = response.urljoin(next_page['href'])
            current_page = response.meta['page']
            self.logger.info(f"Moving to page {current_page + 1} for {response.meta['brand']} {response.meta['model']}.")
            yield Request(next_url, callback=self.parse, meta={
                'brand': response.meta['brand'],
                'model': response.meta['model'],
                'page': current_page + 1
            })
        else:
            self.logger.info(f"No more pages for {response.meta['brand']} {response.meta['model']}.")
            print(f"No more pages for {response.meta['brand']} {response.meta['model']}.")