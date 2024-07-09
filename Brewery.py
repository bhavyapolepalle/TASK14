from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

class BreweryInfo:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_breweries_by_state(self, state):
        response = requests.get(f"{self.base_url}/breweries?by_state={state}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def list_breweries_in_states(self, states):
        breweries = {}
        for state in states:
            breweries[state] = self.fetch_breweries_by_state(state)
        return breweries

    def count_breweries_in_states(self, states):
        breweries = self.list_breweries_in_states(states)
        return {state: len(breweries[state]) for state in states}

    def count_breweries_in_cities(self, state):
        breweries = self.fetch_breweries_by_state(state)
        city_counts = {}
        for brewery in breweries:
            city = brewery.get('city', 'Unknown')
            city_counts[city] = city_counts.get(city, 0) + 1
        return city_counts

    def count_breweries_with_websites(self, states):
        breweries = self.list_breweries_in_states(states)
        website_counts = {}
        for state, brewery_list in breweries.items():
            count = sum(1 for brewery in brewery_list if brewery.get('website_url'))
            website_counts[state] = count
        return website_counts

# Create an instance of BreweryInfo
brewery_url = "https://api.openbrewerydb.org"
brewery_info = BreweryInfo(brewery_url)

states = ["Alaska", "Maine", "New York"]

# List names of all breweries in Alaska, Maine, and New York
print("Breweries in Alaska, Maine, and New York:")
breweries = brewery_info.list_breweries_in_states(states)
for state, brewery_list in breweries.items():
    print(f"\nBreweries in {state}:")
    for brewery in brewery_list:
        print(brewery.get('name', 'N/A'))

# Count of Breweries in each state
print("\nCount of Breweries in each state:")
brewery_counts = brewery_info.count_breweries_in_states(states)
for state, count in brewery_counts.items():
    print(f"{state}: {count}")

# Count of Breweries in each city of the states
print("\nCount of Breweries in each city of the states:")
for state in states:
    city_counts = brewery_info.count_breweries_in_cities(state)
    print(f"\nBreweries in {state} by City:")
    for city, count in city_counts.items():
        print(f"{city}: {count}")

# Count of Breweries with websites in each state
print("\nCount of Breweries with websites in each state:")
website_counts = brewery_info.count_breweries_with_websites(states)
for state, count in website_counts.items():
    print(f"{state}: {count}")