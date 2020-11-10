import React from "react";

import { Breadcrumb, BreadcrumbItem } from "react-bootstrap";

export default (props = {}) => {
    const items = props.items.map(item =>
        item.active ? (
            <BreadcrumbItem key={item.name} active>
                {item.name}
            </BreadcrumbItem>
        ) : (
            <BreadcrumbItem key={item.name} href={item.href}>
                {item.name}
            </BreadcrumbItem>
        )
    );
    return <Breadcrumb>{items}</Breadcrumb>;
};
