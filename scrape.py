from bs4 import BeautifulSoup
import requests
import cfscrape
import sys
import getopt
import os
import string
import random


def main():
    scraper = cfscrape.create_scraper()
    url_site = "https://prnt.sc/"

    # check arguments
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hf:n:c:")
    except getopt.GetoptError:
        print("./scrapy.py -f <OUTPUT-FOLDER> -n <NUMBER OF IMAGES>")
        sys.exit("Wrong arguments")

    amt = 1
    path = "./"
    conf = False
    # parse arguments
    for opt, arg in opts:

        if opt == "-f":
            if not os.path.isdir(arg):
                print("doesnt exist")
                try:
                    os.mkdir(arg)
                except OSError:
                    print("ERROR in creating dir (quitting)")
                    sys.exit(1)
            path = arg
        elif opt == "-n":
            try:
                amt = int(arg)
            except TypeError:
                print("ERROR - incorrect amount type")
            print(amt)
        elif opt == "-c":
            conf = True
            config_name = arg
            if os.path.isfile(config_name):
                print("it exists")
                with open(config_name, "r") as f:
                    config_cont = f.read()
                    name_list = eval(config_cont)

        if not conf and os.path.isfile("./con.txt"):
            with open("./con.txt", "r") as f:
                con_content = f.read()
            if con_content:
                name_list = eval(con_content)
                print(type(name_list))
            else:
                name_list = []

    for i in range(amt):
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
            print(link, name)

            try:
                im = requests.get(link)
            except requests.ConnectionError:
                print(f"doesnt exist - skipping ({url_code})")
            else:
                print(path + name + ".png")
                with open(path + name + ".png", "wb") as f:
                    f.write(im.content)
        else:
            print(f"Image already downloaded {url_code} - skipping ")
            i += 1

    if conf:
        pass
    else:
        with open("con.txt", "w") as f:
            f.write(str(name_list))


if __name__ == "__main__":
    main()
