from scraper import GradcrackerScraper
from data_converter import DataConverter

def main():
    scraper = GradcrackerScraper()
    jobsdf = scraper.scrapeJobData()
    dataConverter = DataConverter(jobsdf)
    dataConverter.exportToCSV()


if __name__ == "__main__":
    main()