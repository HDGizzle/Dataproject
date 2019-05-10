import csv
import json
import pandas as pd


# csv_data = ["Apple.csv", "Apricot.csv", "Banana.csv", "Blackberry.csv", "Blueberry.csv",
# "Cherry.csv", "Cranberry.csv"]

csv_data = "Apple.csv"

# for i in csv_data:
#     csvfile = open(i, "r")
#     df = pd.read_csv(i)

csvfile = open(csv_data, "r")

df = pd.read_csv(csv_data)

print(df)
