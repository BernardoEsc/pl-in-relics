import json
import requests
import time 

url = "https://api.warframe.market/v2/items"

langs = [
    "ko", "ru", "de", "fr", "pt", "zh-hans", 
    "zh-hant", "es", "it", "pl", "uk", "en",
]


for lang in langs:
    headers = {
        "Language": lang
    }   

    response = requests.get(url, headers=headers)
    data = response.json()

    items = data.get("data", [])

    lang = "ch_sim" if lang == "zh-hans" else lang  # change for EasyOCR
    lang = "ch_tra" if lang == "zh-hant" else lang  # change for EasyOCR
    dic = {}
    for item in items:
        i18n = item.get("i18n", {})
        name = i18n.get(lang, {}).get("name", "")
        slug = item.get("slug", "")
        
        if name and slug and "prime" in slug and not "set" in slug:
            dic[name.lower()] = slug

    with open(f'items_{lang}.json', "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)

    print(f'items_{lang}.json')
    time.sleep(1) 