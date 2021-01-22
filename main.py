""".."""
import requests
from bs4 import BeautifulSoup as bs

# get a valid input
url = input("Enter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

# catch errors in requests.get statement
try:
    req = requests.get(url)
    soup = bs(req.text, "lxml")
    page_text = soup.getText(separator=" ")
    print(page_text)

except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
