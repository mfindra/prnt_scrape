from bs4 import BeautifulSoup
import requests
import cfscrape
import sys
import getopt
import os

scraper = cfscrape.create_scraper()
url_site = "https://prnt.sc/"
url_code = "10zy3f5"
url = url_site + url_code

# check arguments
try:
    opts, _ = getopt.getopt(sys.argv[1:], "f:")
except getopt.GetoptError:
    print("./scrapy.py -f <DATA-FILE>")
    sys.exit("Wrong arguments")

# parse arguments
conf = False
for opt, arg in opts:
    if opt == "-f":
        conf = True
        config_name = arg

# check config file
if conf:
    if os.path.isfile("./" + config_name):
        print("it exists")
        with open(config_name) as f:
            config_content = f.readlines()
    else:
        print("doesnt exist")

soup = BeautifulSoup(scraper.get(url).content, "html.parser")
images = soup.find_all("img")

name = url_code
link = images[0]["src"]
print(link, name)

with open(name + ".jpg", "wb") as f:
    im = requests.get(link)
    f.write(im.content)
