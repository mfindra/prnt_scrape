from bs4 import BeautifulSoup
import requests
import cfscrape
import sys
import getopt
import os
import string
import random
import datetime
from tqdm import tqdm


def main():
    scraper = cfscrape.create_scraper()
    url_site = "https://prnt.sc/"

    # check arguments
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "htdf:n:c:")
    except getopt.GetoptError:
        print("./scrape.py -f <OUTPUT-FOLDER> -n <NUMBER OF IMAGES>")
        sys.exit("Wrong arguments")

    amt = 1
    path = "./"
    conf = False
    t_stamp = False
    debug = False

    # parse arguments
    for opt, arg in opts:
        if opt == "-h":
            print("PRNT.SC SCRAPER\n====================")
            print("usage: python3 ./scrape.py <arguments>")
            print("arguments: todo")
            sys.exit(0)
        elif opt == "-f":
            if not os.path.isdir(arg):
                if debug:
                    print("doesnt exist")
                try:
                    os.mkdir(arg)
                except OSError:
                    print("ERROR in creating dir")
                    sys.exit(1)
            path = arg
        elif opt == "-n":
            try:
                amt = int(arg)
            except TypeError:
                print("ERROR - incorrect amount type")
                sys.exit("Wrong argument type")
        elif opt == "-c":
            conf = True
            config_name = arg
            if os.path.isfile(config_name):
                print("it exists")
                with open(config_name, "r") as f:
                    config_cont = f.read()
                    name_list = eval(config_cont)
        elif opt == "-t":
            t_stamp = True
        elif opt == "-d":
            debug = True

    # check for local conf file if not given
    if not conf and os.path.isfile("./con.txt"):
        with open("./con.txt", "r") as f:
            con_content = f.read()
        if con_content:
            name_list = eval(con_content)
        else:
            name_list = []
    else:
        name_list = []

    for i in tqdm(range(amt)):
        url_code = "10" + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=5)
        )
        if url_code not in name_list:
            name_list.append(str(url_code))
            url = url_site + url_code
            soup = BeautifulSoup(scraper.get(url).content, "html.parser")
            images = soup.find_all("img")

            name = url_code
            link = images[0]["src"]
            if debug:
                print(f"Downloading image {name} from {link}")

            try:
                im = requests.get(link)
            except requests.ConnectionError:
                if debug:
                    print(f"doesnt exist - skipping ({url_code})")
            else:
                if t_stamp:
                    name = path + str(datetime.date.today()) + "-" + name + ".png"
                else:
                    name = path + name + ".png"
                with open(name, "wb") as f:
                    f.write(im.content)
        else:
            if debug:
                print(f"Image already downloaded {url_code} - skipping ")
            i += 1

    with open("con.txt", "w") as f:
        f.write(str(name_list))


if __name__ == "__main__":
    main()
