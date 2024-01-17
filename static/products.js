var products_per_row = 5;
var rows = 10;

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

async function getImportantData() {
    let product_count = await httpGetJson(
        "http://127.0.0.1:5000/get_number_of_all_products"
    );
    let get_all_products = await httpGetJson(
        "http://127.0.0.1:5000/get_all_products/" + rows * products_per_row
    );

    return [product_count, get_all_products];
}

async function generateTable(data) {
    let product_count = await httpGetJson(
        "http://127.0.0.1:5000/get_product_count"
    );
    if (product_count > rows * products_per_row) {
        product_count = rows * products_per_row;
    }

    let table = document.createElement("table");
    table.classList.add("table");
    table.classList.add("table-striped");
    table.classList.add("table-hover");

    let thead = document.createElement("thead");
    let tr = document.createElement("tr");
    let th = document.createElement("th");
    th.setAttribute("scope", "col");
    th.innerText = "Products found";
    tr.appendChild(th);

    thead.appendChild(tr);
    table.appendChild(thead);

    let tbody = document.createElement("tbody");
    for (let i = 0; i < data.length; i++) {
        let row = data[i];
        tr = document.createElement("tr");
        let td = document.createElement("td");
        td.innerText = row[0];
        tr.appendChild(td);

        td = document.createElement("td");
        td.innerText = row[1];
        tr.appendChild(td);

        td = document.createElement("td");
        td.innerText = row[2];
        tr.appendChild(td);

        td = document.createElement("td");
        td.innerText = row[3];
        tr.appendChild(td);

        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    return table;
}

async function calculateTable() {
    let table = [];

    let result = await httpGetJson(
        "http://127.0.0.1:5000/get_all_products/" + rows * products_per_row
    );
    result = result.products;

    for (let i = 0; i < rows; i++) {
        let row = [];
        for (let j = 0; j < products_per_row; j++) {
            row.push(result[i * products_per_row + j]);
        }
        table.push(row);
    }

    return table;
}

window.addEventListener("load", function () {
    let importantData = getImportantData();
    console.log(importantData);

    calculateTable().then((table) => {
        console.log(table);
    });
});
