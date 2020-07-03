import csv
import urllib.request
import os 

with open('scrape.csv') as csvfile:
    datareader = csv.reader(csvfile)
    next(datareader)
    for row in datareader:
        image_link = row[2]
        image_name = image_link.split('/')[-1]
        price = row[-1]
        brand = row[1]

        # Check if directory exist, if not create one:
        if not os.path.isdir(f'images/{brand}/'):
            os.makedirs(f'images/{brand}/')

        urllib.request.urlretrieve(image_link,f'images/{brand}/{brand}-{price}-{image_name}')
