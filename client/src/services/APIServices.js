// import axios from "axios";

import { getJWT } from "./AuthService";

export async function callAPI(url, method, headers = {}, data = {}) {
    try {
        headers = getAPIHeaders(headers);
        if (method === "GET") {
            // const response = await axios.get(url, headers);
            const response = await fetch(url, {
                ...headers,
                method: "GET"
            });
            return {
                data: await response.json()
            };
        } else if (method === "POST") {
            // const response = await axios.post(url, data, headers);
            const response = await fetch(url, {
                ...headers,
                method: "POST",
                body: JSON.stringify(data)
            });
            return {
                data: await response.json()
            };
        }
    } catch (error) {
        console.log(error)
        return error.response;
    }
}

export function getAPIHeaders(headers) {
    // if (refresh) {
    //     refreshJWT();
    // }
    const auth = getJWT();
    headers["headers"] = headers["headers"] ?? {};
    headers["headers"]["Authorization"] = `Bearer ${auth.access}`;
    return headers;
}
