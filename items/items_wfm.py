import requests
import csv

url = "https://api.warframe.market/v2/items"
lang = 'en' 

headers = {
    "Language": [lang]  # ["ch_sim", "en"] # ["ch_tra", "en"]
}

response = requests.get(url, headers=headers)
data = response.json()

items = data.get("data", [])

with open(f'items_{lang}.csv', "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # headers
    writer.writerow([lang, "slug"])
    
    for item in items:
        i18n = item.get("i18n", {})
        name_es = i18n.get(lang, {}).get("name", "")
        slug = item.get("slug", "")
        
        if name_es and slug:
            writer.writerow([name_es.lower(), slug])

print(f'items_{lang}.csv')