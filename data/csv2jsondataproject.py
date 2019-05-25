import csv
import json
import pandas as pd
from os import walk

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

nutrientinfo = {
"Carbohydrate, by difference in gram": ["The primary function of carbohydrates is to provide the body with energy. After consumption, carbohydrates (also named carbs) are broken down into glucose. This glucose can then be used to produce ATP (adenosine triphosphate), which can be seen as fuel for the cells in the body. Even though ATP can be produced from different nutrients (for example protein and fats), it is easiest for the body to produce ATP from carbohydrates. ", "If you consume more carbs than your body requires, these carbs will be transformed into glycogen. The glycogen reserves of your body are mostly stored in your liver and muscles, and ensure the presence of fuel for the body in between meals. However, once your glycogen reserves are filled and you consume carbs, the body will convert these carbs into body fat. Systematically consuming too much carbohydrates can thus make you overweight!", "Systematically consuming too little carbs will cause to body to go into a state of ketosis. Ketosis is a state where your body fuels itself with ketones instead of glucose. Ketones can be extracted by the body from protein and fats. Even though the brain can largely function on ketones, it still requires some degree of glucose to maintain full function. Being fully deprived of carbs will therefore cause the conversion of muscle mass and fat tissue into glucose. Because of this fat loss, many people try to lose weight by carbohydrate deprivation. There is no evidence of carbohydrate deprivation being harmful to the human body, unless your body fat percentage is at such a low level that it cannot convert into glucose anymore."],
"Energy in kcal": "energy",
"Fiber, total dietary in gram": "fiber",
"Folate, DFE in microgram": "Folate",
"Iron, Fe in milligram": "Iron",
"Magnesium, Mg in milligram": "Magnesium",
"Niacin in milligram": "Niacin",
"Phosphorus, P in milligram": "Phospor",
"Potassium, K in milligram": "Potassium",
"Riboflavin in milligram": "Riboflavin",
"Sugars, total in gram": "Sugars",
"Thiamin in milligram": "Thiamin",
"Vitamin A, RAE in microgram": "Vit A",
"Vitamin B-6 in milligram": "Vit B",
"Vitamin C, total ascorbic acid in milligram": "Vit C"
}

csv_dataset = []
for (dirpath, dirnames, filenames) in walk("raw_data"):
    csv_dataset.extend(filenames)
    break

# call initial file
csv_data = csv_dataset[0]

# name of the current fruit
fruitname = csv_data[0:-4]

print(fruitname)
print(csv_dataset)
# open fruit csv file
csvfile = open(f"raw_data/{csv_data}", "r")

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




csv_dataset = csv_dataset[1: -1]


for fruit in csv_dataset:
    data = open(f"raw_data/{fruit}", "r")

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



print(jsonfile)

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

with open('nutrientinfo.json', 'w') as outfile:
    json.dump(nutrientinfo, outfile)
