import React from "react";
import { ListGroup } from "react-bootstrap";

import LectureListElement from "./LectureListElement";

function LectureGroup({ title, lectures }) {
    let cards = lectures.map(lecture => (
        <LectureListElement lecture={lecture} key={lecture.slug} />
    ));
    return (
        <>
            <h3>{title}</h3>
            <br />
            <ListGroup>{cards}</ListGroup>
        </>
    );
}

export default LectureGroup;
