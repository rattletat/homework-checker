import React from "react";
import history from "../history";

import { Breadcrumb, BreadcrumbItem } from "react-bootstrap";

export default function BreadcrumbWrapper(props = {}) {
    const items = props.items.map(item =>
        item.active ? (
            <BreadcrumbItem key={item.name} active>
                {item.name}
            </BreadcrumbItem>
        ) : (
            <BreadcrumbItem
                key={item.name}
                onClick={() => history.push(item.href)}
            >
                {item.name}
            </BreadcrumbItem>
        )
    );
    return <Breadcrumb>{items}</Breadcrumb>;
}
