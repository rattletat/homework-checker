import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.interceptors.response.use(
    response => {
        return response;
    },
    err => {
        return new Promise((resolve, reject) => {
            const originalReq = err.config;
            if (
                err.response.status === 401 &&
                err.config &&
                !err.config.__isRetryRequest
            ) {
                originalReq.__isRetryRequest = true;

                let res = fetch("api/token/refresh", {
                    method: "POST",
                    mode: "cors",
                    cache: "no-cache",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        Device: "device",
                        Token: getAuth().access
                    },
                    redirect: "follow",
                    referrer: "no-referrer",
                    body: JSON.stringify({
                        token: getAuth().access,
                        refresh: getAuth().refresh
                    })
                })
                    .then(res => res.json())
                    .then(res => {
                        window.localStorage.setItem(
                            "homework.checker.auth",
                            JSON.stringify({
                                access: res.access,
                                refresh: getAuth().refresh
                            })
                        );
                        originalReq.headers[
                            "Authorization"
                        ] = `Bearer ${res.access}`;
                        originalReq.headers["Device"] = "device";

                        return axios(originalReq);
                    });

                resolve(res);
            } else return Promise.reject(err);
        });
    }
);

export const logIn = async (email, password, setLoggedIn) => {
    const url = "/api/accounts/login";
    try {
        const response = await axios.post(url, { email, password });
        window.localStorage.setItem(
            "homework.checker.auth",
            JSON.stringify(response.data)
        );
        setLoggedIn(true);
        return { response, isError: false };
    } catch (error) {
        console.log(error);
        return { response: error, isError: true };
    }
};

export const logOut = () => {
    window.localStorage.removeItem("homework.checker.auth");
    window.location.href = "/";
};

export const isLoggedIn = () => {
    return window.localStorage.getItem("homework.checker.auth") !== null;
};

// export const getUser = () => {
//     const auth = JSON.parse(
//         window.localStorage.getItem("homework.checker.auth")
//     );
//     if (auth) {
//         const [, payload] = auth.access.split(".");
//         const decoded = window.atob(payload);
//         return JSON.parse(decoded);
//     }
//     return undefined;
// };

export const getAuth = () => {
    return JSON.parse(window.localStorage.getItem("homework.checker.auth"));
};

export const getAuthHeaders = (headers = {}) => {
    const token = getAuth().access;
    headers["headers"] = headers["headers"] ? headers["headers"] : {};
    headers["headers"]["Authorization"] = `Bearer ${token}`;
    return headers;
};
