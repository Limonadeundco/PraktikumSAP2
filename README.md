# PraktikumSAP2

## A repository for the second project while our internship at SAP St. Ingbert

For the second week of our internship at SAP St. Ingbert we decided to create our own API and test it out building a small Webstore with it. The API is written in Python and uses the Flask framework. The Webstore is written in JavaScript and uses the React framework.

## How to use

1. Change the current IP to your IP using the switch_urls script

    - You can specify the Port in the flask_server.py and then change it with the script too

2. Execute flask_server.py to start the API and Webshop
    - You can see the endpoints in the "Endpoints" section

## Endpoints

### GET Requests

-   /get_product/<product_id>/<column> -- Return the column of the product with the given id

-   /get_product/<product_id> -- Return the whole product with the given id

-   /get_all_products/<limit> -- Return all products with the given limit, dont specify a limit to get all products

-   /get_number_of_all_products -- Integer how many products are in the database

*   /get_recommended_products/<limit> -- generate recommended products based on sales in the last 24 hours and return them with the given limit, dont specify a limit to get all recommended products

*   /get_image/<product_id>/<image_id> -- Return the image of the product, if you want to have more than one image per product, then specify the image_id

### POST Requests

### PUT Requests

-   /update_product/<product_id>/<parameters> -- Update values of a product, parameters are seperated by a "&" and the values are seperated by a "="

    -   Example: /update_product/1/name=Test&price=1.99

### DELETE Requests
