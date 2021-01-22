""".."""
import requests
from bs4 import BeautifulSoup as bs
import nltk

# get a valid input
url = input("Enter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

# catch errors in requests.get statement
try:
    req = requests.get(url)

    # get the individual text pieces inside the web page as separate list elements
    soup = bs(req.text, "lxml").main
    text_li = [
        text.lower()
        for text in soup.getText(separator="||").split("||")
        if len(text.split()) >= 3
    ]

    print(text_li)

except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
