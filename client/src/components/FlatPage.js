import React, {useEffect, useState} from "react";
import {Col, Row} from "react-bootstrap";

import BreadcrumbWrapper from "./BreadcrumbWrapper";
import MarkdownRenderer from "../services/MarkdownService";

import {callAPI} from "../services/APIServices";

export default function FlatPage({name}) {
    const [data, setData] = useState({
        title: "",
        content: "",
    });

    useEffect(() => {
        const fetchFlatPage = async () => {
            const response = await callAPI(`/api/flatpages/${name}/`, "GET");
            if (response) {
                setData({...response.data});
            }
        };
        fetchFlatPage();
    }, [name]);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={[
                        {
                            name: "Home",
                            active: false,
                            href: "/"
                        },
                        {
                            name: data.title,
                            active: true
                        }
                    ]}
                />
                <h1>{data.title}</h1>
                <MarkdownRenderer>
                    {data.content}
                </MarkdownRenderer>
            </Col>
        </Row>
    );
}
