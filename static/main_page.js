window.addEventListener("load", function () {
    for (let i = 0; i < 2; i++) {
        let recommended_products = document.getElementsByClassName(
            "recommended-product-" + (i + 1)
        );
        console.log(recommended_products);

        let product_name =
            recommended_products[0].getElementsByClassName("name")[0];
        let product_description =
            recommended_products[0].getElementsByClassName("description")[0];

        console.log(product_name);
        console.log(product_description);

        httpGetJson(
            "http://127.0.0.1:5000/get_recommended/" + (i + 1) + "/name"
        ).then((response) => {
            product_name.textContent = response[0][0]; // Access the first element of the first array
            console.log(response);
        });

        httpGetJson(
            "http://127.0.0.1:5000/get_product/" + (i + 1) + "/description"
        ).then((response) => {
            product_description.textContent = response[0][0]; // Access the first element of the first array
            console.log(response);
        });
    }
});

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
