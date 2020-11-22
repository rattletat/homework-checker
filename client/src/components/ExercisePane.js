import React, { useEffect, useState } from "react";
import MarkdownRenderer from "../services/MarkdownService";
import { Card, Accordion } from "react-bootstrap";
import { callAPI } from "../services/APIServices";
import { toTimeFormat } from "../services/TimeService";

export default function ExercisePane({ exercise, userScores, setUserScores }) {
    const [submissions, setSubmissions] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await callAPI(
                    `/api/exercises/${exercise.id}/submissions/`,
                    "GET"
                );
                setSubmissions(response.data);
                const max_score = Math.max.apply(
                    Math,
                    submissions.map(sub => sub.score)
                );
                const exercise_slug = exercise.slug;
                if (max_score > userScores[exercise_slug]) {
                    setUserScores(scores => ({
                        ...scores,
                        exercise_slug: max_score
                    }));
                }
            } catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, [exercise]);
    return (
        <>
            <hr />
            {userScores && exercise && (
                <center>
                    <strong>{exercise.title}:</strong> You achieved{" "}
                    {userScores[exercise.slug]} out of {exercise.max_score}{" "}
                    points.
                </center>
            )}
            <hr />
            <MarkdownRenderer>{exercise.description}</MarkdownRenderer>
            <Accordion defaultActiveKey="event-0">
                {submissions.map((submission, key) => (
                    <Card key={`card-${key}`}>
                        <Accordion.Toggle
                            as={Card.Header}
                            eventKey={`event-${key}`}
                            key={`toggle-${key}`}
                        >
                            <h6 className="mt-0 mb-1">
                                {submission.score} / {exercise.max_score}
                            </h6>
                            <small>
                                {toTimeFormat(submission.created, "LLL")}
                            </small>
                        </Accordion.Toggle>
                        <Accordion.Collapse
                            eventKey={`event-${key}`}
                            key={`collapse/${key}`}
                        >
                            <Card.Body>
                                {submission.output
                                    .split("\n")
                                    .map((item, key) => (
                                        <p key={`${key}`}>{item}</p>
                                    ))}
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                ))}
            </Accordion>
        </>
    );
}
