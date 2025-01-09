from bs4 import BeautifulSoup
import base64
from datetime import datetime
import requests
import re
from dotenv import load_dotenv
load_dotenv()


import json
import os

STATE_FILE = "data/state.json"

def load_state():
    # Load existing state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {}
    return state

def update_state(state):
    # Update state
    state["count"] += 1
    print(f"Current count: {state['count']}")

def save_state(state):
    # Save state
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def extract_number_id(input_string):
    match = re.search(r'\d+', input_string)

    if match:
        return match.group()
    else:
        return None
    
with open("templates/menu.html", "r") as f:
    menu_html = f.read()

with open("templates/no_menu.html", "r") as f:
    no_menu_html = f.read()

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
    with open("index.html", "w") as f:
        f.write(no_menu_html)
    exit()

url = "https://www.nutritics.com/menu/ma1135/" + menu_id  # Replace with the actual URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
results_div = soup.find('div', id='results')
child_divs = results_div.find_all('div', recursive=False)

main_menu_items = []
other_items = []
for item in child_divs:
    if item.get("data-groupname") == "Main Plate":
        main_menu_items.append(item.get("data-name"))
    else:
        other_items.append(item.get("data-name"))

state = load_state()
menu_items = main_menu_items + other_items
for key in menu_items:
    if key not in state.keys():
        state[key] = {"photo": "", "emoji": ""}

save_state(state)
"""
# This is for lunch photos
divs = results_div.find_all('div', class_=['foodphoto', ' small', 'exists'])
data_uris = []
for div in divs:
    style = div.get('style').split('(')[1][:-1]
    response = requests.get("https://www.nutritics.com"+style)
    image_data = response.content
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{image_base64}"
    data_uris.append(data_uri)
"""

main_menu_html = [f'<div class="table-row">{key}</div>' for key in main_menu_items]
other_items_html = [f'<div class="table-row">{key}</div>' for key in other_items]

with open("index.html", "w") as f:
    html_file = menu_html.replace("[main]", '\n'.join(main_menu_html))
    html_file = html_file.replace("[other]", '\n'.join(other_items_html))
    f.write(html_file)

#print(html_file)

exit()
