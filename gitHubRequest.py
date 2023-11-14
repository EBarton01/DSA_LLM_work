import requests
from bs4 import BeautifulSoup
import openai
import os

from dotenv import load_dotenv, find_dotenv

url = '#'
response = requests.get(url)

data = ""

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract tags and concatenate their content into the 'data' variable
    for tag in ['p', 'h1', 'h2', 'h3', 'table', 'tr']:
        elements = soup.find_all(tag)
        for element in elements:
            data += element.text + '\n'

    # Print or manipulate the concatenated content as needed
    a = input("Do you want to print the data(y/n): ")
    if a == "y":
        print(data)
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)


_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = '#'


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

run  = True
while run:
    user_prompt = input("\nEnter a question based on the webpage(n to stop): ")
    if user_prompt == "n":
        run = False
    else:
        prompt = f"""

        {user_prompt}
        
        Review: ```{data}```
        """

        response = get_completion(prompt)
        print(response)