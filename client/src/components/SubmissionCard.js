import React from "react";

import { Card, Accordion, Button } from "react-bootstrap";
import fileDownload from "js-file-download";

import TapText from "./TapText";
import { toTimeFormat } from "../services/TimeService";
import { callAPI } from "../services/APIServices";

export default function SubmissionCard({ cardKey, submission, max_score }) {
  return (
    <Card key={`card-${cardKey}`}>
      <Accordion.Toggle
        as={Card.Header}
        eventKey={`event-${cardKey}`}
        key={`toggle-${cardKey}`}
      >
        <Button
          size="sm"
          variant="outline-secondary"
          className="float-right"
          onClick={(e) => {
            e.stopPropagation();
            callAPI(submission.download_uri, "GET", {
              responseType: "blob",
            }).then((res) => fileDownload(res.data, submission.filename));
          }}
        >
          Download
        </Button>
        <h6 className="mt-0 mb-1">
          {submission.score} / {max_score}
        </h6>
        <small>{toTimeFormat(submission.created, "LLL")}</small>
      </Accordion.Toggle>
      <Accordion.Collapse
        eventKey={`event-${cardKey}`}
        key={`collapse/${cardKey}`}
      >
        <Card.Body>
          <div>
            {submission.output === "" ? (
              "Running..."
            ) : (
              <TapText>{submission.output}</TapText>
            )}
          </div>
        </Card.Body>
      </Accordion.Collapse>
    </Card>
  );
}
