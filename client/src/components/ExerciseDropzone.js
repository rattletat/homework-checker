import React from "react";
import "react-dropzone-uploader/dist/styles.css";
import Dropzone from "react-dropzone-uploader";
import { Card } from "react-bootstrap";

import { getAPIHeaders } from "../services/APIServices";

export default function ExerciseDropzone({ exercise, setErrors }) {
    const handleChangeStatus = ({ meta, xhr, remove }, status) => {
        if (status === "error_upload") {
            let errors = JSON.parse(`[${xhr.response}]`)[0];
            if (errors && "non_field_errors" in errors) {
                setErrors(errors["non_field_errors"]);
            }
            remove();
        } else if (status === "done") {
            setErrors(null);
            remove();
        }
    };

    const getUploadParams = () => {
        return getAPIHeaders(
            {
                url: `/api/exercises/${exercise.id}/submit`
            },
            true
        );
    };
    if (!exercise) return null;
    return (
        <React.Fragment>
            <Card>
                <Card.Header>
                    <center>Submit {exercise.title} </center>
                </Card.Header>
                <Card.Body>
                    <Dropzone
                        getUploadParams={getUploadParams}
                        onChangeStatus={handleChangeStatus}
                        maxFiles={1}
                        multiple={false}
                        canCancel={false}
                        inputContent="Drop here"
                        styles={{
                            dropzone: {
                                borderStyle: "none"
                            },
                            dropzoneActive: { borderColor: "green" },
                            dropzoneReject: {
                                borderColor: "red",
                                backgroundColor: "#DAA"
                            }
                        }}
                    />
                </Card.Body>
            </Card>
        </React.Fragment>
    );
}
