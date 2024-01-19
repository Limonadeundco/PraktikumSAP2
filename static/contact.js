window.addEventListener("load", function () {
    checkForUserCookie();
});

async function checkForUserCookie() {
    let user_cookie = document.cookie;
    if (user_cookie.length > 0) {
        httpGetText("http://10.183.210.108:5000/check_cookie/" + user_cookie).then(
            (response) => {
                if (response == "Cookie found") {
                    return;
                } else {
                    httpGetJson("http://10.183.210.108:5000/get_cookie").then(
                        (response) => {
                            console.log(response);
                            document.cookie = response.user_id;
                        }
                    );
                }
            }
        );
    } else {
        httpGetJson("http://10.183.210.108:5000/get_cookie").then((response) => {
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
