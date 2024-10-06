class DataConverter:
    def __init__(self, df, categories):
        self.df = df
        self.categories = categories

    def cleanData(self):
        self.df.fillna("N/A", inplace=True)
        self.df.drop_duplicates(inplace=True)

        self.filterByCategory()

    def filterByCategory(self):
        # Dropping rows mid-loop will cause indexing issues
        rowsToDrop = []
        for index, row in self.df.iterrows():
            currentRowCategories = row['Categories'].strip(".").split(', ')
            if not any(category in currentRowCategories for category in self.categories):
                rowsToDrop.append(index)

        self.df.drop(rowsToDrop, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def exportToCSV(self):
        self.cleanData()
        # utf-8-sig puts a BOM at beginning of file to recognise as utf-8, so £ symbol correctly shows
        self.df.to_csv("job_data.csv", encoding="utf-8-sig", index=False)
