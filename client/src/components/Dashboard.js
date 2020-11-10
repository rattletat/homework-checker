import React, { useEffect, useState } from "react";
import { Card, Col, Row, ListGroup } from "react-bootstrap";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import callAPI from "../services/APIServices";

export default () => {
    const breadcrumbs = [
        { name: "Hauptseite", active: false, href: "#/" },
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
            const { response, isError } = await callAPI(
                `accounts/status`,
                "GET"
            );
            if (!isError) {
                setData({ ...response.data });
            }
        };
        fetchAccountStatus();
    }, []);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <h1>Dashboard</h1>
                Hier findest du Informationen zu deinem Account und deinen
                angemeldeten Vorlesungen.
                <br />
                <br />
                <Card className="mb-3">
                    <Card.Header>Dein Account</Card.Header>
                    <Card.Body>
                        <ListGroup variant="flush">
                            <ListGroup.Item>
                                Dein Name: {data.full_name}
                            </ListGroup.Item>
                            <ListGroup.Item>
                                Email-Adresse: {data.email}
                            </ListGroup.Item>
                            <ListGroup.Item>
                                Matrikelnummer: {data.identifier}
                            </ListGroup.Item>
                        </ListGroup>
                    </Card.Body>
                </Card>
                <Card className="mb-3">
                    <Card.Header>Deine Vorlesungen</Card.Header>
                    <Card.Body>
                        {data.enrolled_lectures && (
                            <ListGroup>
                                <>
                                    {data.enrolled_lectures.map(
                                        (lecture, key) => (
                                            <ListGroup.Item key={key}>
                                                {lecture}
                                            </ListGroup.Item>
                                        )
                                    )}
                                </>
                            </ListGroup>
                        )}
                        {!data.enrolled_lectures && (
                            <p>Du bist zu keiner Vorlesung angemeldet!</p>
                        )}
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    );
};
