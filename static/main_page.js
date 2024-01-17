async function httpGetJson(url) {
    return fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch((e) => {
            console.log(
                "There was a problem with your fetch operation: " + e.message
            );
        });
}

async function httpGetText(url) {
    return fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .catch((e) => {
            console.log(
                "There was a problem with your fetch operation: " + e.message
            );
        });
}

async function checkForUserCookie() {
    let user_cookie = document.cookie;
    if (user_cookie.length > 0) {
        httpGetText("http://127.0.0.1:5000/check_cookie/" + user_cookie).then(
            (response) => {
                if (response == "Cookie found") {
                    return;
                } else {
                    httpGetJson("http://127.0.0.1:5000/get_cookie").then(
                        (response) => {
                            console.log(response);
                            document.cookie = response.user_id;
                        }
                    );
                }
            }
        );
    } else {
        httpGetJson("http://127.0.0.1:5000/get_cookie").then((response) => {
            console.log(response);
            document.cookie = response.user_id;
        });
    }
}

async function addProductToCart(product_id, product_container) {
    let inputs = document.getElementsByClassName("product-quantity");
    let quantity = inputs[product_id - 1].value;

    if (quantity < 1) {
        let error_message = document.createElement("p");
        error_message.classList.add("error-message");
        error_message.textContent = "Bitte geben Sie eine gültige Anzahl ein.";

        product_container.appendChild(error_message);

        // Start fading out the error message after 3 seconds
        setTimeout(function() {
            error_message.classList.add("fade-out");
        }, 3000);

        // Remove the error message after it has faded out
        setTimeout(function() {
            if (product_container.contains(error_message)) {
                product_container.removeChild(error_message);
            }
        }, 4000);

        return;
    }

    console.log("Adding product " + product_id + " " + quantity + "x to cart");
    let user_cookie = document.cookie;
    fetch(
        "http://127.0.0.1:5000/add_product_to_basket/" +
            user_cookie +
            "/" +
            product_id +
            "/" +
            quantity,
        {
            method: "POST",
        }
    ).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    });
}

async function createRecommendedProducts() {
    let recommended_elements = 2;

    // Get the recommended products
    let recommended_products = await httpGetJson(
        "http://127.0.0.1:5000/get_recommended_products/" + recommended_elements
    );
    recommended_products = recommended_products.recommended_products;

    // Get the recommended products and put them on the main page
    for (let i = 0; i < recommended_products.length; i++) {
        let recommended_product_id = recommended_products[i].product_id;

        let product_info = await httpGetJson(
            "http://127.0.0.1:5000/get_product/" + recommended_product_id
        );
        product_info = product_info.product;

        let container = document.getElementById(
            "recommended-product-container"
        );

        // create product container
        let product_container = document.createElement("div");
        product_container.classList.add("product-container");
        container.appendChild(product_container);

        //create div in the product-container
        let recommended_product = document.createElement("div");
        recommended_product.classList.add("recommended-product");
        product_container.appendChild(recommended_product);

        // create image
        let product_image = document.createElement("img");
        product_image.classList.add("product-image");
        product_image.src = "http://127.0.0.1:5000/get_image/" + (i + 1);
        product_container.appendChild(product_image);

        // create name
        let product_name = document.createElement("h3");
        product_name.classList.add("name");
        product_name.textContent = product_info.name;
        product_container.appendChild(product_name);

        // create description
        let product_description = document.createElement("p");
        product_description.classList.add("description");
        product_description.textContent = product_info.description;
        product_container.appendChild(product_description);

        // create add to cart button
        let add_to_cart_button = document.createElement("button");
        add_to_cart_button.classList.add("add-to-cart-button");
        add_to_cart_button.textContent = "In den Warenkorb";
        add_to_cart_button.onclick = function () {
            addProductToCart(recommended_product_id, product_container);
        };
        product_container.appendChild(add_to_cart_button);

        // create quantity input
        let product_quantity = document.createElement("input");
        product_quantity.classList.add("product-quantity");
        product_quantity.type = "number";
        product_quantity.min = 1;
        product_quantity.max = product_info.count;
        product_quantity.value = 1;
        product_quantity.addEventListener("input", function () {
            if (this.value > product_info.count) {
                this.value = product_info.count;
            }
        });
        product_container.appendChild(product_quantity);
    }
}

window.addEventListener("load", async function () {
    // Check if the user has a cookie, if not, create one
    await checkForUserCookie();

    await createRecommendedProducts();
});
