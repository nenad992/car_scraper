# Car Data Extraction

This project is a web scraping tool designed to extract car listing data from the website [Polovni Automobili](https://www.polovniautomobili.com). It utilizes the Scrapy framework and includes custom middlewares and pipelines to handle proxies, pausing, and data storage.

## Prerequisites

Before you can run this project, you'll need to have Python installed on your machine. You'll also need to install the required Python libraries. You can do this using `pip`.

## Required Libraries

To install the necessary libraries, run:

```bash
pip install scrapy requests pandas openpyxl xlsxwriter
```

# Project Structure

- ```items.py```: Contains the CarItem class, which defines the structure of the scraped data.
- ```middlewares.py```: Defines custom middlewares for handling proxies and request pausing.
- ```pipelines.py```: Contains the CarDataPipeline class for processing and storing the scraped data in an SQLite database.
- ```polovniautomobili_extraction.py```: Includes functions for extracting specific details from the car listings.
- ```settings.py```: Configures the Scrapy settings for the project, including middlewares, pipelines, and request settings.
- ```utils.py```: Provides utility functions for handling brand models, URL construction, and data sanitization.
- ```spiders/pa_spider.py```: Contains the PolovniAutomobiliSpider class, which defines how to scrape data from the website.

## Getting Started

### Clone the Repository

Clone this repository to your local machine:
```bash
git clone https://github.com/nenad992/car_scraper.git
```
### Install Dependencies

> Install the required Python libraries:
```bash
pip install scrapy requests pandas openpyxl xlsxwriter
```
### Configure Settings

Update the ```settings.py``` file if necessary to adjust configurations such as the number of concurrent requests or user agents.

### Run the Spider

To start scraping, run the following command:
```bash
scrapy crawl polovniautomobili -a bm=1
```
The ```-a bm=1``` argument specifies which brand models to scrape. Adjust the number as needed to target different brands/models.

or

Run via ```runner.py```

### Usage

The spider will scrape car listing data and store it in an SQLite database named ```car_data.db```. Each car's data is inserted or updated in the database, depending on whether the car ID already exists.

### Customization

- Proxies: Configure your proxy list URL in the ```settings.py``` to use custom proxies.
- Data Extraction: Modify the functions in ```polovniautomobili_extraction.py``` if the structure of the listings page changes.
- Database Schema: Adjust the CarDataPipeline in ```pipelines.py``` to change the database schema or handle additional fields.

### Troubleshooting

Issues Fetching Proxies: Ensure that the ```PROXY_LIST_URL``` in ```settings.py``` is correct and reachable. The current implementation is just an example and the list is not accurate.
No Listings Found: Verify the URL and ensure that the structure of the page has not changed. Check the Scrapy logs for more details.
