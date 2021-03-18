import axios from "axios";

import { getJWT } from "./AuthService";

export async function callAPI(url, method, headers = {}, data = {}) {
    try {
        headers = getAPIHeaders(headers);
        if (method === "GET") {
            const response = await axios.get(url, headers);
            return response;
        } else if (method === "POST") {
            const response = await axios.post(url, data, headers);
            return response;
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
