import React from "react";
import {Alert, Button, Card, Form} from "react-bootstrap";
import {Formik} from "formik";
import {callAPI} from "../services/APIServices";

export default function LectureRegister({ refreshPage }) {
    const onSubmit = async (values, actions) => {
        try {
            const response = await callAPI(`/api/lectures/register/${values.code}`, "POST")
            if (response.status === 404) {
                const data = response.data;
                for (const value in data) {
                    actions.setFieldError(value, data[value]);
                }
            }
            else {
                refreshPage();
            }
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <Card>
            <Card.Header>Add Lecture</Card.Header>
            <Card.Body>
                <Formik
                    initialValues={{
                        code: "",
                    }}
                    onSubmit={onSubmit}
                >
                    {({
                        errors,
                        handleChange,
                        handleSubmit,
                        isSubmitting,
                        values
                    }) => (
                        <>
                            {"non_field_errors" in errors && (
                                <Alert variant="danger">
                                    {errors["non_field_errors"]}
                                </Alert>
                            )}
                            {"detail" in errors && (
                                <Alert variant="danger">
                                    {errors["detail"]}
                                </Alert>
                            )}
                            <Form noValidate onSubmit={handleSubmit}>
                                <Form.Group controlId="code">
                                    <Form.Control
                                        className={
                                            "code" in errors
                                                ? "is-invalid"
                                                : ""
                                        }
                                        name="code"
                                        onChange={handleChange}
                                        value={values.code}
                                        placeholder={"Registration Code"}
                                        required
                                    />
                                    {"code" in errors && (
                                        <Form.Control.Feedback type="invalid">
                                            {errors.code}
                                        </Form.Control.Feedback>
                                    )}
                                </Form.Group>
                                <Button
                                    block
                                    disabled={isSubmitting}
                                    type="submit"
                                    variant="primary"
                                >
                                    Add
                                        </Button>
                            </Form>
                        </>
                    )}
                </Formik>
            </Card.Body>
        </Card>
    );
}
