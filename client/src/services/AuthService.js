import axios from "axios";

const JWT_STORAGE = "homework.checker.auth";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.interceptors.response.use(
    response => {
        return response;
    },
    async err => {
        const originalReq = err.config;
        if (
            err.response.status === 401 &&
            err.config &&
            !err.config.__isRetryRequest &&
            hasJWT()
        ) {
            originalReq.__isRetryRequest = true;

            const access = await refreshJWT();
            originalReq.headers["Authorization"] = `Bearer ${access}`;
            originalReq.headers["Device"] = "device";
            return axios(originalReq);
        } else {
            const code = err.response.status;
            if (code !== 404 && code !== 409 && !["/login", "/signup"].includes(window.location.pathname)) {
                logOut();
            }
            throw err;
        }
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
    const response = await fetch("/api/token/refresh", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            Device: "device",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify({refresh: auth.refresh, access: auth.access})
    });
    const access = await response.json().then(auth => auth.access);
    setJWT({access, refresh: auth.refresh});
    return access;
};


export const logIn = async (email, password, setLoggedIn) => {
    const url = "/api/accounts/login";
    try {
        let response = await axios.post(url, {email, password});
        setJWT(response.data);
        setLoggedIn(true);
        return {response, isError: false};
    } catch (error) {
        return {response: error, isError: true};
    }
};

export const logOut = () => {
    removeJWT();
    window.location.reload();
};

export const isLoggedIn = () => {
    return hasJWT();
};
