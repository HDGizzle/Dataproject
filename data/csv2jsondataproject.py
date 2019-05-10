import csv
import json
import pandas as pd

colors = {
# red
"#ff0000": ["Cherry", "Cranberry", "Pomegranate", "Strawberry", "Watermelon"],
# orange
"#EE9A00": ["Apricot", "Mango", "MelonCantaloupe", "Nectarine", "Orange", "Peach", "Tangerine"],
# white
"#f2f5f1": ["Apple", "Banana", "Lychee", "Pear"],
# purple
"#b026a9": ["Blackberry", "Blue Grapes", "Blueberry"],
# pink
"#FF69B4": ["Grapefruit", "Raspberry"],
# green
"#00ad00": ["Green Grapes", "KiwiGreen", "MelonHoneydew"],
# yellow
"#fdfe25": ["KiwiGold", "Passionfruit", "Plum"]
}



# call initial file
csv_data = "Apple.csv"

# name of the current fruit
fruitname = csv_data[0:-4]

print(fruitname)

# open fruit csv file
csvfile = open(csv_data, "r")

# create dataframe of fruit csv
df = pd.read_csv(csvfile, skiprows=4)

# delete unneccesary columns
df = df.loc[:, :"1Value per 100 g"]

df["Unit"] = df["Unit"].replace("mg", "milligram")
df["Unit"] = df["Unit"].replace("µg", "microgram")
df["Unit"] = df["Unit"].replace("g", "gram")

print(df["Unit"])

# add weight unit to nutrient column
df["Nutrient"] = df["Nutrient"] + " in " + df["Unit"]


# delete weight unit column
del df["Unit"]

# make nutrient type dataframe index
df.set_index('Nutrient', inplace=True)

# change column name
df = df.rename(columns = {"1Value per 100 g": fruitname})




csv_dataset = ["Apricot.csv", "Banana.csv", "Blackberry.csv", "Blueberry.csv", "Blue Grapes.csv",
"Cherry.csv", "Cranberry.csv", "Grapefruit.csv", "Green Grapes.csv", "KiwiGold.csv", "KiwiGreen.csv", "Lychee.csv", "Mango.csv",
"MelonCantaloupe.csv", "MelonHoneydew.csv", "Nectarine.csv", "Orange.csv", "Passionfruit.csv", "Peach.csv",
"Pear.csv", "Plum.csv", "Pomegranate.csv", "Raspberry.csv", "Strawberry.csv", "Tangerine.csv", "Watermelon.csv"]

for fruit in csv_dataset:
    data = open(fruit, "r")

    fruittext = fruit[0:-4]

    dataf = pd.read_csv(data, skiprows=4)

    # delete unneccesary columns
    dataf = dataf.loc[:, :"1Value per 100 g"]

    dataf["Unit"] = dataf["Unit"].replace("mg", "milligram")
    dataf["Unit"] = dataf["Unit"].replace("µg", "microgram")
    dataf["Unit"] = dataf["Unit"].replace("g", "gram")

    # add weight unit to nutrient column
    dataf["Nutrient"] = dataf["Nutrient"] + " in " + dataf["Unit"]

    # delete weight unit column
    del dataf["Unit"]

    # make nutrient type dataframe index
    dataf.set_index('Nutrient', inplace=True)

    # change column name
    dataf = dataf.rename(columns = {"1Value per 100 g": fruittext})
    # make nutrient type dataframe index
    # dataf.set_index('Nutrient', inplace=True)
    # print(dataf)


    df = df.join(dataf[fruittext])
    df = df.loc["Caffeine in milligram" : "Vitamin D in IU"]
    df[fruittext] = pd.to_numeric(df[fruittext])
    # # make nutrient type dataframe index
    # dataf.set_index(fruittext, inplace=True)



# df = df.loc["Caffeine in mg" : "Vitamin D in IU"]

df["Apple"] = pd.to_numeric(df["Apple"])

df = df.transpose()

df = df.loc[:, (df != 0).any(axis=0)]

# df = pd.DataFrame(df, columns=headers)
fruitnames = df.index


jsonfile = json.loads(df.to_json(orient="index"))
# jsonfile = json.loads(df.to_json(orient="table"))



# print(jsonfile)

with open('nutrients.json', 'w') as outfile:
    json.dump(jsonfile, outfile)

colordict = {}

for fruit in fruitnames:
    for key, value in colors.items():
        for i in value:
            if i == fruit:
                colordict[fruit] = {"color": key}

with open('fruitcolors.json', 'w') as outfile:
    json.dump(colordict, outfile)
