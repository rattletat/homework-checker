import React, { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { isActive, isUpcoming, isExpired } from "../services/TimeService";

import LectureGroup from "./LectureGroup";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import callAPI from "../services/APIServices";

function LectureList(props) {
    const [data, setData] = useState({ lectures: [] });
    const breadcrumbs = [
        { name: "Hauptseite", active: false, href: "#/" },
        { name: "Vorlesungen", active: true }
    ];

    useEffect(() => {
        const fetchData = async () => {
            const { response, isError } = await callAPI(`lectures`, "GET");
            if (!isError) {
                setData({ lectures: response.data });
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
                <BreadcrumbWrapper items={breadcrumbs} />

                {activeLectures.length !== 0 && (
                    <LectureGroup
                        title="Aktive Vorlesungen"
                        lectures={activeLectures}
                    />
                )}
                {upcomingLectures.length !== 0 && (
                    <LectureGroup
                        title="Bevorstehende Vorlesungen"
                        lectures={upcomingLectures}
                    />
                )}
                {expiredLectures.length !== 0 && (
                    <LectureGroup
                        title="Vergangene Vorlesungen"
                        lectures={expiredLectures}
                    />
                )}
            </Col>
        </Row>
    );
}

export default LectureList;
