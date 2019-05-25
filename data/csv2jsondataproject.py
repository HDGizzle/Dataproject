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

"Fiber, total dietary in gram": ["Fiber is a form of carbohydrates that is not transformed into glucose. Instead, fiber molecules largely stay intact as they travel down the digestive tract. On their way down, they bind the contents of your digestive system and ensure lubrication. Fibers are also fuel for the “good” bacteria present in your intestines. The daily recommended fiber intake is 38 grams in adult men and 25 grams in adult women. ", "Consuming too much fiber can lead to the blockage of your digestive system. However, it is quite difficult to actually achieve overconsumption of fiber. People that consume too much fiber usually eat abundant foods that are fortified with fiber, or take fiber supplements.", "Interesting enough, studies have revealed similar effects for consuming too little fiber in comparison to consuming too much fiber."],

"Folate, DFE in microgram": ["Folate (Vitamin B9) is present in some of the foods we eat. In contrast, folic acid is a synthetic form of folate that needs to be converted before the body can actually do something with it. Your body uses folate to create DNA and cells, as it is unable to divide cells without the use of folate. The recommended daily amount of folate for adults is around 400 micrograms.", "First of all, it is impossible to consume too much folate through a regular diet. However, the intake of supplements containing folate in combination with folate consumed through your diet can lead to abundant folate intake. The abundant intake of folate can mask vitamin B12 (found in animal products) deficiency up to a point where the damage done by this B12 deficiency is irreversible. Furthermore, abundantly consumed folic acid (artificial folate) cannot be converted into actual folate before it reaches the bloodstream. As a result, your cells will absorb folic acid instead of actual folate, which is useless to them. Because the folic acid replaces the folate, your body cells will display behaviors similar to folate deficiency.", "Consuming too little folate can do permanent damage to the body. The symptoms of folate deficiency are fatigue, weakness and shortness of breath. Scientists further suggest that folate deficiency can damage the DNA, but also enables cancers to develop more easily. Furthermore, folate deficiency increases the chances of heart diseases."],

"Iron, Fe in milligram": "Iron",

"Magnesium, Mg in milligram": "Magnesium",

"Niacin in milligram": "Niacin",

"Phosphorus, P in milligram": "Phospor",

"Potassium, K in milligram": ["Potassium is a mineral that functions in the body as an electrolyte. This means that it enables the body to send electric nerve signals from the brain to the cells in the body. Furthermore it helps to maintain a healthy blood pressure, protect from strokes, maintain healthy body water levels and prevents kidney stones. The recommended amount of potassium intake for adults is around 3000 milligrams.", "It is almost impossible to consume too much potassium, and actually most people consume too little potassium on a daily basis. However, by the use of supplements in combination with a regular diet, too much potassium could lead to muscle weakness and disturbances in your heart rhythm.", "Even though most of us consume too little potassium, the effects are usually not notable. However, severe potassium deficiency disturbs the functioning of the nervous system, leading to malfunctioning muscles, including the heart."],

"Riboflavin in milligram": "Riboflavin",
"Sugars, total in gram": "Sugars",
"Thiamin in milligram": "Thiamin",
"Vitamin A, RAE in microgram": "Vit A",
"Vitamin B-6 in milligram": "Vit B",
"Vitamin C, total ascorbic acid in milligram": ["Vitamin C is an ‘antioxidant’, which strengthens the immune system. It prevents damage to your cells and ensures correct functioning of the liver. It also ensures healthy white blood cells, which attack diseases that enter your body. The daily recommended amount of vitamin C is 75 milligram for women and 90 for men.", "It is virtually impossible to consume too much vitamin C by just eating food, as symptoms of overconsumption will occur when more than 2000 milligram per day is consumed. However, supplements could achieve such numbers. Consuming such a large amount of vitamin C can lead to diarrhea and nausea.", "Consuming too little vitamin C will lead to all kinds of visible defects of your body. Amongst these effects are dry skin, bumpy skin, corkscrew-shaped body hair, spots on your fingernails and tooth loss. Furthermore your immune system is weakened, you will feel tired more often and the healing of wounds and bruises will go much slower. Vitamin C deficiency can in extreme cases even lead to scurvy!"]
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



# print(jsonfile)
print(nutrientinfo)

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
