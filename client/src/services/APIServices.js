import axios from "axios";

import { getAuthHeaders } from "./AuthService";

export default async function callAPI(url, method, headers = {}, payload = {}) {
    try {
        if (method === "GET") {
            const response = await axios.get(url, getAuthHeaders(headers));
            return response;
        } else if (method === "POST") {
            const response = await axios.post(
                url,
                payload,
                getAuthHeaders(headers)
            );
            return response;
        }
    } catch (response) {
        console.log(response);
    }
}
