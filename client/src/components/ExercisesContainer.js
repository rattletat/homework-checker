import React, { useState, useEffect } from "react";

import { Row, Col, Nav, Card, Tab } from "react-bootstrap";

import ExerciseDropzone from "./ExerciseDropzone";
import ExercisePane from "./ExercisePane";

export default function ExercisesContainer({ exercises }) {
    const max_score_sum = exercises.reduce((acc, ex) => acc + ex.max_score, 0);
    const [selectedExercise, setSelectedExercise] = useState(null);

    useEffect(() => {
        setSelectedExercise(exercises[0]);
    }, [exercises]);

    return (
        <Card>
            <Card.Header>Lesson Exercises (0/{max_score_sum}) </Card.Header>
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
                                        {exercise.title} (0/
                                        {exercise.max_score})
                                    </Nav.Link>
                                </Nav.Item>
                            ))}
                        </Nav>
                        <br />
                        <ExerciseDropzone exercise={selectedExercise} />
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
