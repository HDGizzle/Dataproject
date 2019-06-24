# Gijs Beerens - 10804463
# This file merges many CSV's with information about fruits into one big
# pandas dataframe. The dataframe is then converted into a JSON file,
# making it suitable for D3 processing. Furthermore a JSON file with fruit
# flesh colors and a JSON file with information about nutrients is created.

# Sources:
# https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
# https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
# https://stackoverflow.com/questions/21164910/how-do-i-delete-a-column-that-contains-only-zeros-in-pandas

import csv
import json
import pandas as pd
from os import walk

# this is the dictionary with fruit flesh colors
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

# this is the dictionary with nutrient information
nutrientinfo = {
"Carbohydrate, by difference in gram": ["The primary function of carbohydrates is to provide the body with energy. After consumption, carbohydrates (also named carbs) are broken down into glucose. This glucose can then be used to produce ATP (adenosine triphosphate), which can be seen as fuel for the cells in the body. Even though ATP can be produced from different nutrients (for example protein and fats), it is easiest for the body to produce ATP from carbohydrates.", "If you consume more carbs than your body requires, these carbs will be transformed into glycogen. The glycogen reserves of your body are mostly stored in your liver and muscles, and ensure the presence of fuel for the body in between meals. However, once your glycogen reserves are filled and you consume carbs, the body will convert these carbs into body fat. Systematically consuming too much carbohydrates can thus make you overweight!", "Systematically consuming too little carbs will cause to body to go into a state of ketosis. Ketosis is a state where your body fuels itself with ketones instead of glucose. Ketones can be extracted by the body from protein and fats. Even though the brain can largely function on ketones, it still requires some degree of glucose to maintain full function. Being fully deprived of carbs will therefore cause the conversion of muscle mass and fat tissue into glucose. Because of this fat loss, many people try to lose weight by carbohydrate deprivation. There is no evidence of carbohydrate deprivation being harmful to the human body, unless your body fat percentage is at such a low level that it cannot convert into glucose anymore."],

"Energy in kcal": ["Kilocalories are units of measurement and not actual substances.  For instance, a calorie of protein contains the same amount of energy as a calorie of fat or a calorie of carbohydrates. If you increase your food energy intake and exceed your body's metabolic requirements, the extra calories in your diet will make you gain weight. You can also gain weight if you maintain your food intake and decrease your body's metabolism by decreasing your level of physical activity. ", "Consuming too many calories relative to how many calories you burn will lead to an increase of body weight.", "Consuming too little calories relative to how many calories you burn will lead to a decrease of body weight."],

"Fiber, total dietary in gram": ["Fiber is a form of carbohydrates that is not transformed into glucose. Instead, fiber molecules largely stay intact as they travel down the digestive tract. On their way down, they bind the contents of your digestive system and ensure lubrication. Fibers are also fuel for the “good” bacteria present in your intestines. The daily recommended fiber intake is 38 grams in adult men and 25 grams in adult women.", "Consuming too much fiber can lead to the blockage of your digestive system. However, it is quite difficult to actually achieve overconsumption of fiber. People that consume too much fiber usually eat abundant foods that are fortified with fiber, or take fiber supplements.", "Interesting enough, studies have revealed similar effects for consuming too little fiber in comparison to consuming too much fiber."],

"Folate, DFE in microgram": ["Folate (Vitamin B9) is present in some of the foods we eat. In contrast, folic acid is a synthetic form of folate that needs to be converted before the body can actually do something with it. Your body uses folate to create DNA and cells, as it is unable to divide cells without the use of folate. The recommended daily amount of folate for adults is around 400 micrograms.", "First of all, it is impossible to consume too much folate through a regular diet. However, the intake of supplements containing folate in combination with folate consumed through your diet can lead to abundant folate intake. The abundant intake of folate can mask vitamin B12 (found in animal products) deficiency up to a point where the damage done by this B12 deficiency is irreversible. Furthermore, abundantly consumed folic acid (artificial folate) cannot be converted into actual folate before it reaches the bloodstream. As a result, your cells will absorb folic acid instead of actual folate, which is useless to them. Because the folic acid replaces the folate, your body cells will display behaviors similar to folate deficiency.", "Consuming too little folate can do permanent damage to the body. The symptoms of folate deficiency are fatigue, weakness and shortness of breath. Scientists further suggest that folate deficiency can damage the DNA, but also enables cancers to develop more easily. Furthermore, folate deficiency increases the chances of heart diseases."],

"Iron, Fe in milligram": ["Iron is a mineral that is vital for many bodily functions. It is a crucial part of hemoglobin, a protein found in red blood cells. Hemoglobin is responsible for delivering oxygen to all of the body's cells. It is also essential for the correct development and functioning of cells, and the production of some hormones and tissues. The recommended daily allowance of Iron is 11 milligram in men and 16 milligrams in women.", "Consuming too much iron (usually through supplements) can lead to so-called “iron overload”. Excess iron in vital organs, even in mild cases of iron overload, increases the risk for liver disease (cirrhosis, cancer), heart attack or heart failure, diabetes mellitus, osteoarthritis, osteoporosis, metabolic syndrome, hypothyroidism, hypogonadism, numerous symptoms and in some cases premature death.", "Iron deficiency can result in a confusing array of symptoms, including fatigue and weakness, poor work performance, increased risk of infections, difficulty keeping warm, lightheadedness, rapid heartbeat, and shortness of breath with exercise."],

"Magnesium, Mg in milligram": ["Magnesium acts as the gatekeeper for NMDA receptors, which are involved in healthy brain development, memory and learning. It prevents nerve cells from being overstimulated, which can kill them and may cause brain damage. Magnesium helps your heart muscle cells relax by countering calcium, which stimulates contractions. These minerals compete with each other to ensure heart cells contract and relax properly. The recommended daily allowance of Magnesium is 300 milligrams.", "It is almost impossible to consume too much magnesium from a regular diet, however supplements could lead to abnormal intakes of magnesium. Symptoms of taking too much magnesium include diarrhea, vomiting, stomach cramps and depression.", "Magnesium acts as a natural calcium blocker, helping your muscle cells relax after contracting. When magnesium levels are low, your muscles may contract too much and cause symptoms such as cramps or muscle spasms. Furthermore low magnesium levels are linked to osteoporosis, high blood pressure and fatigue."],

"Niacin in milligram": ["Niacin, or vitamin B3, is a vitamin that acts as an antioxidant and plays a role in cell signaling and DNA repair. It furthermore helps balance your cholesterol levels, decreasing the risk and effects of type 1 diabetes. The recommended daily allowance of Niacin is 15 milligrams.", "Taking in too much Niacin is not possible through a regular diet, but can be achieved by taking supplements. Symptoms of Niacin overdose include vomiting, diarrhea, stomach pains and an itching skin. An intake of above 2000 milligrams can even lead to death.", "Structural Niacin deficiency leads to Pellagra, which is a disease where the body has issues with regenerating body cells and can be lethal if untreated."],

"Phosphorus, P in milligram": ["The main function of phosphorus is in the formation of bones and teeth. It plays an important role in how the body uses carbohydrates and fats. It is also needed for the body to make protein for the growth, maintenance, and repair of cells and tissues. Phosphorus also helps the body make ATP, a molecule the body uses to store energy. Furthermore, Phosphorus works together with the B vitamins. It also helps with kidney function, muscle contractions, normal heartbeat and nerve signaling. The recommended daily allowance of Phosphorus is 550 milligrams.", "It’s rare to have too much phosphorus in your blood. Typically, only people with kidney problems or those who have problems regulating their calcium develop this problem. Too much phosphate can be toxic. An excess of the mineral can cause diarrhea, as well as a hardening of organs and soft tissue. High levels of phosphorus can affect your body’s ability to effectively use other minerals, such as iron, calcium, magnesium, and zinc. It can combine with calcium causing mineral deposits to form in your muscles.", "Phosphorus deficiency is rare. Even when people don’t get enough of this mineral in their diets, the body can compensate by reabsorbing what’s already in the bloodstream. That said, severe starvation cases can result in hypophosphatemia. If you are deficient in other vitamins, like vitamin D, you may also have more trouble absorbing phosphorus and other minerals, like calcium, because of how they work together."],

"Potassium, K in milligram": ["Potassium is a mineral that functions in the body as an electrolyte. This means that it enables the body to send electric nerve signals from the brain to the cells in the body. Furthermore it helps to maintain a healthy blood pressure, protect from strokes, maintain healthy body water levels and prevents kidney stones. The recommended amount of potassium intake for adults is around 3000 milligrams.", "It is almost impossible to consume too much potassium, and actually most people consume too little potassium on a daily basis. However, by the use of supplements in combination with a regular diet, too much potassium could lead to muscle weakness and disturbances in your heart rhythm.", "Even though most of us consume too little potassium, the effects are usually not notable. However, severe potassium deficiency disturbs the functioning of the nervous system, leading to malfunctioning muscles, including the heart."],

"Riboflavin in milligram": ["Riboflavin (Vitamin B2) is a water-soluble vitamin, which helps break down proteins, fats, and carbohydrates. It plays a vital role in maintaining the body's energy supply. Riboflavin helps convert carbohydrates into adenosine triphosphate (ATP). The human body produces ATP from food, and ATP produces energy as the body requires it. The compound ATP is vital for storing energy in muscles. The recommended daily allowance of Riboflavin is 1.3 milligrams.", "An overdose is unlikely, as the body can absorb up to around 27 milligrams of riboflavin, and it expels any additional amounts in the urine. However, very high amounts of vitamin B2 may lead to itching, numbness, burning or prickling, yellow or orange urine and sensitivity to light.", "Symptoms of Riboflavin deficiency include sore throat, redness and swelling of the lining of the mouth and throat, cracks or sores on the outsides of the lips and at the corners of the mouth, inflammation and redness of the tongue, and a moist, scaly skin inflammation. Other symptoms may involve the formation of blood vessels in the clear covering of the eye and decreased red blood cell count."],

"Sugars, total in gram": ["On the back of food packaging, you will most likely to be able to see the carb content per 100 grams of the particular product. Underneath the carbs you can then see: of which sugars. Sugars are also a form of carbohydrates (see carbohydrates) which can be converted into glucose faster than other carbs. So if you need a quick energy boost, consuming something with sugar is the best way to go.", "Too much sugar will have the same effect as too many carbohydrates.", "Too little sugar will have the same effect as too little carbohydrates."],

"Thiamin in milligram": ["Thiamine is an essential nutrient that all tissues of the body need to function properly. Thiamine was the first B vitamin that scientists discovered. This is why its name carries the number 1. Like the other B vitamins, thiamine is water-soluble and helps the body turn food into energy. The recommended daily allowance of Thiamin is 1 milligram.", "Evidence does not confirm any harm from too much vitamin B1.", "Thiamin deficiency can lead to two major health problems: beriberi and Wernicke-Korsakoff syndrome. Beriberi affects breathing, eye movements, heart function, and alertness. It’s caused by a buildup of pyruvic acid in the bloodstream, which is a side effect of your body not being able to turn food into fuel. Wernicke-Korsakoff syndrome is technically two different disorders. Wernicke’s disease affects the nervous system and causes visual impairments, a lack of muscle coordination, and mental decline. If Wernicke’s disease is left untreated, it can lead to Korsakoff syndrome. Korsakoff syndrome permanently impairs memory functions in the brain."],

"Vitamin A, RAE in microgram": ["Vitamin A helps form and maintain healthy teeth, skeletal and soft tissue, mucus membranes, and skin. It is also known as retinol because it produces the pigments in the retina of the eye. Vitamin A promotes good vision, especially in low light. It may also be needed for reproduction and breastfeeding. Even though vitamin A largely occurs in animal products, it can also be found in fruits and vegetables in the form of carotenoids. These carotenoids first need to be converted by the body into usable vitamin A, but this takes relatively little effort. A well-known carotenoid is beta-carotene, and foods containing beta-carotene usually have an orange color. The recommended daily allowance of vitamin A is 800 micrograms.", "Overconsumption of vitamin A is virtually impossible from eating fruits or vegetables. However, eating a lot of beta-carotenes can temporarily give your skin a yellow/orange glow! However, consuming certain animal products (such as liver) and supplements can lead to excessive vitamin A intake. This is especially harmful for pregnant women as it can lead to birth defects.", "Vitamin A deficiency can lead to various kinds of eye diseases, including preventable blindness! Furthermore vitamin A deficiency weakens the immune system, making you more vulnerable to infection. Vitamin A deficiency is also especially dangerous to pregnant women, as a lack of vitamin A can lead to fetal defects in unborn babies."],

"Vitamin B-6 in milligram": ["Vitamin B6, also known as pyridoxine, is a water-soluble vitamin that your body needs for several functions. It’s significant to protein, fat and carbohydrate metabolism and the creation of red blood cells and neurotransmitters. Vitamin B6 may prevent a decline in brain function by decreasing homocysteine levels that have been associated with Alzheimer’s disease and memory impairments. Furthermore, Vitamin B6 may help reduce high homocysteine levels that lead to narrowing of arteries. This may minimize heart disease risk. The recommended daily allowance of Vitamin B6 is 1.3 milligram.", "People almost never get too much vitamin B6 from food. But taking high levels of vitamin B6 from supplements for a year or longer can cause severe nerve damage, leading people to lose control of their bodily movements. The symptoms usually stop when they stop taking the supplements. Other symptoms of too much vitamin B6 include painful, unsightly skin patches, extreme sensitivity to sunlight, nausea, and heartburn.", "People who don’t get enough vitamin B6 can have a range of symptoms, including anemia, itchy rashes, scaly skin on the lips, cracks at the corners of the mouth, and a swollen tongue. Other symptoms of very low vitamin B6 levels include depression, confusion, and a weak immune system. Infants who do not get enough vitamin B6 can become irritable or develop extremely sensitive hearing or seizures."],

"Vitamin C, total ascorbic acid in milligram": ["Vitamin C is an ‘antioxidant’, which strengthens the immune system. It prevents damage to your cells and ensures correct functioning of the liver. It also ensures healthy white blood cells, which attack diseases that enter your body. The daily recommended amount of vitamin C is 75 milligram for women and 90 for men.", "It is virtually impossible to consume too much vitamin C by just eating food, as symptoms of overconsumption will occur when more than 2000 milligram per day is consumed. However, supplements could achieve such numbers. Consuming such a large amount of vitamin C can lead to diarrhea and nausea.", "Consuming too little vitamin C will lead to all kinds of visible defects of your body. Amongst these effects are dry skin, bumpy skin, corkscrew-shaped body hair, spots on your fingernails and tooth loss. Furthermore your immune system is weakened, you will feel tired more often and the healing of wounds and bruises will go much slower. Vitamin C deficiency can in extreme cases even lead to scurvy!"]
}

