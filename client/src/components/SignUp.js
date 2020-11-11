import React, { useState } from "react";
import axios from "axios";
import { Formik } from "formik";
import { Button, Card, Col, Form, Row } from "react-bootstrap";
import { Link, Redirect } from "react-router-dom";
import BreadcrumbWrapper from "./BreadcrumbWrapper";

export default () => {
    const [isSubmitted, setSubmitted] = useState(false);
    const breadcrumbs = [
        { name: "Hauptseite", active: false, href: "#/" },
        { name: "Registrierung", active: true }
    ];

    const onSubmit = async (
        { email, identifier, full_name, password },
        actions
    ) => {
        const url = "/api/accounts/signup";
        try {
            await axios.post(url, {
                email,
                identifier,
                full_name,
                password1: password,
                password2: password
            });
            setSubmitted(true);
        } catch (response) {
            const data = response.response.data;
            for (const value in data) {
                actions.setFieldError(value, data[value].join(" "));
            }
        }
    };

    if (isSubmitted) {
        return <Redirect to="/login" />;
    }

    return (
        <Row>
            <Col lg={12}>
                <BreadcrumbWrapper items={breadcrumbs} />
                <Card className="mb-3">
                    <Card.Header>Registrierung</Card.Header>
                    <Card.Body>
                        <Formik
                            initialValues={{
                                email: "",
                                identifier: "",
                                full_name: "",
                                password: ""
                            }}
                            onSubmit={onSubmit}
                        >
                            {({
                                errors,
                                handleChange,
                                handleSubmit,
                                isSubmitting,
                                setFieldValue,
                                values
                            }) => (
                                <Form noValidate onSubmit={handleSubmit}>
                                    <Form.Group controlId="email">
                                        <Form.Label>
                                            Deine Email-Adresse:
                                        </Form.Label>
                                        <Form.Control
                                            className={
                                                "email" in errors
                                                    ? "is-invalid"
                                                    : ""
                                            }
                                            name="email"
                                            onChange={handleChange}
                                            values={values.email}
                                            required
                                        />
                                        {"email" in errors && (
                                            <Form.Control.Feedback type="invalid">
                                                {errors.email}
                                            </Form.Control.Feedback>
                                        )}
                                    </Form.Group>
                                    <Form.Group controlId="full_name">
                                        <Form.Label>
                                            Vollständiger Name:
                                        </Form.Label>
                                        <Form.Control
                                            className={
                                                "full_name" in errors
                                                    ? "is-invalid"
                                                    : ""
                                            }
                                            name="full_name"
                                            onChange={handleChange}
                                            values={values.full_name}
                                            required
                                        />
                                        {"full_name" in errors && (
                                            <Form.Control.Feedback type="invalid">
                                                {errors.full_name}
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
                                    <Form.Group controlId="identifier">
                                        <Form.Label>
                                            Deine Matrikelnummer:
                                        </Form.Label>
                                        <Form.Control
                                            className={
                                                "identifier" in errors
                                                    ? "is-invalid"
                                                    : ""
                                            }
                                            name="identifier"
                                            onChange={handleChange}
                                            type="number"
                                            value={values.identifier}
                                        />
                                        {"identifier" in errors && (
                                            <Form.Control.Feedback type="invalid">
                                                {errors.identifier}
                                            </Form.Control.Feedback>
                                        )}
                                    </Form.Group>
                                    <Button
                                        block
                                        type="submit"
                                        variant="primary"
                                    >
                                        Registrieren
                                    </Button>
                                </Form>
                            )}
                        </Formik>
                    </Card.Body>
                    <p className="mt-3 text-center">
                        Du bist schon registriert?{" "}
                        <Link to="/login">Anmelden!</Link>
                    </p>
                </Card>
            </Col>
        </Row>
    );
};
