var image = null;

async function httpGetJson(url, method = "GET") {
    return fetch(url, { method: method })
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

async function addProduct() {
    let product_name = document.getElementById("product_name").value;
    let product_price = document.getElementById("product_price").value;
    let product_id = document.getElementById("product_id").value;
    let product_description = document.getElementById(
        "product_description"
    ).value;
    let product_count = document.getElementById("product_count").value;

    let response = await httpGetJson(
        "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/add_product/name=" +
            product_name +
            "&price=" +
            product_price +
            "&description=" +
            product_description +
            "&count=" +
            product_count +
            "&id=" +
            product_id,
        "POST"
    );

    sendImageToServer(image);
}

window.addEventListener("load", async function () {
    let add_product_button = document.getElementById("addProduct");
    add_product_button.addEventListener("click", addProduct);
});

function dropHandler(event) {
    console.log("File(s) dropped");
    // Prevent default behavior (Prevent file from being opened)
    event.preventDefault();

    if (event.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (var i = 0; i < event.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (event.dataTransfer.items[i].kind === "file") {
                var file = event.dataTransfer.items[i].getAsFile();
                console.log("... file[" + i + "].name = " + file.name);
            }
        }
    } else {
        // Use DataTransfer interface to access the file(s)
        for (var i = 0; i < event.dataTransfer.files.length; i++) {
            console.log(
                "... file[" + i + "].name = " + event.dataTransfer.files[i].name
            );
        }
    }
    console.log(file);
    image = file;
}

function dragOverHandler(event) {
    // Prevent default behavior (Prevent file from being opened)
    event.preventDefault();
}

function sendImageToServer(image) {
    console.log("image", image);
    let product_id = document.getElementById("product_id").value;
    let image_id = document.getElementById("image_id").value;
    var formData = new FormData();
    formData.append("image", image, image.name);
    fetch(
        "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/add_image/product/" +
            product_id +
            "/" +
            image_id,
        {
            method: "POST",
            body: formData,
        }
    )
        .then((response) => response.json())
        .then((result) => {
            console.log("Success:", result);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
