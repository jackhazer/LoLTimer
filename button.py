from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import pyperclip
from loltimer import Timer
import auto

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.clipboard_file = "LoLTimer.txt"
        self.clipboard = ''
        self.setWindowTitle("Overlay Window")
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("background-color:transparent;")

        layout = QVBoxLayout()

        self.text_label = QLabel()
        font = QFont()
        font.setPointSize(12)
        self.text_label.setFont(font)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setStyleSheet("color: white;")
        layout.addWidget(self.text_label)

        grid_layout = QGridLayout()

        self.buttons = []
        roles = ['TOPF', 'JGF', 'MIDF', 'ADF', 'SUPF']
        for i, role in enumerate(roles):
            button = QPushButton(role)
            button.setObjectName(role)
            button.setDisabled(True)  # Disable the buttons initially
            button.clicked.connect(self.handle_button_click)
            button.setFixedSize(50, 30)  # Set the button size
            button.setStyleSheet(
                "QPushButton { background-color: #3D85C6; border-radius: 0px; color: white; font-size: 16px; }"
                "QPushButton:hover { background-color: #3074A4; }"
                "QPushButton:pressed { background-color: #265C8D; }"
            )

            self.buttons.append(button)
            grid_layout.addWidget(button, i, 0)

        layout.addLayout(grid_layout)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(-100, 100)
        self.slider.setValue(0)
        self.slider.setEnabled(False)  # Disable the slider initially
        layout.addWidget(self.slider)

        self.setLayout(layout)

        self.init_button = QPushButton("Initialize")
        self.init_button.clicked.connect(self.handle_init_button_click)
        self.set_init_button_style()
        layout.addWidget(self.init_button)

        self.init_cooldown = 60  # 10 minutes cooldown in milliseconds
        self.is_initialized = False  # Flag to track initialization

    def set_overlay_text(self, text):
        self.text_label.setText(text)

    def handle_button_click(self):
        sender = self.sender()
        button_id = sender.objectName()
        offset = self.slider.value()  # Get the value from the single slider
        self.clipboard = self.timer.click(button_id,  self.clipboard)
        self.copy_to_clipboard(self.clipboard)
        auto.modify_clipboard_file(self.clipboard)
        auto.run_ahk_script()


    def handle_init_button_click(self):
        if not self.is_initialized:  # Check if already initialized
            self.init_button.setEnabled(False)
            self.timer.initialize()  # Call the initialize method of the timer
            self.enable_buttons()  # Enable the buttons after initialization
            self.slider.setEnabled(True)  # Enable the single slider after initialization
            self.is_initialized = True  # Set initialization flag
            self.start_init_cooldown()  # Start the cooldown timer
            print("Initialization complete")
        else:
            print("Already initialized. Please wait for the cooldown period.")

    def copy_to_clipboard(self, message):
        pyperclip.copy(message)

    def set_init_button_style(self):
        self.init_button.setStyleSheet(
            "QPushButton { background-color: #C63E3E; border-radius: 0px; color: white; font-size: 16px; }"
            "QPushButton:hover { background-color: #A53232; }"
            "QPushButton:pressed { background-color: #8D2626; }"
        )

    def enable_buttons(self):
        for button in self.buttons:
            button.setEnabled(True)

    def start_init_cooldown(self):
        self.init_button.setEnabled(False)  # Disable the init button during cooldown
        QtCore.QTimer.singleShot(self.init_cooldown, self.handle_cooldown_finished)

    def handle_cooldown_finished(self):
        self.init_button.setEnabled(True)  # Enable the init button after cooldown
        self.is_initialized = False  # Reset the initialization flag

def show_overlay(width, height):
    app = QApplication([])

    window = OverlayWindow()
    window.setGeometry(0, 0, width, height)
    # Adjust the position to the top-right corner
    screen_geometry = app.desktop().screenGeometry()
    x = screen_geometry.width() - width
    y = 0
    window.move(x, y)
    window.show()
    app.exec_()

# Usage example
show_overlay(200, 200)