import requests
from bs4 import BeautifulSoup
from lxml import html 
import csv_creator
from fake_useragent import UserAgent
ua = UserAgent()
header  = {'User-Agent':str(ua)}
import time


def Search_url(url_check, category_name, pagination_url):
    category_name = category_name.replace(' ','+')    
    if url_check == 'pagination':
        url = pagination_url
    else:
        url = 'https://www.ebay.com/sch/i.html?_nkw='+(category_name)+'&_sop=12'
    response = requests.get(url,headers = header)
    soup = BeautifulSoup(response.text,"html.parser")
    anchor_tags =[]
    for anchor_tag in soup.find_all(class_='s-item__link'):
        tag = anchor_tag.get('href')
#         print(tag)
        Search_product(tag, category_name)
    #all_anchor_tags.append(anchor_tag.get('href'))
    

    
    pagination = soup.find(class_='x-pagination__ol')
    pages =[]
    for page in pagination:
        for li in page:
            pages.append(li.get('href'))
    if pagination is not None:
        for link in pages[1:]:
            pagination_url = link
            Search_pagination('pagination',category_name,pagination_url)
            
        
    
        
def Search_pagination(pagination,category_name,pagination_url):
    print(pagination)
    page_response = requests.get(pagination_url,headers = header)
    soup = BeautifulSoup(page_response.text,"html.parser")

    for anchor_tag in soup.find_all(class_='s-item__link'):
        tag = anchor_tag.get('href')
        Search_product(tag, category_name)
        time.sleep(2)
    
    
def Search_product(url, category_name):
    product_details = {}
    ua = UserAgent()
    header = {'User-Agent': str(ua)}
    ajax_url = url
#     print(url)
    page_response = requests.get(ajax_url,headers =header)
    bs_result = BeautifulSoup(page_response.content,'lxml')
    
    product_details={}
    try:
        Name = bs_result.find('h1',class_='it-ttl').text.strip()
        product_details['product-name'] = Name.replace('\xa0','')
    except:
        product_details['product-name'] ='Nill'
    try:    
        product_details[''] = bs_result.find('span',{'class':'ebay-review-start-rating'}).text.strip()
    except:
        product_details['review'] = 'Nill'
    try:
        product_details['price'] = bs_result.find('span',{'class':'notranslate'}).text.strip()
    except:
        product_details['price'] = 'Nill'
    try:
        product_details['Review_count'] = bs_result.find('span',{'class':'ebay-reviews-count'}).text
        product_detials['Review_count'] = re.findall(r'\d+', Review_count)
    except:
        product_details['Review_count'] ='Nill'
    try:
        product_details['Image'] = bs_result.find('img',{'id':'icImg'})['src']
    except:
        product_details['Image'] ='Nill'
    print(product_details)
    
    csv_creator.product_csv_creator_file(product_details, category_name)

    
Search_url('category_name','Camera RICOH','')
    


