var products_per_row = 5;
var rows = 10;
var search_results = null;
var products_found_count;

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

async function getImportantData() {
    let product_count = await httpGetJson(
        "http://127.0.0.1:5000/get_number_of_all_products"
    );
    let get_all_products = await httpGetJson(
        "http://127.0.0.1:5000/get_all_products/" + rows * products_per_row
    );

    return { productCount: product_count[0][0], allProducts: get_all_products };
}

async function addProductToCart(product_id, product_container) {
    let inputs = document.getElementsByClassName("product-quantity");
    let quantity = inputs[product_id - 1].value;

    if (quantity < 1) {
        displayErrorMessage(
            "Ungülitge Anzahl, bitte mindestens 1 Produkt auswählen!",
            product_container
        );
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

async function generateTable(initData, tableData) {
    let table = document.getElementById("products");
    let table_body = table.getElementsByTagName("tbody")[0];

    if (initData.allProducts != null) {
        products_found_count = initData.allProducts.products.length;
    } else {
        products_found_count = 0;
    }

    let products_found = document.getElementById("product-count-thead");
    products_found.innerHTML = products_found_count + " Produkte gefunden";

    if (products_found_count == 0) {
        let no_products_found = document.createElement("p");
        no_products_found.innerHTML = "Keine Produkte gefunden";
        no_products_found.classList.add("no-products-found");
        table_body.appendChild(no_products_found);

        return;
    }

    console.log(initData.allProducts.products.length);

    for (let i = 0; i < tableData.length; i++) {
        let row = document.createElement("tr");
        for (let y = 0; y < tableData[i].length; y++) {
            let product = tableData[i][y];

            if (product == null) {
                break;
            }

            product = product.product;

            let product_container = document.createElement("td");
            product_container.classList.add("product-container");

            let product_image = document.createElement("img");
            product_image.src = "http://127.0.0.1:5000/get_image/" + product.id;
            product_image.alt = product.product_name;
            product_image.classList.add("product-image");
            product_container.appendChild(product_image);

            let product_name = document.createElement("p");
            product_name.innerHTML = product.name;
            product_name.classList.add("product-name");
            product_container.appendChild(product_name);

            let product_price = document.createElement("p");
            product_price.innerHTML = product.price + "€";
            product_price.classList.add("product-price");
            product_container.appendChild(product_price);

            let product_description = document.createElement("p");
            product_description.innerHTML = product.description;
            product_description.classList.add("product-description");
            product_container.appendChild(product_description);

            // create add to cart button
            let add_to_cart_button = document.createElement("button");
            add_to_cart_button.classList.add("add-to-cart-button");
            add_to_cart_button.textContent = "In den Warenkorb";
            add_to_cart_button.onclick = function () {
                addProductToCart(product.id, product_container);
            };
            product_container.appendChild(add_to_cart_button);

            // create quantity input
            let product_quantity = document.createElement("input");
            product_quantity.classList.add("product-quantity");
            product_quantity.type = "number";
            product_quantity.min = 1;
            product_quantity.max = initData.productCount;
            product_quantity.value = 1;
            product_quantity.addEventListener("input", function () {
                if (this.value > initData.productCount) {
                    this.value = initData.productCount;
                }
            });
            product_container.appendChild(product_quantity);

            //create status message
            let product_status = document.createElement("p");
            product_status.classList.add("status", "fade-out");
            product_status.textContent = "";
            product_container.appendChild(product_status);

            row.appendChild(product_container);
        }
        table_body.appendChild(row);
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

async function calculateTable(initData) {
    let table = [];

    if (initData.allProducts != null) {
        let products = initData.allProducts.products;
        console.log(products);

        for (let i = 0; i < rows; i++) {
            let row = [];
            for (let j = 0; j < products_per_row; j++) {
                row.push(products[i * products_per_row + j]);
            }
            table.push(row);
        }

        return table;
    } else {
        return table;
    }
}

async function deleteTable() {
    let table = document.getElementById("products");
    let table_body = table.getElementsByTagName("tbody")[0];

    while (table_body.firstChild) {
        table_body.removeChild(table_body.firstChild);
    }
}

async function searchProducts() {
    let search_input = document.getElementById("search").value;
    search_results = await httpGetJson(
        "http://127.0.0.1:5000/search/" + search_input
    );

    let product_count = await httpGetJson(
        "http://127.0.0.1:5000/get_number_of_all_products"
    );

    return { productCount: product_count[0][0], allProducts: search_results };
}

async function onSearch() {
    let search_input = document.getElementById("search").value;

    if (search_input.length < 3) {
        initData = await getImportantData();
    } else {
        initData = await searchProducts();
    }

    deleteTable();
    calculateTable(initData).then((table) => {
        generateTable(initData, table).then((table) => {});
    });
}

window.addEventListener("load", async function () {
    initData = await getImportantData();
    console.log(initData);

    calculateTable(initData).then((table) => {
        console.log(table);
        generateTable(initData, table).then((table) => {
            console.log(table);
        });
    });
});
