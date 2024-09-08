import re
import pandas as pd
import hashlib
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareType

# List of available brands
'''
brand_models = {
        'alfa-romeo': [
            "33", "145", "146", "147", "155", "156", "156-crosswagon", "159", "164",
            "166", "alfasud", "brera", "giulia", "giulietta", "gt", "gtv", "mito",
            "spider", "sprint", "stelvio", "tonale", "ostalo"
        ],
        'audi': [
            "80", "90", "100", "200", "a1", "a2", "a3", "a4", "a4-allroad", "a5", 
            "a6", "a6-allroad", "a7", "a8", "e-tron", "e-tron-gt", "q2", "q3", 
            "q4-e-tron", "q5", "q7", "q8", "q8-e-tron", "r8", "rs3", "rs4", 
            "rs5", "rs6", "rs7", "rs-e-tron-gt", "rs-q3", "rs-q8", "s1", "s3", 
            "s4", "s5", "s6", "s7", "s8", "sq5", "sq7", "sq8", "tt", "tts", 
            "v8", "ostalo"
        ],
        'bentley': [
            'bentayga', 'continental', 'mulsanne', 'ostalo' 
        ],
        'bmw': [
            "serija-1", "114", "116", "118", "120", "123", "125", "128ti", "m-135i", 
            "serija-2", "214", "216", "218", "220", "225", "m-235i", "m-240i", 
            "serija-3", "315", "316", "318", "318-gt", "320", "320-gt", "324", 
            "325", "325-gt", "328", "328-gt", "330", "330-gt", "335", "340i", 
            "m-340i", "compact", "serija-4", "418", "420", "425", "428", "430", 
            "435", "m440i", "serija-5", "518", "520", "520-gt", "523", "524", 
            "525", "528", "530", "530-gt", "535", "535-gt", "540", "545", "550", 
            "m550", "m-550i", "serija-6", "620-gt", "630", "630-gt", "633", "635", 
            "640", "645", "650", "serija-7", "725", "728", "730", "735", "740", 
            "745", "750", "760", "m760e", "serija-8", "840", "m-850i", "serija-i", 
            "i3", "i4", "i5", "i8", "ix", "ix1", "ix3", "serija-m", "m2", "m3", 
            "m4", "m5", "m6", "m8", "x3-m", "x4-m", "x5-m", "x6-m", "z4-m", 
            "serija-x", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "xm", 
            "serija-z", "z4", "ostalo"
        ],
        'chery': [
            'ego', 'fx', 'tiggo', 'ostalo'
        ],
        'chevrolet': [
            "aveo", "blazer", "camaro", "captiva", "corvette", "cruze", "epica",
            "evanda", "kalos", "lacetti", "lumina", "matiz", "nubira", "orlando",
            "spark", "suburban", "tacuma", "trailblazer", "trax", "ostalo"
        ],
        'citroen': [
            "2cv", "ami", "ax", "berlingo", "bx", "c-crosser", "c-elysee", 
            "c-zero", "c1", "c2", "c3", "c3-aircross", "c3-picasso", "c3-pluriel", 
            "e-c4", "c4", "c4-aircross", "c4-cactus", "c4-grand-picasso", 
            "c4-grand-spacetourer", "c4-picasso", "c4-spacetourer", "c4x", "c5", 
            "c5-aircross", "c5x", "c6", "c8", "c15", "cx", "ds", "ds3", "ds4", 
            "ds5", "ds7", "dyane", "evasion", "jumpy", "nemo", "saxo", "xantia", 
            "xm", "xsara", "xsara-picasso", "zx", "ostalo"
        ],
        'dacia': [
        'dokker', 'duster', 'jogger', 'lodgy', 'logan', 'pickup', 'sandero', 'solenza',
        'spring', stepway', 'super-nova', 'ostalo'
        ]
        'ford': [
            "b-max", "c-max", "capri", "cortina", "courier", "ecosport",
            "edge", "escort", "expedition", "explorer", "falcon", "festiva",
            "fiesta", "focus", "fusion", "galaxy", "granada", "grand-c-max",
            "ka", "ka+", "kuga", "maverick", "mondeo", "mustang", "orion",
            "probe", "puma", "ranger", "s-max", "scorpio", "xierra",
            "street-ka", "Taunus", "taurus", "tourneo", "tourneo-connect",
            "tourneo-courier", "tourneo-custom", "ostalo"
        ],
        'fiat': [
            "125", "126", "127", "131", "500", "500e", "500c", "500l", "500x",
            "600", "850", "1107", "albea", "brava", "bravo", "campagnola", 
            "cinquecento", "coupe", "croma", "doblo", "evo", "fiorino", 
            "freemont", "fullback", "grande-punto", "idea", "linea", "marea", 
            "marengo", "multipla", "palio", "panda", "punto", "qubo", 
            "regata", "scudo", "sedici", "seicento", "spider-europa", 
            "stilo", "tempra", "tipo", "ulysse", "uno", "ostalo"
        ],
        'honda': [
            "accord", "civic", "concerto", "cr-v", "cr-z", "crx", "fr-v", 
            "hr-v", "insight", "jazz", "legend", "prelude", "shuttle", 
            "stream", "zr-v", "ostalo"
        ],
        'hyundai': [
            "accent", "atos", "bayon", "coupe", "elantra", "galloper", 
            "genesis", "getz", "h-1", "i10", "i20", "i30", "i40", 
            "ioniq", "ioniq-5", "ioniq-6", "ix20", "ix35", "ix55", 
            "kona", "lantra", "matrix", "pony", "santa-fe", "santamo", 
            "sonata", "sonica", "staria", "terracan", "trajet", 
            "tucson", "veloster", "venue", "ostalo"
        ],
        'jaguar': [
            "e-pace", "f-type", "f-pace", "i-pace", "s-type", "x-type", 
            "xe", "xf", "xj", "xj6", "xj40", "xk", "xkr", "ostalo"
        ],
        'jeep': [
            "avenger", "cherokee", "commander", "compass", "grand-cherokee", 
            "liberty", "patriot", "renegade", "willys", "wrangler", "ostalo"
        ],
        'kia': [
            "carens", "carnival", "ceed", "ceed-sw", "cerato", "ev6", 
            "magentis", "niro", "optima", "picanto", "pride", "pro-ceed", 
            "rio", "sephia", "shuma", "sorento", "soul", "spectra", 
            "sportage", "stonic", "venga", "xceed", "ostalo"
        ],
        'lada': [
            "110", "111", "112", "1200", "1300", "1500", "1600", 
            "2101", "2104", "2105", "2107", "granta", "kalina", 
            "niva", "samara", "vesta", "ostalo"
        ],
        'land-rover': [
            "defender", "discovery", "discovery-sport", "freelander",
            "range-rover", "range-rover-autobiography", "range-rover-evoque",
            "range-rover-sport", "range-rover-velar", "range-rover-vogue",
            "serija-ii", "serija-iii", "ostalo"
        ],
        'lexus': [
            "ct-200h", "es", "gs", "gs-300", "is", "is-200", "is-220",
            "ls", "ls-460", "ls-600h", "nx", "rx", "rx-300", "rx-400",
            "rx-450", "ux", "ostalo"
        ],
        'maserati': [
            "224", "4200", "ghibli", "granturismo", "grecale",
            "levante", "quattroporte", "ostalo"
        ],
        'mazda': [
            "2", "3", "5", "6", "121", "323", "626", "b-250",
            "bt-50", "cx-3", "cx-5", "cx-7", "cx-30", "cx-60",
            "demio", "mpv", "mx-5", "premacy", "rx-7", "rx-8",
            "serija-e", "tribute", "xedos", "ostalo"
        ],
        'mercedes-benz': [
            "180", "190", "a-klasa", "a-140", "a-150", "a-160", "a-170", "a-180",
            "a-190", "a-200", "a-210", "a-220", "a-250", "a-35-amg", "a-45-amg",
            "b-klasa", "b-150", "b-160", "b-170", "b-180", "b-200", "b-250",
            "c-klasa", "c-180", "c-200", "c-220", "c-230", "c-240", "c-250", "c-270",
            "c-280", "c-300", "c-320", "c-32-amg", "c-350", "c-350e", "c-43-amg",
            "c-63-amg", "citan", "cla-klasa", "cla-180", "cla-180-shooting-brake",
            "cla-200", "cla-200-shooting-brake", "cla-220", "cla-220-shooting-brake",
            "cla-250", "cla-35-amg", "cla-45-amg", "cl-klasa", "cl-500", "cl-600",
            "cl-65-amg", "clc-klasa", "clc-180", "clc-200", "clc-220", "cle-klasa",
            "cle-220d", "clk-klasa", "clk-200", "clk-220", "clk-230", "clk-240",
            "clk-270", "clk-320", "clk-350", "clk-430", "cls-klasa", "cls-220",
            "cls-220-shooting-brake", "cls-250", "cls-250-shooting-brake", "cls-280",
            "cls-300", "cls-320", "cls-350", "cls-350-shooting-brake", "cls-400",
            "cls-450", "cls-500", "cls-53-amg", "cls-55-amg", "e-klasa", "e-124",
            "e-200", "e-220", "e-230", "e-240", "e-250", "e-260", "e-270", "e-280",
            "e-290", "e-300", "e-320", "e-350", "e-400", "e-43-amg", "e-450",
            "e-53-amg", "e-63-amg", "eqa", "eqb", "eqc-400", "eqe", "eqs", "g-klasa",
            "g-290", "g-300", "g-320", "g-350", "g-400", "g-450", "g-500", "g-63-amg",
            "gl-klasa", "gl-320", "gl-350", "gl-420", "gl-450", "gl-55-amg",
            "gla-klasa", "gla-35-amg", "gla-45-amg", "gla-180", "gla-200", "gla-220",
            "gla-250", "glb-klasa", "glb-180", "glb-200", "glb-220", "glc-klasa",
            "glc-43-amg", "glc-63", "glc-200", "glc-220", "glc-250", "glc-300",
            "glc-350", "gle-klasa", "gle-43-amg", "gle-53-amg", "gle-63-amg",
            "gle-250", "gle-300", "gle-350", "gle-400", "gle-450", "glk-klasa",
            "glk-200", "glk-220", "glk-250", "glk-320", "glk-350", "gls-klasa",
            "gls-63-amg", "gls-350-d", "gls-400", "gls-450", "gls-580", "gls-600",
            "gt", "gt-klasa", "gt-43-amg", "gt-53-amg", "gt-63-amg", "gt-r", "gt-s",
            "ml-klasa", "ml-230", "ml-250", "ml-270", "ml-280", "ml-300", "ml-320",
            "ml-350", "ml-400", "ml-420", "ml-430", "ml-500", "ml-55-amg", "r-klasa",
            "r-320", "r-350", "s-klasa", "s-250", "s-280", "s-300", "s-320", "s-350",
            "s-400", "s-420", "s-450", "s-500", "s-550", "s-560-maybach", "s-580",
            "s-580-maybach", "s-63-amg", "sl-klasa", "sl-280", "sl-300", "sl-320",
            "sl-350", "sl-380", "sl-500", "sl-55-amg", "sl-600", "sl-63-amg",
            "sl-65-amg", "slk-klasa", "slk-200", "slk-230", "slk-250", "slk-320",
            "t-klasa", "v-klasa", "vaneo", "w123", "w124", "x-klasa", "ostalo"
        ],
        'mini': [
            "1000", "clubman", "cooper", "cooper-s", "countryman", "john-cooper-works",
            "paceman", "one", "ostalo"
        ],
        'mitsubishi': [
            "asx", "carisma", "colt", "eclipse", "eclipse-cross", "galant", "grandis",
            "i-miev", "l200", "lancer", "outlander", "pajero", "pajero-pinin", "pajero-sport",
            "sapporo", "space-star", "space-wagon", "ostalo"
        ],
        'nissan': [
            "100-nx", "350z", "almera", "almera-tino", "cube", "juke", "leaf", "micra",
            "murano", "navara", "note", "nv200", "pathfinder", "patrol", "pixo", "praire",
            "primera", "pulsar", "qashqai", "qashqai-+-2", "sunny", "terrano", "x-trail",
            "ostalo"
        ],
        'opel': [
            "adam", "agila", "ampera", "antara", "ascona", "astra", "astra-f", "astra-g",
            "astra-h", "astra-j", "astra-k", "astra-l", "calibra", "cascada", "combo",
            "corsa", "corsa-a", "corsa-b", "corsa-c", "corsa-d", "corsa-e", "corsa-f",
            "crossland-x", "frontera", "gt", "grandland-x", "insignia", "kadett", "karl",
            "manta", "meriva", "monterey", "mokka", "mokka-x", "olympia", "omega",
            "rekord", "senator", "signum", "tigra", "vectra", "vectra-a", "vectra-b",
            "vectra-c", "zafira", "ostalo"
        ],
        'peugeot': [
            "106", "107", "108", "204", "205", "206", "206-plus", "207", "208", "301",
            "305", "306", "307", "308", "309", "405", "406", "407", "408", "505",
            "508", "508-rxh", "607", "806", "807", "1007", "2008", "3008", "4007",
            "4008", "5008", "bipper", "expert", "ion", "partner", "ranch", "rcz", "rifter",
            "tepee", "ostalo"
        ],
        'porsche': [
            "718", "911", "944", "Boxster", "Cayenne", "Cayman", "Macan", "Panamera", 
            "Taycan", "ostalo"
        ],
        'renault': [
            "alpine-v6", "austral", "captur", "clio", "espace", "express", "fluence", 
            "grand-espace", "grand-modus", "grand-scenic", "kadjar", "kangoo", "koleos", 
            "laguna", "latitude", "megane", "megane-conquest", "modus", "nevada", "r-4", 
            "r-5", "r-8", "r-9", "r-10", "r-19", "r-21", "r-25", "rafale", "rapid", "rx", 
            "safrane", "scenic", "talisman", "thalia", "twingo", "twizy", "vel-satis", 
            "wind", "zoe", "ostalo"
        ],
        'rover': [
            "25", "45", "75", "200", "214", "216", "400", "414", "600", "620", 
            "streetwise", "ostalo"
        ],
        'saab': [
            "900", "9000", "9-3", "9-5", "ostalo"
        ],
        'seat': [
            "alhambra", "altea", "altea-xl", "arona", "arosa", "ateca", "cordoba",
            "exeo", "ibiza", "inca", "leon", "mii", "tarraco", "toledo", "ostalo"
        ],
        'subaru': [
            "crosstrek", "forester", "impreza", "justy", "legacy", "leone", "levorg",
            "outback", "trezia", "tribeca", "xv", "ostalo"
        ],
        'suzuku': [
            "alto", "baleno", "celerio", "grand-vitara", "ignis", "jimny", 
            "liana", "maruti", "sj-samurai", "splash", "swift", "sx4", 
            "sx4-s-cross", "vitara", "wagon-r+", "ostalo"
        ],
        'tesla': [
            "model-s", "model-3", "model-x", "model-y", "ostalo"    
        ],
        'toyota': [
            "4runner", "auris", "avensis", "aygo", "aygo-x", "c-hr", "camry", 
            "carina", "celica", "corolla", "corolla-cross", "corolla-verso", 
            "gt86", "highlander", "hilux", "iq", "land-cruiser", "mr2", 
            "paseo", "prius", "prius-plus", "prius-plug-in", "proace-city-verso", 
            "rav-4", "urban-cruiser", "verso", "verso-s", "yaris", "yaris-cross", 
            "yaris-verso", "ostalo"
        ],
        'volkswagen': [
            "amarok", "arteon", "bora", "buba", "nova-buba", "caddy", "corrado", 
            "cross-polo", "eos", "fox", "golf", "golf-1", "golf-2", "golf-3", 
            "golf-4", "golf-5", "golf-6", "golf-7", "golf-7-alltrack", "golf-8", 
            "golf-plus", "golf-sportsvan", "id3", "id4", "jetta", "lupo", 
            "multivan", "passat", "passat-b1", "passat-b2", "passat-b3", 
            "passat-b4", "passat-b5", "passat-b55", "passat-b6", "passat-b7", 
            "passat-b7-alltrack", "passat-b8", "passat-b8-alltrack", "passat-cc", 
            "phaeton", "polo", "scirocco", "sharan", "t-cross", "t-roc", 
            "taigo", "tiguan", "tiguan-allspace", "touareg", "touran", "up", 
            "vento", "ostalo"
        ],
        'volvo': [
            "240", "460", "740", "760", "850", "940", "c30", "c70", 
            "ex30", "s40", "s60", "s70", "s80", "s90", "v40", "v50", 
            "v60", "v60-cross-country", "v70", "v90", "v90-cross-country", 
            "xc40", "xc60", "xc70", "xc90", "ostalo"
        ],
        'zastava': [
            "10", "101", "128", "1300", "1500", "750", "850", "ar-55", 
            "florida", "florida-in", "koral", "koral-in", "poly", "skala-55", 
            "yugo", "yugo-45", "yugo-55", "yugo-60", "yugo-65", 
            "yugo-cabrio", "yugo-ciao", "yugo-in-l", "yugo-tempo", 
            "ostalo"
        ],
        'skoda': [
            "100", "110", "120", "1000-mb", "citigo", "enyaq", "fabia",
            "favorit", "felicia", "kamiq", "karoq", "kodiaq", "octavia",
            "praktik", "rapid", "roomster", "scala", "superb", "yeti",
            "ostalo"
        ]
}'''
brand_models = {
'ford': [
            "b-max", "c-max", "capri", "cortina", "courier", "ecosport",
            "edge", "escort", "expedition", "explorer", "falcon", "festiva",
            "fiesta", "focus", "fusion", "galaxy", "granada", "grand-c-max",
            "ka", "ka+", "kuga", "maverick", "mondeo", "mustang", "orion",
            "probe", "puma", "ranger", "s-max", "scorpio", "xierra",
            "street-ka", "Taunus", "taurus", "tourneo", "tourneo-connect",
            "tourneo-courier", "tourneo-custom", "ostalo"
        ],
}
def get_brand_models(index: int, brand_models = brand_models) -> dict: # 38 brands
    brands = list(brand_models.keys())
    # Check if the index is valid
    if 1 <= index <= len(brands):
        brand = brands[index - 1]
        return {brand: brand_models[brand]}  # Correct dictionary syntax
    else:
        return {}  # Return an empty dictionary if index is invalid
