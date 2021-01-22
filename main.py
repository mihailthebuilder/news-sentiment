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

    # get the text
    soup = bs(req.text, "lxml").main

    # remove pieces of
    for html_tag in soup.find_all():

        words_num = len(html_tag.get_text(strip=True).split())

        if words_num <= 2:
            html_tag.extract()

    with open("testing.html", "w") as file:
        file.write(soup.prettify())

    # without separator, text in different html elements would be joined together
    page_text = soup.getText(separator=". ")

    with open("testing.txt", "w") as file:
        file.write(page_text)
    # print(page_text)

    """
    # get stopwords
    sw = nltk.corpus.stopwords.words("english")

    # get all words in lower case, excluding stopwords
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
    tokens = [
        token.lower() for token in tokenizer.tokenize(page_text) if token not in sw
    ]

    print(tokens)
    """

except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
