# Gradcracker Scraper

## Overview
This project is a scraper tool designed to easily extract job listings from the Gradcracker website.
This tool allows users to filter jobs by job level (Graduate/Placement) and expertise (Aerospace, Computing/Technology, Maths/Business, etc), making it easier to access and analyse relevant job opportunities.
These opportunities can either be displayed on the GUI or exported to a CSV.

![image](https://github.com/user-attachments/assets/1765b64c-934a-4b60-982f-4f43199d9bb5)

## Features
- **Job Filtering**: Choosing job level (Graduate/Placement) and expertise (Aerospace, Computing/Technology, Maths/Business, etc) to filter job listings.
- **Friendly User-Interface**: Simple GUI which allows the user to select the options they prefer and start scraping.
- **CSV Exporting**: Job data can be exported to CSV format.
- **IN PROGRESS - Verbatim mode**: Allow user to get all job listings for a particular category independent of the job listing's listed categories. Highly recommended to only do this with 1 category.

## Installation Guide
Clone the repository

```
https://github.com/uckkla/gradcracker-scraper.git
cd gradcracker-scraper
```

Install requirements

```
pip install -r requirements.txt
```

Run program

```
cd src
python3 main.py
```


## Notes
A big issue with Gradcracker is that job listings are inconsistent with if they are adding categories, and some only show up as "Accepting x principles" when the topic is selected.
In those instances the job listing will not be found, however a large chunk of job listings do correctly categorise themselves.

This can be fixed by using verbatim mode (IN PROGRESS), which specifically selects the category to avoid missing any job listing.
Avoid doing this with multiple job listings as it will take a huge amount of time, and Gradcracker may temporarily block your IP.

It is also advised to avoid abusing the scraping as it will also likely temporarily block your IP.
