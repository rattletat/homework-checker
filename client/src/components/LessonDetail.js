import React, { useEffect, useState } from "react";
import { Col, Row, Jumbotron } from "react-bootstrap";
import { Redirect, useParams } from "react-router-dom";

import callAPI from "../services/APIServices";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

import MarkdownRenderer from "../services/MarkdownService";

function LessonDetail() {
    const { lecture_slug, lesson_slug } = useParams();

    const breadcrumbsBase = [
        { name: "Hauptseite", active: false, href: "#/" },
        { name: "Vorlesungen", active: false, href: "#/lectures/" }
    ];
    const [data, setData] = useState({
        lecture: null,
        lesson: null,
        breadcrumbsTail: []
    });
    const [isError, setIsError] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            setIsError(false);

            const {
                response: lectureResponse,
                isError: isLectureError
            } = await callAPI(`lectures/${lecture_slug}/`, "GET");
            const {
                response: lessonResponse,
                isError: isLessonError
            } = await callAPI(`lessons/${lesson_slug}/`, "GET");
            if (!isLectureError && !isLessonError) {
                setData({
                    lecture: lectureResponse.data,
                    lesson: lessonResponse.data,
                    breadcrumbsTail: [
                        {
                            name: lectureResponse.data.title,
                            active: false,
                            href: `#/lectures/${lectureResponse.data.slug}/`
                        },
                        {
                            name: lessonResponse.data.title,
                            active: true
                        }
                    ]
                });
            } else {
                setIsError(true);
            }
        };
        fetchData();
    }, [lecture_slug, lesson_slug]);

    if (isError) {
        return <Redirect to="/" />;
    }

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={breadcrumbsBase.concat(data.breadcrumbsTail)}
                />

                {data.lesson && (
                    <Jumbotron>
                        <h1>{data.lesson.title}</h1>
                        <MarkdownRenderer>
                            {data.lesson.description}
                        </MarkdownRenderer>
                    </Jumbotron>
                )}
            </Col>
        </Row>
    );
}

export default LessonDetail;
