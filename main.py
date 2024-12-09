from bs4 import BeautifulSoup
import base64
from datetime import datetime
import requests
import re

def extract_number_id(input_string):

    # Use regular expression to find the number

    match = re.search(r'\d+', input_string)

    if match:

        return match.group()

    else:

        return None  # Return None if no number is found



# Step 1: Get the current date in mm/dd format

current_date = datetime.now().strftime("%m/%d")



url = "https://www.nutritics.com/menu/ma1135"

response = requests.get(url)

# Step 2: Parse the HTML document with BeautifulSoup

soup = BeautifulSoup(response.content, 'html.parser')



# Step 3: Search for the div that contains the current date within the span tag

menu_div = None

for div in soup.find_all("div", class_='menu'):

    span = div.find("span", class_='title')

    if span and current_date in span.text:

        menu_div = div

        break



# Step 4: Extract the id attribute if the div is found

menu_id = None

if menu_div:
    menu_id = menu_div.get("id")
    menu_id = extract_number_id(menu_id)
    print(f"Menu ID: {menu_id}")

else:
    print("No menu found for today's date.")
    exit()

html_file = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Items</title>
    <style>
        /* Ensure no margin or padding and that the content fills the page */
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            /*overflow: hidden;  /* Prevent scrolling */
        }
        .circular-image {
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    border: 5px solid #333;
                    object-fit: fill;
                }

        /* Style for the main title */
        h1.main-title {
            font-size: 5vw;  /* Adjust text size based on viewport width */
            text-align: center;
            margin: 0;
        }

        /* Responsive text size for individual items */
        h1 {
            font-size: 4vw;  /* Adjust text size based on viewport width */
            text-align: center;
            margin: 10;
        }

        /* Flexbox container for center alignment */
        .content {
            width: 60%;
            height: 40%;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            /*overflow: hidden;  /* Prevent scrolling within the content */
        }

        /* Media Queries to adjust text size on smaller screens */
        @media (max-width: 600px) {
            h1.main-title {
                font-size: 10vw; /* Larger font for smaller screens */
            }
            h1 {
                font-size: 15vw; /* Larger font for smaller screens */
            }
        }

        @media (max-width: 400px) {
            h1.main-title {
                font-size: 15vw; /* Even larger font for very small screens */
            }
            h1 {
                font-size: 20vw; /* Larger font for very small screens */
            }
        }
    </style>
</head>
<h1 class="main-title">Lunch Items Today:</h1>
<body>
    <div class="content">
        [keys]
    </div>
</body>
</html>
"""

url = "https://www.nutritics.com/menu/ma1135/" + menu_id  # Replace with the actual URL

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

results_div = soup.find('div', id='results')

child_divs = results_div.find_all('div', recursive=False)


menu_items = []
for item in child_divs:
    if item.get("data-groupname") == "Main Plate":
        menu_items.append(item.get("data-name"))




divs = results_div.find_all('div', class_=['foodphoto', ' small', 'exists'])
data_uris = []
for div in divs:
    style = div.get('style').split('(')[1][:-1]
    response = requests.get("https://www.nutritics.com"+style)
    image_data = response.content
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{image_base64}"
    data_uris.append(data_uri)

menu_html = [f"<h1>{key}</h1>" for key in menu_items]




from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    url = "https://www.nutritics.com/menu/ma1135/" + menu_id  # Replace with the actual URL

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    results_div = soup.find('div', id='results')

    child_divs = results_div.find_all('div', recursive=False)


    menu_items = []
    for item in child_divs:
        if item.get("data-groupname") == "Main Plate":
            menu_items.append(item.get("data-name"))




    divs = results_div.find_all('div', class_=['foodphoto', ' small', 'exists'])
    data_uris = []
    for div in divs:
        style = div.get('style').split('(')[1][:-1]
        response = requests.get("https://www.nutritics.com"+style)
        image_data = response.content
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{image_base64}"
        data_uris.append(data_uri)

    print(len(menu_items))
    print(len(data_uris))
    data_dict = dict(zip(menu_items, data_uris[::2]))
    

    return render_template('index.html', items=data_dict)

if __name__ == '__main__':
    app.run()
