import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

# Function to generate a random color
def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

import requests
from bs4 import BeautifulSoup
import random

def generate_random_name():
    url = 'https://www.chefkoch.de/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with the class 'item-name' and extract their text
    grocery_items = [item.text for item in soup.find_all(class_='ds-recipe-card__headline ds-teaser-link__headline ds-trunc ds-trunc-3 ds-text-sans ds-h4')]

    # Remove duplicates by converting the list to a set and back to a list
    grocery_items = list(set(grocery_items))

    return random.choice(grocery_items)

# Specify the number of pictures to generate
num_pictures = 5

# Specify the output directory where the pictures will be saved
output_directory = 'images2/'

# Specify the font file path
print(os.getcwd())

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

font_size = 30
font = ImageFont.truetype("arial.ttf", font_size)

# Loop to generate the pictures
for i in range(num_pictures):
    # Generate a random color
    color = generate_random_color()

    # Generate a random grocery item name
    name = generate_random_name()
    name = name.replace('\n', '')
    name = name.replace('/n', '')
    name = name.strip()
    name = name.rstrip()

    # Create a new image with a white background
    image = Image.new('RGB', (500, 500), color=(255, 255, 255))

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Specify the font size and font file

    # Calculate the position to write the name on the image
    bbox = draw.textbbox((0, 0), name)

    text_width, text_height = draw.textsize(name, font=font)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Write the name on the image
    draw.text((x, y), name, fill=color, font=font)

    # Save the image
    image.save(output_directory + name + '.png')
