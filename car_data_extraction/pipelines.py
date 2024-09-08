import sqlite3
from scrapy.exceptions import DropItem
from car_data_extraction.utils import sanitize_table_name

class CarDataPipeline:
    def open_spider(self, spider):
        # Open a connection to the database
        self.conn = sqlite3.connect('car_data.db')
        self.cursor = self.conn.cursor()

        # Function to check if a column exists
        def column_exists(table_name, column_name):
            query = f"PRAGMA table_info({table_name});"
            self.cursor.execute(query)
            columns = self.cursor.fetchall()
            return any(column[1] == column_name for column in columns)

        # Iterate over all tables and add 'ad_available' column if it doesn't exist
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(tables_query)
        tables = self.cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Check if the table is related to car listings
            if '_listings' in table_name:
                if not column_exists(table_name, 'ad_available'):
                    # Add the 'ad_available' column if it doesn't exist
                    self.cursor.execute(f"""
                        ALTER TABLE {table_name}
                        ADD COLUMN ad_available TEXT;
                    """)
                    print(f"Added 'ad_available' column to table: {table_name}")

                # Mark all records as "EXPIRED" in the ad_available column
                self.cursor.execute(f"UPDATE {table_name} SET ad_available = 'EXPIRED'")
                print(f"Marked all entries as EXPIRED in ad_available column in table: {table_name}")

        self.conn.commit()

    def close_spider(self, spider):
        # Commit changes and close the database connection
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        brand = item['brand']
        sanitized_brand = sanitize_table_name(brand)
        table_name = f"{sanitized_brand}_listings"

        # Create the table if it doesn't exist
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                model TEXT,
                title TEXT NOT NULL,
                current_price INTEGER,
                old_price INTEGER,
                currency TEXT,
                mileage INTEGER,
                location TEXT,
                year_produced TEXT,
                car_type TEXT,
                posted_date TEXT,
                fuel TEXT,
                ccm INTEGER,
                kw INTEGER,
                hp INTEGER,
                url TEXT,
                scraped TEXT,
                ad_available TEXT
            );
        """)

        # Check if the record already exists
        self.cursor.execute(f"SELECT current_price FROM {table_name} WHERE id = ?", (item['id'],))
        result = self.cursor.fetchone()

        if result:
            current_price = result[0]

            # Update if the price has changed
            if current_price != item['current_price']:
                self.cursor.execute(f"""
                    UPDATE {table_name} 
                    SET old_price = current_price, 
                        current_price = ?, 
                        model = ?, 
                        title = ?, 
                        currency = ?, 
                        mileage = ?, 
                        location = ?, 
                        year_produced = ?, 
                        car_type = ?, 
                        posted_date = ?, 
                        fuel = ?, 
                        ccm = ?, 
                        kw = ?, 
                        hp = ?, 
                        url = ?, 
                        scraped = ?, 
                        ad_available = ''
                    WHERE id = ?;
                """, (
                    item['current_price'], item['model'], item['title'], item['currency'], item['mileage'], item['location'], 
                    item['year_produced'], item['car_type'], item['posted_date'], item['fuel'], item['ccm'], 
                    item['kw'], item['hp'], item['url'], item['scraped'], item['id']
                ))
            else:
                # Update only the scraped and ad_available fields if the price hasn't changed
                self.cursor.execute(f"""
                    UPDATE {table_name} 
                    SET scraped = ?, 
                        ad_available = ''
                    WHERE id = ?;
                """, (item['scraped'], item['id']))
        else:
            # Insert a new record
            self.cursor.execute(f"""
                INSERT INTO {table_name} (
                    id, model, title, current_price, old_price, currency, mileage, location, 
                    year_produced, car_type, posted_date, fuel, ccm, kw, hp, url, scraped, ad_available
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '');
            """, (
                item['id'], item['model'], item['title'], item['current_price'], None, item['currency'], 
                item['mileage'], item['location'], item['year_produced'], item['car_type'], 
                item['posted_date'], item['fuel'], item['ccm'], item['kw'], item['hp'], item['url'], item['scraped']
            ))

        # Commit changes to the database
        self.conn.commit()

        return item
