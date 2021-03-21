import React from "react";
import history from "../history";

import { Breadcrumb, BreadcrumbItem } from "react-bootstrap";

export default function BreadcrumbWrapper(props = {}) {
    const items = props.items.map((item, key) =>
        item.active ? (
            <BreadcrumbItem key={key} active>
                {item.name}
            </BreadcrumbItem>
        ) : (
            <BreadcrumbItem
                key={key}
                onClick={() => history.push(item.href)}
            >
                {item.name}
            </BreadcrumbItem>
        )
    );
    return <Breadcrumb>{items}</Breadcrumb>;
}
