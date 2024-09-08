from car_data_extraction.utils import replace_special_chars, extract_numeric
import re

# Extracting and using 8 num ID from the URL of polovniautomobili
def extract_id_from_url_polovniautomobili(url):
    """
    Extracts the 8-digit numeric ID from the URL.
    
    Args:
        url (str): The URL string from which to extract the ID.
    
    Returns:
        str: The extracted 8-digit numeric ID.
    """
    # Use regex to find an 8-digit numeric sequence in the URL
    match = re.search(r'/(\d{8})/', url)
    
    if match:
        return match.group(1)  # Return the first 8-digit match found
    else:
        print("No 8-digit ID found in the URL.")
        return None

# Function to extract mileage robustly using multiple locators
def extract_car_id(listing):
    id = extract_id_from_url_polovniautomobili('https://www.polovniautomobili.com' + listing.find('a')['href'])
    return id
def extract_mileage(listing):
    mileage_text = ""
    # Try multiple approaches to find the mileage
    try:
        # Primary locator
        mileage_text = listing.find('div', class_='setInfo').find_next_sibling('div', class_='setInfo').find('div', class_='top').get_text(strip=True)
    except AttributeError:
        try:
            # Alternative locator strategy if structure changes
            mileage_text = listing.find('div', class_='mileage').get_text(strip=True)
        except AttributeError:
            try:
                # Fallback locator strategy
                mileage_text = listing.find('span', class_='mileage-info').get_text(strip=True)
            except AttributeError:
                print("Mileage not found for this listing.")
    # Extract only the numeric part and return as an integer
    mileage = int(''.join(filter(str.isdigit, mileage_text))) if mileage_text else 0
    return mileage
def extract_title(listing):
    # Extract data fields with multiple locators
    title = listing.find('h2') or listing.find('h3') or listing.find('a', class_='ga-title')
    title = title.get_text(strip=True).replace("\t", "").strip() if title else 'Unknown Title'
    return title
def extract_posted_date(listing):
    # Extract the renewed date
    renewed_date = listing.get('data-renewdate', '').strip()
    return renewed_date
def extract_fuel_ccm(listing):
    fuel_and_ccm = listing.find('div', class_='setInfo')
    fuel_and_ccm = fuel_and_ccm.find('div', class_='bottom') if fuel_and_ccm else None
    fuel_and_ccm = fuel_and_ccm.get('title', '') if fuel_and_ccm else ''
    fuel_type, ccm = fuel_and_ccm.split('|') if '|' in fuel_and_ccm else (fuel_and_ccm, '')
    ccm = ''.join(filter(str.isdigit, ccm)).strip()[:-1]  # Clean and convert cubic capacity
    ccm = int(ccm) if ccm else 0
    return fuel_type, ccm
def extract_kw_hp(listing):
    # Extract horsepower and kilowatt
    hp_kw_info = listing.find_all('div', class_='setInfo')
    hp_kw_info = hp_kw_info[1].find('div', class_='bottom').get('title', '') if len(hp_kw_info) > 1 else ''
    kw = ''.join(filter(str.isdigit, hp_kw_info.split('(')[0].strip()))
    kw = int(kw) if kw else 0
    hp = hp_kw_info.split('(')[1].replace('KS)', '').strip() if '(' in hp_kw_info else ''
    hp = int(''.join(filter(str.isdigit, hp))) if hp else 0
    return kw, hp
def extract_year_type(listing):
    info_div = listing.find('div', class_='setInfo')
    top_div = info_div.find('div', class_='top') if info_div else None
    text = top_div.get_text(strip=True) if top_div else ''
    year_type = text.split('.', 1) if '.' in text else [text, '']
    year = year_type[0].strip() if len(year_type) > 0 else ''
    car_type = replace_special_chars(year_type[1].strip()) if len(year_type) > 1 else ''
    return year, car_type 
def extract_price(listing):
    price_text = ""
    
    try:
        # Check the data-price attribute first
        data_price = listing.get('data-price')
        if data_price:
            price_text = data_price
        else:
            # Try primary locator for discount price
            price_discount = listing.find('span', class_='priceDiscount')
            if price_discount:
                price_text = price_discount.get_text(strip=True)
            else:
                # Alternative locators
                price_container = listing.find('div', class_='price')
                if price_container:
                    price_elements = price_container.find_all('span')
                    if price_elements:
                        price_text = price_elements[0].get_text(strip=True)
                    else:
                        price_text = price_container.get_text(strip=True)
    except AttributeError:
        print("Price not found using primary locators.")

    # Clean up the price string by removing unwanted characters
    price_text = price_text.replace("\t", "").strip()

    # Extract the numeric value
    str_price = extract_numeric(price_text)

    # Convert to integer, handling errors and filtering high values
    try:
        price = int(str_price) if str_price else 0
    except ValueError:
        price = 0

    # Handle cases where the price is unusually high (Optional)
    if price > 200000:
        price = 0

    return price


def extract_location(listing):
    location = listing.find('div', class_='city')
    location = replace_special_chars(location.get_text(strip=True) if location else 'Unknown Location')
    return location

# Main function to extract car details and instantiate the Car class
def extract_car_details(listing):
    car_id = extract_car_id(listing)
    title = extract_title(listing)
    price = extract_price(listing)
    currency = "EUR"
    old_price = 0
    mileage = extract_mileage(listing)
    location = extract_location(listing)
    year, car_type = extract_year_type(listing)
    posted_date = extract_posted_date(listing)
    fuel_type, ccm = extract_fuel_ccm(listing)
    kw, hp = extract_kw_hp(listing)
    url = 'https://www.polovniautomobili.com' + listing.find('a')['href']

    # Create an tuple of a car
    car = (
        car_id, 
        title,
        price,
        old_price,
        currency,
        mileage,
        location,
        year,
        car_type,
        posted_date,
        fuel_type,
        ccm,
        kw,
        hp,
        url
    )
    return car