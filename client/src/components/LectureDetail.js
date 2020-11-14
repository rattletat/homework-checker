import React, { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { useParams } from "react-router-dom";

import callAPI from "../services/APIServices";

import BreadcrumbWrapper from "./BreadcrumbWrapper";
import LectureRegisterAlert from "./LectureRegisterAlert";
import MarkdownContent from "./MarkdownContent";
import ResourceList from "./ResourceList";
import LessonTable from "./LessonTable";

export default function LectureDetail() {
    const { lecture_slug } = useParams();

    const [data, setData] = useState({
        lecture: null,
        breadcrumbs: []
    });

    const [registered, setRegistered] = useState({
        state: false,
        loaded: false
    });

    useEffect(() => {
        const fetchLecture = async () => {
            const response = await callAPI(
                `api/lectures/${lecture_slug}`,
                "GET"
            );
            setData({
                lecture: response.data
            });
        };
        fetchLecture();
    }, [lecture_slug]);

    useEffect(() => {
        const checkRegistered = async () => {
            setRegistered({ registeredLoaded: false });
            const response = await callAPI(
                `api/lectures/${lecture_slug}/status`,
                "GET"
            );
            setRegistered({
                state: response.data.registered,
                loaded: true
            });
        };
        checkRegistered();
    }, [lecture_slug]);

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper
                    items={[
                        {
                            name: "Home",
                            active: false,
                            href: "#/"
                        },
                        {
                            name: "Lectures",
                            active: false,
                            href: "#/lectures/"
                        },
                        {
                            name: data.lecture ? data.lecture.title : "",
                            active: true
                        }
                    ]}
                />

                <LectureRegisterAlert
                    loaded={registered.loaded}
                    registered={registered.state}
                    clickAction={() => {
                        callAPI(`api/lectures/${lecture_slug}/signup`, "POST");
                    }}
                />

                {data.lecture && (
                    <>
                        <MarkdownContent
                            title={data.lecture.title}
                            content={data.lecture.description}
                        />

                        <ResourceList resources={data.lecture.resources} />
                        <br />
                        <LessonTable lessons={data.lecture.lessons} />
                    </>
                )}
            </Col>
        </Row>
    );
}
