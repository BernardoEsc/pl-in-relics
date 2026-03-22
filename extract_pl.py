from ultralytics import YOLO
from difflib import get_close_matches
import numpy as np
import mss
import cv2
import easyocr
import requests

class Extract_pl():
    def __init__(self, lang=['en']):
        self.__model__ = YOLO("model/best.pt")
        self.__lang__ = lang
        self.__reader__ = easyocr.Reader(self.__lang__, gpu=True)
        self.__translates__ = self.load_items()

    def show_img(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)

    def screenshot(self):
        sct = mss.mss() 
        ss = sct.grab(sct.monitors[1])
        img = np.array(ss)
        return img

    def ocr_easyocr(self, img):
        predict = self.__reader__.readtext(img)

        text = ""
        for detection in predict:
            text += detection[1] + " "
        
        return text[:-1].lower().replace("\n", " ")

    def load_items(self):
        import csv
        
        translates = {}
        with open(f'items/items_{self.__lang__[0]}.csv', newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                translates[row[f'{self.__lang__[0]}']] = row["slug"]

        return translates

    def translate(self, text, translations):
        match = get_close_matches(text, translations.keys(), n=1, cutoff=0.9)
        if match:
            slug = translations[match[0]]
            return slug

    def api_wf(self, text):
        url = f'https://api.warframe.market/v2/orders/item/{text}/top'
        try:
            response = requests.get(url)
            data = response.json()
            sellers = data["data"]["sell"]
            seller = next(
                (item for item in sellers if item["user"]["status"] == "ingame"),
                None
            )
            if seller:
                return str(seller["platinum"]) # int -> str
        except:
            pass

    def pl_detector(self):
        img = self.screenshot()
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # predict YOLO
        predicts = self.__model__(img)
        # show_img( predicts[0].plot() )

        results = []
        for predict in predicts:
            idx_texts = (predict.boxes.cls == 2).nonzero(as_tuple=True)[0]

            for idx_text in idx_texts:
                xyxy = predict.boxes.xyxy[idx_text].squeeze().tolist()
                x1, y1 = int(xyxy[0]), int(xyxy[1])
                x2, y2 = int(xyxy[2]), int(xyxy[3])

                text_img = img[y1:y2, x1:x2]
                text_img = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
                # show_img(text_img)

                text = self.ocr_easyocr(text_img)
                text = self.translate(text, self.__translates__)
                if text:
                    pl = self.api_wf(text) 
                    if pl:
                        results.append( (x1, y1, x2-x1, y2-y1, y2, text, pl) )

        return results