import React from "react";
import { Button, Card, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import { getTimeIndicator, toTimeFormat } from "../services/TimeService";

function LectureListElement({ lecture }) {
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
                            Lecture end: {toTimeFormat(lecture.start)}
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

export default LectureListElement;
