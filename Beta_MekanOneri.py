import requests
import json

# Foursquare API credentials
client_id = "fsq34aNO4SAETJI3XkmqJGQVRvgigpo3pq+pboj6FNRkzNU="
client_secret = ""  # Not needed for v3 API

# List of Turkish categories
categories = [
    "Restoran",
    "Kafe",
    "Bar",
    "Gece kulübü",
    "Müze",
    "Sanat galerisi",
    "Park",
    "Plaj",
    "Alışveriş merkezi",
    "Sinema",
    "Tiyatro",
    "Konser salonu",
    "Spor salonu",
    "Yüzme havuzu",
    "Sauna",
    "Masaj salonu",
    "Kuaför",
    "Güzellik salonu",
    "Dişçi",
    "Doktor",
    "Eczane",
    "Hastane",
    "Veteriner kliniği",
    "Otel",
    "Motel",
    "Pansiyon",
    "Kamp alanı",
    "Karavan parkı"
]

# Print the list of categories
print("Kategoriler:")
for i, category in enumerate(categories):
    print(f"{i + 1}. {category}")

# Get the user's location
city = input("Şehir Seçiniz: ")

# Get the user's desired category
category_index = int(input("Kategori Seçiniz (1-{}): ".format(len(categories))))
category = categories[category_index - 1]

# Build the Foursquare API request URL
url = "https://api.foursquare.com/v3/places/search"
headers = {
    "Authorization": "fsq34aNO4SAETJI3XkmqJGQVRvgigpo3pq+pboj6FNRkzNU="
}
params = {
    "near": city,
    "query": category,
    "limit": 5
    
}

# Make the API request
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    exit()

# Parse the JSON response
try:
    data = json.loads(response.text)
except json.decoder.JSONDecodeError as e:
    print(f"An error occurred: {e}")
    exit()

# Print the results
if "results" in data:
    print("En iyi 5 mekan:")
    for venue in data["results"]:
        address = venue['location'].get('formatted_address')
        
        if address:
            print(f"{venue['name']} | {address}")
        else:
            print(f"{venue['name']} : No address available ")
else:
    print("No results found.")