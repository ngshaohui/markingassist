import csv

with open('reference/tempread.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # compare 5 (student answer) and 6 (model answer)
        if row[2] == "7" and \
                row[5] == "A04-Insecure Design" and \
                row[6] == "A01-Broken Access Control":
            print(row[0])
