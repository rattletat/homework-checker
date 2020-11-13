import React, { useState } from "react";
import { Alert, Button, Row } from "react-bootstrap";

export default ({ loaded, registered, clickAction }) => {
    const [show, setShow] = useState(true);

    if (loaded && registered) {
        // Can be removed when there is a status panel.
        return (
            <Alert variant="dark">You are registered for this course.</Alert>
        );
    }

    if (loaded && !registered) {
        return (
            <Alert show={show} variant="warning">
                <Alert.Heading>Not registered!</Alert.Heading>
                <p>
                    You are not registered for this course.
                    <br />
                    In order to do the exercises, you need to register for this
                    course first.
                </p>
                <hr />
                <Row>
                    <Button
                        onClick={() => clickAction()}
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
    }
};
