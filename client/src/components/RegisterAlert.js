import React, { useState } from "react";
import { Alert, Button } from "react-bootstrap";
import { postAction } from "../services/APIServices";

export default ({ clickAction }) => {
    const [show, setShow] = useState(true);

    return (
        <>
            <Alert show={show} variant="dark">
                <Alert.Heading>Nicht angemeldet!</Alert.Heading>
                <p>
                    Du bist noch nicht für diese Vorlesung angemeldet.
                    <br />
                    Damit du an den Übungen und Quizzes teilnehmen kannst, musst
                    du dich erst anmelden.
                </p>
                <hr />
                <div className="row">
                    <Button
                        onClick={() => clickAction()}
                        variant="success"
                        className="m-2 col-sm"
                    >
                        Zu dieser Vorlesung anmelden.
                    </Button>
                    <Button
                        onClick={() => setShow(false)}
                        variant="secondary"
                        className="m-2 col-sm"
                    >
                        Ausblenden
                    </Button>
                </div>
            </Alert>
        </>
    );
};
