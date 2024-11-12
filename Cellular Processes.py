#Daniel Cohen 209313311

import pandas as pd

class myData:

    def __init__(self, path1, path2, path3) -> None:
        self.books_data = pd.read_csv(path1, sep=";", on_bad_lines='skip',encoding='latin-1')
        self.rating_data = pd.read_csv(path2, sep=";", on_bad_lines="skip", encoding='latin-1')
        self.users_data = pd.read_csv(path3, sep=";", on_bad_lines="skip", encoding='latin-1')
        # Fix mixed type in column 3 of books_data and remove non-numeric rows
        # Convert column with index 3 to numeric, coercing errors to NaN
        self.books_data.iloc[:, 3] = pd.to_numeric(self.books_data.iloc[:, 3], errors='coerce')
        # Remove rows where the column is NaN after the conversion
        self.books_data = self.books_data.dropna(subset=[self.books_data.columns[3]])
        # Convert column to int32
        self.books_data.iloc[:, 3] = self.books_data.iloc[:, 3].astype('int32')

    @classmethod 
    def fromFile(cls, pathToFileOfFiles):
        try:
            with open(pathToFileOfFiles, "r") as file:
                paths = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"The specified file {pathToFileOfFiles} does not exist.")
            return None

        if len(paths) != 3:
            print("The file should contain exactly three lines, each representing a file path.")
            return

        for path in paths:
            try:
                with open(path, "r"):
                    pass  # Just to check if the file exists
            except FileNotFoundError:
                print(f"The specified path {path} in the file does not exist.")
                return None

        try:
            return myData(paths[0], paths[1], paths[2])

            # Add any processing needed for cls.books_data as previously discussed
            return cls
        except Exception as ex:
            raise Exception(f"An error occurred while processing the files: {ex}")
        return None


        # function returns sum of books written in a certain year, between year x and y
    def num_year(self, x, y):
        return len(self.books_data[(self.books_data["Year-Of-Publication"] >= x) & (self.books_data["Year-Of-Publication"] < y)])


    # function returns data frame with book title and book author of certain yer
    def df_published(self, year):
        published_year = self.books_data[self.books_data["Year-Of-Publication"] == year]
        return published_year[["Book-Title", "Book-Author"]]


    def num_books_by_year(self, x, y):
        year_counts = self.books_data[(self.books_data['Year-Of-Publication'] >= x) & (self.books_data['Year-Of-Publication'] <= y)]
        return year_counts.groupby('Year-Of-Publication').size().to_dict().items()


   # returns the average and mean of users age from specific country
    def mean_std(self, country):
        citizens = self.users_data[self.users_data["Location"].str.contains(country)]
        mean = citizens["Age"].mean()
        std = citizens["Age"].std()
        return (round(mean, 3), round(std, 3))

        # function returns average rating for a certain book
    def mean_rating(self, book_name):
        isbns = self.books_data[self.books_data["Book-Title"] == book_name]["ISBN"].values
        rating = self.rating_data[self.rating_data["ISBN"].isin(isbns)]["Book-Rating"].mean()
        return rating

    # function returns a dataframe with k highest ratings
    def top_k(self, k):
        df = pd.DataFrame(self.rating_data.groupby("ISBN")["Book-Rating"].mean())
        # ISBN in books data to ISBN in df and conjoin according to ISBN
        df = df.join(self.books_data.set_index("ISBN"), on="ISBN")[["Book-Title", "Book-Author", "Book-Rating"]]
        # drop the books that dont exist in books, but exist in rating
        df = df.dropna(subset=["Book-Title"])
        df = df.sort_values(by=["Book-Rating", "Book-Author", "Book-Title"], ascending=[False, True, True])
        df = df.head(k)
        return df

        # function returns the most active user

    def most_active(self, k):
        df = pd.DataFrame(self.rating_data)
        # Group by user id and count the number of times each user id appears
        count = df["User-ID"].groupby(df["User-ID"]).count()
        # Add the count column to the dataframe
        df["Count"] = df["User-ID"].map(count)
        # Drop irrelevant columns + duplicates
        df = df[["User-ID", "Count"]]
        df = df.drop_duplicates(subset=["User-ID"])
        # Sort by count + return the k'th row starting from 1
        df = df.sort_values("Count", ascending=False)
        return df.iloc[k - 1]["Count"]

if __name__ == "__main__":
    #df = pd.read_csv("C:\\Users\\dcohe\\Downloads\\books.csv",nrows=30, sep=";")
    #print(df.head())
    #md = myData("books.csv", "ratings.csv", "users.csv")
    md = myData.fromFile("fileOfFiles.txt")

    print(str(md.most_active(3)))
    # books_data = pd.read_csv("C:\\Users\\dcohe\\Downloads\\books.csv", sep=";", on_bad_lines='skip', encoding='latin-1')
    # print(books_data["Year-Of-Publication"].str.isnumeric().dropna())
    # print(books_data.groupby("Year-Of-Publication").count()["ISBN"])
