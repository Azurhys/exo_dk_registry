import argparse
import requests
from bs4 import BeautifulSoup
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

class CryptoScraper:
    def __init__(self, url):
        self.url = os.getenv("URL", "https://coinmarketcap.com/fr/")
        self.verbose = os.getenv("VERBOSE", False)

    def scrape_data(self, verbose=False):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        elements = soup.find_all('tr', class_=lambda value: value and 'sc-' in value)
        cursor_pointer_elements = self.get_elements_with_cursor_pointer()

        elements += cursor_pointer_elements

        self.filtered_elements = []
        seen_markets = set()

        for element in elements:
            crypto_name = element.find('a', class_='cmc-link').text.strip()

            if 'cursor:pointer' in element.get('style', ''):
                price = element.find_all('td')[3].text.strip()
                crypto_market = element.find_all('td')[-2].text.strip() 
            else:
                price = element.find_all('td')[-2].text.strip()
                crypto_market = element.find('a', class_='cmc-link')['href'].split('/')[-2].capitalize()

            if crypto_market not in seen_markets:
                self.filtered_elements.append((crypto_name, price, crypto_market))
                seen_markets.add(crypto_market)

        if self.verbose:
            for crypto_name, price, crypto_market in self.filtered_elements:
                print(crypto_name, price, crypto_market)
            print("Data scraped successfully.")

    def get_elements_with_cursor_pointer(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        elements = soup.find_all('tr', style=lambda style: style and 'cursor:pointer' in style)
        return elements

    def save_to_database(self, verbose=False):
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password="example",
            database="scrap"
        )
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS crypto_info')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price VARCHAR(255),
                market VARCHAR(255)
            )
        ''')
        for element in self.filtered_elements:   
            cursor.execute('INSERT INTO crypto_info (name, price, market) VALUES (%s, %s, %s)', element)
        conn.commit()
        conn.close()
        if self.verbose:
            print("Data saved to database successfully.")

    def analyze_data(self):
        total_elements = len(self.filtered_elements)
        print("Nombre total d'éléments :", total_elements)

        prices = []
        for element in self.filtered_elements:
            price_str = element[1].replace('$', '').replace(',', '') 
            if '€' in price_str:
                price_str = str(float(price_str.replace('€', '')) * 1.18)
            prices.append(float(price_str))

        print("Format des prix des jetons :", type(prices[0]))

        ranks = np.arange(1, total_elements + 1)
        prices_sorted = sorted(prices, reverse=True)  
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"graph_{date_time}.png"

        plt.figure(figsize=(10, 6))
        plt.scatter(ranks, prices_sorted, color='blue', alpha=0.5)
        plt.title(f'Relation entre le rang et le prix du jeton le {date_time}')
        plt.xlabel('Rang (capitalisation boursière)')
        plt.ylabel('Prix du jeton ($)')
        plt.xlim(1, total_elements + 1)
        plt.yscale('log')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.savefig(f'/app/graphs/{file_name}')
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Scraping crypto data from CoinMarketCap and analyzing it.")
    parser.add_argument("--url", default="https://coinmarketcap.com/fr/", help="URL to scrape data from")
    parser.add_argument("--v", action="store_true", help="Verbose mode to print additional information")
    args = parser.parse_args()

    scraper = CryptoScraper(args.url)
    scraper.scrape_data(args.v)
    scraper.save_to_database(args.v)
    scraper.analyze_data()

if __name__ == "__main__":
    main()
