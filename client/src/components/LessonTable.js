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
                    <th className="text-center">Title</th>
                    {hasStart &&
                        <th className="text-center">Start</th>
                    }
                    {hasDeadline &&
                        <th className="text-center">Deadline</th>
                    }
                </tr>
            </thead>
            <tbody>
                {lessons.map((lesson, index) => (

                    <tr key={index}
                        onClick={() => lesson.status === "WAITING" ? alert(`${lesson.title} ${getTimeIndicator(lesson)}.`) : history.push(`${lesson.slug}/`)}
                        className={lesson.status === "ACTIVE" ? "table-primary" : ""}
                    >
                        <td className="text-left">
                            {lesson.title}
                        </td>
                        {hasStart &&
                            <td className="text-center">{toTimeFormat(lesson.start)}</td>
                        }
                        {hasDeadline &&
                            <td className="text-center">{toTimeFormat(lesson.end)}</td>
                        }
                    </tr>
                ))}
            </tbody>
        </Table>
    );
}
