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
    <title>Lunch Items Today</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.6.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100%;
            width: 100%;
            box-sizing: border-box;
            position: relative;
        }

        .main-container {
            width: 90%;
            max-width: 600px;
            height: auto;
            margin: auto;
        }

        .main-title {
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }

        .lunch-table {
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .table-header {
            background-color: #343a40;
            color: #fff;
            text-align: center;
            font-weight: bold;
            padding: 10px;
            font-size: 1.2rem;
        }

        .table-content {
            width: 100%;
        }

        .table-row {
            text-align: center;
            padding: 10px;
            border-top: 1px solid #ddd;
        }

        .table-row:nth-child(even) {
            background-color: #f2f2f2;
        }

        .footer-text {
            position: absolute;
            bottom: 10px;
            right: 10px;
            font-size: 0.9rem;
            color: #555;
            font-style: italic;
            text-align: right;
            background-color: #fff;
            padding: 5px 10px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
    </style>
</head>
<body>

    <div class="main-container">
        <h1 class="main-title">Lunch Items Today:</h1>
        <div class="lunch-table">
            <div class="table-header">Lunch Items</div>
            <div class="table-content">
                [keys]
            </div>
        </div>
    </div>

    <div class="footer-text">Built by STEM</div>

    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.6.2/js/bootstrap.min.js"></script>
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

menu_html = [f'<div class="table-row">{key}</div>' for key in menu_items]

with open("index.html", "w") as f:
    f.write(html_file.replace("[keys]", '\n'.join(menu_html)))

#print(html_file)

exit()
from flask import Flask, render_template, jsonify

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

@app.route("/menu", methods=["GET"])
def menu():
    return jsonify(menu_items)

if __name__ == '__main__':
    app.run()
