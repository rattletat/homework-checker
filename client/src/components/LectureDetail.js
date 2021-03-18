import React, {useEffect, useState} from "react";
import {Col, Row, Jumbotron} from "react-bootstrap";
import {useParams} from "react-router-dom";

import {callAPI} from "../services/APIServices";

import BreadcrumbWrapper from "./BreadcrumbWrapper";
import MarkdownRenderer from "../services/MarkdownService";
import ResourceList from "./ResourceList";
import LessonTable from "./LessonTable";

export default function LectureDetail() {
    const {lecture_slug} = useParams();

    const [data, setData] = useState({
        lecture: null,
        breadcrumbs: []
    });

    useEffect(() => {
        const fetchLecture = async () => {
            const response = await callAPI(
                `/api/lectures/${lecture_slug}`,
                "GET"
            );
            if (response) {
                setData({
                    lecture: response.data
                });
            }
        };
        fetchLecture();
    }, [lecture_slug]);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={[
                        {
                            name: "Home",
                            active: false,
                            href: "/"
                        },
                        {
                            name: "Lectures",
                            active: false,
                            href: "/lectures/"
                        },
                        {
                            name: data.lecture ? data.lecture.title : "",
                            active: true
                        }
                    ]}
                />

                {data.lecture && (
                    <>
                        <Jumbotron>
                            <h1>{data.lecture.title}</h1>
                            <MarkdownRenderer>
                                {data.lecture.description}
                            </MarkdownRenderer>
                        </Jumbotron>

                        <ResourceList resources={data.lecture.resources} />
                        <br />
                        {data.lecture.lessons &&
                            <LessonTable lessons={data.lecture.lessons} />
                        }
                    </>
                )}
            </Col>
        </Row>
    );
}
