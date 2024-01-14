import requests
import json
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Foursquare API key
client_id = "fsq34aNO4SAETJI3XkmqJGQVRvgigpo3pq+pboj6FNRkzNU="

# Türkiyedeki şehirlerin verisetini yüklüyoruz
turkey_cities_df = pd.read_excel("turkey_cities.xlsx")
turkey_cities = set(turkey_cities_df["Şehir"].str.lower())

# Kategorilerimizin Listesi
categories = [
    "Restoran", "Kafe", "Bar", "Gecekulübü", "Müze", "Sanat galerisi", "Park", "Plaj", "Alışveriş merkezi",
    "Sinema", "Tiyatro", "Konser", "Spor", "Yüzmehavuzu", "Sauna", "Masaj", "Kuaför",
    "Güzellik salonu", "Dişçi", "Doktor", "Eczane", "Hastane", "Veteriner", "Otel", "Motel", "Pansiyon",
    "Kamp alanı"
]


#Uygulama çalıştırıldığında terminalde daha güzel bir karşılama için ASCII Art bastırdık
with open("karsilama.txt", "r") as file:
    ascii_art = file.read()

print(ascii_art)
print("Mekan Öneri Sistemine Hoş Geldiniz... ")

# Kategori listesini kullanıcıya göster
print("Kategoriler:")
for i, category in enumerate(categories):
    print(f"## {i + 1}. {category}")

def get_city_from_user_input(user_input):
    # Kullanıcı inputuna Tokenize işlemi
    tokens = word_tokenize(user_input)

    # Tokenlardan stopword leri çıkartıyoruz
    stop_words = set(stopwords.words("turkish"))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Kullanıcı girdisinde ki şehri, verisetinde ki şehirler arasında buluyoruz
    city = next((city for city in filtered_tokens if city in turkey_cities), None)

    return city.capitalize() if city else None

def get_category_from_user_input(user_input):
    # Kullanıcı inputuna Tokenize işlemi
    tokens = word_tokenize(user_input)

    # Tokenlardan stopword leri çıkartıyoruz
    stop_words = set(stopwords.words("turkish"))
    filtered_tokens = [word.capitalize() for word in tokens if word.lower() not in stop_words]

    # Tanımlanan kategori listesinden kullanıcı girdisinde ki kategoriyi bul
    category = next((category for category in filtered_tokens if category in categories), None)

    return category

# Kullanıcıdan doğal bir dil ile şehir ve kategori bilgisi alma işlemi
user_input = input("Şehir ve kategori seçiniz (örneğin: İstanbul'da bir restoran): ")

# Kullanıcı girdisinden şehir ve kategori doğal dil işlemeyle alındı ve tanımlandı
city = get_city_from_user_input(user_input)
category = get_category_from_user_input(user_input)

# Eğer şehir işlenirken bir sorun olursa kullanıcıdan şehir bilgisi tekrar alınır
if not city:
    city = input("Hangi şehirde arama yapmak istediğinizi belirtin (örneğin: Ankara): ").capitalize()

# Eğer kategori işlenirken bir sorun olursa kullanıcıdan kategori bilgisi tekrar alınır
if not category:
    category = input("Hangi kategoride arama yapmak istediğinizi belirtin (örneğin: Kafe): ").capitalize()

# Foursquare API kullanımı
url = "https://api.foursquare.com/v3/places/search"
headers = {
    "Authorization": "fsq34aNO4SAETJI3XkmqJGQVRvgigpo3pq+pboj6FNRkzNU="
}
params = {
    
    #"query": category,
    "query" : category,
    "fields" : "fsq_id,name,rating,location,categories,popularity",
    "near": city,
    "sort" : "RATING",
    "sort" : "RELEVANCE",
    "limit": 10,
    #"sort" : "relevance"
    
}

# API isteği yapılır
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    exit()

# API den dönen JSON parsellenir
try:
    data = json.loads(response.text)
except json.decoder.JSONDecodeError as e:
    print(f"An error occurred: {e}")
    exit()

# Sonuçlar yazdırılır
if "results" in data:
    print(f"{city} şehrindeki en iyi 10 {category}  :")
    for venue in data["results"]:
        address = venue['location'].get('formatted_address') or "Adres bilgisi bulunamadı"
        rating = venue.get('rating', "Puanlanmamış")
        print(f"--> {venue['name']} | Adres : {address} | Ortalama Puan :  {rating}")
else:
    print("Sonuç bulunamadı.")
