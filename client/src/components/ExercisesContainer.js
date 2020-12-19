import React, { useState, useEffect } from "react";

import { Row, Col, Nav, Card, Tab, Alert } from "react-bootstrap";

import ExerciseDropzone from "./ExerciseDropzone";
import ExercisePane from "./ExercisePane";
import { callAPI } from "../services/APIServices";

export default function ExercisesContainer({
    lecture_slug,
    lesson_slug,
    exercises
}) {
    const [selectedExercise, setSelectedExercise] = useState(exercises[0]);
    const [errors, setErrors] = useState(null);
    const [userScores, setUserScores] = useState({});

    useEffect(() => {
        const fetchScores = async () => {
            const statusResponse = await callAPI(
                `/api/lectures/${lecture_slug}/lessons/${lesson_slug}/exercises/status`,
                "GET"
            );
            if (statusResponse) {
                setUserScores(statusResponse.data);
            }
        };

        fetchScores()
        const interval = setInterval(() => fetchScores(), 2000);

        return () => {
            clearInterval(interval);
        };
    }, [lecture_slug, lesson_slug]);

    return (
        <Card>
            <Card.Header>Lesson Exercises</Card.Header>
            {errors && <Alert variant="danger">{errors}</Alert>}
            <Tab.Container defaultActiveKey={0}>
                <Row>
                    <Col sm={3}>
                        <Nav
                            fill
                            variant="pills"
                            className="flex-column"
                            onSelect={eventKey =>
                                setSelectedExercise(exercises[eventKey])
                            }
                        >
                            {exercises.map((exercise, index) => (
                                <Nav.Item key={`item-${index}`}>
                                    <Nav.Link
                                        key={`nav-${index}`}
                                        eventKey={index}
                                    >
                                        {exercise.title} (
                                        {userScores[exercise.slug]}/
                                        {exercise.max_score})
                                    </Nav.Link>
                                </Nav.Item>
                            ))}
                        </Nav>
                        <br />
                        <ExerciseDropzone
                            exercise={selectedExercise}
                            setErrors={setErrors}
                        />
                    </Col>
                    <Col sm={9}>
                        <Tab.Content>
                            {exercises.map((exercise, index) => (
                                <Tab.Pane
                                    key={`pane-${index}`}
                                    eventKey={index}
                                >
                                    <ExercisePane
                                        key={index}
                                        exercise={exercise}
                                        active={exercise === selectedExercise}
                                    />
                                </Tab.Pane>
                            ))}
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>
        </Card>
    );
}
