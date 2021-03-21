import React, {useState, useEffect} from "react";

import {Row, Col, Alert, Accordion} from "react-bootstrap";

import ExerciseDropzone from "./ExerciseDropzone";
import SubmissionCard from "./SubmissionCard";

import {callAPI} from "../services/APIServices";
import MarkdownRenderer from "../services/MarkdownService";

export default function ExercisePane({exercise, active}) {
    const [submissions, setSubmissions] = useState([]);
    const [errors, setErrors] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await callAPI(
                    `/api/exercises/${exercise.id}/submissions/`,
                    "GET"
                );
                setSubmissions(response.data);
            } catch (error) {
                console.log(error);
            }
        };
        const interval = setInterval(() => (active ? fetchData() : {}), 2000);

        return () => {
            clearInterval(interval);
        };
    }, [exercise, active]);
    return (
        <>
            <Row>
                <Col lg={{span: 10, offset: 1}} className="center-block">
                    <MarkdownRenderer>{exercise.description}</MarkdownRenderer>
                </Col>
            </Row >
            <hr />
            {errors && <Alert variant="danger">{errors}</Alert>}
            <ExerciseDropzone
                exercise={exercise}
                setErrors={setErrors}
            />
            <Accordion defaultActiveKey="event-0">
                {submissions.map((submission, key) => (
                    <SubmissionCard {...{key, submission, cardKey: key, max_score: exercise.max_score}} />
                ))}
            </Accordion>
        </>
    );
}
