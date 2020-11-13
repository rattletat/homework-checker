import React from "react";
import { Jumbotron } from "react-bootstrap";
import MarkdownRenderer from "../services/MarkdownService";

export default ({ title, content }) => {
    return (
        <Jumbotron>
            <h1>{title}</h1>
            <MarkdownRenderer>{content}</MarkdownRenderer>
        </Jumbotron>
    );
};
