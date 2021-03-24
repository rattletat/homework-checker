import React from "react";
import {Table} from "react-bootstrap";
import {useHistory} from "react-router-dom";

import {toTimeFormat, getTimeIndicator} from "../services/TimeService";

export default function LessonTable({lessons}) {
    const history = useHistory();
    const hasStart = lessons.some(lesson => lesson.start)
    const hasDeadline = lessons.some(lesson => lesson.end)
    return (
        <Table striped hover className={"text-center"}>
            <thead>
                <tr>
                    <th>Title</th>
                    {hasStart &&
                        <th>Start</th>
                    }
                    {hasDeadline &&
                        <th>Deadline</th>
                    }
                </tr>
            </thead>
            <tbody>
                {lessons.map((lesson, index) => (

                    <tr key={index}
                        onClick={() => lesson.status === "WAITING" ? alert(`Lesson ${getTimeIndicator(lesson)}.`) : history.push(`${lesson.slug}/`)}
                        className={lesson.status === "ACTIVE" ? "table-primary" : ""}
                    >
                        <td>
                            {lesson.title}
                        </td>
                        {hasStart &&
                            <td>{toTimeFormat(lesson.start)}</td>
                        }
                        {hasDeadline &&
                            <td>{toTimeFormat(lesson.end)}</td>
                        }
                    </tr>
                ))}
            </tbody>
        </Table>
    );
}
