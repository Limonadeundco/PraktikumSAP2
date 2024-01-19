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
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

async function checkForUserCookie() {
    let user_cookie = document.cookie.split("=")[1];
    if (user_cookie.length > 0) {
        httpGetText(
            "http://10.183.210.108:5000/check_cookie/" + user_cookie
        ).then((response) => {
            if (response == "Cookie found") {
                return;
            } else {
                httpGetJson("http://10.183.210.108:5000/get_cookie").then(
                    (response) => {
                        console.log(response);
                        setCookie("user_id", response.user_id, 7); // Set/replace the 'user_id' cookie
                    }
                );
            }
        });
    } else {
        httpGetJson("http://10.183.210.108:5000/get_cookie").then(
            (response) => {
                console.log(response);
                setCookie("user_id", response.user_id, 7); // Set/replace the 'user_id' cookie
                console.log("doc cookier" + document.cookie);
            }
        );
    }
}

async function addProductToCart(product_id, product_container) {
    let inputs = document.getElementsByClassName("product-quantity");
    //console.log(inputs);
    let quantity = inputs[product_id - 1].value;

    if (quantity < 1) {
        displayErrorMessage(
            "Ungülitge Anzahl, bitte mindestens 1 Produkt auswählen!",
            product_container
        );
        return;
    }

    console.log("Adding product " + product_id + " " + quantity + "x to cart");
    let user_cookie = document.cookie.split("=")[1];
    fetch(
        "http://10.183.210.108:5000/add_product_to_basket/" +
            user_cookie +
            "/" +
            product_id +
            "/" +
            quantity,
        {
            method: "POST",
        }
    ).then((response) => {
        if (response.status == 299) {
            displayErrorMessage(
                "Nicht genügend Produkte auf Lager!",
                product_container
            );
        } else if (response.status == 200) {
            displayErrorMessage(
                "Produkt erfolgreich in den Warenkorb gelegt!",
                product_container
            );
        }
        return;
    });
}

async function createRecommendedProducts() {
    let recommended_elements = 6;

    // Get the recommended products
    let recommended_products = await httpGetJson(
        "http://10.183.210.108:5000/get_recommended_products/" +
            recommended_elements
    );
    recommended_products = recommended_products.recommended_products;

    // Get the recommended products and put them on the main page
    for (let i = 0; i < recommended_products.length; i++) {
        let recommended_product_id = recommended_products[i].product_id;

        let product_info = await httpGetJson(
            "http://10.183.210.108:5000/get_product/" + recommended_product_id
        );
        product_info = product_info.product;

        let container = document.getElementById(
            "recommended-product-container"
        );

        // create product container
        let product_container = document.createElement("ul");
        product_container.classList.add("product-container");
        container.appendChild(product_container);

        //create div in the product-container
        let recommended_product = document.createElement("li");
        recommended_product.classList.add("recommended-product");
        product_container.appendChild(recommended_product);

        // create image
        let product_image = document.createElement("img");
        product_image.classList.add("product-image");
        product_image.src = "http://10.183.210.108:5000/get_image/" + (i + 1);
        recommended_product.appendChild(product_image);

        // create name
        let product_name = document.createElement("h3");
        product_name.classList.add("name");
        product_name.textContent = product_info.name;
        recommended_product.appendChild(product_name);

        // create description
        let product_description = document.createElement("p");
        product_description.classList.add("description");
        product_description.textContent = product_info.description;
        recommended_product.appendChild(product_description);

        // create add to cart button
        let add_to_cart_button = document.createElement("button");
        add_to_cart_button.classList.add("add-to-cart-button");
        add_to_cart_button.textContent = "In den Warenkorb";
        add_to_cart_button.onclick = function () {
            addProductToCart(recommended_product_id, recommended_product);
        };
        recommended_product.appendChild(add_to_cart_button);

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
        recommended_product.appendChild(product_quantity);

        //create status message
        let product_status = document.createElement("p");
        product_status.classList.add("status", "fade-out");
        product_status.textContent = "";
        recommended_product.appendChild(product_status);
    }
}

function displayErrorMessage(message, product_container) {
    let error_message = product_container.getElementsByClassName("status")[0];
    error_message.textContent = message;
    error_message.classList.add("error-message");
    error_message.classList.remove("fade-out");

    // Start fading out the error message after 3 seconds
    setTimeout(function () {
        error_message.classList.add("fade-out");
    }, 3000);
}

function displaySuccessMessage(message, product_container) {
    let success_message =
        product_container.getElementsByClassName("success-message")[0];
    success_message.textContent = message;
    success_message.classList.add("success-message");
    success_message.classList.remove("fade-out");

    // Start fading out the success message after 3 seconds
    setTimeout(function () {
        success_message.classList.add("fade-out");
    }, 3000);
}

window.addEventListener("load", async function () {
    // Check if the user has a cookie, if not, create one
    await checkForUserCookie();

    await createRecommendedProducts();
});
