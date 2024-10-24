import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup


class GradcrackerScraper:
    def __init__(self, jobLevel="All", expertise="All"):
        # Filter based on which job scheme and main category user has chosen
        baseURL = "https://www.gradcracker.com/search"
        # Job level
        jobLevelURL = {
            "Graduate": "/engineering-graduate-jobs",
            "Placement": "/engineering-work-placements-internships",
            "All": "/engineering-jobs"
            #"Apprenticeship": "degree-apprenticeships" - Requires changing a lot of code
        }
        expertiseURL = {
            "Aerospace": "/aerospace",
            "Chemical/Process": "/chemical-process",
            "Civil/Building": "/civil-building",
            "Computing/Technology": "/computing-technology",
            "Electronic/Electrical": "/electronic-electrical",
            "Maths/Business": "/maths-business",
            "Mechanical/Manufacturing": "/mechanical-manufacturing",
            "Science": "/science",
            "All": "/all-disciplines"
        }

        self.url = baseURL + expertiseURL.get(expertise) + jobLevelURL.get(jobLevel) + "?page="
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/129.0.0.0 Safari/537.36", }

        # Needs to be stored as each batch is executed separately
        self.pageNumber = 1

        # Needed for updating progress bar in GUI
        self.totalJobs = self.fetchTotalJobs()
        self.iteratedJobs = 0

    # Scrapes a page of job listings, returns in df format
    def scrapeJobBatch(self):

        df = pd.DataFrame(columns=["Title", "Categories", "Salary", "Location", "Degree required", "Job type",
                                   "Duration", "Starting", "Deadline"])

        # Random sleep to avoid temporarily being IP banned
        time.sleep(random.randint(1,3))
        response = requests.get(self.url+str(self.pageNumber), headers=self.headers)

        # Page automatically sets to last page no matter how large the number
        # So if not equal, last page was found
        if response.url != self.url+str(self.pageNumber):
            return None

        # Status Code 200 - response successful
        if response.status_code == 200:
            currentJobs = []
            soup = BeautifulSoup(response.content, "html.parser")

            # Need to get label first, as employees label and count also use same class name
            # Get total jobs to accurately present progress bar
            totalJobsLabel = soup.find("div", class_="tw-text-sm tw-font-semibold tw-text-gray-900",
                                       string="Graduate Opportunities")
            totalJobsCount = totalJobsLabel.find_previous_sibling(
                "div", class_="tw-text-2xl tw-font-bold tw-text-orange-500")
            self.totalJobs = int(totalJobsCount.text.strip().replace(",", ""))

            for job in soup.find_all("div", class_="tw-w-3/5 tw-pr-4 tw-space-y-2"):
                self.iteratedJobs += 1

                # Need to store as elements first, rare case where it does not exist
                titleElement = job.find("a", class_="tw-block tw-text-base tw-font-semibold")
                title = titleElement.text.strip() if titleElement else "N/A"

                categoriesElement = job.find("div", class_="tw-text-xs tw-font-bold tw-text-gray-800")
                categories = categoriesElement.text.strip() if categoriesElement else "N/A"

                attributes = {}
                attributeList = job.find_all("li", class_="tw-flex")

                for attribute in attributeList:
                    attributeName, attributeData = attribute.text.strip().split(":", 1)
                    attributes[attributeName.strip()] = attributeData.strip()

                # **attributes unpacks into key-value pairs
                # It will add other categories if they don't exist on the df column
                currentJobs.append({
                    "Title": title,
                    "Categories": categories,
                    **attributes
                })

            # If no jobs exist, rare case when page is empty
            if not currentJobs:
                return None

            currentdf = pd.DataFrame(currentJobs)
            df = pd.concat([df, currentdf]).reset_index(drop=True)

            self.pageNumber += 1
        else:
            return f"Failed to retrieve data, status code: {response.status_code}"
        return df

    def fetchTotalJobs(self):
        response = requests.get(self.url + "1", headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            totalJobsLabel = soup.find("div", class_="tw-text-sm tw-font-semibold tw-text-gray-900",
                                       string="Graduate Opportunities")
            totalJobsCount = totalJobsLabel.find_previous_sibling(
                "div", class_="tw-text-2xl tw-font-bold tw-text-orange-500")

            return int(totalJobsCount.text.strip().replace(",", ""))
        else:
            return f"Failed to retrieve data, status code: {response.status_code}"

    # Use getter to avoid continuously fetching job total
    def getTotalJobs(self):
        return self.totalJobs

    def getIteratedJobs(self):
        return self.iteratedJobs