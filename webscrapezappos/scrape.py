from bs4 import BeautifulSoup
import requests
import csv

# Open csv file
csv_file = open('scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product_name', 'Brand_name', 'Img_source', 'Price_tag'])

# Do  the work
for i in range(11):
    source = requests.get(f'https://www.zappos.com/filters/men-shoes/CK_XAVoFCwQ2bwHAAQLiAgMBCxg.zso?s=recentSalesStyle%2Fdesc%2F&p={i}').text
    soup = BeautifulSoup(source, 'lxml')

    for article in soup.find_all('article'):
        
        try:
            product_name = article.find('a')['aria-label'].split('.')[:2]
            product_name = ''.join(product_name)
            print(product_name)

            brand_name = article.find('p', class_='Xf').span.text
            print(brand_name)

            img_src = article.find('img', class_='Mg')['src']
            print(img_src)

            price_tag = article.find('span', class_='gg').text[1:]
            print(price_tag)

        except Exception as e:
            pass
        
        csv_writer.writerow([product_name, brand_name, img_src, price_tag])

# Close csv file
csv_file.close()

