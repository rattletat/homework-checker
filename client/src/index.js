import React from "react";
import ReactDOM from "react-dom";
import "bootswatch/dist/litera/bootstrap.css";
import axios from "axios";
import { HashRouter } from "react-router-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";

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

                let res = fetch("/api/token/refresh", {
                    method: "POST",
                    mode: "cors",
                    cache: "no-cache",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        Device: "device",
                        Token: localStorage.getItem("token")
                    },
                    redirect: "follow",
                    referrer: "no-referrer",
                    body: JSON.stringify({
                        token: localStorage.getItem("token"),
                        refresh_token: localStorage.getItem("refresh_token")
                    })
                })
                    .then(res => res.json())
                    .then(res => {
                        console.log(res);
                        this.setSession({
                            token: res.token,
                            refresh_token: res.refresh
                        });
                        originalReq.headers["Token"] = res.token;
                        originalReq.headers["Device"] = "device";

                        return axios(originalReq);
                    });

                resolve(res);
            }

            return Promise.reject(err);
        });
    }
);

ReactDOM.render(
    <HashRouter>
        <App />
    </HashRouter>,
    document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
