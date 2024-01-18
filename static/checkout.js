window.addEventListener("load", function () {
    checkForUserCookie();
    var payButton = document.getElementById("pay");
    payButton.addEventListener("click", onPayButton);
});

async function onPayButton() {
    user_id = document.cookie;
    let response = await fetch("http://127.0.0.1:5000/payment/" + user_id, {
        method: "POST",
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! message: ${response.json()}`);
        }
        return response.json();
    });

    let status_element = document.getElementById("status");
    status_element.innerHTML = response.status;
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
