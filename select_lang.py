from PyQt5 import QtWidgets
import sys
import json

class LanguageDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Language")

        layout = QtWidgets.QVBoxLayout()
        self.group = QtWidgets.QButtonGroup(self)

        languages = [
            ("한국어", ["ko"]),
            ("Русский", ["ru"]),
            ("Deutsch", ["de"]),
            ("Français", ["fr"]),
            ("Português", ["pt"]),
            ("简体中文", ["ch_sim", "en"]),
            ("繁體中文", ["ch_tra", "en"]),
            ("Español", ["es"]),
            ("Italiano", ["it"]),
            ("Polski", ["pl"]),
            ("Українська", ["uk"]),
            ("English", ["en"]),
        ]

        self.lang_map = {}

        for i, (name, code) in enumerate(languages):
            rb = QtWidgets.QRadioButton(name)
            if code == ["en"]:
                rb.setChecked(True)

            self.group.addButton(rb, i)
            layout.addWidget(rb)
            self.lang_map[i] = code

        btn = QtWidgets.QPushButton("Accept")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def get_language(self):
        return self.lang_map[self.group.checkedId()]
    
    def save_config(self, data, CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    CONFIG_FILE = "config.json"

    app = QtWidgets.QApplication(sys.argv)
    
    dialog = LanguageDialog()
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        lang = dialog.get_language()
        dialog.save_config({"language": lang}, CONFIG_FILE)
    
    sys.exit()