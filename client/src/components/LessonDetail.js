import React, { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { useParams } from "react-router-dom";

import callAPI from "../services/APIServices";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

import MarkdownContent from "../components/MarkdownContent";
import ResourceList from "./ResourceList";

export default () => {
    const { lecture_slug, lesson_slug } = useParams();

    const [data, setData] = useState({
        lecture: null,
        lesson: null
    });

    useEffect(() => {
        const fetchData = async () => {
            const lectureResponse = await callAPI(
                `api/lectures/${lecture_slug}`,
                "GET"
            );
            const lessonResponse = await callAPI(
                `api/lectures/${lecture_slug}/lessons/${lesson_slug}`,
                "GET"
            );
            setData({
                lecture: lectureResponse.data,
                lesson: lessonResponse.data
            });
        };
        fetchData();
    }, [lecture_slug, lesson_slug]);

    return (
        <Row>
            <Col lg={12}>
                {data.lecture && data.lesson && (
                    <BreadcrumbWrapper
                        items={[
                            {
                                name: "Hauptseite",
                                active: false,
                                href: "#/"
                            },
                            {
                                name: "Vorlesungen",
                                active: false,
                                href: "#/lectures/"
                            },
                            {
                                name: data.lecture.title,
                                active: false,
                                href: `#/lectures/${data.lecture.slug}/`
                            },
                            {
                                name: data.lesson.title,
                                active: true
                            }
                        ]}
                    />
                )}
                {data.lesson && (
                    <>
                        <MarkdownContent
                            title={data.lesson.title}
                            content={data.lesson.description}
                        />
                        <ResourceList resources={data.lesson.resources} />
                    </>
                )}
            </Col>
        </Row>
    );
};
