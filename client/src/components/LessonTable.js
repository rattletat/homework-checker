import React from "react";
import {Table} from "react-bootstrap";
import {useHistory} from "react-router-dom";

import {toTimeFormat, getTimeIndicator} from "../services/TimeService";

export default function LessonTable({lessons}) {
    const history = useHistory();
    const hasStart = lessons.some(lesson => lesson.start)
    const hasDeadline = lessons.some(lesson => lesson.end)
    const hasMaxScore = lessons.some(lesson => lesson.max_score)
    const hasUserScore = lessons.some(lesson => lesson.user_score)
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
                    {(hasUserScore || hasMaxScore) &&
                        <th>Score</th>
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
                            <td>{toTimeFormat(lesson.start)}</td>
                        }
                        {hasDeadline &&
                            <td>{toTimeFormat(lesson.end)}</td>
                        }
                        {(hasUserScore || hasMaxScore) &&
                            <td>{lesson.max_score !== 0 &&
                                <>
                                    {lesson.user_score} / {lesson.max_score}
                                </>
                            }</td>
                        }
                    </tr>
                ))}
            </tbody>
        </Table>
    );
}
