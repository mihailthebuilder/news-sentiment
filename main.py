""".."""
import requests

# get a valid input

while True:
    url = input("Enter the site you wish to analyse: ")

# check if valid input

req = requests.get(url)

print(req.text)


# calculate the sentiment using the dictionary
