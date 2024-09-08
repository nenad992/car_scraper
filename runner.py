import subprocess
import time
import random
from car_data_extraction.utils import brand_models

# Function to run the scraper and measure time
def run_scraper(index):
    start_time = time.time()
    subprocess.run(['scrapy', 'crawl', 'polovniautomobili', '-a', f'bm={index}'])
    end_time = time.time()
    return end_time - start_time

# List of brand indices
brands = list(range(1, len(brand_models) + 1))

# Shuffle the list of brands
random.shuffle(brands)

# Track total time including pauses and total scraping time
total_scraping_time = 0
start_script_time = time.time()

for index in brands:
    # Run the scraper and get the time taken
    scraping_time = run_scraper(index)
    total_scraping_time += scraping_time
    # Pause for a random duration between spiders
    pause_duration = random.uniform(60, 300)  # Pause for 1 to 5 minutes 
    print(f"Pausing for {pause_duration:.2f} seconds before next brand and model...")
    time.sleep(pause_duration)

end_script_time = time.time()
total_time = end_script_time - start_script_time

# Print the results
print(f"Total time including pauses: {total_time:.2f} seconds")
print(f"Total scraping time (excluding pauses): {total_scraping_time:.2f} seconds")
