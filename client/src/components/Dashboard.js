import React, { useEffect, useState } from "react";
import { Card, Col, Row, ListGroup } from "react-bootstrap";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import { callAPI } from "../services/APIServices";
import LectureDashboard from "./LectureDashboard";

export default function Dashboard() {
    const breadcrumbs = [
        { name: "Home", active: false, href: "/" },
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
            const response = await callAPI(`/api/accounts/dashboard`, "GET");
            if (response) {
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
                Here you find information about lectures you are enrolled in. 
                <br />
                <br />
                <ListGroup>
                            <>
                                {data.enrolled_lectures.map((lecture, key) => (
                                    <LectureDashboard lecture={lecture} key={key} />
                                ))}
                            </>
                </ListGroup>
                {!data.enrolled_lectures.length &&
                    "You're not signed up for any lectures!"}
            </Col>
        </Row>
    );
}
