from src.data_converter import DataConverter
import pandas as pd


def test_cleanData():
    # Left out other criteria, should not change the testing
    testData = {"Title": [None, "Data Management Graduate Scheme", "Engineering", "Engineering"],
                "Categories": ["Analytics, Data, Statistics.", "Data.", "Data, Statistics.", "Data, Statistics."]}

    df = pd.DataFrame(testData)

    categories = ["Analytics", "Data"]
    cleaner = DataConverter(df, categories)
    cleaner.cleanData()

    assert len(df.index) == 3  # 3 jobs left over after removing duplicate
    assert df.duplicated().sum() == 0  # No duplicates left after filter
    assert df.isnull().sum().sum() == 0  # All NaN should be converted to N/A


def test_filterByCategory():

    testData = {"Title": ["Data Management Graduate", "Data Analytic Summer Program", "Engineering",
                          "Cyber Security Internship", "Machine Learning Engineer"],
                "Categories": ["Analytics, Statistics.", "Data.", "Data, Statistics", "Cyber Security, Data",
                               "Maths, AI, Robots"]}

    df = pd.DataFrame(testData)
    categories = ["Analytics", "Data"]
    cleaner = DataConverter(df, categories)
    cleaner.filterByCategory()

    assert len(df.index) == 4  # 4 jobs left after filtering
    assert "Machine Learning Engineer" not in cleaner.df["Title"].values  # Ensure ML Engineer is filtered

