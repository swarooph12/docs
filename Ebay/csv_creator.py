import csv
import os
import os.path
import io
import datetime
today_date = datetime.date.today()


def product_csv_creator_file(data, category_name):

    if not os.path.exists('product_csv/'+str(today_date)+'/'):
        
        os.makedirs('product_csv/'+str(today_date)+'/')
    filename = 'product_csv/'+str(today_date)+'/'+category_name+'.csv'
    file_exists = os.path.isfile(filename)
    with io.open(filename, 'a', encoding='utf-8') as csvfile:
        fieldnames = ['product-name','review','price','review-count','image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            
            writer.writeheader()

        writer.writerows([{'product-name':data['product-name'], 'review': data['review'], 'price': data['price'],
                           'review-count': data['Review_count'],'image': data['Image']}])

        
        print("Writing complete")
