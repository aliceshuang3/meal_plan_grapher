import csv
import random
import time

dollars = 0
projected = 1000
rec = 1000

fieldnames = ["dollars", "projected", "rec"]


with open('static/diningDollars2.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('static/diningDollars2.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "dollars": dollars,
            "projected": projected,
            "rec": rec
        }

        csv_writer.writerow(info)
        print(dollars, projected, rec)

        dollars = dollars + random.randint(-100, 50)
        projected = projected + random.randint(-20, 20)
        rec = rec + random.randint(-15, 25)

    time.sleep(1)
