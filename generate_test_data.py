import database_commands.database_commands as database_commands
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from bs4 import BeautifulSoup
import shutil

database_commands = database_commands.DataBase()

connection, cursor = database_commands.connect_database("database.db")


#delte all data from the database but the first two
database_commands.delete_all_data(connection, cursor, "products", "id > 2")
database_commands.delete_all_data(connection, cursor, "images", "id > 2")

# Delete "images2" directory if it exists
if os.path.exists("images2"):
    shutil.rmtree("images2")

# Function to generate a random color
def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    if r < 100 and g < 100 or r < 100 and b < 100 or g < 100 and b < 100:
        r = r + 100
        g = g + 100
        b = b + 100
    
    return (r, g, b)

def generate_random_background_color():
    i = random.randint(0, 2)
    
    if i == 0:
        r = random.randint(0, 255)
        g = 0
        b = 0
    elif i == 1:
        r = 0
        g = random.randint(0, 255)
        b = 0
    else:
        r = 0
        g = 0
        b = random.randint(0, 255)
        
    if r < 100 and g < 100 or r < 100 and b < 100 or g < 100 and b < 100:
        r = r + 100
        g = g + 100
        b = b + 100
    

    
    return (r, g, b)


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
num_pictures = 80

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
    name = name.replace('\r', '')
    name = name.replace('/', '')
    name = name.replace('\\', '')
    name = name.replace('//', '')
    name = name.replace('-', ' ')
    name = name.strip()
    name = name.rstrip()

    r, g, b = generate_random_background_color()
    
    # Create a new image with a white background
    image = Image.new('RGB', (500, 500), color=(r, g, b))

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Specify the font size and font file

    # Calculate the position to write the name on the image
    
    #remove all special characters from the name like ä,ü,ö,ß
    
    name = name.replace('ä', 'ae')
    name = name.replace('ü', 'ue')
    name = name.replace('ö', 'oe')
    name = name.replace('ß', 'ss')
    
    
    try:
        bbox = draw.textbbox((0, 0), name)
        
    except UnicodeEncodeError:
        print("UnicodeEncodeError", name)
        continue

    text_width, text_height = draw.textsize(name, font=font)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Write the name on the image
    draw.text((x, y), name, fill=color, font=font)

    # Save the image
    image.save(output_directory + name + '.png')
    
    #generate 50 funny descriptions for the products
    
    adjectives = ["lustig", " albern", "verrueckt", "hilarisch", "laecherlich", "albern", "verrueckt", "skurril", "komisch", "absurd"]
    nouns = ["Katze", "Hund", "Elefant", "Clown", "Banane", "Alien", "Huhn", "Roboter", "Pirat", "Ninja"]

    descriptions = []

    for _ in range(50):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        descriptions.append(f"{adjective} {noun}")

    which_description = random.randint(0, 49)

    
    #save image path and name in the database
    
    print("i", i)
    
    database_commands.insert_data(connection, cursor, "products", "id, name, price, description", (i+3, name, random.randint(1, 10000)/100, descriptions[which_description]))
    database_commands.insert_data(connection, cursor, "images", "image_path, product_id, image_id", (output_directory + name + '.png', i+3,1))

database_commands.disconnect_database(connection)