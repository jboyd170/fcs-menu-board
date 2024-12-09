import requests

url = "https://wiki.hypixel.net/Salvaging"

response = requests.get(url)

with open("out.html","w") as f:
    f.write(response.text)