# add all filenames in the raw_data directory to the array
csv_dataset = []
for (dirpath, dirnames, filenames) in walk("raw_data"):
    csv_dataset.extend(filenames)
    break

# call initial file
csv_data = csv_dataset[0]

# name of the current fruit
fruitname = csv_data[0:-4]

# open fruit csv file
csvfile = open(f"raw_data/{csv_data}", "r")

# create dataframe of fruit csv
df = pd.read_csv(csvfile, skiprows=4)

# delete unneccesary columns
df = df.loc[:, :"1Value per 100 g"]

# replace the unit names for abbreviations
df["Unit"] = df["Unit"].replace("mg", "milligram")
df["Unit"] = df["Unit"].replace("µg", "microgram")
df["Unit"] = df["Unit"].replace("g", "gram")

# add weight unit to nutrient column
df["Nutrient"] = df["Nutrient"] + " in " + df["Unit"]

# delete weight unit column
del df["Unit"]

# make nutrient type dataframe index
df.set_index('Nutrient', inplace=True)

# change column name
df = df.rename(columns = {"1Value per 100 g": fruitname})

csv_dataset = csv_dataset[1: ]

# loop through every csv file
for fruit in csv_dataset:
    data = open(f"raw_data/{fruit}", "r")

    # trim names
    fruittext = fruit[0:-4]

    # create dataframe of fruit csv's
    dataf = pd.read_csv(data, skiprows=4)

    # delete unneccesary columns
    dataf = dataf.loc[:, :"1Value per 100 g"]

    # replace unit names with abbreviations
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

    # select relevant data
    df = df.join(dataf[fruittext])
    df = df.loc["Caffeine in milligram" : "Vitamin D in IU"]
    df[fruittext] = pd.to_numeric(df[fruittext])

# turn all string numbers into real numbers
df["Apple"] = pd.to_numeric(df["Apple"])

# transpose table
df = df.transpose()

# delete all nutrients that are not present in fruit
df = df.loc[:, (df != 0).any(axis=0)]

# turn fruitnames into index
fruitnames = df.index

# turn df into JSON format
jsonfile = json.loads(df.to_json(orient="index"))

with open('nutrients.json', 'w') as outfile:
    json.dump(jsonfile, outfile)

# create colordict with data from top of page
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
