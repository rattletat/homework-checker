import React from "react";

import {Card, Accordion} from "react-bootstrap";
import {toTimeFormat} from "../services/TimeService";

export default function SubmissionCard({cardKey, submission, max_score}) {
    return (
        <Card key={`card-${cardKey}`}>
            <Accordion.Toggle
                as={Card.Header}
                eventKey={`event-${cardKey}`}
                key={`toggle-${cardKey}`}
            >
                <h6 className="mt-0 mb-1">
                    {submission.score} / {max_score}
                </h6>
                <small>
                    {toTimeFormat(submission.created, "LLL")}
                </small>
            </Accordion.Toggle>
            <Accordion.Collapse
                eventKey={`event-${cardKey}`}
                key={`collapse/${cardKey}`}
            >
                <Card.Body>
                    <div className="display-linebreak">{submission.output === "" ? "Running..." : submission.output}</div>
                </Card.Body>
            </Accordion.Collapse>
        </Card>
    );
}
