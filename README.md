# prnt.sc scraper

## Description
Prnt.sc image downloader and data scraper.
## Requirments and setup
Python3.8< <br>
`pip install requirments.txt`

## Usage
`python scrape.py -f <OUTPUT-FOLDER> -n <NUMBER OF IMAGES> -c <CONFIG-FILE>`

Arguments
- -h Print help
- -f Dir path to store all downloaded images
- -n Number of images to download
- -c Config file - contains list of downloaded images, to prevent duplicates
- -m (todo) download mode
- -t (todo) timestamp picture name
- -d Show debug info

## TODO
Image comare to prevent duplicates \
Image machine learning to catch phrases(mails, passwds, ...) \
Download mode - user given(number, type) or most recent \
Crate config from given diroctory \
Debug mode - write formated debug output \
Timestamp images (regex check for list!) \
Complete implementation description \