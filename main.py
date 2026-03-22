from PyQt5 import QtWidgets, QtCore
import sys
import os
import json
import keyboard
import threading

CONFIG_FILE = "config.json"

def close_app():
    QtCore.QMetaObject.invokeMethod(
        app,
        "quit",
        QtCore.Qt.QueuedConnection
    )

def on_press_0():
    overlay.trigger.emit([[], 0])
    results = pl.pl_detector()
    overlay.trigger.emit([results, 1])

def keyboard_listener():
    keyboard.add_hotkey("ctrl+0", close_app)
    keyboard.add_hotkey("0", on_press_0)
    keyboard.wait()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lang():
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

    lang = load_lang()
    
    from extract_pl import Extract_pl
    from overlay import Overlay
    overlay = Overlay()
    pl = Extract_pl(lang)
    
    threading.Thread(target=keyboard_listener, daemon=True).start()
    
    sys.exit(app.exec_())