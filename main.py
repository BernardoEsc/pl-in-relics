from extract_pl import Extract_pl
from overlay import Overlay
from PyQt5 import QtWidgets, QtCore
from typing import Dict, List
import json
import keyboard
import os
import sys
import threading

CONFIG_FILE: str = "config.json"
QUIT_BUTTON: str = "ctrl+0"
START_BUTTON: str = "0"

def close_app() -> None:
    QtCore.QMetaObject.invokeMethod(
        app,
        "quit",
        QtCore.Qt.QueuedConnection
    )

def start_scan() -> None:
    overlay.trigger.emit([[], 0])
    results = pl.pl_detector()
    overlay.trigger.emit([results, 1])

def keyboard_listener() -> None:
    keyboard.add_hotkey(QUIT_BUTTON, close_app)
    keyboard.add_hotkey(START_BUTTON, start_scan)
    keyboard.wait()

def load_config() -> Dict[str, str] | None:
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lang() -> List[str]:
    config = load_config()

    if not config or "language" not in config:
        from select_lang import LanguageDialog
        dialog = LanguageDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            lang = dialog.get_language()
            dialog.save_config({"language": lang}, CONFIG_FILE)
        else:
            sys.exit()
    else:
        lang = config["language"]
    
    return lang

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    lang: List[str] = load_lang()
    print("\nLanguage:", lang[0])

    overlay = Overlay()
    pl = Extract_pl(lang)

    print(f'\nPRESS "{START_BUTTON}" TO GET THE PRICE\n')
    
    threading.Thread(target=keyboard_listener, daemon=True).start()
    
    sys.exit(app.exec_())