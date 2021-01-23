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
    soup_li = bs(req.text, "lxml").main.getText(separator="||").split("||")

    text_li = []
    afinn = Afinn()
    analyzer = SentimentIntensityAnalyzer()

    for text in soup_li:
        if len(text.split()) >= 5:
            text_lower = re.sub(r"\u2018|\u2019|\u2014", "", text.lower())

            afinn_score = round(afinn.score(text_lower) * 100 / 6, 2)  # from -6 to +6
            vader_score = round(
                (analyzer.polarity_scores(text_lower)["compound"] * 100), 2
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
                    "vader_score": vader_score,
                    "afinn_score": afinn_score,
                }
            )

    with open("output.json", "w") as file:
        json.dump(text_li, file)

    min_value = 0
    key_min = 0
    max_value = 0
    key_max = 0

    for key, value in enumerate(text_li):
        if value["score"] > max_value:
            key_max = key
            max_value = value["score"]
        if value["score"] < min_value:
            key_min = key
            min_value = value["score"]

    sum_text = 0
    count = 0

    for text in text_li:
        if text["score"] != 0:
            sum_text += text["score"]
            count += 1

    print(f"\n'{url}' has an average positivity score of {round(sum_text/count)}")
    print(
        f"\nThe most negative score was {min_value}, which came from this piece of text '{text_li[key_min]['text']}'"
    )
    print(
        f"\nThe most positive score was {max_value}, which came from this piece of text '{text_li[key_max]['text']}'"
    )
    print(
        "\n**Note: all values range between -100 and 100. The processed data has been dumped into the 'output.json' file."
    )

# catch errors in requests.get statement
except requests.exceptions.ConnectionError as error:
    print(
        f"\nAn error occurred when submitting a request with the '{url}' URL.\n\nError message: '{error}'"
    )
