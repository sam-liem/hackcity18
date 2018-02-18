import csv
import os

def to_csv(data):

    keys = data[0].keys()
    print(data)

    with open(os.getcwd()+'/tmp/bankData.csv', 'w') as f:
        headers = sorted([k for k, v in data[0].items() if k != "_links"])
        csv_data = [headers]

        for d in data:
            csv_data.append([d[h] for h in headers])

        writer = csv.writer(f)
        writer.writerows(csv_data)