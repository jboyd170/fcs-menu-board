from bs4 import BeautifulSoup

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



# URL of the webpage you want to scrape

url = "https://www.nutritics.com/menu/ma1135/" + menu_id  # Replace with the actual URL



# Step 1: Send a GET request to retrieve the HTML

response = requests.get(url)



# Check if the request was successful (status code 200)

if response.status_code == 200:

    # Step 2: Parse the HTML content with BeautifulSoup

    soup = BeautifulSoup(response.content, 'html.parser')



    # Step 3: Find the div with id 'results'

    results_div = soup.find('div', id='results')

    div = soup.find('div', class_=['foodphoto', ' small', 'exists'])

    if div:
        style = div.get('style').split('(')[1][:-1]
        img = requests.get("https://www.nutritics.com"+style)
        with open("download.jpg","wb") as file:
            file.write(img.content)



    if results_div:

        # Step 4: Get the first and second child divs of 'results' and extract 'data-name' attributes

        child_divs = results_div.find_all('div', recursive=False)


        menu_items = []
        for item in child_divs:
            menu_items.append(item.get("data-name"))
        """
        if len(child_divs) >= 2:  # Ensure there are at least two divs

            first_data_name = child_divs[0]
            with open("output.html", "w") as file:
                file.write(str(first_data_name))

            second_data_name = child_divs[1].get('data-name')



            print(f"First div data-name: {first_data_name.get('data-name')}")

            print(f"Second div data-name: {second_data_name}")

        else:

            print("Less than two div elements found inside the results div.")
            """

    else:

        print("No div with id 'results' found.")

else:

    print(f"Failed to retrieve the page. Status code: {response.status_code}")



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', items=menu_items)

if __name__ == '__main__':
    app.run()
