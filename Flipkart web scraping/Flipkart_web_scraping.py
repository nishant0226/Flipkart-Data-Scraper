import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging

flipkart_url = "https://www.flipkart.com/search?q=tv"
try:
    urlclient = urlopen(flipkart_url)
    flipkart_page = urlclient.read()
    flipkart_html = BeautifulSoup(flipkart_page, "html.parser")
except Exception as e:
    logging.error(str(e))
    exit()

big_boxes = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
del big_boxes[0:3]

for big_box in big_boxes:
    product_link = "https://www.flipkart.com" + big_box.div.div.div.a['href']
    try:
        product_req = requests.get(product_link)
        product_html = BeautifulSoup(product_req.text, "html.parser")
    except Exception as e:
        logging.error(str(e))
        continue

    comment_box = product_html.find_all("div", {"class": "_16PBlm"})
    for box in comment_box:
        if box is not None:
            comments = box.div.div.find_all("p", {"class": "_2sc7ZR _2V5EHH"})
            if len(comments) > 0:
                print(f"The Customer's Name is {comments[0].text}")
            ratings = box.div.div.div.div.text
            print(f'The rating are {ratings}')
            summaries = box.div.div.div.find_all("p", {"class": "_2-N8zT"})
            if len(summaries) > 0:
                print(f'The summary is as {summaries[0].text}')
            likes = box.div.div.find_all("div", {"class": ""})
            if len(likes) > 0:
                print(f'The likes are {likes[0].text}')

