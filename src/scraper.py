import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup


class GradcrackerScraper:
    def __init__(self, jobLevel, expertise):
        # Filter based on which job scheme and main category user has chosen
        baseURL = "https://www.gradcracker.com/search"
        # Job level
        jobLevelURL = {
            "Graduate": "/engineering-graduate-jobs",
            "Placement": "/engineering-work-placements-internships",
            "Graduate+Placement": "/engineering-jobs",
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

    def scrapeJobData(self):
        pageNumber = 1
        df = pd.DataFrame(columns=["Title", "Categories", "Salary", "Location", "Degree required", "Job type",
                                   "Duration", "Starting", "Deadline"])
        while True:
            # Random sleep to avoid temporarily being IP banned
            time.sleep(random.randint(1,3))
            print(df)
            response = requests.get(self.url+str(pageNumber), headers=self.headers)
            if response.url != self.url+str(pageNumber):
                break

            # Error 200 - response successful
            if response.status_code == 200:
                currentJobs = []
                soup = BeautifulSoup(response.content, "html.parser")

                for job in soup.find_all("div", class_="tw-w-3/5 tw-pr-4 tw-space-y-2"):
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
                    currentJobs.append({
                        "Title": title,
                        "Categories": categories,
                        **attributes
                    })

                currentdf = pd.DataFrame(currentJobs)
                df = pd.concat([df, currentdf]).reset_index(drop=True)

                pageNumber += 1
            else:
                return f"Failed to retrieve data, status code: {response.status_code}"
        return df
