import csv

with open('texts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    text_d = {}
    for row in reader:
        text_d[row["name_of_text"]] = row["text"]
