import sys
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QScrollArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("God Counter")
        self.setFixedSize(500, 600)

        # Load gods from JSON file
        with open("gods.json", "r") as f:
            self.gods = json.load(f)

        # Create main widget and layout
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        # Set font
        font = QFont()
        font.setPointSize(14)

        # Add labels and buttons for each god
        row = 0
        for god in self.gods:
            name_label = QLabel(god["name"])
            name_label.setFont(font)
            self.layout.addWidget(name_label, row, 0)

            count_label = QLabel(str(god["count"]))
            count_label.setAlignment(Qt.AlignCenter)
            count_label.setFont(font)
            self.layout.addWidget(count_label, row, 1)

            inc_button = QPushButton("+")
            inc_button.setObjectName(str(row))
            inc_button.clicked.connect(self.increment_count)
            inc_button.setFont(font)
            self.layout.addWidget(inc_button, row, 2)

            dec_button = QPushButton("-")
            dec_button.setObjectName(str(row))
            dec_button.clicked.connect(self.decrement_count)
            dec_button.setFont(font)
            self.layout.addWidget(dec_button, row, 3)

            row += 1

        # Create scroll area and set main widget as its child
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.widget)
        self.setCentralWidget(scroll_area)

    def increment_count(self):
        button = self.sender()
        row = int(button.objectName())
        self.gods[row]["count"] += 1
        self.update_counts()

    def decrement_count(self):
        button = self.sender()
        row = int(button.objectName())
        self.gods[row]["count"] -= 1
        if self.gods[row]["count"] < 0:
            self.gods[row]["count"] = 0
        self.update_counts()

    def update_counts(self):
        # Update count labels for each god
        for i in range(len(self.gods)):
            count_label = self.layout.itemAtPosition(i, 1).widget()
            count_label.setText(str(self.gods[i]["count"]))

        # Save updated gods to JSON file
        with open("gods.json", "w") as f:
            json.dump(self.gods, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())