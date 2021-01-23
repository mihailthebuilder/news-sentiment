"""main script"""
from os import path
import json
from sentiment import sentiment_analyze


def main():
    """main function"""
    print("--STARTED--")
    summary_data = []
    raw_data = []

    if path.exists("websites.txt"):

        with open("websites.txt", "r") as file:
            for url_raw in file:

                url = url_raw.strip("\n")
                print(f"Analyzing: {url}  ...")

                analyzed_site = sentiment_analyze(url)
                summary_dict = {"url": url}

                if analyzed_site["success"]:
                    summary_dict["data"] = {
                        key: analyzed_site[key]
                        for key in [
                            "avg_score",
                            "max_score",
                            "max_text",
                            "min_score",
                            "min_text",
                        ]
                    }

                else:
                    summary_dict["data"] = analyzed_site["message"]

                summary_data.append(summary_dict)
                raw_data.append({"url": url, "data": analyzed_site.get("raw_data")})

    with open("summary.json", "w") as file:
        file.write(json.dumps(summary_data))

    with open("raw_data.json", "w") as file:
        file.write(json.dumps(raw_data))

    print("--COMPLETE--")


if __name__ == "__main__":
    main()
