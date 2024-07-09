from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

class CountryData:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            print("Failed to retrieve data")
            self.data = []

    def display_countries_and_currencies(self):
        if self.data:
            for country in self.data:
                name = country.get('name', {}).get('common', 'Unknown')
                currencies = country.get('currencies', {})
                for currency_code, currency_info in currencies.items():
                    currency_name = currency_info.get('name', 'Unknown')
                    currency_symbol = currency_info.get('symbol', 'Unknown')
                    print(f"Country: {name}, Currency: {currency_name}, Symbol: {currency_symbol}")

    def display_countries_with_currency(self, currency_name):
        if self.data:
            for country in self.data:
                currencies = country.get('currencies', {})
                for currency_info in currencies.values():
                    if currency_info.get('name') == currency_name:
                        print(country.get('name', {}).get('common', 'Unknown'))

    def display_countries_with_dollar(self):
        self.display_countries_with_currency("Dollar")

    def display_countries_with_euro(self):
        self.display_countries_with_currency("Euro")

# Using the class
url = "https://restcountries.com/v3.1/all"
country_data = CountryData(url)
country_data.fetch_data()

print("All countries with their currencies and symbols:")
country_data.display_countries_and_currencies()
print("\nCountries using Dollar as currency:")
country_data.display_countries_with_dollar()
print("\nCountries using Euro as currency:")
country_data.display_countries_with_euro()