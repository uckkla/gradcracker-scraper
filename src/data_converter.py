class DataConverter:
    def __init__(self, df):
        self.df = df

    def cleanData(self):
        print(self.df)
        self.df.fillna("N/A", inplace=True)
        self.df.drop_duplicates(inplace=True)

    def exportToCSV(self):
        self.cleanData()
        # utf-8-sig puts a BOM at beginning of file to recognise as utf-8, so £ symbol correctly shows
        self.df.to_csv("job_data.csv", encoding="utf-8-sig", index=False)
