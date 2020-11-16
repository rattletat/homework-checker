import axios from "axios";

import { getJWT } from "./AuthService";

export async function callAPI(url, method, headers = {}, payload = {}) {
    try {
        if (method === "GET") {
            headers = await getAPIHeaders(headers);
            const response = await axios.get(url, headers);
            return response;
        } else if (method === "POST") {
            const response = await axios.post(url, payload, headers);
            return response;
        }
    } catch (response) {
        console.log(response);
    }
}

export async function getAPIHeaders(headers) {
    // if (refresh) {
    //     refreshJWT();
    // }
    const auth = await getJWT();
    headers["headers"] = headers["headers"] ? headers["headers"] : {};
    headers["headers"]["Authorization"] = `Bearer ${auth.access}`;
    return headers;
}
