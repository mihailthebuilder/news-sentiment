"""Function which calculates how positive a website's content is. Scores usually range between -10 and +10"""
import requests
from bs4 import BeautifulSoup as bs
from afinn import Afinn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentiment_analyze(url):
    """calculates a website's positivity"""

    # add https if not in there at start
    if url[0:8] != "https://":
        url = "https://" + url

    try:
        my_session = requests.session()
        for_cookies = requests.get(url).cookies
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
        }

        response = my_session.get(url, headers=headers, cookies=for_cookies)

        req_text = response.text

        # checking request html output
        # with open("testing.html", "w") as file:
        #    file.write(req_text)

        # remove unicode characters
        decoded_text = req_text.encode("ascii", "ignore").decode("unicode_escape")

        # get the individual text pieces inside the web page as separate list elements
        soup_li = bs(decoded_text, "lxml").body.getText(separator="||").split("||")

        # list which will hold the pieces of text together with their scores
        text_li = []

        # Initialise the 2 sentiment analysis libraries used
        afinn = Afinn()
        analyzer = SentimentIntensityAnalyzer()

        # sum of non-0 scores
        sum_text = 0

        # count of non-0 scores
        count_text = 0

        # max/min text scores holders
        max_score = 0
        max_text = ""
        min_score = 0
        min_text = ""

        for text in soup_li:

            # only look at pieces of text with 5+ sentences
            if len(text.split()) >= 5:

                afinn_score = afinn.score(text)  # usually from -5 to +5
                vader_score = analyzer.polarity_scores(text)[
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
                        max_text = text

                    elif combined_score < min_score:
                        min_score = combined_score
                        min_text = text

                text_li.append(
                    {
                        "text": text,
                        "combined_score": combined_score,
                        "vader_score": vader_score,
                        "afinn_score": afinn_score,
                    }
                )

        if count_text == 0:
            return {"success": False, "message": "Unable to calculate the scores."}

        else:

            return {
                "success": True,
                "avg_score": round(sum_text / count_text * 2),
                "max_score": max_score,
                "max_text": max_text,
                "min_score": min_score,
                "min_text": min_text,
                "raw_data": text_li,
            }

    # catch errors in requests.get statement
    except requests.exceptions.ConnectionError as error:
        return {
            "success": False,
            "message": f"\nAn error occurred when trying to access the '{url}' URL.\n\nError message: '{error}'",
        }
    except Exception as error:
        return {
            "success": False,
            "message": f"\nSomething went wrong when processing the '{url}' URL.\n\nError message: '{error}'",
        }