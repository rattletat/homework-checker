import axios from "axios";

import { getAuth } from "./AuthService";

export default async function callAPI(url, method, data = {}) {
    const token = getAuth().access;
    data["headers"] = data["headers"] ? data["headers"] : {};
    data["headers"]["Authorization"] = `Bearer ${token}`;
    try {
        if (method === "GET") {
            const response = await axios.get(url, data);
            return response;
        } else if (method === "POST") {
            const response = await axios.post(url, data);
            return response;
        }
    } catch (response) {
        console.log(response);
    }
}
