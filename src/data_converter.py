import json
import os


class DataConverter:
    def __init__(self, df, categories):
        self.df = df
        self.categories = categories
        # Gradcracker's selected categories are inconsistent to the job's specific category, so need to convert
        # Even with this there will be some jobs with no category, or not having the category in it at all
        # Due to them replacing it with "Accepting x disciplines"
        # currentDir and jsonPath used when unit testing, as it runs from a different directory
        currentDir = os.path.dirname(__file__)
        jsonPath = os.path.join(currentDir, "formattedCategories.json")
        with open(jsonPath, 'r') as file:
            categoryMap = json.load(file)
        self.categoryList = [category for key in self.categories for category in categoryMap.get(key)]
        print(self.categoryList)

    # Remove duplicates, fill any NaN values
    def cleanData(self):
        self.df.fillna("N/A", inplace=True)
        self.df.drop_duplicates(inplace=True)
        self.filterByCategory()

    # Remove all rows that do not contain any selected category
    def filterByCategory(self):
        # Dropping rows mid-loop will cause indexing issues
        rowsToDrop = []
        for index, row in self.df.iterrows():
            currentRowCategories = row['Categories'].strip(".").split(', ')
            if not any(category in currentRowCategories for category in self.categoryList):
                rowsToDrop.append(index)
        print(rowsToDrop)
        self.df.drop(rowsToDrop, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def exportToCSV(self):
        # utf-8-sig puts a BOM at beginning of file to recognise as utf-8, so £ symbol correctly shows
        self.df.to_csv("job_data.csv", encoding="utf-8-sig", index=False)

    # Convert df to string to output on gui
    def toString(self):
        arr = self.df.to_numpy()
        stringArr = []

        for job in arr:
            stringJob = ", ".join(str(category) for category in job)
            stringArr.append(stringJob)

        return stringArr
