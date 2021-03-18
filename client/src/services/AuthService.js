import axios from "axios";

const JWT_STORAGE = "homework.checker.auth";

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
                !err.config.__isRetryRequest &&
                hasJWT()
            ) {
                originalReq.__isRetryRequest = true;

                let res = refreshJWT().then(res => {
                    originalReq.headers[
                        "Authorization"
                    ] = `Bearer ${res.access}`;
                    originalReq.headers["Device"] = "device";

                    return axios(originalReq);
                });
                resolve(res);
            } else {
                if (err.response.status !== 404 && !["/login", "/signup"].includes(window.location.pathname)) {
                    logOut();
                }
                return reject(err);
            }
        });
    }
);

export const setJWT = data => {
    return window.localStorage.setItem(JWT_STORAGE, JSON.stringify(data));
};

export const getJWT = () => {
    const auth = window.localStorage.getItem(JWT_STORAGE);
    return JSON.parse(auth);
};

export const removeJWT = async () => {
    window.localStorage.removeItem(JWT_STORAGE);
};

export const hasJWT = () => {
    return window.localStorage.getItem(JWT_STORAGE) !== null;
};

export const refreshJWT = async () => {
    const auth = getJWT();
    return await fetch("/api/token/refresh", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            Device: "device",
            Token: auth.token
        },
        redirect: "follow",
        referrer: "no-referrer",
        body: JSON.stringify({ refresh: auth.refresh, access: auth.access })
    })
        .then(res => res.json())
        .then(res => {
            setJWT({ access: res.access, refresh: auth.refresh });
            return res;
        });
};

export const logIn = async (email, password, setLoggedIn) => {
    const url = "/api/accounts/login";
    try {
        let response = await axios.post(url, { email, password });
        setJWT(response.data);
        setLoggedIn(true);
        return { response, isError: false };
    } catch (error) {
        return { response: error, isError: true };
    }
};

export const logOut = () => {
    removeJWT();
    window.location.reload();
};

export const isLoggedIn = () => {
    return hasJWT();
};
