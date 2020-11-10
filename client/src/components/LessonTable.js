import React from "react";
import { Table } from "react-bootstrap";

import LessonTableRow from "./LessonTableRow";

function LessonTable({ lecture }) {
    let rows = lecture.lessons.map((lesson, index) => (
        <LessonTableRow key={lesson.slug} {...{ index, lecture, lesson }} />
    ));

    if (lecture) {
        return (
            <Table striped hover className={"text-center"}>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Lektion</th>
                        <th>Start</th>
                        <th>Deadline</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </Table>
        );
    }
}

export default LessonTable;
