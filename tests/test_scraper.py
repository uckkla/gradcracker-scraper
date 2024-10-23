import pytest
import requests
import pandas as pd
from src.scraper import GradcrackerScraper
from unittest.mock import patch


@pytest.fixture
def scraper():
    return GradcrackerScraper(jobLevel="Graduate", expertise="Computing/Technology")

# Test if correct url is provided given jobLevel/expertise
def test_initialization(scraper):
    assert scraper.url == "https://www.gradcracker.com/search/computing-technology/engineering-graduate-jobs?page="

@patch("requests.get")
def test_scrapeData(mock_get, scraper):
    mock_get.return_value.status_code = 200
    mock_get.return_value.url = "https://www.gradcracker.com/search/computing-technology/engineering-graduate-jobs?page=1"
    mock_get.return_value.content = """
    <div class="tw-text-2xl tw-font-bold tw-text-orange-500">
    1
    </div>
    <div class="tw-w-3/5 tw-pr-4 tw-space-y-2">
        <a class="tw-block tw-text-base tw-font-semibold"> Technology Graduate Programme</a>
        <div class="tw-text-xs tw-font-bold tw-text-gray-800"> IT, Software, Computing, Data Science.</div>
        <ul>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Salary:</span> Competitive</li>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Location:</span> Multiple UK Locations</li>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Degree required:</span> 2:1 and above</li>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Hiring multiple candidates:</span> Yes</li>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Starting:</span> September 2025</li>
            <li class="tw-flex"><span class="tw-pr-1 tw-font-semibold tw-text-gray-900">Deadline:</span> Ongoing</li>
        </ul>
    </div>
    """

    df = scraper.scrapeJobData()

    assert df["Title"][0] == "Technology Graduate Programme"
    assert df["Categories"][0] == "IT, Software, Computing, Data Science."
    assert df["Salary"][0] == "Competitive"
    assert df["Location"][0] == "Multiple UK Locations"
    assert df["Degree required"][0] == "2:1 and above"
    assert df["Hiring multiple candidates"][0] == "Yes"  # Ensures dynamically added columns work
    assert df["Starting"][0] == "September 2025"
    assert df["Deadline"][0] == "Ongoing"

@patch("requests.get")
def test_scrapeDataInvalidResponse(mock_get):
    mock_get.return_value.status_code = 403  # Forbidden error, rate limited
    # Needed to pass the if statement break
    mock_get.return_value.url = "https://www.gradcracker.com/search/computing-technology/engineering-graduate-jobs?page=1"

    scraper = GradcrackerScraper(jobLevel="Graduate", expertise="Computing/Technology")
    result = scraper.scrapeJobData()
    assert result == "Failed to retrieve data, status code: 403"