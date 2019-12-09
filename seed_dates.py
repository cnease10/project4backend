import csv
import models

are_you_sure = input('Are you sure? ')
if are_you_sure == 'y':
    with open('./date-ideas.csv', 'r') as f:
        reader = csv.DictReader(f)
        for date_reader in reader:
            date = {
                'name': date_reader['name'].strip(),
                'description': date_reader['description'].strip()
            }
            models.Date.create(**date)