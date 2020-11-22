import React, { useState } from "react";

import { Row, Col, Nav, Card, Tab, Alert } from "react-bootstrap";

import ExerciseDropzone from "./ExerciseDropzone";
import ExercisePane from "./ExercisePane";

export default function ExercisesContainer({
    exercises,
    userScores,
    setUserScores
}) {
    const [selectedExercise, setSelectedExercise] = useState(exercises[0]);
    const [errors, setErrors] = useState(null);

    const max_score_sum = exercises.reduce((acc, ex) => acc + ex.max_score, 0);
    const user_score_sum = Object.values(userScores).reduce(
        (acc, val) => acc + val,
        0
    );

    return (
        <Card>
            <Card.Header>
                Lesson Exercises ({user_score_sum}/{max_score_sum}){" "}
            </Card.Header>
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
                                        userScores={userScores}
                                        setUserScores={setUserScores}
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
