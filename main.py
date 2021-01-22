""".."""
import requests
import json
from bs4 import BeautifulSoup as bs
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# get a valid input
url = input("Enter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

try:
    req = requests.get(url)

    # get the individual text pieces inside the web page as separate list elements
    soup_li = bs(req.text, "lxml").main.getText(separator="||").split("||")

    text_li = []
    afinn = Afinn()
    analyzer = SentimentIntensityAnalyzer()

    for text in soup_li:
        if len(text.split()) >= 3:
            text_lower = text.lower()

            afinn_score = afinn.score(text_lower) * 20  # from -5 to +5
            vader_score = (
                analyzer.polarity_scores(text_lower)["compound"] * 100
            )  # from -1 to +1

            combined_score = 0

            if afinn_score == 0:
                if vader_score != 0:
                    combined_score = round(vader_score)
            elif afinn_score != 0:
                if vader_score != 0:
                    combined_score = round((afinn_score + vader_score) / 2)
                else:
                    combined_score = round(afinn_score)

            text_li.append(
                {
                    "text": text_lower,
                    "score": combined_score,
                }
            )

    with open("output.json", "w") as file:
        json.dump(text_li, file)

# catch errors in requests.get statement
except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
