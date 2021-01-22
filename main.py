""".."""
import requests
from bs4 import BeautifulSoup as bs
from nltk.tokenize import RegexpTokenizer

# get a valid input
url = input("Enter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

# catch errors in requests.get statement
try:
    req = requests.get(url)

    # get the text
    soup = bs(req.text, "lxml")

    # without separator, text in different html elements would be joined together
    page_text = soup.getText(separator=" ")

    tokenizer = RegexpTokenizer("\w+")
    tokens = tokenizer.tokenize(page_text)
    print(tokens)

except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
