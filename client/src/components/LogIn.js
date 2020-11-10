import React from "react";
import { Alert, Button, Card, Col, Form, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Formik } from "formik";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

export default ({ logIn }) => {
    const breadcrumbs = [
        { name: "Hauptseite", active: false, href: "#/" },
        { name: "Anmeldung", active: true }
    ];

    const onSubmit = async (values, actions) => {
        try {
            const { response, isError } = await logIn(
                values.email,
                values.password
            );

            if (isError) {
                const data = response.response.data;
                for (const value in data) {
                    actions.setFieldError(value, data[value]);
                }
            }
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <Card>
                    <Card.Header>Anmeldung</Card.Header>
                    <Card.Body>
                        <Formik
                            initialValues={{
                                email: "",
                                password: ""
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
                                    {"__all__" in errors && (
                                        <Alert variant="danger">
                                            {errors["__all__"]}
                                        </Alert>
                                    )}
                                    {"detail" in errors && (
                                        <Alert variant="danger">
                                            {errors["detail"]}
                                        </Alert>
                                    )}
                                    <Form noValidate onSubmit={handleSubmit}>
                                        <Form.Group controlId="email">
                                            <Form.Label>
                                                Email-Adresse:
                                            </Form.Label>
                                            <Form.Control
                                                className={
                                                    "email" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="email"
                                                onChange={handleChange}
                                                value={values.email}
                                                required
                                            />
                                            {"email" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.email}
                                                </Form.Control.Feedback>
                                            )}
                                        </Form.Group>
                                        <Form.Group controlId="password">
                                            <Form.Label>Passwort:</Form.Label>
                                            <Form.Control
                                                className={
                                                    "password" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="password"
                                                onChange={handleChange}
                                                type="password"
                                                value={values.password}
                                                required
                                            />
                                            {"password" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.password}
                                                </Form.Control.Feedback>
                                            )}
                                        </Form.Group>
                                        <Button
                                            block
                                            disabled={isSubmitting}
                                            type="submit"
                                            variant="primary"
                                        >
                                            Anmelden
                                        </Button>
                                    </Form>
                                </>
                            )}
                        </Formik>
                    </Card.Body>
                    <p className="mt-3 text-center">
                        Du bist noch nicht registriert?{" "}
                        <Link to="/signup">Registrieren!</Link>
                    </p>
                </Card>
            </Col>
        </Row>
    );
};
