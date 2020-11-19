import React from "react";
import { Alert, Button, Card, Col, Form, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Formik } from "formik";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

export default function LogIn({ logIn }) {
    const breadcrumbs = [
        { name: "Home", active: false, href: "#/" },
        { name: "Log in", active: true }
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
                    <Card.Header>Log in</Card.Header>
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
                                        <Form.Group controlId="email">
                                            <Form.Control
                                                className={
                                                    "email" in errors
                                                        ? "is-invalid"
                                                        : ""
                                                }
                                                name="email"
                                                onChange={handleChange}
                                                value={values.email}
                                                placeholder={"Email"}
                                                required
                                            />
                                            {"email" in errors && (
                                                <Form.Control.Feedback type="invalid">
                                                    {errors.email}
                                                </Form.Control.Feedback>
                                            )}
                                        </Form.Group>
                                        <Form.Group controlId="password">
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
                                                placeholder={"Password"}
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
                                            Log in
                                        </Button>
                                    </Form>
                                </>
                            )}
                        </Formik>
                    </Card.Body>
                    <p className="mt-3 text-center">
                        {"Not registered yet?"}{" "}
                        <Link to="/signup">Sign up.</Link>
                    </p>
                </Card>
            </Col>
        </Row>
    );
}
