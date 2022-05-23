from datetime import date
import csv

def get_user_csv_data(filename):
    with open(filename, encoding='utf8') as file:
        csvreader = csv.reader(file)
        return [{
            'id':index + 1,
            'name':row[1],
            'nickname':row[2],
            'email':row[3],
            'password':row[4],
            'dob':date.fromisoformat(row[5])
        }
        for index,row in enumerate(csvreader)]