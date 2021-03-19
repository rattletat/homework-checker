import React, {useEffect, useState} from "react";
import {Col, Row, ListGroup} from "react-bootstrap";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import {callAPI} from "../services/APIServices";
import LectureEntry from "./LectureEntry";
import LectureRegister from "./LectureRegister";

export default function Lectures() {
    const breadcrumbs = [
        {name: "Home", active: false, href: "/"},
        {name: "Lectures", active: true}
    ];
    const [updated, setUpdated] = useState(true);
    const [data, setData] = useState({
        email: "",
        full_name: "",
        identifier: "",
        enrolled_lectures: []
    });

    useEffect(() => {
        const fetchAccountStatus = async () => {
            const response = await callAPI(`/api/lectures/`, "GET");
            if (response) {
                setData({...response.data});
            }
        };
        fetchAccountStatus();
        setUpdated(true);
    }, [updated]);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <h1>Lectures</h1>
                Here you find information about lectures you are enrolled in.
                <br />
                <br />
                <LectureRegister refreshPage={() => setUpdated(false)} />
                <br />
                <h3>Your Lectures</h3>
                <ListGroup>
                    <>
                        {data.enrolled_lectures.map((lecture, key) => (
                            <LectureEntry lecture={lecture} key={key} />
                        ))}
                    </>
                </ListGroup>
            </Col>
        </Row>
    );
}
