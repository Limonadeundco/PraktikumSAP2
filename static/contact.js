window.addEventListener("load", function () {
    checkForUserCookie();
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
