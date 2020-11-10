export const getUser = () => {
    const auth = JSON.parse(
        window.localStorage.getItem("homework.checker.auth")
    );
    if (auth) {
        const [, payload] = auth.access.split(".");
        const decoded = window.atob(payload);
        return JSON.parse(decoded);
    }
    return undefined;
};

export const getAccessToken = () => {
    const auth = JSON.parse(
        window.localStorage.getItem("homework.checker.auth")
    );
    if (auth) {
        return auth.access;
    }
    return undefined;
};
