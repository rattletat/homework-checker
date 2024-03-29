import React, { useState, useEffect } from "react";

import { Row, Col, Nav, Card, Tab } from "react-bootstrap";
import ExercisePane from "./ExercisePane";
import { callAPI } from "../services/APIServices";
import MarkdownRenderer from "../services/MarkdownService";
import Badge from "react-bootstrap/Badge";

export default function ExercisesContainer({
  lecture_slug,
  lesson_slug,
  exercises,
}) {
  const [selectedExercise, setSelectedExercise] = useState(exercises[0]);
  const [userScores, setUserScores] = useState({});

  useEffect(() => {
    const fetchScores = async () => {
      const statusResponse = await callAPI(
        `/api/lectures/${lecture_slug}/lessons/${lesson_slug}/exercises/status`,
        "GET"
      );
      if (statusResponse) {
        setUserScores(statusResponse.data.highest_scores);
      }
    };

    fetchScores();
    const interval = setInterval(() => fetchScores(), 2000);

    return () => {
      clearInterval(interval);
    };
  }, [lecture_slug, lesson_slug]);

  return (
    <Card>
      <Card.Header>Exercises</Card.Header>
      <Tab.Container defaultActiveKey={0}>
        <Row>
          <Col lg={12}>
            <Nav
              fill
              variant="pills"
              className="nav-item center-block"
              onSelect={(eventKey) => setSelectedExercise(exercises[eventKey])}
            >
              {exercises.map((exercise, index) => (
                <Nav.Item key={`item-${index}`}>
                  <Nav.Link key={`nav-${index}`} eventKey={index}>
                    {exercise.title}
                    {exercise.graded ? (
                      <Badge
                        pill
                        variant="light"
                        className="text-primary float-right"
                      >
                        graded: {userScores[exercise.id]} / {exercise.max_score}
                      </Badge>
                    ) : (
                      <Badge
                        pill
                        variant="light"
                        className="text-primary float-right"
                      >
                        not graded: {userScores[exercise.id]} /{" "}
                        {exercise.max_score}
                      </Badge>
                    )}
                  </Nav.Link>
                </Nav.Item>
              ))}
            </Nav>
          </Col>
        </Row>
        <Row>
          <Col sm={12}>
            <Tab.Content>
              {exercises.map((exercise, index) => (
                <Tab.Pane key={`pane-${index}`} eventKey={index}>
                  <Row>
                    <Col sm={{ span: 10, offset: 1 }} className="center-block">
                      <br />
                      <h2>{exercise.title}</h2>
                      <MarkdownRenderer>
                        {exercise.description}
                      </MarkdownRenderer>
                    </Col>
                  </Row>
                  <ExercisePane
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
