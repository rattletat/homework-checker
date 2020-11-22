import React from "react";
import { Table } from "react-bootstrap";

import LessonTableRow from "./LessonTableRow";

export default function LessonTable({ lessons }) {
    let rows = lessons.map((lesson, index) => (
        <LessonTableRow key={lesson.slug} {...{ index, lesson }} />
    ));

    return (
        <Table striped hover className={"text-center"}>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Lektion</th>
                    <th>Start</th>
                    <th>Deadline</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </Table>
    );
}
