import React, { useEffect, useState } from "react";
import { Col, Row, Jumbotron } from "react-bootstrap";
import { useParams } from "react-router-dom";

import { callAPI } from "../services/APIServices";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

import MarkdownRenderer from "../services/MarkdownService";
import ResourceList from "./ResourceList";
import ExercisesContainer from "./ExercisesContainer";

export default function LessonDetail() {
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
        const interval = setInterval(() => fetchHomeworkData(), 1000);

        return () => {
            clearInterval(interval);
        };
    }, [lecture_slug, lesson_slug]);

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
                        <Jumbotron>
                            <h1>{teachingData.lesson.title}</h1>
                            <MarkdownRenderer>
                                {teachingData.lesson.description}
                            </MarkdownRenderer>
                        </Jumbotron>
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
}
