import React from "react";
import "react-dropzone-uploader/dist/styles.css";
import Dropzone from "react-dropzone-uploader";
import { Card } from "react-bootstrap";

import { getAuthHeaders } from "../services/AuthService";

const ExerciseDropzone = ({ exercise }) => {
    const handleChangeStatus = ({ meta, remove }, status) => {
        if (status === "headers_received") {
            console.log("uploaded");
            remove();
        } else if (status === "aborted") {
            console.log("aborted");
        }
    };

    const getUploadParams = () => {
        return getAuthHeaders({
            url: `api/homework/exercise/${exercise.id}/submit`
        });
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
};

export default ExerciseDropzone;
