import React from "react";
import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { toTimeFormat } from "../services/TimeService";

function LessonTableRow({ index, lesson }) {
    return (
        <tr key={index}>
            <td>{index + 1}</td>
            <td>{lesson.title}</td>
            <td>{toTimeFormat(lesson.start)}</td>
            <td>{toTimeFormat(lesson.end)}</td>
            <td>
                <Link to={lesson.slug}>
                    <Button className="btn-sm">
                        <span>Zur Aufgabe</span>
                    </Button>
                </Link>
            </td>
        </tr>
    );
}

export default LessonTableRow;
