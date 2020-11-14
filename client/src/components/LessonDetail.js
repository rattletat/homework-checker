import React, { useEffect, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { useParams } from "react-router-dom";

import callAPI from "../services/APIServices";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

import MarkdownContent from "../components/MarkdownContent";
import ResourceList from "./ResourceList";
import ExercisesContainer from "./ExercisesContainer";

export default () => {
    const { lecture_slug, lesson_slug } = useParams();

    const [teachingData, setTeachingData] = useState({
        lecture: null,
        lesson: null
    });

    const [homeworkData, setHomeworkData] = useState({
        exercises: []
    });

    useEffect(() => {
        const fetchTeachingData = async () => {
            const lectureResponse = await callAPI(
                `api/lectures/${lecture_slug}`,
                "GET"
            );
            const lessonResponse = await callAPI(
                `api/lectures/${lecture_slug}/lessons/${lesson_slug}`,
                "GET"
            );
            setTeachingData({
                lecture: lectureResponse.data,
                lesson: lessonResponse.data
            });
        };
        fetchTeachingData();
    }, [lecture_slug, lesson_slug]);

    useEffect(() => {
        const fetchHomeworkData = async () => {
            const exercisesResponse = await callAPI(
                `api/lectures/${lecture_slug}/lessons/${lesson_slug}/exercises/`,
                "GET"
            );
            setHomeworkData({
                exercises: exercisesResponse.data
            });
        };
        fetchHomeworkData();
    }, []);
    return (
        <Row>
            <Col lg={12}>
                {teachingData.lecture && teachingData.lesson && (
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
                                name: teachingData.lecture.title,
                                active: false,
                                href: `#/lectures/${teachingData.lecture.slug}/`
                            },
                            {
                                name: teachingData.lesson.title,
                                active: true
                            }
                        ]}
                    />
                )}
                {teachingData.lesson && (
                    <>
                        <MarkdownContent
                            title={teachingData.lesson.title}
                            content={teachingData.lesson.description}
                        />
                        <ResourceList
                            resources={teachingData.lesson.resources}
                        />
                    </>
                )}
                <br />
                {homeworkData.exercises && (
                    <ExercisesContainer exercises={homeworkData.exercises} />
                )}
            </Col>
        </Row>
    );
};
