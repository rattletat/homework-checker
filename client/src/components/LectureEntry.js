import React from "react";
import { Card, ListGroup } from "react-bootstrap";
import { Link } from "react-router-dom";
import BarChart from "./BarChart";
import { getTimeIndicator, toTimeFormat } from "../services/TimeService";

function LectureEntry({ lecture }) {
  return (
    <Card className="mb-3">
      <Card.Header>
        {lecture.status !== "WAITING" && (
          <Link to={`/lectures/${lecture.slug}/`}>
            <h6 className="mt-0 mb-1">{lecture.title}</h6>
          </Link>
        )}
        {lecture.status === "WAITING" && (
          <h6 className="mt-0 mb-1">{lecture.title}</h6>
        )}
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
          {lecture.user_score != null && lecture.max_score != null && (
            <ListGroup.Item>
              <strong>Score</strong>: {lecture.user_score} / {lecture.max_score}
            </ListGroup.Item>
          )}
          {lecture.grade != null && lecture.status === "ACTIVE" && (
            <ListGroup.Item>
              <strong>Current grade</strong>: {lecture.grade}
            </ListGroup.Item>
          )}
          {lecture.grade != null && lecture.status === "FINISHED" && (
            <ListGroup.Item>
              <strong>Final Grade</strong>: {lecture.grade}
            </ListGroup.Item>
          )}
          {lecture.next_deadline != null && (
            <ListGroup.Item>
              <strong>Next deadline</strong>: {lecture.next_deadline.title}{" "}
              {getTimeIndicator(lecture.next_deadline)}
            </ListGroup.Item>
          )}
          {lecture.all_scores != null &&
            lecture.user_score != null &&
            lecture.max_score != null && (
              <ListGroup.Item>
                <BarChart
                  all_scores={lecture.all_scores}
                  user_score={lecture.user_score}
                  max_score={lecture.max_score}
                />
              </ListGroup.Item>
            )}
        </ListGroup>
      </Card.Body>
    </Card>
  );
}

export default LectureEntry;
