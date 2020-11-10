import React, { useEffect, useState } from "react";
import { Alert, Col, Row, Jumbotron } from "react-bootstrap";
import { Redirect, useParams } from "react-router-dom";
import BreadcrumbWrapper from "./BreadcrumbWrapper";
import RegisterAlert from "./RegisterAlert";

import callAPI from "../services/APIServices";

import MarkdownRenderer from "../services/MarkdownService";
import LessonTable from "./LessonTable";

function LectureDetail(props) {
    const { lecture_slug } = useParams();
    const breadcrumbsBase = [
        { name: "Hauptseite", active: false, href: "#/" },
        { name: "Vorlesungen", active: false, href: "#/lectures/" }
    ];

    const [data, setData] = useState({
        lecture: null,
        registered: false,
        registeredLoaded: false,
        breadcrumbsTail: []
    });
    const [isError, setIsError] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            const { response, isError } = await callAPI(
                `lectures/${lecture_slug}/`,
                "GET"
            );
            if (!isError) {
                setData({
                    lecture: response.data,
                    breadcrumbsTail: [
                        {
                            name: response.data.title,
                            active: true
                        }
                    ]
                });
            } else {
                setIsError(true);
            }
        };
        fetchData();
    }, [lecture_slug]);

    useEffect(() => {
        const checkRegistered = async () => {
            const { response, isError } = await callAPI(
                `lectures/${lecture_slug}/status`,
                "GET"
            );
            if (!isError) {
                setData(d => ({
                    ...d,
                    registered: response.data.registered,
                    registeredLoaded: true
                }));
            } else {
                setIsError(true);
            }
        };
        checkRegistered();
    }, [lecture_slug]);

    if (isError) {
        return <Redirect to="/" />;
    }

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={breadcrumbsBase.concat(data.breadcrumbsTail)}
                />

                {data.registeredLoaded && !data.registered && (
                    <RegisterAlert
                        clickAction={() =>
                            callAPI(`lectures/${lecture_slug}/signup`, "POST")
                        }
                    />
                )}
                {data.registeredLoaded && data.registered && (
                    <Alert variant="success">
                        Du bist für diese Vorlesung angemeldet.
                    </Alert>
                )}
                {data.lecture && (
                    <>
                        <Jumbotron>
                            <h1>{data.lecture.title}</h1>
                            <MarkdownRenderer>
                                {data.lecture.description}
                            </MarkdownRenderer>
                        </Jumbotron>
                        <LessonTable lecture={data.lecture} />
                    </>
                )}
            </Col>
        </Row>
    );
}

export default LectureDetail;
