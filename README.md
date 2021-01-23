# News Sentiment

Analyzes the overall positivity of news sites. Can be used on any other sites as well.

# Table of Contents
- [News Sentiment](#news-sentiment)
- [Table of Contents](#table-of-contents)
- [How to use](#how-to-use)
  - [`summary.json`](#summaryjson)
  - [`raw_data.json`](#raw_datajson)
- [How it works](#how-it-works)
- [License](#license)

# How to use

Place all the sites you wish to analyse in the [websites.txt](./websites.txt) file and install all the packages from [requirements.txt](./requirements.txt). Then run [main.py](./main.py) with your **Python 3** interpreter.

The script will show the website it's processing at a given point in time:
![processing](./demo/processing.png)

When it's complete, the script will print a notification and generate two `JSON` files.

## `summary.json`

`summary.json` contains a list of dictionaries, each representing one URL that we had in `requirements.txt`. 

```json
{
  "url": "wired.com",
  "data": {
    "avg_score": 5,
    "max_score": 9.062999999999999,
    "max_text": "The Best Laptop Stands to Save Your Neck",
    "min_score": -7.548,
    "min_text": "A Fight Over GameStop's Soaring Stock Turns Ugly"
  }
}
```

## `raw_data.json`

# How it works

# License 
Licensed under [Mozilla Public License 2.0](./LICENSE)