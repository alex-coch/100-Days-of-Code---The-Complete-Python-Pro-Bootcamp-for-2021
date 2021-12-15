import requests

response = requests.get(url="https://elephant-api.herokuapp.com/elephants/random")
response.raise_for_status()
data = response.json()
print(data[0]['_id'])


# "_id": "5cf1d0dbcd5e98f2540c4d1c",
# "index": 3,
# "name": "Balarama",
# "affiliation": "Dasara",
# "species": "Asian",
# "sex": "Male",
# "fictional": "false",
# "dob": "1958",
# "dod": "-",
# "wikilink": "https://en.wikipedia.org/wiki/Balarama_(elephant)",
# "image": "https://elephant-api.herokuapp.com/pictures/missing.jpg",
# "note": "A lead elephant of the world-famous Mysore Dasara procession."

