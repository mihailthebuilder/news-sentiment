""".."""
import requests

# get a valid input
url = input("Enter the site you wish to analyse: ")

# add https if not in there at start
if url[0:9] != "https://":
    url = "https://" + url

try:
    req = requests.get(url)

except:
    print(f"An error occurred when submitting a request with the '{url}' URL")
