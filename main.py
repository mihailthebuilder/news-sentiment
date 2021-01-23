""".."""
import json
import re
import requests
from bs4 import BeautifulSoup as bs
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# get a valid input
url = input("\nEnter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

try:
    req = requests.get(url)

    # get the individual text pieces inside the web page as separate list elements
    soup_li = bs(req.text, "lxml").body.getText(separator="||").split("||")

    text_li = []
    afinn = Afinn()
    analyzer = SentimentIntensityAnalyzer()

    sum_text = 0
    count_text = 0

    max_score = 0
    max_text = ""
    min_score = 0
    min_text = ""

    for text in soup_li:
        if len(text.split()) >= 5:
            text_lower = re.sub(r"\u2018|\u2019|\u2014", "", text.lower())

            afinn_score = afinn.score(text_lower)  # usually from -5 to +5
            vader_score = analyzer.polarity_scores(text_lower)[
                "compound"
            ]  # from -1 to +1

            combined_score = 0

            if afinn_score != 0 or vader_score != 0:
                count_text += 1

                if afinn_score == 0:
                    combined_score = vader_score
                elif vader_score == 0:
                    combined_score = afinn_score
                else:
                    combined_score = (afinn_score * 2 + vader_score * 10) / 2

                sum_text += 10 if combined_score > 0 else -10

                if combined_score > max_score:
                    max_score = combined_score
                    max_text = text_lower
                elif combined_score < min_score:
                    min_score = combined_score
                    min_text = text_lower

            text_li.append(
                {
                    "text": text_lower,
                    "combined_score": combined_score,
                    "vader_score": vader_score,
                    "afinn_score": afinn_score,
                }
            )

    with open("output.json", "w") as file:
        json.dump(text_li, file)

    print(
        f"\n'{url}' has an average positivity score of {round(sum_text/count_text*2)}."
    )
    print(
        f"\nThe most negative score was {min_score}, which came from this piece of text '{min_text}'"
    )
    print(
        f"\nThe most positive score was {max_score}, which came from this piece of text '{max_text}'"
    )
    print(f"\n**Note: scores usually range between -10 and +10")

# catch errors in requests.get statement
except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when trying to access the '{url}' URL.\n\nError message: '{error}'"
    )
except Exception as error:
    print(
        f"Something went wrong after a successful request was made to the '{url}' URL.\n\nError message: '{error}'"
    )
