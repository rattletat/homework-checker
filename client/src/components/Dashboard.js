import React, { useEffect, useState } from "react";
import { Card, Col, Row, ListGroup } from "react-bootstrap";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import callAPI from "../services/APIServices";

export default () => {
    const breadcrumbs = [
        { name: "Home", active: false, href: "#/" },
        { name: "Dashboard", active: true }
    ];
    const [data, setData] = useState({
        email: "",
        full_name: "",
        identifier: "",
        enrolled_lectures: []
    });

    useEffect(() => {
        const fetchAccountStatus = async () => {
            const response = await callAPI(`accounts/status`, "GET");
            setData({ ...response.data });
        };
        fetchAccountStatus();
    }, []);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <h1>Dashboard</h1>
                Here you find information regarding your account status and
                lectures you signed up for.
                <br />
                <br />
                <Card className="mb-3">
                    <Card.Header>Your account</Card.Header>
                    <Card.Body>
                        <ListGroup variant="flush">
                            <ListGroup.Item>
                                Name: {data.full_name}
                            </ListGroup.Item>
                            <ListGroup.Item>Email: {data.email}</ListGroup.Item>
                            <ListGroup.Item>
                                Student ID:{" "}
                                {data.identifier
                                    ? data.identifier
                                    : "Not specified"}
                            </ListGroup.Item>
                        </ListGroup>
                    </Card.Body>
                </Card>
                <Card className="mb-3">
                    <Card.Header>Your Lectures</Card.Header>
                    <Card.Body>
                        <ListGroup>
                            <>
                                {data.enrolled_lectures.map((lecture, key) => (
                                    <ListGroup.Item key={key}>
                                        {lecture}
                                    </ListGroup.Item>
                                ))}
                            </>
                        </ListGroup>
                        {!data.enrolled_lectures.length &&
                            "You're not signed up for any lecture!"}
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    );
};
