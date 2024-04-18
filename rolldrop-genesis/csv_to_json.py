from decimal import Decimal
import csv 
import json 
import os
import argparse

def is_address(address):
    return len(address) == 42 and address.startswith('0x')

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
    
        #convert each csv row into python dict
        for row in csvReader: 
            if not is_address(row['claim_address']):
                print(f"Invalid address: {row['claim_address']}")
                continue
            amount = row['amount']
            # print(amount)
            amount = int(Decimal(amount) * (Decimal(10) ** 18))
            # print(amount)
            row['amount'] = amount
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process user allocations csv.')
  parser.add_argument('filepath', type=str, help='path to the csv file')

  args = parser.parse_args()
  filepath = args.filepath
  
  path, filename = os.path.split(filepath)
  jsonFilePath = os.path.join(path, filename.split('.')[0] + '.json')
  print(f'Converting {filepath} CSV to JSON at {jsonFilePath}...')
  csv_to_json(filepath, jsonFilePath)