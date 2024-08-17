import dotenv
import os
import csv
import random


dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

situations_list = []
with open('situation_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        situations_list.append(row[0])
    file.close()

current_situation = situations_list[random.randint(0, len(situations_list))]

items_list = []
with open('items_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        items_list.append(row[0])
    file.close()

selectable_items = random.sample(items_list, k=4)


print("Current situation: ", current_situation)
print("Selectable items: ", selectable_items)