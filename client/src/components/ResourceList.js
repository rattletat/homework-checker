import React from "react";
import { Card, ListGroup } from "react-bootstrap";

import callAPI from "../services/APIServices";

import fileDownload from "js-file-download";

export default function ResourceList({ resources }) {
    return (
        <Card>
            <Card.Header>Lecture Resources</Card.Header>
            <ListGroup variant="flush">
                {resources.map((resource, index) => (
                    <ListGroup.Item
                        key={index}
                        action
                        onClick={() => {
                            callAPI(
                                resource.download_uri,
                                "GET",
                                {},
                                {
                                    responseType: "blob"
                                }
                            )
                                .then(res => {
                                    console.log(res);
                                    return res;
                                })
                                .then(res =>
                                    fileDownload(res.data, resource.filename)
                                );
                        }}
                    >
                        {resource.title}
                    </ListGroup.Item>
                ))}
            </ListGroup>
        </Card>
    );
}
