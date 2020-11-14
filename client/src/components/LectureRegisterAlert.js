import React, { useState } from "react";
import { Alert, Button, Row } from "react-bootstrap";

export default function LectureRegisterAlert({
    loaded,
    registered,
    clickAction
}) {
    const [show, setShow] = useState(true);

    if (loaded && registered) {
        // Can be removed when there is a status panel.
        return (
            <Alert variant="dark">You are registered for this course.</Alert>
        );
    } else if (loaded && !registered) {
        return (
            <Alert show={show} variant="dark">
                <Alert.Heading>Not registered!</Alert.Heading>
                <p>
                    You are not registered for this course.
                    <br />
                    In order to do the exercises, please register for this
                    course first.
                </p>
                <hr />
                <Row>
                    <Button
                        onClick={() => {
                            clickAction();
                            setShow(false);
                        }}
                        variant="success"
                        className="m-2 col-sm"
                    >
                        Register
                    </Button>
                    <Button
                        onClick={() => setShow(false)}
                        variant="secondary"
                        className="m-2 col-sm"
                    >
                        Hide
                    </Button>
                </Row>
            </Alert>
        );
    } else return null;
}
