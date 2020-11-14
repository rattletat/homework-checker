import React from "react";
import { ListGroup } from "react-bootstrap";

export default function ExercisePane({ exercise }) {
    return (
        <>
            <hr />
            <center>
                <strong>{exercise.title}:</strong> You achieved 0 out of{" "}
                {exercise.max_score} points.
            </center>
            <hr />
            {exercise.description}
            <ListGroup></ListGroup>
        </>
    );
}
