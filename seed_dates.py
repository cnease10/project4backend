import csv
import models
with open('./date-ideas.csv', 'r') as f:
    reader = csv.DictReader(f)
    for date_reader in reader:
        # print('Id:', date['date_id)
        date = {
            'date_id': date_reader['date_id'].strip(),
            'name': date_reader['name'].strip(),
            'description': date_reader['description'].strip()
        }
        print(date)
        models.Date.create(**date)