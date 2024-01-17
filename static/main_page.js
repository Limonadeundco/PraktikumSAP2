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

async function addProductToCart(product_id) {
    let inputs = document.getElementsByClassName("product-quantity");
    let quantity = inputs[product_id - 1].value;

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

window.addEventListener("load", async function () {
    let recommended_elements = 2;
    let recommended_products = await httpGetJson(
        "http://127.0.0.1:5000/get_recommended_products/" + recommended_elements
    );

    // Check if the user has a cookie, if not, create one
    checkForUserCookie();

    // Get the recommended products and put them on the main page
    for (let i = 0; i < recommended_products.length; i++) {
        let recommended_products = document.createElement("div");
        recommended_products.classList.add("recommended-product");

        let product_image = document.createElement("img");
        product_image.classList.add("product-image");
        product_image.src = "http://127.0.0.1:5000/get_image/" + (i + 1);

        let product_name = document.createElement("h3");
        product_name.classList.add("name");

        let product_description = document.createElement("p");
        product_description.classList.add("description");

        let recommended_product_id = recommended_products[i].product_id;
        httpGetJson(
            "http://127.0.0.1:5000/get_product/" +
                recommended_product_id +
                "/name"
        ).then((response) => {
            product_name.textContent = response[0][0]; // Access the first element of the first array
        });

        httpGetJson(
            "http://127.0.0.1:5000/get_product/" +
                recommended_product_id +
                "/description"
        ).then((response) => {
            product_description.textContent = response[0][0]; // Access the first element of the first array
        });
    }
});

let add_to_cart_buttons = document.getElementsByClassName("add-product");
console.log(add_to_cart_buttons);

for (let i = 0; i < add_to_cart_buttons.length; i++) {
    add_to_cart_buttons[i].addEventListener("click", function () {
        addProductToCart(i + 1);
    });
}
