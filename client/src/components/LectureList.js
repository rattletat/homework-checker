import React, { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { isActive, isUpcoming, isExpired } from "../services/TimeService";

import LectureGroup from "./LectureGroup";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import { callAPI } from "../services/APIServices";

function LectureList(props) {
    const [data, setData] = useState({ lectures: [] });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await callAPI("api/lectures/", "GET");
                setData({ lectures: response.data });
            } catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, []);

    const activeLectures = data.lectures.filter(isActive);
    const upcomingLectures = data.lectures.filter(isUpcoming);
    const expiredLectures = data.lectures.filter(isExpired);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={[
                        { name: "Home", active: false, href: "#/" },
                        { name: "Lectures", active: true }
                    ]}
                />

                {activeLectures.length !== 0 && (
                    <LectureGroup
                        title="Active Lectures"
                        lectures={activeLectures}
                    />
                )}
                {upcomingLectures.length !== 0 && (
                    <LectureGroup
                        title="Upcoming Lectures"
                        lectures={upcomingLectures}
                    />
                )}
                {expiredLectures.length !== 0 && (
                    <LectureGroup
                        title="Past Lectures"
                        lectures={expiredLectures}
                    />
                )}
            </Col>
        </Row>
    );
}

export default LectureList;
