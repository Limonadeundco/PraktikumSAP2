window.addEventListener("load", function () {
    checkForUserCookie();
    var payButton = document.getElementById("pay");
    payButton.addEventListener("click", onPayButton);
});

async function onPayButton() {
    window.location.href = "/";

    user_id = document.cookie.split("user_id=")[1];
    user_id = user_id.split(";")[0];
    let response = await fetch(
        "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/payment/" + user_id,
        {
            method: "POST",
        }
    ).then((response) => {
        if (!response.ok) {
            console.log(`HTTP error! message: ${response.json()}`);
        }
    });

    let status_element = document.getElementById("status");
    status_element.innerHTML = response.status;
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
