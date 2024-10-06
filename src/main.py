from scraper import GradcrackerScraper
from data_converter import DataConverter

def main():
    categories = ["Statistics"]
    scraper = GradcrackerScraper("Graduate", "Computing/Technology")
    jobsdf = scraper.scrapeJobData()
    dataConverter = DataConverter(jobsdf, categories)
    dataConverter.exportToCSV()


if __name__ == "__main__":
    main()