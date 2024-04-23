from decimal import Decimal
import csv 
import json 
import os
import argparse
import traceback

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
            try:
                if not is_address(row['claim_address']):
                    print(f"Invalid address: {row['claim_address']}")
                    continue
                jsonRow = {}
                for key, value in row.items():
                    if '.' in key:
                       parent_key, child_key = key.split('.')
                       actualKey = child_key
                       if parent_key not in jsonRow:
                            jsonRow[parent_key] = {}
                       actualObject = jsonRow[parent_key] 
                    else:
                        actualKey = key
                        actualObject = jsonRow
                    
                    if actualKey == 'amount':
                        clearedAmount = Decimal(value.replace(',', ''))
                        actualObject['amount'] = int(clearedAmount * (Decimal(10) ** 18))
                    else:
                        actualObject[actualKey] = value
                #add this python dict to json array
                jsonArray.append(jsonRow)
            except Exception:
                print(f"\Parsing row failed: {row}")
                print(traceback.format_exc())
                continue
  
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