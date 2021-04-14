import csv
import json

places = dict()

progress = 0;
with open('allCountries.txt', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter='\t')
    for row in reader:
        places[row[1]] = 1
        progress += 1
        if (progress % 100000 == 0):
            print("still processing... progress = " + str(progress))
    
print("saving...")
with open("all_countries_dict.json", "w", encoding='utf-8') as f:
    f.write(json.dumps(places))
