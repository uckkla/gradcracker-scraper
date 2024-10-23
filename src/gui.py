import os

from scraper import GradcrackerScraper
from data_converter import DataConverter
import pandas as pd
import json
import time

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, \
    QPushButton, QListWidget, QLabel, QComboBox, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal


# Thread needed to prevent GUI freezing - show progress
class ScrapeThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(pd.DataFrame)

    def __init__(self, expertise, jobLevel):
        super().__init__()
        self.expertise = expertise
        self.jobLevel = jobLevel

    def run(self):
        scraper = GradcrackerScraper(self.jobLevel, self.expertise)
        jobsdf = scraper.scrapeJobData()
        self.progress.emit((scraper.getJobsIterated()/scraper.getJobsTotal())*100)
        self.finished.emit(jobsdf)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Instantiating for better readability - needed for multiple methods
        self.jobsdf = None
        self.dataConverter = None
        # currentDir and jsonPath used when unit testing, as it runs from a different directory
        currentDir = os.path.dirname(__file__)
        jsonPath = os.path.join(currentDir, "expertiseCategories.json")
        with open(jsonPath, 'r') as file:
            self.expertiseCategories = json.load(file)

        self.createUI()

    def createUI(self):
        self.setWindowTitle('Gradcracker Scraper')
        self.setFixedSize(450, 700)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)

        # Job Level Section
        self.jobLevelLabel = QLabel("Select Job Level:")
        mainLayout.addWidget(self.jobLevelLabel)

        self.jobLevelDropdown = QComboBox()
        self.jobLevelDropdown.addItems(["All", "Graduate", "Placement"])  # Internship TBA
        mainLayout.addWidget(self.jobLevelDropdown)

        # Expertise Section
        self.expertiseLabel = QLabel("Select Expertise:")
        mainLayout.addWidget(self.expertiseLabel)

        self.expertiseDropdown = QComboBox()
        self.expertiseDropdown.addItems(list(self.expertiseCategories.keys()))
        mainLayout.addWidget(self.expertiseDropdown)

        # Categories Section - varies on what expertise selected
        self.categoriesLabel = QLabel("Select Categories")
        mainLayout.addWidget(self.categoriesLabel)

        self.categoriesList = QListWidget()  # May try custom QComboBox() in future
        self.categoriesList.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.categoriesList.addItems(["All"])
        self.expertiseDropdown.currentIndexChanged.connect(self.updateCategories)

        mainLayout.addWidget(self.categoriesList)

        # Start Scraping Button
        self.startButton = QPushButton("Start Scraping")
        self.startButton.clicked.connect(self.startScrape)
        mainLayout.addWidget(self.startButton)

        # Convert to CSV Button
        self.convertButton = QPushButton("Convert to CSV")
        self.convertButton.clicked.connect(self.convertToCSV)
        mainLayout.addWidget(self.convertButton)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        mainLayout.addWidget(self.progressBar)

        # Job Listings Display
        self.jobsLabel = QLabel("Job Listings:")
        mainLayout.addWidget(self.jobsLabel)

        self.jobsList = QListWidget()
        mainLayout.addWidget(self.jobsList)

        # Refresh Button
        self.refreshButton = QPushButton("Refresh Data")
        self.refreshButton.clicked.connect(self.refreshData)
        mainLayout.addWidget(self.refreshButton)

    def test(self):
        for i in range(100):
            time.sleep(0.01)
            self.progressBar.setValue(i+1)

    # Update categories whenever expertise is changed
    def updateCategories(self):
        self.categoriesList.clear()
        self.categoriesList.addItems(self.expertiseCategories.get(self.expertiseDropdown.currentText()))

    # Create scraper and converter, clean data and refresh list
    def startScrape(self):
        # Stop button - only one scrape at a time
        self.startButton.setEnabled(False)

        expertise = self.expertiseDropdown.currentText()
        jobLevel = self.jobLevelDropdown.currentText()

        self.scrapeThread = ScrapeThread(expertise, jobLevel)

        self.scrapeThread.progress.connect(self.updateProgressBar)
        self.scrapeThread.finished.connect(self.scrapingFinished)

        self.scrapeThread.start()

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def scrapingFinished(self, df):
        self.startButton.setEnabled(True)
        categories = [category.text() for category in self.categoriesList.selectedItems()]

        self.dataConverter = DataConverter(df, categories)
        self.dataConverter.cleanData()

    def convertToCSV(self):
        if self.dataConverter is not None:
            self.dataConverter.exportToCSV()

    def refreshData(self):
        if self.dataConverter is not None:
            self.jobsList.clear()
            self.jobsList.addItems(self.dataConverter.toString())
