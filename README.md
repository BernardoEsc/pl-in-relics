A tool that detects in-game elements and extracts text using YOLO and EasyOCR, displaying the price of items directly on screen without interrupting gameplay.

## Example

https://github.com/user-attachments/assets/91445fbf-c604-4cd3-8fa9-f7d028358e35

<img width="1013" height="394" alt="image" src="https://github.com/user-attachments/assets/138e8359-a83a-44d5-af16-d19ecad4928c" />

### How It Works

1. Capture screen
2. YOLO model detect regions (e.g., text class)
3. Apply EasyOCR to cropped regions
4. Process text to send it to WFM API
5. Render price of items on top of the game

## Installation

Install [Python](https://www.python.org/downloads/release/python-3117/) < 3.12 
and [Git](https://git-scm.com/install/).

1. Clone this repo
  ```commandline
  git clone https://github.com/BernardoEsc/pl-in-relics.git && cd pl-in-relics
  ```
2. Install libraries
  ```commandline
  pip install -r requirements.txt
  ```

## Usage

Go to `C:\Users\UserName\pl-in-relics\` and run `pl-in-relics.bat`.

If you want to change the language, run `change_language.bat`


---

### Object Detection
The model (YOLOv8) was trained on images of opened relics, where you must choose an item.
- Detects:
  - Items    
  - Formas  
  - Their text regions

The model has three classes, but only one is used (text of items and formas) ._. 

### OCR
[EasyOCR](https://github.com/JaidedAI/EasyOCR) is used to extract the text. Supports all languages of WFM Api.
```commandline
  - 한국어: ko
  - Русский: ru
  - Deutsch: de
  - Français: fr
  - Português: pt
  - 简体中文: ch_sim
  - 繁體中文: ch_tra
  - Español: es
  - Italiano: it
  - Polski: pl
  - Українська: uk
  - English: en
```

_NOTE: `ch_sim` and `ch_tra` use English text, so you must use both languages, `ch` and `en`, for proper operation._

### WFM Api
The extracted text must contain the item's name. This is processed to send a request to the API `https://api.warframe.market/v2/orders/item/{slug}`.

_NOTE: slug is the item's name_

The response provides a list of all orders for an item from users who were online within the last 7 days.
This is processed to get the median price of the item. Then, it's displayed on the screen.

For more details about the API, refer to the [documentation](https://42bytes.notion.site/WFM-Api-v2-Documentation-5d987e4aa2f74b55a80db1a09932459d)

---
