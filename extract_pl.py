from ultralytics import YOLO
from difflib import get_close_matches
from typing import Dict, List, Tuple
import cv2
import easyocr
import json
import mss
import numpy as np
import os
import requests
import tempfile

class Extract_pl():
    def __init__(self, lang: List[str]) -> None:
        self.__model__ = YOLO("model/best.pt")
        self.__lang__: List[str] = lang
        self.__reader__ = easyocr.Reader(self.__lang__, gpu=True)
        self.__translations__: Dict[str,str] = self.load_items()
        self.__temp_dir__ = tempfile.TemporaryDirectory()
        self.__cache_path__: str = self.__temp_dir__.name

    def show_img(self, img: np.ndarray) -> None:
        cv2.imshow('img', img)
        cv2.waitKey(0)

    def screenshot(self) -> np.ndarray:
        sct = mss.mss() 
        ss = sct.grab(sct.monitors[1])
        img = np.array(ss)
        return img

    def ocr_easyocr(self, img: np.ndarray) -> str:
        predict = self.__reader__.readtext(img)

        text = ""
        for detection in predict:
            text += detection[1] + " "
        
        return text[:-1].lower().replace("\n", " ")

    def load_items(self) -> Dict[str,str]:   
        with open(f'items/items_{self.__lang__[0]}.json', encoding="utf-8") as f:
            translations = json.load(f)
            return translations

    def translate(self, text: str, translations: Dict[str, str]) -> str|None:
        match = get_close_matches(text, translations.keys(), n=1, cutoff=0.9)
        if match:
            slug = translations[match[0]]
            return slug

    def get_item_price(self, item_name: str) -> int|None:
        file_path = os.path.join(self.__cache_path__, f"{item_name}.json")

        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)

        price = self.api_wf(item_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(price, f, ensure_ascii=False, indent=4)
            
        return price

    def api_wf(self, item_name: str) -> int|None:
        url = f'https://api.warframe.market/v2/orders/item/{item_name}'
        response = requests.get(url)
        
        data = response.json()
        orders: List[Dict] | None = data["data"] 

        if orders:
            price = [order["platinum"] for order in orders if order["type"] == "sell"]
            price.sort()
            return price[len(price) // 2]   # Median

    def pl_detector(self) -> List[ Tuple[int, int, int, int, int, str, int] | None ]:
        img = self.screenshot()
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # predict YOLO
        predicts = self.__model__(img)
        # self.show_img( predicts[0].plot() )

        results = []
        for predict in predicts:
            idx_texts = (predict.boxes.cls == 2).nonzero(as_tuple=True)[0]

            for idx_text in idx_texts:
                xyxy = predict.boxes.xyxy[idx_text].squeeze().tolist()
                x1, y1 = int(xyxy[0]), int(xyxy[1])
                x2, y2 = int(xyxy[2]), int(xyxy[3])

                item_name_img = img[y1:y2, x1:x2]
                item_name_img = cv2.cvtColor(item_name_img, cv2.COLOR_BGR2GRAY)
                # self.show_img(item_name_img)

                item_name: str = self.ocr_easyocr(item_name_img)
                # print(item_name)
                item_name: str|None = self.translate(item_name, self.__translations__)
                try:
                    if item_name:
                        price: int|None = self.get_item_price(item_name)
                    else: price = None
                except:
                    print("ERROR TO GET THE PRICE")
                else:
                    if price:
                        results.append( (x1, y1, x2-x1, y2-y1, y2, item_name, price) )
                    print(f'{item_name}: {price} pl')     
        return results