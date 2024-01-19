import requests

# Specify the URL of the Flask server endpoint
url = "http://10.183.210.108:5000/add_image/product/17/1"

# Open the image file in binary mode
with open(r"C:\Users\Admin\OneDrive\Dokumente\GitHub\PraktikumSAP2\images2\test.png", "rb") as image_file:
    # Create a dictionary with the file data
    files = {"image": image_file}

    # Send a POST request to the Flask server with the image file
    response = requests.post(url, files=files)

# Check the response status code
if response.status_code == 200:
    print("Image sent successfully!")
else:
    print("Failed to send image.")
