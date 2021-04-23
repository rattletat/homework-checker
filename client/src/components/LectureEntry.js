import React from "react";
import {Card, ListGroup} from "react-bootstrap";
import {Link} from "react-router-dom";
import {getTimeIndicator, toTimeFormat} from "../services/TimeService";

function LectureEntry({lecture}) {
    return (
        <Card className="mb-3">
            <Card.Header>
                {lecture.status !== "WAITING" &&
                    <Link to={`/lectures/${lecture.slug}/`}>
                        <h6 className="mt-0 mb-1">{lecture.title}</h6>
                    </Link>
                }
                {lecture.status === "WAITING" &&
                    <h6 className="mt-0 mb-1">{lecture.title}</h6>
                }
                <small>{getTimeIndicator(lecture)}</small>
            </Card.Header>
            <Card.Body>
                <ListGroup>
                    {lecture.start && (
                        <ListGroup.Item>
                            <strong>Lecture start</strong>: {toTimeFormat(lecture.start)}
                        </ListGroup.Item>
                    )}
                    {lecture.end && (
                        <ListGroup.Item>
                            <strong>Lecture end</strong>: {toTimeFormat(lecture.end)}
                        </ListGroup.Item>
                    )}
                    {lecture.score !== null && (
                        <ListGroup.Item>
                            <strong>Score</strong>: {lecture.score}
                        </ListGroup.Item>
                    )}
                    {lecture.grade && lecture.status === "ACTIVE" && (
                        <ListGroup.Item>
                            <strong>Current grade</strong>: {lecture.grade}
                        </ListGroup.Item>
                    )}
                    {lecture.grade && lecture.status === "FINISHED" && (
                        <ListGroup.Item>
                            <strong>Final Grade</strong>: {lecture.grade}
                        </ListGroup.Item>
                    )}
                    {lecture.next_deadline !== null && (
                        <ListGroup.Item>
                            <strong>Next deadline</strong>: {lecture.next_deadline.title} {getTimeIndicator(lecture.next_deadline)}
                        </ListGroup.Item>
                    )}

                </ListGroup>
            </Card.Body>
        </Card>
    );
}

export default LectureEntry;
