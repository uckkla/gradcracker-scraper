from scraper import GradcrackerScraper
from data_converter import DataConverter
import sys
from PyQt6.QtWidgets import QApplication
from src.gui import MainWindow


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def start(self):
        self.window.show()
        self.app.exec()


if __name__ == "__main__":
    app = MainApp()
    app.start()

