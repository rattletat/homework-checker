import React from "react";
import { Button, Card, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import { getTimeIndicator, toTimeFormat } from "../services/TimeService";

function LectureEntry({ lecture }) {
    return (
        <Card className="mb-3">
            <Card.Header>
                <h6 className="mt-0 mb-1">{lecture.title}</h6>
                <small>{getTimeIndicator(lecture)}</small>
            </Card.Header>
            <Card.Body>
                <ListGroup>
                    {lecture.start && (
                        <ListGroup.Item>
                            Lecture start: {toTimeFormat(lecture.start)}
                        </ListGroup.Item>
                    )}
                    {lecture.end && (
                        <ListGroup.Item>
                            Lecture end: {toTimeFormat(lecture.end)}
                        </ListGroup.Item>
                    )}
                    {lecture.score !== null && (
                        <ListGroup.Item>
                            Score: {lecture.score }
                        </ListGroup.Item>
                    )}
                    {lecture.grade && lecture.status === "ACTIVE" && (
                        <ListGroup.Item>
                            Current grade: {lecture.grade}
                        </ListGroup.Item>
                    )}
                    {lecture.grade && lecture.status === "FINISHED" && (
                        <ListGroup.Item>
                            Final Grade: {lecture.grade}
                        </ListGroup.Item>
                    )}
                </ListGroup>
                <Card.Footer>
                    <Link to={`/lectures/${lecture.slug}/`}>
                        <Button>
                            <span>Go to lecture</span>
                        </Button>
                    </Link>
                </Card.Footer>
            </Card.Body>
        </Card>
    );
}

export default LectureEntry;
