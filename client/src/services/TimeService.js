import moment from "moment";
import "moment/locale/de";

export const isActive = object => {
    return (
        (!object.start || moment(object.start) < moment()) &&
        (!object.end || moment() < moment(object.end))
    );
};

export const isUpcoming = object => {
    return object.start && moment() < moment(object.start);
};

export const isExpired = object => {
    return object.end && moment(object.end) < moment();
};

export const getTimeIndicator = object => {
    if (isUpcoming(object)) {
        return "startet " + moment(object.start).fromNow();
    }
    if (isExpired(object)) {
        return "beendet " + moment(object.end).fromNow();
    }
    if (isActive(object) && object.end) {
        return "endet " + moment(object.end).fromNow();
    }
    return "";
};

export const toTimeFormat = (datetime, spec = "LL") => {
    return datetime ? moment(datetime).format(spec) : "";
};
