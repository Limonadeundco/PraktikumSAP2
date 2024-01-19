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

all_grocery_items = []


#delte all data from the database but the first two
database_commands.delete_all_data(connection, cursor, "products", "id > 0")
database_commands.delete_all_data(connection, cursor, "images", "id > 0")

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
    grocery_items = []
    grocery_item_pictures = []
    while True:
        if not grocery_items:  # if grocery_items is empty
            url = 'https://www.chefkoch.de/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.find_all(class_='ds-recipe-card__image-wrap ds-teaser-link__image-wrap'):
                grocery_item_pictures.append(item.find('img')['src'])
                grocery_items.append(item.find('img')['alt'])

        # Shuffle the items to ensure randomness
        combined = list(zip(grocery_items, grocery_item_pictures))
        random.shuffle(combined)
        grocery_items, grocery_item_pictures = zip(*combined)

        for grocery_item, grocery_item_picture in zip(grocery_items, grocery_item_pictures):
            if grocery_item not in all_grocery_items and "newsletter" not in grocery_item_picture:
                all_grocery_items.append(grocery_item)
                return grocery_item, grocery_item_picture

        # Clear the lists for the next iteration
        grocery_items = []
        grocery_item_pictures = []

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
    name, picture_link = generate_random_name()
    name = name.replace('\n', '')
    name = name.replace('/n', '')
    name = name.replace('\r', '')
    name = name.replace('/', '')
    name = name.replace('\\', '')
    name = name.replace('//', '')
    name = name.replace('-', ' ')
    name = name.replace('„', '')
    name = name.replace("“", '')
    name = name.strip()
    name = name.rstrip()

    r, g, b = generate_random_background_color()
    
    # Create a new image with a white background
    image = Image.open(BytesIO(requests.get(picture_link).content))

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Specify the font size and font file

    # Calculate the position to write the name on the image
    
    #remove all special characters from the name like ä,ü,ö,ß
    
    name = name.replace('ä', 'ae')
    name = name.replace('ü', 'ue')
    name = name.replace('ö', 'oe')
    name = name.replace('ß', 'ss')
    name = name.replace('Ä', 'Ae')
    name = name.replace('Ü', 'Ue')
    name = name.replace('Ö', 'Oe')
    name = name.replace('ß', 'Ss')
    name = name.replace('"', '')
    name = name.replace("'", '')
    name = name.replace(":", '')
    name = name.replace(";", '')
    name = name.replace("!", '')
    name = name.replace("?", '')
    name = name.replace("(", '')
    name = name.replace(")", '')
    
    
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
    
    adjectives = ["lustig", "albern", "verrueckt", "hilarisch", "laecherlich", "albern", "verrueckt", "skurril", "komisch", "absurd", 
                  "grotesk", "bizarr", "seltsam", "unheimlich", "merkwuerdig", "sonderbar", "kurios", "eigenartig", "ungewoehnlich", 
                  "absonderlich", "fremdartig", "exzentrisch", "wunderlich", "schrullig", "spassig", "ulkig", "witzig", "scherzhaft", 
                  "humorvoll", "amuesant", "unterhaltsam", "lustig", "heiter", "froehlich", "vergnuegt", "gluecklich", "zufrieden", 
                  "befriedigt", "erfreut", "begeistert", "entzueckt", "hocherfreut", "uebergluecklich"]
    nouns = ["Katze", "Hund", "Elefant", "Clown", "Banane", "Alien", "Huhn", "Roboter", "Pirat", "Ninja", 
             "Auto", "Baum", "Stuhl", "Buch", "Tisch", "Haus", "Schuh", "Schlüssel", "Lampe", "Computer", 
             "Fenster", "Tür", "Bild", "Uhr", "Telefon", "Brille", "Kugelschreiber", "Tasse", "Teller", "Löffel"]

    descriptions1 = []
    descriptions2 = []

    for _ in range(50):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        descriptions1.append(f"{adjective} {noun}.")
        
    for _ in range(50):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        descriptions2.append(f"{adjective} {noun}.")
        

    which_description1 = random.randint(0, 49)
    which_description2 = random.randint(0, 49)

    
    #save image path and name in the database
    
    print("i", i)
    
    count_category = random.randint(1, 4)
    
    if count_category == 1:
        count = random.randint(1, 10)
    elif count_category == 2:
        count = random.randint(11, 100)
    elif count_category == 3:
        count = random.randint(1, 5)
    else:
        count = random.randint(20, 200)
        
    price_category = random.randint(1, 6)
    
    if price_category == 1:
        price = random.randint(1, 100) / 100
        
    elif price_category == 2:
        price = random.randint(1, 1000000000) / 1000
        
    elif price_category == 3:
        price = random.randint(1, 100) / 10
        
    elif price_category == 4:
        random.randint(1,2  )
        if random.randint(1,2) == 1:
            price = random.randint(1, 1000000) / 100
        else:
            
            price = random.randint(1, 10) / 10
        
    elif price_category == 5:
        price = random.randint(1, 500) / 10
    
    else:
        price = random.randint(1, 10000)/100
    
    
    database_commands.insert_data(connection, cursor, "products", "id, name, price, description, count", (i+1, name, price, f"{descriptions1[which_description1]} {descriptions2[which_description2]}", count))
    database_commands.insert_data(connection, cursor, "images", "image_path, product_id, image_id", (output_directory + name + '.png', i+1,1))

database_commands.disconnect_database(connection)