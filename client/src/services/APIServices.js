import axios from "axios";

import { getAccessToken } from "./AuthService";

const BASE_URL = process.env.REACT_APP_BASE_URL;

export default async (url, method, data = {}) => {
    const token = getAccessToken();
    const headers = { Authorization: `Bearer ${token}` };
    try {
        if (method == "GET") {
            const response = await axios.get(`${BASE_URL}/api/${url}`, {
                headers
            });
            return { response, isError: false };
        } else if (method == "POST") {
            const response = await axios.post(`${BASE_URL}/api/${url}`, data, {
                headers
            });
            return { response, isError: false };
        }
    } catch (response) {
        return { response, isError: true };
    }
};