def url_constructor(brand, model, page=int) -> str:
    url = f'https://www.polovniautomobili.com/auto-oglasi/pretraga?page={page}&sort=basic&brand={brand}&model%5B0%5D={model}&city_distance=0&showOldNew=old&wheel_side=2630&damaged%5B0%5D=3799&damaged%5B1%5D=3798'
    return url

# Replace special chars like š, č, ć, etc.
def replace_special_chars(text):
    # Define a mapping from special characters to their Latin equivalents
    special_chars = {
        'š': 's', 'ć': 'c', 'č': 'c', 'ž': 'z', 'đ': 'd', 'dž': 'dz',
        'Š': 'S', 'Ć': 'C', 'Č': 'C', 'Ž': 'Z', 'Đ': 'D', 'Dž': 'Dz',
        # Add more mappings if needed
    }
    
    # Replace each special character in the text
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    
    return text

# Function to extract numeric values from text
def extract_numeric(text):
    return re.sub(r'\D', '', text)  # Remove non-numeric characters

# Save the data to excel
def save_brand_data_to_excel(brand_data, brand):
    """
    Save data for each model of a brand to a single Excel file with separate sheets.

    Parameters:
    - brand_data (dict): Dictionary where keys are model names and values are DataFrames containing the data for each model.
    - brand (str): The brand name to be used in the Excel filename.
    """
    excel_filename = f'car_listings_{brand}.xlsx'
    
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        for model, df in brand_data.items():
            df.to_excel(writer, sheet_name=model, index=False)
    
    print(f"Excel file '{excel_filename}' with sheets for each model created successfully.")

# Creating 8 char ID from last part of the URL
def extract_id_from_url(url): 
    # Extract the last part of the URL after the last '/'
    last_part = url.split('/')[-1]
    
    # Generate a SHA-256 hash of the last part
    hash_object = hashlib.sha256(last_part.encode())
    
    # Convert the hash to a hexadecimal string and take the first 8 characters
    hex_id = hash_object.hexdigest()[:8]
    
    return hex_id

def sanitize_table_name(name):
    # Replace invalid characters with underscores
    sanitized_name = re.sub(r'[^\w]+', '_', name)  # Replace non-alphanumeric characters with underscores
    return sanitized_name


# NOT IN USE user agent generator from a github
def user_agent_generator():
    #software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
    #operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.IOS.value, OperatingSystem.ANDROID.value, OperatingSystem.CHROMEOS.value]
    software_type = [SoftwareType.APPLICATION.value, SoftwareType.WEB_BROWSER.value, SoftwareType.BROWSER__IN_APP_BROWSER.value]

    user_agent_rotator = UserAgent(limit=10)

    # Get list of user agents.
    user_agents = user_agent_rotator.get_user_agents()
    
    return user_agents