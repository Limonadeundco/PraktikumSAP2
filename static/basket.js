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

async function getInfosForProductID(product_id) {
    let response = await httpGetJson(
        "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/get_product/" + product_id
    );
    let product_infos = response.product;

    return product_infos;
}

async function getProductsForBasketId(basket_id) {
    let response = await httpGetJson(
        "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/get_basket_for_user/" + basket_id
    );
    let basket_products = response.basket;

    return basket_products;
}

window.addEventListener("load", async function () {
    await checkForUserCookie();

    let basket_id = document.cookie.split("user_id=")[1];
    basket_id = basket_id.split(";")[0];
    let basket_products = await getProductsForBasketId(basket_id);

    console.log(basket_products);

    var total_price = 0;

    let basket_table = document.getElementById("basket-table");
    basket_table = basket_table.getElementsByTagName("tbody")[0];
    for (let i = 0; i < basket_products.length; i++) {
        let product = basket_products[i].product;
        console.log(product);

        let product_infos = await getInfosForProductID(product.product_id);
        product_infos = product_infos;

        let row = basket_table.insertRow(-1);
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        let cell3 = row.insertCell(2);
        let cell4 = row.insertCell(3);

        cell1.innerHTML = product_infos.name;
        cell2.innerHTML = product_infos.price + "€";
        cell3.innerHTML = product.count;
        cell4.innerHTML =
            (parseFloat(product_infos.price) * product.count).toFixed(2) + "€";

        total_price += product_infos.price * product.count;

        console.log(product.product_id);
        console.log(product.count);
    }

    let total_price_element = document.getElementById("total-price");
    total_price_element.innerHTML =
        "Zu zahlen: " + total_price.toFixed(2) + "€";
});

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
    if (document.cookie != null) {
        let user_cookie = document.cookie.split("user_id=")[1];
        user_cookie = user_cookie.split(";")[0];

        if (user_cookie.length > 0) {
            httpGetText(
                "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/check_cookie/" + user_cookie
            ).then((response) => {
                if (response == "Cookie found") {
                    return;
                } else {
                    httpGetJson("https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/get_cookie").then(
                        (response) => {
                            console.log(response);
                            setCookie("user_id", response.user_id, 7); // Set/replace the 'user_id' cookie
                        }
                    );
                }
            });
        } else {
            httpGetJson("https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/get_cookie").then(
                (response) => {
                    console.log(response);
                    setCookie("user_id", response.user_id, 7); // Set/replace the 'user_id' cookie
                    console.log("doc cookier" + document.cookie);
                }
            );
        }
    } else {
        httpGetJson("https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/get_cookie").then(
            (response) => {
                console.log(response);
                setCookie("user_id", response.user_id, 7); // Set/replace the 'user_id' cookie
                console.log("doc cookier" + document.cookie);
            }
        );
    }
}
